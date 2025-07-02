# Railway Backend Deployment Guide

## Prerequisites

1. Railway account: https://railway.app
2. GitHub repository connected to Railway

## Step 1: Create New Project

1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `gymintel-web` repository

## Step 2: Add PostgreSQL Database

1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create and link the database

## Step 3: Enable PostGIS Extension

Railway PostgreSQL doesn't have PostGIS by default. You need to:

1. Click on your PostgreSQL service
2. Go to "Connect" tab
3. Copy the connection string
4. Connect using `psql` or pgAdmin
5. Run: `CREATE EXTENSION IF NOT EXISTS postgis;`

Or use the Railway CLI:
```bash
railway run psql -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

## Step 4: Set Environment Variables

Click on your backend service and go to "Variables" tab. Add:

```env
# Required API Keys
YELP_API_KEY=your-yelp-api-key
GOOGLE_PLACES_API_KEY=your-google-places-api-key

# Security (generate strong keys)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Frontend URL
FRONTEND_URL=https://gymintel.vercel.app

# Environment
ENVIRONMENT=production
```

## Step 5: Configure Build Settings

1. Go to Settings → Deploy
2. Set Root Directory: `/`
3. Build Command: (leave empty - using Dockerfile)
4. Start Command: `cd backend && python start.py`

## Step 6: Deploy

1. Railway will automatically deploy on push to main
2. Check the deployment logs for any errors
3. Once deployed, you'll get a URL like: `https://your-app.railway.app`

## Step 7: Initialize Database

You have two options for database initialization:

### Option A: Automatic Initialization (Recommended for new projects)

Add this environment variable in Railway:
```bash
AUTO_INIT_DB=true
```

The application will automatically:
- Create PostGIS extension
- Create all required tables
- Run initial setup on first startup

### Option B: Manual Initialization (Recommended for production)

1. **Enable PostGIS Extension**:
   ```bash
   railway run psql -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

2. **Run Database Migrations**:
   ```bash
   # Using Railway CLI
   railway run --service=your-backend-service cd backend && alembic upgrade head

   # Or using the init script
   railway run --service=your-backend-service cd backend && python scripts/init_db.py
   ```

**Note**: After initial setup, set `AUTO_INIT_DB=false` in production to prevent accidental recreation.

## Common Issues

### 1. "No module named 'app'"
**Solution**: Make sure start command includes `cd backend`

### 2. "Connection refused" or database errors
**Solution**:
- Check DATABASE_URL is set by Railway
- Ensure PostGIS extension is enabled
- Check logs for connection string issues

### 3. "Port already in use"
**Solution**: Use the PORT environment variable provided by Railway

### 4. Build failures
**Solution**:
- Check Python version in Dockerfile matches requirements
- Ensure all dependencies in requirements.txt are valid
- Check for PostGIS/GDAL system dependencies

## Testing the Deployment

Once deployed, test these endpoints:

1. Health check: `https://your-app.railway.app/health`
2. GraphQL playground: `https://your-app.railway.app/graphql`
3. API docs: `https://your-app.railway.app/docs`

## Getting the Backend URL for Frontend

After successful deployment:
1. Copy your Railway app URL
2. Use these values for Vercel environment variables:
   - `VITE_GRAPHQL_ENDPOINT`: `https://your-app.railway.app/graphql`
   - `VITE_GRAPHQL_WS_ENDPOINT`: `wss://your-app.railway.app/graphql`
