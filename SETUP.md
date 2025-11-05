# FOPE Local Development Setup Guide

## Overview

FOPE (Field Optimization Protocol Engine) is a construction management system with GPS tracking, photo documentation, and AI assistance.

## Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** v18+ and npm
- **PostgreSQL** 12+
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ConstruX
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Copy the example environment file and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` and configure:
- Database credentials (if different from defaults)
- JWT secret (use a secure random string for production)
- Gemini API key (optional, for AI features)

### 4. Set Up Database

Create the database and tables:

```bash
npm run db:setup
```

This will:
- Create the `fope_db` database
- Create all necessary tables
- Insert sample data
- Create a default admin user

**Default Admin Credentials:**
- Email: `admin@fope.com`
- Password: `admin123`
- ⚠️ **CHANGE THIS PASSWORD IN PRODUCTION!**

### 5. Start Development Servers

Run both backend and frontend:

```bash
npm run dev
```

Or run them separately:

```bash
# Terminal 1 - Backend
npm run dev:backend

# Terminal 2 - Frontend
npm run dev:frontend
```

### 6. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:3000/api
- **Health Check**: http://localhost:3000/health

## Project Structure

```
ConstruX/
├── src/
│   ├── backend/
│   │   ├── server.js          # Express server
│   │   ├── database.js        # Database connection
│   │   ├── middleware/        # Auth middleware
│   │   └── routes/            # API routes
│   │       ├── auth.js        # Authentication
│   │       ├── checkins.js    # Check-in/out
│   │       ├── tasks.js       # Task management
│   │       ├── photos.js      # Photo uploads + AI
│   │       ├── dashboard.js   # Analytics
│   │       ├── projects.js    # Project management
│   │       └── workers.js     # Worker management
│   └── frontend/
│       └── index.html         # Landing page
├── scripts/
│   └── setup-database.js      # Database setup script
├── uploads/                   # Photo uploads
├── database-schema.sql        # Database schema
├── .env                       # Environment config
├── package.json
└── vite.config.js             # Vite configuration
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Check-ins (GPS-verified)
- `POST /api/checkins/checkin` - Clock in
- `POST /api/checkins/checkout` - Clock out
- `GET /api/checkins` - Get all check-ins
- `GET /api/checkins/active` - Get active check-in

### Tasks
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/:id` - Get task details
- `POST /api/tasks` - Create task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `POST /api/tasks/:id/assign` - Assign worker
- `POST /api/tasks/:id/unassign` - Unassign worker

### Photos (Before/During/After)
- `POST /api/photos/upload` - Upload photo
- `GET /api/photos/task/:taskId` - Get task photos
- `GET /api/photos/:id` - Get photo details
- `POST /api/photos/:id/analyze` - AI analysis
- `DELETE /api/photos/:id` - Delete photo

### Dashboard
- `GET /api/dashboard/overview` - Dashboard stats
- `GET /api/dashboard/time-theft` - Time theft analytics
- `GET /api/dashboard/worker-performance` - Worker performance
- `GET /api/dashboard/cost-analytics` - Cost analytics

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/:id` - Get project details
- `POST /api/projects` - Create project
- `PUT /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project

### Workers
- `GET /api/workers` - Get all workers
- `GET /api/workers/:id` - Get worker details
- `POST /api/workers` - Create worker
- `PUT /api/workers/:id` - Update worker
- `DELETE /api/workers/:id` - Delete worker
- `GET /api/workers/:id/checkins` - Get worker check-ins

## Features

### 1. GPS-Verified Check-in/Out
- Location-based clock in/out
- Geofencing validation
- Mandatory photo documentation
- Late arrival tracking
- Automatic hours calculation

### 2. Recursive Quality Monitoring
- Before/During/After photo documentation
- Photo upload for every task
- Quality benchmarking
- Visual proof of work

### 3. Gemini AI Integration
- Photo analysis for quality control
- Safety hazard detection
- Material identification
- Real-time feedback

### 4. Predictive Dashboard
- Real-time project statistics
- Cost tracking and overrun prediction
- Worker performance analytics
- Time theft detection
- Equipment efficiency tracking

## Development

### Running Tests

```bash
npm test
```

### Building for Production

```bash
npm run build
```

### Database Management

Reset database:
```bash
npm run db:setup
```

Seed test data:
```bash
npm run db:seed
```

## Configuration

### Database Configuration

Edit `.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fope_db
DB_USER=postgres
DB_PASSWORD=your-password
```

### Gemini AI Configuration

To enable AI photo analysis:
1. Get an API key from https://makersuite.google.com/app/apikey
2. Add to `.env`:
```
GEMINI_API_KEY=your-api-key-here
```

### Geofencing Configuration

Default geofence radius is 100 meters. Adjust in `.env`:
```
DEFAULT_GEOFENCE_RADIUS_METERS=150
```

## Troubleshooting

### Database Connection Failed

Check PostgreSQL is running:
```bash
sudo service postgresql status
```

Verify credentials in `.env` match your PostgreSQL setup.

### Port Already in Use

Change ports in `.env` and `vite.config.js`:
```
PORT=3001  # Backend
```

### Photos Not Uploading

Ensure `uploads/` directory exists and has write permissions:
```bash
mkdir -p uploads
chmod 755 uploads
```

## Production Deployment

### Security Checklist

- [ ] Change default admin password
- [ ] Use strong JWT_SECRET
- [ ] Enable HTTPS
- [ ] Set NODE_ENV=production
- [ ] Secure database credentials
- [ ] Configure CORS properly
- [ ] Set up backup system
- [ ] Enable rate limiting
- [ ] Add monitoring/logging

### Environment Variables for Production

```bash
NODE_ENV=production
PORT=3000
JWT_SECRET=<strong-random-secret>
DB_PASSWORD=<secure-password>
CORS_ORIGIN=https://your-domain.com
```

## Support

For issues or questions:
- Check the troubleshooting section
- Review API documentation
- Contact the development team

## License

MIT
