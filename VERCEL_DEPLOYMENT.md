# Vercel Deployment Guide

## Quick Deploy to Vercel

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from project root**:
   ```bash
   vercel
   ```

4. **For production deployment**:
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via GitHub Integration

1. Push your code to GitHub (already on branch: `claude/create-legal-dashboard-jggBZ`)

2. Go to [Vercel Dashboard](https://vercel.com/dashboard)

3. Click **"Add New Project"**

4. Import your GitHub repository: `nvxcii/ConstruX`

5. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (leave empty for static site)
   - **Output Directory**: (leave empty)

6. Click **"Deploy"**

### Accessing the Dashboards

After deployment, your dashboards will be available at:

- **FOPE Construction Dashboard**: `https://your-project.vercel.app/`
- **Legal Dashboard**: `https://your-project.vercel.app/legal`

Or directly:
- `https://your-project.vercel.app/index.html` - FOPE Dashboard
- `https://your-project.vercel.app/legal-dashboard.html` - Legal Dashboard

## Project Structure

```
ConstruX/
├── index.html              # FOPE Construction Dashboard
├── legal-dashboard.html    # Legal Practice Management Dashboard
├── vercel.json            # Vercel configuration
└── VERCEL_DEPLOYMENT.md   # This file
```

## Features

### Legal Dashboard Features
- **Case Management**: Track active cases, deadlines, and statuses
- **Client Management**: Organize client information and communications
- **Document Tracking**: Upload and manage case documents
- **Time Tracking**: Log billable hours for accurate billing
- **Analytics**: View case distribution and performance metrics
- **Deadline Alerts**: Stay on top of critical deadlines
- **Activity Feed**: Monitor recent activities across all cases

### FOPE Dashboard Features
- **GPS Check-In/Out**: Location-verified time tracking
- **Recursive Quality Monitoring**: Before/During/After photo documentation
- **Predictive Intelligence Dashboard**: Cost overrun predictions
- **AI Field Assistant**: Gemini-powered real-time assistance

## Environment Variables (if needed)

If you plan to add backend functionality, create a `.env` file:

```env
# Add any API keys or environment variables here
# Example:
# GEMINI_API_KEY=your_api_key_here
# DATABASE_URL=your_database_url
```

## Custom Domain Setup

1. Go to your Vercel project settings
2. Navigate to **Domains**
3. Add your custom domain
4. Update DNS records as instructed by Vercel

## Support

For issues or questions:
- Vercel Documentation: https://vercel.com/docs
- GitHub Issues: https://github.com/nvxcii/ConstruX/issues

---

**Last Updated**: December 27, 2024
