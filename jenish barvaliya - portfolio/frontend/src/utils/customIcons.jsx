import React from 'react'

// Custom Black & White Icon Components
// These icons are designed to work perfectly with dark and light modes

export const CustomIcons = {
  // AI/ML Icons
  Brain: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
      <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>
    </svg>
  ),

  // Code Icon
  Code: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <polyline points="16,18 22,12 16,6"/>
      <polyline points="8,6 2,12 8,18"/>
    </svg>
  ),

  // Database Icon
  Database: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <ellipse cx="12" cy="5" rx="9" ry="3"/>
      <path d="m3 5 0 14c0 1.8 4 3 9 3s9-1.2 9-3V5"/>
      <path d="m3 12c0 1.8 4 3 9 3s9-1.2 9-3"/>
    </svg>
  ),

  // User Icon
  User: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
      <circle cx="12" cy="7" r="4"/>
    </svg>
  ),

  // Chart Icons
  BarChart: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <line x1="12" y1="20" x2="12" y2="10"/>
      <line x1="18" y1="20" x2="18" y2="4"/>
      <line x1="6" y1="20" x2="6" y2="16"/>
    </svg>
  ),

  // Award Icon
  Award: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <circle cx="12" cy="8" r="6"/>
      <path d="m9 12 2 2 4-4"/>
      <path d="m8 14 1.5 1.5L12 13"/>
      <path d="m16 14-1.5 1.5L12 13"/>
    </svg>
  ),

  // Building Icon
  Building: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <rect x="4" y="2" width="16" height="20" rx="2"/>
      <path d="M9 22v-4h6v4"/>
      <path d="M8 6h.01"/>
      <path d="M16 6h.01"/>
      <path d="M12 6h.01"/>
      <path d="M12 10h.01"/>
      <path d="M12 14h.01"/>
      <path d="M16 10h.01"/>
      <path d="M16 14h.01"/>
      <path d="M8 10h.01"/>
      <path d="M8 14h.01"/>
    </svg>
  ),

  // Shield Icon
  Shield: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <path d="M20 13c0 5-3.5 7.5-8 7.5s-8-2.5-8-7.5c0-1 0-3 0-3S6 8 12 8s8 2 8 2 0 2 0 3z"/>
      <path d="m9 12 2 2 4-4"/>
    </svg>
  ),

  // Clock Icon
  Clock: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <circle cx="12" cy="12" r="10"/>
      <polyline points="12,6 12,12 16,14"/>
    </svg>
  ),

  // Folder Icon
  Folder: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
    </svg>
  ),

  // Lightbulb Icon
  Lightbulb: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <path d="M9 18h6"/>
      <path d="M10 22h4"/>
      <path d="m15.09 9a5 5 0 0 0-6.18 0"/>
      <path d="M12 3a5 5 0 0 1 5 5 5 5 0 0 1-2 4v2a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-2a5 5 0 0 1-2-4 5 5 0 0 1 5-5z"/>
    </svg>
  ),

  // Sparkles Icon
  Sparkles: ({ className = "w-6 h-6", darkMode = false }) => (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke={darkMode ? "#ffffff" : "#000000"} 
      strokeWidth="2"
    >
      <path d="M9 11H5l7-9 2 3"/>
      <path d="m13 11 4-4-6-6"/>
      <path d="m11 15H7l-7 9 9-1"/>
      <path d="M15 15l7-1-1 7"/>
    </svg>
  )
}

// Utility function to get appropriate color for dark/light mode
export const getIconColor = (darkMode) => ({
  primary: darkMode ? '#ffffff' : '#000000',
  secondary: darkMode ? '#9ca3af' : '#6b7280',
  accent: darkMode ? '#3b82f6' : '#1d4ed8'
})

export default CustomIcons
