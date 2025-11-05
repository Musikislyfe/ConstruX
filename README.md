# FOPE - Field Optimization Protocol Engine

A comprehensive construction and property management system that optimizes field operations through GPS-verified check-ins, recursive quality monitoring, and AI-powered assistance.

## Features

🎯 **Intelligent Check-In/Out** - GPS-verified location tracking with mandatory photo documentation and late arrival detection

🔄 **Recursive Quality Monitoring** - Before/During/After photo documentation for every task with quality benchmarking

🤖 **Gemini AI Assistant** - Real-time photo analysis, safety compliance checks, and material identification

📊 **Predictive Intelligence Dashboard** - High-level systems view with equipment efficiency tracking and cost overrun prediction

## Quick Start

```bash
# Install dependencies
npm install

# Setup database
npm run db:setup

# Start development servers
npm run dev
```

Access the app at http://localhost:5173

**Default Admin Login:**
- Email: admin@fope.com
- Password: admin123

## Documentation

See [SETUP.md](./SETUP.md) for detailed setup instructions and API documentation.

## Tech Stack

- **Backend**: Node.js, Express, PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (Vite)
- **AI**: Google Gemini API
- **Auth**: JWT

## Project Structure

```
├── src/
│   ├── backend/       # Express API server
│   └── frontend/      # Landing page
├── scripts/           # Setup scripts
├── database-schema.sql
└── SETUP.md          # Detailed documentation
```

## License

MIT
