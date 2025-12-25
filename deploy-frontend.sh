#!/bin/bash
# Frontend Deployment Script for Netlify

echo "🚀 Deploying Frontend to Netlify..."

# Navigate to frontend directory
cd frontend

# Install dependencies
npm ci

# Build the project
npm run build

echo "✅ Frontend build completed successfully!"
echo "📁 Build output is in frontend/dist directory"
echo "🌐 Ready for Netlify deployment!"

# Instructions for manual deployment
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://netlify.com and sign in"
echo "2. Drag and drop the 'frontend/dist' folder to deploy"
echo "3. Or connect your GitHub repository for automatic deployments"
