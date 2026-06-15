import fs from 'fs';
import path from 'path';
import { query, getClient } from '../config/database';
import { logger } from '../config/logger';

interface Migration {
  version: string;
  filename: string;
  content: string;
}

const MIGRATIONS_DIR = path.join(__dirname);

async function readMigrations(): Promise<Migration[]> {
  const files = fs.readdirSync(MIGRATIONS_DIR)
    .filter(file => file.match(/^\d+_.*\.sql$/))
    .sort();

  const migrations: Migration[] = [];
  for (const file of files) {
    const [version] = file.split('_');
    const content = fs.readFileSync(path.join(MIGRATIONS_DIR, file), 'utf-8');
    migrations.push({ version, filename: file, content });
  }

  return migrations;
}

async function getMigratedVersions(): Promise<string[]> {
  try {
    await query(`
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version VARCHAR(255) PRIMARY KEY,
        filename VARCHAR(255) NOT NULL UNIQUE,
        executed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
      )
    `);

    const result = await query('SELECT version FROM schema_migrations ORDER BY version');
    return result.rows.map(row => row.version);
  } catch (error) {
    logger.error('Failed to get migrated versions:', error);
    throw error;
  }
}

async function runMigration(migration: Migration): Promise<void> {
  const client = await getClient();
  try {
    await client.query('BEGIN');
    await client.query(migration.content);
    await client.query(
      'INSERT INTO schema_migrations (version, filename) VALUES ($1, $2)',
      [migration.version, migration.filename]
    );
    await client.query('COMMIT');
    logger.info(`✓ Migrated: ${migration.filename}`);
  } catch (error) {
    await client.query('ROLLBACK');
    logger.error(`✗ Migration failed: ${migration.filename}`, error);
    throw error;
  } finally {
    client.release();
  }
}

async function migrate(): Promise<void> {
  try {
    logger.info('Starting database migrations...');
    
    const migrations = await readMigrations();
    const migratedVersions = await getMigratedVersions();

    const pendingMigrations = migrations.filter(
      m => !migratedVersions.includes(m.version)
    );

    if (pendingMigrations.length === 0) {
      logger.info('All migrations up to date');
      process.exit(0);
    }

    for (const migration of pendingMigrations) {
      await runMigration(migration);
    }

    logger.info(`✓ All ${pendingMigrations.length} migration(s) completed successfully`);
    process.exit(0);
  } catch (error) {
    logger.error('Migration failed:', error);
    process.exit(1);
  }
}

migrate();
