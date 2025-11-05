import pkg from 'pg';
const { Pool, Client } = pkg;
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT) || 5432,
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
};

const dbName = process.env.DB_NAME || 'fope_db';

async function setupDatabase() {
  console.log('🚀 Starting FOPE database setup...\n');

  // Connect to PostgreSQL server (not to a specific database)
  const client = new Client(dbConfig);

  try {
    await client.connect();
    console.log('✓ Connected to PostgreSQL server');

    // Check if database exists
    const checkDb = await client.query(
      `SELECT 1 FROM pg_database WHERE datname = $1`,
      [dbName]
    );

    if (checkDb.rows.length === 0) {
      // Create database
      console.log(`📦 Creating database: ${dbName}`);
      await client.query(`CREATE DATABASE ${dbName}`);
      console.log(`✓ Database ${dbName} created successfully`);
    } else {
      console.log(`✓ Database ${dbName} already exists`);
    }

    await client.end();

    // Now connect to the newly created database and run schema
    const dbClient = new Client({
      ...dbConfig,
      database: dbName,
    });

    await dbClient.connect();
    console.log(`✓ Connected to database: ${dbName}`);

    // Read and execute schema file
    const schemaPath = path.join(__dirname, '..', 'database-schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf-8');

    console.log('📋 Executing database schema...');
    await dbClient.query(schema);
    console.log('✓ Database schema created successfully');

    // Verify tables were created
    const tablesResult = await dbClient.query(`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE'
      ORDER BY table_name
    `);

    console.log('\n📊 Created tables:');
    tablesResult.rows.forEach(row => {
      console.log(`   • ${row.table_name}`);
    });

    await dbClient.end();

    console.log('\n✅ Database setup completed successfully!');
    console.log('\n📝 Default admin credentials:');
    console.log('   Email: admin@fope.com');
    console.log('   Password: admin123');
    console.log('   ⚠️  CHANGE THIS PASSWORD IN PRODUCTION!\n');

  } catch (error) {
    console.error('❌ Database setup failed:', error.message);
    process.exit(1);
  }
}

setupDatabase();
