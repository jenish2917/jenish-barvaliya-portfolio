import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Toaster } from 'react-hot-toast'
import ErrorBoundary from './components/ErrorBoundary'

// Components
import Navbar from './components/Navbar'
import Hero from './components/sections/Hero'
import About from './components/sections/About'
import Experience from './components/sections/Experience'
import Projects from './components/sections/Projects'
import Skills from './components/sections/Skills'
import Certifications from './components/sections/Certifications'
import Education from './components/sections/Education'
import Contact from './components/sections/Contact'
import Background3D from './components/3d/Background3D'
import LoadingScreen from './components/LoadingScreen'

function App() {
  const [isLoading, setIsLoading] = useState(true)
  const [darkMode, setDarkMode] = useState(true)

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 2500)

    return () => clearTimeout(timer)
  }, [])

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-black text-white' : 'bg-white text-black'} transition-colors duration-500`}>
      <AnimatePresence mode="wait">
        {isLoading ? (
          <LoadingScreen key="loading" />
        ) : (
          <ErrorBoundary>
            <motion.div
              key="main"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              style={{ background: 'transparent' }}
            >
              {/* 3D Background (guarded to avoid blocking UI) */}
              {(() => {
                try {
                  return <Background3D darkMode={darkMode} />
                } catch (e) {
                  console.error('Background3D failed:', e)
                  return null
                }
              })()}
              
              {/* Navigation */}
              <Navbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
              
              {/* Main Content */}
              <main className="relative z-20">
                <Hero darkMode={darkMode} />
                <About darkMode={darkMode} />
                <Experience darkMode={darkMode} />
                <Projects darkMode={darkMode} />
                <Skills darkMode={darkMode} />
                <Certifications darkMode={darkMode} />
                <Education darkMode={darkMode} />
                <Contact darkMode={darkMode} />
              </main>
              
              {/* Toast notifications */}
              <Toaster
                position="bottom-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    background: darkMode ? '#1a1a1a' : '#f3f4f6',
                    color: darkMode ? '#ffffff' : '#000000',
                    border: `1px solid ${darkMode ? '#333333' : '#e5e7eb'}`,
                  },
                }}
              />
            </motion.div>
          </ErrorBoundary>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App
