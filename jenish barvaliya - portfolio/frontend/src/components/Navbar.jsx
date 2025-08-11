import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sun, Moon, Menu, X, Github, Linkedin, Mail, ExternalLink } from 'lucide-react'

const Navbar = ({ darkMode, toggleDarkMode }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [activeSection, setActiveSection] = useState('hero')
  const [scrolled, setScrolled] = useState(false)

  const navItems = [
    { id: 'hero', label: 'Home' },
    { id: 'about', label: 'About' },
    { id: 'experience', label: 'Experience' },
    { id: 'projects', label: 'Projects' },
    { id: 'skills', label: 'Skills' },
    { id: 'education', label: 'Education' },
    { id: 'contact', label: 'Contact' }
  ]

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
      
      // Update active section based on scroll position
      const sections = navItems.map(item => document.getElementById(item.id))
      const scrollPosition = window.scrollY + 100

      sections.forEach((section, index) => {
        if (section) {
          const offsetTop = section.offsetTop
          const offsetHeight = section.offsetHeight
          
          if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
            setActiveSection(navItems[index].id)
          }
        }
      })
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToSection = (sectionId) => {
    const section = document.getElementById(sectionId)
    if (section) {
      const navbarHeight = 80 // Account for navbar height
      const offsetTop = section.offsetTop - navbarHeight
      window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
      })
    }
    setIsOpen(false)
  }

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled 
          ? `${darkMode ? 'bg-black/80' : 'bg-white/80'} backdrop-blur-xl border-b ${darkMode ? 'border-white/10' : 'border-black/10'} shadow-lg` 
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Enhanced Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex-shrink-0"
          >
            <button
              onClick={() => scrollToSection('hero')}
              className={`text-2xl font-bold font-mono ${darkMode ? 'text-white' : 'text-black'} hover:opacity-80 transition-opacity`}
            >
              <span className="relative">
                &lt;JB/&gt;
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.8, duration: 0.3 }}
                  className={`absolute -top-1 -right-1 w-2 h-2 ${darkMode ? 'bg-white' : 'bg-black'} rounded-full`}
                />
              </span>
            </button>
          </motion.div>

          {/* Enhanced Desktop Navigation */}
          <div className="hidden md:block">
            <div className="flex items-center space-x-1">
              {navItems.map((item, index) => (
                <motion.button
                  key={item.id}
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * index, duration: 0.5 }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => scrollToSection(item.id)}
                  className={`relative px-4 py-2 mx-1 rounded-xl text-sm font-medium transition-all duration-300 ${
                    activeSection === item.id
                      ? `${darkMode ? 'text-white bg-white/10' : 'text-black bg-black/10'} shadow-lg`
                      : `${darkMode ? 'text-gray-400 hover:text-white hover:bg-white/5' : 'text-gray-600 hover:text-black hover:bg-black/5'}`
                  }`}
                >
                  {item.label}
                  {activeSection === item.id && (
                    <motion.div
                      layoutId="activeSection"
                      className={`absolute inset-0 rounded-xl ${darkMode ? 'bg-white/10' : 'bg-black/10'} -z-10`}
                      transition={{ type: "spring", stiffness: 380, damping: 30 }}
                    />
                  )}
                </motion.button>
              ))}
            </div>
          </div>

          {/* Enhanced Social Links & Theme Toggle */}
          <div className="hidden md:flex items-center space-x-3">
            {[
              { icon: Github, href: "https://github.com/jenish2917", label: "GitHub" },
              { icon: Linkedin, href: "https://linkedin.com/in/jenish-barvaliya", label: "LinkedIn" },
              { icon: Mail, href: "mailto:jenish.barvaliya@example.com", label: "Email" }
            ].map(({ icon: Icon, href, label }) => (
              <motion.a
                key={label}
                whileHover={{ scale: 1.1, y: -2 }}
                whileTap={{ scale: 0.9 }}
                href={href}
                target={href.startsWith('mailto:') ? undefined : "_blank"}
                rel={href.startsWith('mailto:') ? undefined : "noopener noreferrer"}
                className={`group relative p-2 rounded-xl transition-all duration-300 ${
                  darkMode ? 'text-gray-400 hover:text-white hover:bg-white/10' : 'text-gray-600 hover:text-black hover:bg-black/10'
                }`}
                title={label}
              >
                <Icon size={20} />
              </motion.a>
            ))}
            
            {/* Enhanced Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.1, rotate: 180 }}
              whileTap={{ scale: 0.9 }}
              onClick={toggleDarkMode}
              className={`p-3 rounded-xl transition-all duration-300 ${
                darkMode 
                  ? darkMode ? 'text-white hover:bg-white/10 shadow-lg shadow-white/20' : 'text-black hover:bg-black/10 shadow-lg shadow-black/20' 
                  : 'text-gray-800 hover:bg-gray-800/10'
              }`}
              title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              <motion.div
                initial={false}
                animate={{ rotate: darkMode ? 0 : 180 }}
                transition={{ duration: 0.3 }}
              >
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </motion.div>
            </motion.button>
          </div>

          {/* Enhanced Mobile menu button */}
          <div className="md:hidden flex items-center space-x-3">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={toggleDarkMode}
              className={`p-2 rounded-xl transition-all duration-300 ${
                darkMode ? 'text-white' : 'text-gray-800'
              }`}
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </motion.button>
            
            <motion.button
              whileTap={{ scale: 0.9 }}
              onClick={() => setIsOpen(!isOpen)}
              className={`p-2 rounded-xl transition-all duration-300 ${
                darkMode ? 'text-white hover:bg-white/10' : 'text-black hover:bg-black/10'
              }`}
            >
              <motion.div
                animate={{ rotate: isOpen ? 180 : 0 }}
                transition={{ duration: 0.3 }}
              >
                {isOpen ? <X size={24} /> : <Menu size={24} />}
              </motion.div>
            </motion.button>
          </div>
        </div>
      </div>

      {/* Enhanced Mobile Navigation */}
      <motion.div
        initial={false}
        animate={{ 
          height: isOpen ? 'auto' : 0,
          opacity: isOpen ? 1 : 0
        }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className={`md:hidden overflow-hidden ${
          darkMode ? 'bg-black/95' : 'bg-white/95'
        } backdrop-blur-xl border-t ${darkMode ? 'border-white/10' : 'border-black/10'}`}
      >
        <div className="px-6 pt-4 pb-6 space-y-2">
          {navItems.map((item, index) => (
            <motion.button
              key={item.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ 
                opacity: isOpen ? 1 : 0, 
                x: isOpen ? 0 : -20 
              }}
              transition={{ delay: index * 0.05, duration: 0.3 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => scrollToSection(item.id)}
              className={`block w-full text-left px-4 py-3 rounded-xl text-base font-medium transition-all duration-300 ${
                activeSection === item.id
                  ? `${darkMode ? 'text-white bg-white/10' : 'text-black bg-black/10'}`
                  : `${darkMode ? 'text-gray-300 hover:text-white hover:bg-white/5' : 'text-gray-600 hover:text-black hover:bg-black/5'}`
              }`}
            >
              {item.label}
            </motion.button>
          ))}
          
          {/* Enhanced Mobile Social Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ 
              opacity: isOpen ? 1 : 0, 
              y: isOpen ? 0 : 20 
            }}
            transition={{ delay: 0.2, duration: 0.3 }}
            className="flex items-center justify-center space-x-6 pt-6 border-t border-white/10"
          >
            {[
              { icon: Github, href: "https://github.com/jenish2917" },
              { icon: Linkedin, href: "https://linkedin.com/in/jenish-barvaliya" },
              { icon: Mail, href: "mailto:jenish.barvaliya@example.com" }
            ].map(({ icon: Icon, href }, index) => (
              <motion.a
                key={index}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                href={href}
                target={href.startsWith('mailto:') ? undefined : "_blank"}
                rel={href.startsWith('mailto:') ? undefined : "noopener noreferrer"}
                className={`p-3 rounded-xl transition-all duration-300 ${
                  darkMode ? 'text-gray-300 hover:text-white hover:bg-white/10' : 'text-gray-600 hover:text-black hover:bg-black/10'
                }`}
              >
                <Icon size={20} />
              </motion.a>
            ))}
          </motion.div>
        </div>
      </motion.div>
    </motion.nav>
  )
}

export default Navbar
