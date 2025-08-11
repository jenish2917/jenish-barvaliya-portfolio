// API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// API endpoints
export const API_ENDPOINTS = {
  contact: `${API_BASE_URL}/contact/`,
  projects: `${API_BASE_URL}/projects/`,
  skills: `${API_BASE_URL}/skills/`,
  experience: `${API_BASE_URL}/experience/`,
  certifications: `${API_BASE_URL}/certifications/`,
  education: `${API_BASE_URL}/education/`,
  portfolioSummary: `${API_BASE_URL}/portfolio-summary/`,
  health: `${API_BASE_URL}/health/`
}

// Utility functions
export const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

export const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

export const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text
  return text.substr(0, maxLength) + '...'
}

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Theme utilities
export const getTheme = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('theme') || 'dark'
  }
  return 'dark'
}

export const setTheme = (theme) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('theme', theme)
  }
}

// Animation variants for Framer Motion
export const fadeInUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.8, ease: "easeOut" }
  }
}

export const fadeInLeft = {
  hidden: { opacity: 0, x: -30 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.8, ease: "easeOut" }
  }
}

export const fadeInRight = {
  hidden: { opacity: 0, x: 30 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.8, ease: "easeOut" }
  }
}

export const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
      duration: 0.8
    }
  }
}

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { 
    opacity: 1, 
    scale: 1,
    transition: { duration: 0.6, ease: "easeOut" }
  }
}

// Portfolio data helpers
export const getSkillsByCategory = (skills) => {
  return skills.reduce((acc, skill) => {
    const category = skill.category
    if (!acc[category]) {
      acc[category] = []
    }
    acc[category].push(skill)
    return acc
  }, {})
}

export const getFeaturedProjects = (projects, count = 6) => {
  return projects
    .filter(project => project.is_featured)
    .slice(0, count)
}

export const getCurrentExperience = (experiences) => {
  return experiences.find(exp => exp.is_current) || experiences[0]
}

// SEO helpers
export const updateMetaTags = (title, description, image = null) => {
  if (typeof document === 'undefined') return

  // Update title
  document.title = title

  // Update meta description
  const metaDescription = document.querySelector('meta[name="description"]')
  if (metaDescription) {
    metaDescription.setAttribute('content', description)
  }

  // Update Open Graph tags
  const ogTitle = document.querySelector('meta[property="og:title"]')
  if (ogTitle) {
    ogTitle.setAttribute('content', title)
  }

  const ogDescription = document.querySelector('meta[property="og:description"]')
  if (ogDescription) {
    ogDescription.setAttribute('content', description)
  }

  if (image) {
    const ogImage = document.querySelector('meta[property="og:image"]')
    if (ogImage) {
      ogImage.setAttribute('content', image)
    }
  }
}
