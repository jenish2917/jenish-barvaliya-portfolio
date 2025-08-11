#!/bin/bash
# Backend Deployment Script for Railway/Render

echo "🚀 Preparing Backend for Railway/Render Deployment..."

# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "✅ Backend preparation completed successfully!"
echo ""
echo "📋 Next Steps for Railway Deployment:"
echo "1. Go to https://railway.app and sign in with GitHub"
echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
echo "3. Select your portfolio repository"
echo "4. Add these environment variables:"
echo "   - SECRET_KEY=your-secret-key-here"
echo "   - DEBUG=False"
echo "   - ALLOWED_HOSTS=.railway.app"
echo ""
echo "📋 Next Steps for Render Deployment:"
echo "1. Go to https://render.com and sign in with GitHub"
echo "2. Click 'New' → 'Web Service'"
echo "3. Connect your repository"
echo "4. Set build command: pip install -r backend/requirements.txt"
echo "5. Set start command: gunicorn --chdir backend portfolio_backend.wsgi:application"
# python manage.py createsuperuser

echo "Backend setup complete!"
