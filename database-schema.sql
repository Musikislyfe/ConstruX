-- FOPE Database Schema
-- Field Optimization Protocol Engine

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS photos CASCADE;
DROP TABLE IF EXISTS task_assignments CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS checkins CASCADE;
DROP TABLE IF EXISTS workers CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table (for authentication and admin access)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'worker', -- 'admin', 'supervisor', 'worker'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    gps_latitude DECIMAL(10, 8),
    gps_longitude DECIMAL(11, 8),
    geofence_radius_meters INTEGER DEFAULT 100,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'completed', 'paused'
    start_date DATE,
    estimated_completion DATE,
    budget DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workers table
CREATE TABLE workers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(100), -- 'electrician', 'plumber', 'carpenter', etc.
    hourly_rate DECIMAL(8, 2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Check-ins table (GPS-verified clock in/out)
CREATE TABLE checkins (
    id SERIAL PRIMARY KEY,
    worker_id INTEGER REFERENCES workers(id),
    project_id INTEGER REFERENCES projects(id),
    checkin_time TIMESTAMP NOT NULL,
    checkout_time TIMESTAMP,
    checkin_gps_lat DECIMAL(10, 8) NOT NULL,
    checkin_gps_lng DECIMAL(11, 8) NOT NULL,
    checkout_gps_lat DECIMAL(10, 8),
    checkout_gps_lng DECIMAL(11, 8),
    checkin_photo_url TEXT,
    checkout_photo_url TEXT,
    is_late BOOLEAN DEFAULT false,
    hours_worked DECIMAL(5, 2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255), -- e.g., "Unit 101", "Building A"
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'needs_review'
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'urgent'
    estimated_hours DECIMAL(5, 2),
    actual_hours DECIMAL(5, 2),
    due_date DATE,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Task assignments (many-to-many relationship between workers and tasks)
CREATE TABLE task_assignments (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    worker_id INTEGER REFERENCES workers(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(task_id, worker_id)
);

-- Photos table (Before/During/After documentation)
CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    worker_id INTEGER REFERENCES workers(id),
    photo_type VARCHAR(20) NOT NULL, -- 'before', 'during', 'after'
    photo_url TEXT NOT NULL,
    gps_latitude DECIMAL(10, 8),
    gps_longitude DECIMAL(11, 8),
    ai_analysis_result TEXT, -- Gemini API analysis results
    ai_safety_flags TEXT[], -- Array of safety issues detected
    notes TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_checkins_worker ON checkins(worker_id);
CREATE INDEX idx_checkins_project ON checkins(project_id);
CREATE INDEX idx_checkins_time ON checkins(checkin_time);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_photos_task ON photos(task_id);
CREATE INDEX idx_photos_type ON photos(photo_type);
CREATE INDEX idx_workers_user ON workers(user_id);

-- Create a view for dashboard statistics
CREATE VIEW dashboard_stats AS
SELECT
    p.id as project_id,
    p.name as project_name,
    COUNT(DISTINCT w.id) as total_workers,
    COUNT(DISTINCT t.id) as total_tasks,
    COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END) as completed_tasks,
    COUNT(DISTINCT ph.id) as total_photos,
    SUM(c.hours_worked) as total_hours_worked,
    SUM(c.hours_worked * w.hourly_rate) as total_labor_cost
FROM projects p
LEFT JOIN checkins c ON p.id = c.project_id
LEFT JOIN workers w ON c.worker_id = w.id
LEFT JOIN tasks t ON p.id = t.project_id
LEFT JOIN photos ph ON t.id = ph.task_id
WHERE p.status = 'active'
GROUP BY p.id, p.name;

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workers_updated_at BEFORE UPDATE ON workers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_checkins_updated_at BEFORE UPDATE ON checkins
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default admin user (password: admin123 - CHANGE IN PRODUCTION!)
-- Password hash is bcrypt hash of 'admin123'
INSERT INTO users (email, password_hash, role) VALUES
('admin@fope.com', '$2b$10$rQVYj0cGdnX.YNhvVmjBJeO8ZN6z7gN6N.8qJvH0HtK7l7K8DzKXK', 'admin');

-- Insert some sample data for development
INSERT INTO projects (name, address, gps_latitude, gps_longitude, budget, start_date) VALUES
('Riverside Apartments Renovation', '123 River St, Austin, TX', 30.2672, -97.7431, 500000.00, '2025-01-15'),
('Downtown Office Complex', '456 Main St, Austin, TX', 30.2656, -97.7467, 1200000.00, '2025-02-01');

-- Create database user for the application (run this manually with appropriate credentials)
-- CREATE USER fope_app WITH PASSWORD 'your_secure_password_here';
-- GRANT ALL PRIVILEGES ON DATABASE fope_db TO fope_app;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fope_app;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fope_app;
