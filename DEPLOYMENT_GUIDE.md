# LogiTrack Deployment Guide

This guide will help you deploy the LogiTrack application with the backend on Railway and frontend on Netlify.

## Prerequisites

1. GitHub account
2. Railway account (https://railway.app)
3. Netlify account (https://netlify.com)

## Backend Deployment (Railway)

### Step 1: Prepare Your Repository
1. Push your code to a GitHub repository
2. Make sure the `backend` folder contains all the necessary files

### Step 2: Deploy to Railway
1. Go to https://railway.app and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect it's a Python app

### Step 3: Configure Environment Variables
In Railway dashboard, go to your project → Variables tab and add:

```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
SECURITY_PASSWORD_SALT=your-password-salt-here-also-random
FLASK_ENV=production
CORS_ORIGINS=https://your-netlify-app-name.netlify.app
```

**Important**: Replace `your-netlify-app-name.netlify.app` with your actual Netlify domain once you deploy the frontend.

### Step 4: Set Root Directory
1. In Railway dashboard, go to Settings
2. Set "Root Directory" to `backend`
3. Railway will automatically use the Procfile for deployment

### Step 5: Get Your Railway URL
1. After deployment, Railway will provide a URL like: `https://your-app-name.railway.app`
2. Copy this URL - you'll need it for frontend configuration

## Frontend Deployment (Netlify)

### Step 1: Update Environment Variables
1. In your local `frontend/.env.production` file, update:
   ```
   VITE_API_BASE_URL=https://your-railway-app-url.railway.app
   ```
2. Replace `your-railway-app-url.railway.app` with your actual Railway URL

### Step 2: Deploy to Netlify
1. Go to https://netlify.com and sign in
2. Click "New site from Git"
3. Connect your GitHub repository
4. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

### Step 3: Configure Environment Variables in Netlify
1. In Netlify dashboard, go to Site settings → Environment variables
2. Add:
   ```
   VITE_API_BASE_URL=https://your-railway-app-url.railway.app
   ```

### Step 4: Update CORS Settings
1. Go back to Railway dashboard
2. Update the `CORS_ORIGINS` environment variable with your Netlify URL:
   ```
   CORS_ORIGINS=https://your-netlify-app-name.netlify.app
   ```
3. Redeploy your Railway app

## Post-Deployment Steps

### 1. Test the Application
1. Visit your Netlify URL
2. Try logging in with demo credentials:
   - **Admin**: username: `admin01`, password: `1234`
   - **User**: username: `user01`, password: `1234`

### 2. Verify API Connection
1. Check browser developer tools for any CORS errors
2. Ensure all API calls are working properly

### 3. Custom Domain (Optional)
- **Netlify**: Go to Domain settings to add a custom domain
- **Railway**: Go to Settings → Domains to add a custom domain

## Troubleshooting

### Common Issues:

1. **CORS Errors**
   - Ensure `CORS_ORIGINS` in Railway matches your Netlify domain exactly
   - Include `https://` in the URL

2. **API Not Found (404)**
   - Verify `VITE_API_BASE_URL` in Netlify environment variables
   - Check that Railway app is running

3. **Database Issues**
   - Railway provides PostgreSQL by default
   - The app will auto-create tables on first run

4. **Build Failures**
   - Check build logs in both Railway and Netlify
   - Ensure all dependencies are listed in requirements.txt and package.json

### Environment Variables Summary:

**Railway (Backend):**
```
SECRET_KEY=your-super-secret-key
SECURITY_PASSWORD_SALT=your-password-salt
FLASK_ENV=production
CORS_ORIGINS=https://your-netlify-app.netlify.app
```

**Netlify (Frontend):**
```
VITE_API_BASE_URL=https://your-railway-app.railway.app
```

## Security Notes

1. Use strong, random values for `SECRET_KEY` and `SECURITY_PASSWORD_SALT`
2. Never commit real environment variables to your repository
3. Use the `.env.example` files as templates
4. Consider using Railway's PostgreSQL addon for production database

## Support

If you encounter issues:
1. Check the deployment logs in Railway and Netlify dashboards
2. Verify all environment variables are set correctly
3. Ensure CORS origins match exactly between frontend and backend