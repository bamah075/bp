import { query } from '../config/database';
import { User } from '../types/models';
import { AuthService } from '../services/authService';

export class UserRepository {
  static async create(
    email: string,
    password: string,
    fullName: string
  ): Promise<User> {
    const passwordHash = await AuthService.hashPassword(password);
    
    const result = await query(
      `INSERT INTO users (email, password_hash, full_name, role, status)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING id, email, password_hash, full_name, avatar_url, role, status, created_at, updated_at`,
      [email, passwordHash, fullName, 'member', 'active']
    );
    
    return result.rows[0];
  }

  static async findByEmail(email: string): Promise<User | null> {
    const result = await query(
      `SELECT id, email, password_hash, full_name, avatar_url, role, status, created_at, updated_at
       FROM users WHERE email = $1`,
      [email]
    );
    
    return result.rows[0] || null;
  }

  static async findById(id: string): Promise<User | null> {
    const result = await query(
      `SELECT id, email, password_hash, full_name, avatar_url, role, status, created_at, updated_at
       FROM users WHERE id = $1`,
      [id]
    );
    
    return result.rows[0] || null;
  }

  static async emailExists(email: string): Promise<boolean> {
    const result = await query(
      `SELECT COUNT(*) FROM users WHERE email = $1`,
      [email]
    );
    
    return parseInt(result.rows[0].count, 10) > 0;
  }

  static async update(
    id: string,
    updates: Partial<Omit<User, 'id' | 'password_hash' | 'created_at'>>
  ): Promise<User | null> {
    const updateFields: string[] = [];
    const values: any[] = [id];
    let paramIndex = 2;

    if (updates.full_name !== undefined) {
      updateFields.push(`full_name = $${paramIndex++}`);
      values.push(updates.full_name);
    }
    if (updates.avatar_url !== undefined) {
      updateFields.push(`avatar_url = $${paramIndex++}`);
      values.push(updates.avatar_url);
    }
    if (updates.role !== undefined) {
      updateFields.push(`role = $${paramIndex++}`);
      values.push(updates.role);
    }
    if (updates.status !== undefined) {
      updateFields.push(`status = $${paramIndex++}`);
      values.push(updates.status);
    }

    if (updateFields.length === 0) {
      return this.findById(id);
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);

    const result = await query(
      `UPDATE users SET ${updateFields.join(', ')}
       WHERE id = $1
       RETURNING id, email, password_hash, full_name, avatar_url, role, status, created_at, updated_at`,
      values
    );

    return result.rows[0] || null;
  }
}
