import React from 'react'
import { motion } from 'framer-motion'
import { Download, Mail, Clock, FolderOpen, Lightbulb, Star } from 'lucide-react'
import { usePersonalInfo } from '../../hooks/useApiData'
import { personalInfo as fallbackPersonalInfo } from '../../data/portfolio'

const Hero = ({ darkMode }) => {
  const { data: personalInfo, loading: personalInfoLoading } = usePersonalInfo(fallbackPersonalInfo);
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 1.2,
        staggerChildren: 0.15
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.8, ease: "easeOut" }
    }
  }

  const floatingIconVariants = {
    hidden: { opacity: 0, scale: 0 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { duration: 0.6, delay: 2.5 }
    }
  }

  const typewriterText = "AI/ML Engineer & Developer"

  return (
    <section id="hero" className="min-h-screen flex items-center justify-center relative overflow-hidden px-2 sm:px-4 lg:px-8 pt-16 sm:pt-20 pb-8 sm:pb-0">
      {/* Simplified background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Subtle gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/[0.005] to-transparent" />
      </div>

      <div className="max-w-6xl mx-auto text-center relative z-10 w-full min-w-0">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-8 sm:space-y-12"
        >
          {/* Greeting with enhanced styling */}
          <motion.div variants={itemVariants} className="space-y-2">
            <motion.span
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5, duration: 0.6 }}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-mono ${
                darkMode ? 'bg-white/5 text-gray-300 border border-white/10' : 'bg-black/5 text-gray-600 border border-black/10'
              } backdrop-blur-sm`}
            >
              Hello, I'm
            </motion.span>
          </motion.div>

          {/* Name with enhanced typography */}
          <motion.h1
            variants={itemVariants}
            className={`text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-black ${
              darkMode ? 'text-white' : 'text-black'
            } tracking-tight leading-none`}
          >
            <span className="relative inline-block">
              {personalInfo.name.split(' ').map((word, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, y: 50, rotateX: -90 }}
                  animate={{ opacity: 1, y: 0, rotateX: 0 }}
                  transition={{ 
                    delay: 0.8 + index * 0.15, 
                    duration: 0.8,
                    type: "spring",
                    stiffness: 100
                  }}
                  className="inline-block mr-4 sm:mr-6"
                  style={{ transformOrigin: "center bottom" }}
                >
                  {word}
                </motion.span>
              ))}
            </span>
          </motion.h1>

          {/* Enhanced animated title */}
          <motion.div 
            variants={itemVariants} 
            className="h-16 sm:h-20 flex items-center justify-center w-full"
          >
            <motion.h2
              className={`text-base sm:text-lg md:text-xl lg:text-2xl ${
                darkMode ? 'text-gray-300' : 'text-gray-600'
              } font-mono w-full font-medium px-2 sm:px-4 text-center leading-tight`}
            >
              <motion.span
                initial={{ width: 0 }}
                animate={{ width: "auto" }}
                transition={{ delay: 1.5, duration: 3, ease: "easeInOut" }}
                className="inline-block whitespace-nowrap"
                style={{ minWidth: "280px" }}
              >
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1.5, duration: 0.1 }}
                  className="border-r-2 border-current"
                >
                  {typewriterText}
                </motion.span>
              </motion.span>
            </motion.h2>
          </motion.div>

          {/* Enhanced subtitle */}
          <motion.p
            variants={itemVariants}
            className={`text-sm sm:text-base md:text-lg ${
              darkMode ? 'text-gray-400' : 'text-gray-500'
            } max-w-3xl mx-auto leading-relaxed font-light px-6 text-center`}
          >
            Passionate Information Technology student specializing in{' '}
            <span className={`font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
              Machine Learning
            </span>
            {', '}
            <span className={`font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
              Artificial Intelligence
            </span>
            {', and modern web technologies. Building innovative solutions that bridge the gap between AI research and real-world applications.'}
          </motion.p>

          {/* Enhanced action buttons */}
          <motion.div
            variants={itemVariants}
            className="flex flex-col gap-4 sm:flex-row sm:gap-6 justify-center items-center pt-6 sm:pt-12 px-4 max-w-sm sm:max-w-none mx-auto"
          >
            <motion.a
              whileHover={{ 
                scale: 1.05, 
                boxShadow: "0 20px 40px rgba(255,255,255,0.1)" 
              }}
              whileTap={{ scale: 0.95 }}
              href={personalInfo.resume}
              download
              aria-label="Download resume PDF"
              className={`group relative inline-flex items-center px-6 py-3 sm:px-8 sm:py-4 rounded-2xl font-semibold text-sm sm:text-base lg:text-lg transition-all duration-300 overflow-hidden w-full sm:w-auto justify-center focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                darkMode 
                  ? 'bg-white text-black hover:bg-gray-100 focus:ring-white focus:ring-offset-black' 
                  : 'bg-black text-white hover:bg-gray-900 focus:ring-black focus:ring-offset-white'
              } shadow-lg hover:shadow-xl`}
            >
              {/* Button shine effect */}
              <div className="absolute inset-0 -top-1 -left-1 bg-gradient-to-r from-transparent via-white/20 to-transparent rotate-45 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700" />
              
              <Download size={18} className="mr-2 sm:mr-3 transition-transform group-hover:scale-110" />
              Download Resume
            </motion.a>

            <motion.a
              whileHover={{ 
                scale: 1.05,
                borderColor: darkMode ? "#ffffff" : "#000000"
              }}
              whileTap={{ scale: 0.95 }}
              href={`mailto:${personalInfo.email}`}
              aria-label="Send email to contact"
              className={`group inline-flex items-center px-6 py-3 sm:px-8 sm:py-4 rounded-2xl font-semibold text-sm sm:text-base lg:text-lg border-2 transition-all duration-300 backdrop-blur-sm w-full sm:w-auto justify-center focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                darkMode 
                  ? 'border-gray-500 text-white hover:border-white hover:bg-white/5 hover:shadow-glow-md focus:ring-white focus:ring-offset-black' 
                  : 'border-gray-400 text-black hover:border-black hover:bg-black/5 focus:ring-black focus:ring-offset-white'
              }`}
            >
              <Mail size={18} className="mr-2 sm:mr-3 transition-transform group-hover:scale-110" />
              Contact Me
            </motion.a>
          </motion.div>

        </motion.div>
      </div>
    </section>
  )
}

export default Hero
