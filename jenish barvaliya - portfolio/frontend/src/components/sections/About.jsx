import React from 'react'
import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { Brain, Code, Database, Lightbulb, User, Target, Award, Zap } from 'lucide-react'
import { useAbout, usePersonalInfo } from '../../hooks/useApiData'
import { about as fallbackAbout, personalInfo as fallbackPersonalInfo } from '../../data/portfolio'

const About = ({ darkMode }) => {
  const { data: about, loading: aboutLoading } = useAbout(fallbackAbout);
  const { data: personalInfo, loading: personalInfoLoading } = usePersonalInfo(fallbackPersonalInfo);
  const [ref, inView] = useInView({
    threshold: 0.1,
    triggerOnce: true
  })

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        duration: 0.8
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

  const cardVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  }

  const highlightIcons = [
    { icon: Brain, color: darkMode ? "text-white" : "text-black", bg: darkMode ? "bg-white/10" : "bg-black/10", label: "AI/ML" },
    { icon: Code, color: darkMode ? "text-white" : "text-black", bg: darkMode ? "bg-white/10" : "bg-black/10", label: "Development" },
    { icon: Database, color: darkMode ? "text-white" : "text-black", bg: darkMode ? "bg-white/10" : "bg-black/10", label: "Data Science" },
    { icon: Lightbulb, color: darkMode ? "text-white" : "text-black", bg: darkMode ? "bg-white/10" : "bg-black/10", label: "Innovation" }
  ]

  return (
    <section id="about" className="py-24 relative pt-28">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <motion.div
          ref={ref}
          variants={containerVariants}
          initial="hidden"
          animate={inView ? "visible" : "hidden"}
          className="space-y-20"
        >
          {/* Enhanced Section Header */}
          <motion.div variants={itemVariants} className="text-center">
            <motion.span
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-mono ${
                darkMode ? 'bg-white/10 text-gray-300' : 'bg-black/10 text-gray-600'
              } mb-6 backdrop-blur-sm border border-white/10`}
            >
              <User size={16} />
              About Me
            </motion.span>
            <h2 className={`text-4xl sm:text-5xl md:text-6xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-6`}>
              Who I{' '}
              <span className="relative">
                Am
                <motion.span
                  initial={{ width: 0 }}
                  animate={inView ? { width: "100%" } : { width: 0 }}
                  transition={{ delay: 1, duration: 0.8 }}
                  className={`absolute -bottom-2 left-0 h-1 ${darkMode ? 'bg-white' : 'bg-black'} rounded-full`}
                />
              </span>
            </h2>
            <p className={`text-lg sm:text-xl ${darkMode ? 'text-gray-400' : 'text-gray-600'} max-w-3xl mx-auto leading-relaxed`}>
              Passionate developer crafting intelligent solutions at the intersection of AI and technology
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-20 items-center">
            {/* Enhanced Profile Section */}
            <motion.div variants={itemVariants} className="space-y-10">
              <div className="relative">
                {/* Enhanced Profile Image */}
                <motion.div
                  whileHover={{ scale: 1.02, rotateY: 5 }}
                  transition={{ duration: 0.3 }}
                  className={`relative w-72 h-96 mx-auto rounded-3xl ${
                    darkMode ? 'bg-gradient-to-br from-gray-800 via-gray-900 to-black' : 'bg-gradient-to-br from-gray-100 via-gray-200 to-gray-300'
                  } flex items-center justify-center shadow-2xl border border-white/10 backdrop-blur-sm overflow-hidden`}
                >
                  {personalInfo?.profile_image ? (
                    <img 
                      src={`${personalInfo.profile_image.startsWith('http') 
                        ? personalInfo.profile_image 
                        : personalInfo.profile_image.startsWith('/media/') 
                          ? `${import.meta.env.VITE_API_BASE_URL?.replace('/api', '') || 'http://127.0.0.1:8001'}${personalInfo.profile_image}`
                          : personalInfo.profile_image}?v=${Date.now()}`}
                      alt={personalInfo.name || 'Jenish Barvaliya'}
                      className="w-full h-full object-cover rounded-3xl"
                      style={{
                        filter: 'brightness(1.02) contrast(1.03)'
                      }}
                      onError={(e) => {
                        // Fallback to User icon if image fails to load
                        e.target.style.display = 'none';
                        e.target.nextElementSibling.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div 
                    className={`${personalInfo?.profile_image ? 'hidden' : 'block'} text-9xl ${darkMode ? 'text-gray-600' : 'text-gray-400'} flex items-center justify-center`}
                    id="fallback-icon"
                  >
                    <User size={140} className={darkMode ? 'text-white/60' : 'text-black/60'} />
                  </div>
                  
                  {/* Glowing border effect */}
                  <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-white/5 via-white/5 to-white/5 blur-xl -z-10" />
                </motion.div>

                {/* Enhanced Floating Icons */}
                {highlightIcons.map((item, index) => (
                  <motion.div
                    key={index}
                    initial={{ scale: 0, rotate: -180 }}
                    animate={inView ? { scale: 1, rotate: 0 } : { scale: 0, rotate: -180 }}
                    transition={{ delay: 0.5 + index * 0.15, duration: 0.8, type: "spring" }}
                    className={`absolute ${
                      index === 0 ? '-top-6 -left-6' :
                      index === 1 ? '-top-6 -right-6' :
                      index === 2 ? '-bottom-6 -left-6' :
                      '-bottom-6 -right-6'
                    }`}
                  >
                    <motion.div
                      animate={{ y: [0, -12, 0] }}
                      transition={{ duration: 3, repeat: Infinity, delay: index * 0.7 }}
                      whileHover={{ scale: 1.1, rotate: 5 }}
                      className={`p-4 rounded-2xl ${item.bg} ${darkMode ? 'bg-black border border-white/10' : 'bg-white border border-black/10'} shadow-xl backdrop-blur-sm group cursor-pointer`}
                    >
                      <item.icon size={28} className={item.color} />
                      <div className={`absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-xs font-medium ${darkMode ? 'text-gray-400' : 'text-gray-600'} opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap`}>
                        {item.label}
                      </div>
                    </motion.div>
                  </motion.div>
                ))}
              </div>

              {/* Enhanced Skills Grid */}
              <motion.div variants={cardVariants} className="grid grid-cols-2 gap-4">
                {[
                  { icon: Target, label: "Problem Solver", value: "100%" },
                  { icon: Zap, label: "Fast Learner", value: "95%" },
                  { icon: Award, label: "Team Player", value: "98%" },
                  { icon: Brain, label: "Creative Thinker", value: "92%" }
                ].map((skill, index) => (
                  <motion.div
                    key={index}
                    whileHover={{ scale: 1.05, y: -5 }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
                    transition={{ delay: 1 + index * 0.1, duration: 0.6 }}
                    className={`p-5 rounded-2xl ${darkMode ? 'bg-white/5' : 'bg-black/5'} backdrop-blur-sm border border-white/10 hover:border-white/20 transition-all duration-300 group`}
                  >
                    <skill.icon size={24} className={`${darkMode ? 'text-white' : 'text-black'} mb-3 group-hover:scale-110 transition-transform`} />
                    <h4 className={`text-sm font-semibold ${darkMode ? 'text-white' : 'text-black'} mb-1`}>
                      {skill.label}
                    </h4>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                      {skill.value}
                    </p>
                  </motion.div>
                ))}
              </motion.div>
            </motion.div>

            {/* Enhanced Content Section */}
            <motion.div variants={itemVariants} className="space-y-8">
              {/* Enhanced Summary */}
              <motion.div
                variants={cardVariants}
                className={`p-8 rounded-3xl ${darkMode ? 'bg-white/5' : 'bg-black/5'} backdrop-blur-sm border border-white/10`}
              >
                <h3 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-4 flex items-center gap-3`}>
                  <User className={darkMode ? "text-white" : "text-black"} size={28} />
                  My Story
                </h3>
                <p className={`text-base ${darkMode ? 'text-gray-300' : 'text-gray-700'} leading-relaxed mb-6`}>
                  {about.summary}
                </p>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className={`p-4 rounded-2xl ${darkMode ? 'bg-white/5' : 'bg-black/5'} border-l-4 border-blue-400`}
                >
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} italic`}>
                    "{about.vision}"
                  </p>
                </motion.div>
              </motion.div>

              {/* Enhanced Highlights */}
              <motion.div
                variants={cardVariants}
                className={`p-8 rounded-3xl ${darkMode ? 'bg-white/5' : 'bg-black/5'} backdrop-blur-sm border border-white/10`}
              >
                <h3 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-6 flex items-center gap-3`}>
                  <Award className={darkMode ? "text-white" : "text-black"} size={28} />
                  Key Achievements
                </h3>
                <div className="space-y-4">
                  {about.highlights.map((highlight, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={inView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
                      transition={{ delay: 1.5 + index * 0.1, duration: 0.6 }}
                      whileHover={{ x: 10, scale: 1.02 }}
                      className="flex items-start gap-4 group"
                    >
                      <motion.div
                        whileHover={{ rotate: 90 }}
                        className={`mt-1 w-2 h-2 rounded-full ${darkMode ? 'bg-white' : 'bg-black'} flex-shrink-0 group-hover:scale-150 transition-all duration-300`}
                      />
                      <p className={`text-base ${darkMode ? 'text-gray-300 group-hover:text-white' : 'text-gray-700 group-hover:text-black'} leading-relaxed transition-colors`}>
                        {highlight}
                      </p>
                    </motion.div>
                  ))}
                </div>
              </motion.div>

              {/* Call to Action */}
              <motion.div
                variants={cardVariants}
                className="text-center"
              >
                <motion.a
                  href="#contact"
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className={`inline-flex items-center gap-3 px-8 py-4 rounded-2xl font-semibold transition-all duration-300 ${
                    darkMode 
                      ? 'bg-white text-black hover:bg-gray-200 shadow-lg hover:shadow-xl' 
                      : 'bg-black text-white hover:bg-gray-800 shadow-lg hover:shadow-xl'
                  }`}
                >
                  <span>Let's Connect</span>
                  <motion.div
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    →
                  </motion.div>
                </motion.a>
              </motion.div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default About
