# 🚀 Complete Free Deployment Guide

## Overview
This guide will help you deploy your portfolio completely free using:
- **Backend**: Railway (Free tier - $5 credit monthly)
- **Frontend**: Netlify (Free tier)
- **Database**: PostgreSQL on Railway (Free)

## 📋 Prerequisites
1. GitHub account
2. Railway account (sign up at https://railway.app)
3. Netlify account (sign up at https://netlify.com)

## 🔧 Step 1: Prepare Your Repository

### Push to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

## 🖥️ Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your portfolio repository
5. Railway will auto-detect the Django app

### 2.2 Add Environment Variables
In Railway project settings, add these environment variables:
```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=.railway.app
PORT=8000
```

### 2.3 Add PostgreSQL Database
1. In Railway project, click "New" → "Database" → "Add PostgreSQL"
2. Railway will automatically set DATABASE_URL

### 2.4 Deploy
Railway will automatically deploy. Your backend URL will be:
`https://[project-name].up.railway.app`

## 🌐 Step 3: Deploy Frontend to Netlify

### 3.1 Build the Frontend
```bash
cd frontend
npm ci
npm run build
```

### 3.2 Manual Deployment (Quick)
1. Go to https://netlify.com
2. Drag and drop the `frontend/dist` folder to the deploy area
3. Your site will be live at `https://[random-name].netlify.app`

### 3.3 Automatic Deployment (Recommended)
1. In Netlify, click "New site from Git"
2. Connect GitHub and select your repository
3. Set build settings:
   - **Build command**: `cd frontend && npm ci && npm run build`
   - **Publish directory**: `frontend/dist`
4. Add environment variable:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://[your-railway-backend].up.railway.app/api`

## 🔗 Step 4: Connect Frontend to Backend

### 4.1 Update Frontend Environment
In Netlify site settings → Environment variables, add:
```
VITE_API_BASE_URL=https://your-railway-backend.up.railway.app/api
```

### 4.2 Update Backend CORS
Your backend is already configured to accept requests from Netlify domains.

## ✅ Step 5: Verification

### Test Backend
Visit: `https://your-railway-backend.up.railway.app/api/personal-info/`

### Test Frontend
Visit: `https://your-netlify-site.netlify.app`

## 🎯 Expected Results

### ✅ What You'll Get (100% Free):
- **Backend**: Deployed Django API with PostgreSQL database
- **Frontend**: Deployed React portfolio with optimized build
- **SSL**: Automatic HTTPS for both sites
- **Custom Domain**: Option to add your own domain later
- **Database**: PostgreSQL with reasonable free limits

### 💰 Free Tier Limits:
- **Railway**: $5 credit monthly (usually sufficient for portfolio)
- **Netlify**: 100GB bandwidth/month, 300 build minutes/month
- **PostgreSQL**: 512MB storage on Railway free tier

## 🔧 Troubleshooting

### Backend Issues
- Check Railway logs if deployment fails
- Ensure all environment variables are set
- DATABASE_URL should be automatically provided by Railway

### Frontend Issues
- Verify build command in Netlify settings
- Check that VITE_API_BASE_URL points to your Railway backend
- Ensure frontend/dist directory is being published

### CORS Issues
- Backend is configured to allow Netlify domains
- If you use a custom domain, add it to CORS_ALLOWED_ORIGINS

## 🚀 Going Live Checklist

- [ ] Backend deployed on Railway
- [ ] Database connected and migrations run
- [ ] Frontend deployed on Netlify
- [ ] Environment variables configured
- [ ] CORS properly set up
- [ ] API endpoints working
- [ ] Profile image loading correctly
- [ ] Contact form functional (if implemented)

## 🎉 Congratulations!

Your AI/ML Engineer portfolio is now live and accessible worldwide for free!

**Next Steps:**
1. Update your resume with the live portfolio URL
2. Share on LinkedIn and professional networks
3. Consider adding a custom domain later
4. Monitor usage to stay within free limits

**Your Live URLs:**
- Portfolio: `https://[your-netlify-site].netlify.app`
- API: `https://[your-railway-backend].up.railway.app/api`
