# Jenish Barvaliya - Portfolio Website

A modern, responsive, and 3D animated portfolio website showcasing my expertise as a Professional Machine Learning & AI Engineer. Built with React + Vite frontend and Django REST API backend.

## 🚀 Features

### Frontend
- **Modern 3D Animations**: Three.js/react-three-fiber with floating geometric shapes, neural network animations, and particle effects
- **Responsive Design**: Fully responsive across desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between black-and-white themes with smooth transitions
- **Smooth Animations**: Framer Motion for seamless page transitions and micro-interactions
- **Interactive Sections**: 
  - Hero with animated typewriter effect
  - About me with floating icons
  - Timeline-based experience section
  - Project showcase with modal details
  - Animated skill bars and progress indicators
  - Certification gallery
  - Education timeline
  - Contact form with real-time validation

### Backend
- **Django REST API**: Robust backend with Django Rest Framework
- **Contact Form**: Email notifications and database storage
- **Admin Interface**: Django admin for content management
- **CORS Enabled**: Secure cross-origin resource sharing
- **Production Ready**: Configured for deployment with PostgreSQL support

## 🛠️ Tech Stack

### Frontend
- **React 18** with **Vite** for fast development and building
- **Tailwind CSS** for utility-first styling
- **Framer Motion** for smooth animations
- **Three.js & React Three Fiber** for 3D graphics
- **React Intersection Observer** for scroll-based animations
- **Axios** for API communication
- **React Hot Toast** for notifications
- **Lucide React** for icons

### Backend
- **Django 4.2** with **Django REST Framework**
- **SQLite** (development) / **PostgreSQL** (production)
- **Django CORS Headers** for cross-origin requests
- **WhiteNoise** for static file serving
- **Gunicorn** for production WSGI server

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.9 or higher)
- **npm** or **yarn**
- **pip** (Python package installer)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jenish2917/portfolio-website.git
cd portfolio-website
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Backend Setup

```bash
# Navigate to backend directory (from project root)
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### 4. Environment Configuration

Edit `backend/.env` with your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

## 📁 Project Structure

```
portfolio-website/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── 3d/          # Three.js 3D components
│   │   │   └── sections/     # Page sections
│   │   ├── data/            # Portfolio data
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                 # Django backend
│   ├── portfolio_backend/   # Django project settings
│   ├── api/                 # Django REST API app
│   │   ├── models.py        # Database models
│   │   ├── serializers.py   # API serializers
│   │   ├── views.py         # API views
│   │   └── urls.py          # API URLs
│   ├── requirements.txt     # Backend dependencies
│   └── manage.py           # Django management script
└── README.md               # This file
```

## 🎨 Customization

### Portfolio Data
Update your personal information in `frontend/src/data/portfolio.js`:

- Personal information and contact details
- Work experience and projects
- Skills and technologies
- Education and certifications
- Social media links

### Styling
Customize the design in `frontend/tailwind.config.js` and component-specific styles.

### 3D Animations
Modify 3D effects in `frontend/src/components/3d/Background3D.jsx` to suit your preferences.

## 🚀 Deployment

### Frontend Deployment (Netlify)

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Deploy the `dist` folder to Netlify

3. Set environment variables in Netlify:
```
VITE_API_URL=https://your-backend-url.com
```

### Backend Deployment (Render/Railway/Heroku)

1. Set environment variables:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=your-postgres-url
ALLOWED_HOSTS=your-domain.com
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Collect static files:
```bash
python manage.py collectstatic
```

### Alternative Deployment Options

- **Frontend**: Vercel, GitHub Pages, Firebase Hosting
- **Backend**: DigitalOcean, AWS, Google Cloud Platform

## 📧 Contact Form Setup

To enable the contact form:

1. **Gmail Setup** (recommended):
   - Enable 2-factor authentication
   - Generate an app password
   - Use app password in EMAIL_HOST_PASSWORD

2. **Alternative Email Services**:
   - Update EMAIL_HOST settings in Django settings
   - Configure SMTP credentials

## 🔧 Development

### Available Scripts

#### Frontend
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

#### Backend
```bash
python manage.py runserver      # Start development server
python manage.py makemigrations # Create database migrations
python manage.py migrate        # Apply migrations
python manage.py test          # Run tests
python manage.py createsuperuser # Create admin user
```

### API Endpoints

- `GET /api/portfolio-summary/` - Portfolio overview
- `GET /api/projects/` - List projects
- `GET /api/experience/` - List work experience
- `GET /api/skills/` - List skills by category
- `GET /api/certifications/` - List certifications
- `GET /api/education/` - List education
- `POST /api/contact/` - Submit contact form
- `GET /api/health/` - Health check

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Update CORS_ALLOWED_ORIGINS in Django settings
2. **Email Not Sending**: Verify SMTP credentials and app passwords
3. **3D Animations Not Working**: Ensure WebGL is supported in browser
4. **Build Errors**: Clear node_modules and reinstall dependencies

### Performance Optimization

- Lazy load 3D components
- Optimize images and assets
- Use React.memo for expensive components
- Implement proper error boundaries

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/jenish2917/portfolio-website/issues).

## 📞 Contact

**Jenish Barvaliya**
- Email: jenish.barvaliya@example.com
- LinkedIn: [linkedin.com/in/jenish-barvaliya](https://linkedin.com/in/jenish-barvaliya)
- GitHub: [github.com/jenish2917](https://github.com/jenish2917)

---

⭐ **Star this repository if you found it helpful!**
