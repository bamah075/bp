const fs = require('node:fs');
const path = require('node:path');

// Load .env if present (built into Node >= 20.12, no dotenv needed)
const envFile = path.join(__dirname, '..', '.env');
if (fs.existsSync(envFile)) process.loadEnvFile(envFile);

const env = process.env;

module.exports = {
  port: Number(env.PORT || 3000),
  dbPath: env.DB_PATH || path.join(__dirname, '..', 'data', 'crm.db'),
  adminUser: env.ADMIN_USER || '',
  adminPassword: env.ADMIN_PASSWORD || '',
  schedulerIntervalMs: Number(env.SCHEDULER_INTERVAL_SECONDS || 30) * 1000,
  whatsapp: {
    token: env.WHATSAPP_TOKEN || '',
    phoneNumberId: env.WHATSAPP_PHONE_NUMBER_ID || '',
    verifyToken: env.WHATSAPP_VERIFY_TOKEN || 'my-verify-token',
    appSecret: env.WHATSAPP_APP_SECRET || '',
    graphVersion: env.GRAPH_API_VERSION || 'v26.0',
  },
};
