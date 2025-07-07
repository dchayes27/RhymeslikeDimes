# Deployment Guide for RhymeslikeDimes

This guide will help you deploy RhymeslikeDimes to the web using Railway (backend) and Vercel (frontend).

## Prerequisites

1. GitHub account
2. Railway account (https://railway.app)
3. Vercel account (https://vercel.com)

## Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:

```bash
cd /Users/danielchayes/Workspace/RhymeslikeDimes
git init
git add .
git commit -m "Initial commit - RhymeslikeDimes app"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/RhymeslikeDimes.git
git push -u origin main
```

## Step 2: Deploy Backend to Railway

1. Go to https://railway.app and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your RhymeslikeDimes repository
4. Railway will automatically detect it's a Python app
5. Set these environment variables in Railway:
   - `PORT`: (Railway sets this automatically)
   - `PYTHONPATH`: `/app/backend`
6. Railway will build and deploy automatically
7. Copy the provided Railway URL (something like `https://rhymeslikedimes-production.up.railway.app`)

## Step 3: Update Frontend Configuration

1. Create a `vercel.json` file in the project root with a rewrite that
   forwards API requests to your Railway backend:
```json
{
  "rewrites": [
    { "source": "/api/(.*)",
      "destination": "https://rhymeslikedimes-production.up.railway.app/api/$1" }
  ]
}
```
Replace the `destination` URL with your actual Railway URL.

## Step 4: Deploy Frontend to Vercel

1. Go to https://vercel.com and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect it's a Vite app
5. Set these build settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Deploy!

## Step 5: Update CORS Settings

1. Go back to Railway
2. Add your Vercel domain to the CORS origins
3. Set environment variable:
   - `CORS_ORIGINS`: `https://your-vercel-app.vercel.app,http://localhost:3000`
   - Avoid wildcard origins when `allow_credentials` is enabled

## Step 6: Test Your Deployment

1. Visit your Vercel URL
2. Try typing "ate spaghetti" and verify rhymes appear
3. Check that all three rhyme types (perfect, near, slant) are working

## Troubleshooting

### Backend Issues
- Check Railway logs for Python errors
- Verify all dependencies are in `requirements.txt`
- Check that `PYTHONPATH` is set to `/app/backend`

### Frontend Issues
- Check Vercel build logs
- Verify the API URL in your `vercel.json` rewrite matches your Railway URL
- Check browser console for CORS errors

### CORS Issues
- Add your Vercel domain to Railway's `CORS_ORIGINS` environment variable
- Format: `https://your-app.vercel.app,http://localhost:3000`

## Alternative: Render + Netlify

If you prefer different platforms:

### Render (Backend)
1. Connect GitHub repo
2. Use these settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

### Netlify (Frontend)
1. Connect GitHub repo
2. Build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

## Cost

Both Railway and Vercel offer generous free tiers:
- **Railway**: $5/month for hobby plan (includes 500 hours)
- **Vercel**: Free for personal projects

Your app should run comfortably within free tier limits for personal use.

## Custom Domain (Optional)

1. **Vercel**: Go to Project Settings → Domains → Add your domain
2. **Railway**: Go to Project → Settings → Domains → Add custom domain

## Updates

To update your deployed app:
1. Push changes to GitHub
2. Both Railway and Vercel will auto-deploy from your main branch
3. No manual redeployment needed!

## Environment Variables Summary

### Railway (Backend)
```
PORT=8001 (auto-set)
PYTHONPATH=/app/backend
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:3000
```

### Vercel (Frontend)
```
VITE_API_URL=https://your-railway-app.up.railway.app
```

Your RhymeslikeDimes app will be live and accessible worldwide! 🚀
