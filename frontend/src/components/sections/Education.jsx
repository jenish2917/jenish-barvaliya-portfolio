import React from 'react'
import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { Calendar, MapPin, GraduationCap, BookOpen } from 'lucide-react'
import { useEducation } from '../../hooks/useApiData'
import { education as fallbackEducation } from '../../data/portfolio'

const Education = ({ darkMode }) => {
  const { data: education, loading: educationLoading } = useEducation(fallbackEducation);
  const [ref, inView] = useInView({
    threshold: 0.1,
    triggerOnce: true
  })

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.3,
        duration: 0.8
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, x: -50 },
    visible: { 
      opacity: 1, 
      x: 0,
      transition: { duration: 0.8, ease: "easeOut" }
    }
  }

  return (
    <section id="education" className="py-20 relative pt-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          ref={ref}
          variants={containerVariants}
          initial="hidden"
          animate={inView ? "visible" : "hidden"}
          className="space-y-16"
        >
          {/* Section Header */}
          <motion.div variants={itemVariants} className="text-center">
            <motion.span
              className={`inline-block px-4 py-2 rounded-full text-sm font-mono ${
                darkMode ? 'bg-white/10 text-gray-300' : 'bg-black/10 text-gray-600'
              } mb-4`}
            >
              Academic Journey
            </motion.span>
            <h2 className={`text-3xl sm:text-4xl md:text-5xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-4 sm:mb-6`}>
              Education
            </h2>
            <div className={`w-20 h-1 ${darkMode ? 'bg-white' : 'bg-black'} mx-auto`} />
          </motion.div>

          {/* Timeline */}
          <div className="relative">
            {/* Timeline Line */}
            <div className={`absolute left-8 md:left-1/2 transform md:-translate-x-1/2 top-0 bottom-0 w-0.5 ${
              darkMode ? 'bg-gray-700' : 'bg-gray-300'
            }`} />

            <div className="space-y-12">
              {Array.isArray(education) && education.length > 0 ? (
                education.map((edu, index) => (
                <motion.div
                  key={edu.id}
                  variants={itemVariants}
                  className={`relative flex items-center ${
                    index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'
                  } flex-col md:gap-8`}
                >
                  {/* Timeline Dot */}
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={inView ? { scale: 1 } : { scale: 0 }}
                    transition={{ delay: 0.5 + index * 0.2, duration: 0.5 }}
                    className={`absolute left-8 md:left-1/2 transform -translate-x-1/2 w-4 h-4 rounded-full ${
                      darkMode ? 'bg-white' : 'bg-black'
                    } border-4 ${darkMode ? 'border-black' : 'border-white'} z-10`}
                  />

                  {/* Content Card */}
                  <motion.div
                    whileHover={{ scale: 1.02, y: -5 }}
                    className={`w-full md:w-5/12 ml-16 md:ml-0 p-6 rounded-xl ${
                      darkMode ? 'bg-white/5 border border-gray-700' : 'bg-black/5 border border-gray-200'
                    } backdrop-blur-sm shadow-lg`}
                  >
                    {/* Header */}
                    <div className="mb-4">
                      <div className="flex items-start gap-3 mb-3">
                        <GraduationCap 
                          size={24} 
                          className={`${darkMode ? 'text-white' : 'text-black'} mt-1 flex-shrink-0`}
                        />
                        <div className="flex-1">
                          <h3 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-1`}>
                            {edu.degree}
                          </h3>
                          <div className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-black'} mb-2`}>
                            {edu.institution}
                          </div>
                        </div>
                      </div>
                      
                      <div className={`flex flex-wrap items-center gap-4 text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-2`}>
                        <div className="flex items-center gap-1">
                          <Calendar size={16} />
                          <span>{edu.duration}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <MapPin size={16} />
                          <span>{edu.location}</span>
                        </div>
                      </div>

                      {/* GPA */}
                      <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold ${
                        darkMode ? 'bg-white/20 text-white' : 'bg-black/20 text-black'
                      }`}>
                        GPA: {edu.gpa}
                      </div>
                    </div>

                    {/* Description */}
                    <div className="mb-6">
                      <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} mb-4`}>
                        {edu.description}
                      </p>
                    </div>

                    {/* Coursework */}
                    <div>
                      <div className={`flex items-center gap-2 text-sm font-semibold ${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-3`}>
                        <BookOpen size={16} />
                        Key Coursework:
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {edu.coursework.map((course, courseIndex) => (
                          <motion.span
                            key={courseIndex}
                            initial={{ opacity: 0, scale: 0 }}
                            animate={inView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0 }}
                            transition={{ delay: 1 + index * 0.2 + courseIndex * 0.05, duration: 0.4 }}
                            whileHover={{ scale: 1.1 }}
                            className={`px-3 py-1 text-xs rounded-full ${
                              darkMode 
                                ? 'bg-white/20 text-white border border-white/30' 
                                : 'bg-black/20 text-black border border-black/30'
                            } font-medium`}
                          >
                            {course}
                          </motion.span>
                        ))}
                      </div>
                    </div>
                  </motion.div>

                  {/* Spacer for alternating layout */}
                  <div className="hidden md:block md:w-5/12" />
                </motion.div>
              ))
              ) : (
                <motion.div
                  variants={itemVariants}
                  className="text-center py-12"
                >
                  <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Education information is currently being updated.
                    <br />
                    Please check back soon for academic details.
                  </p>
                </motion.div>
              )}
            </div>
          </div>

          {/* Additional Education Stats */}
          <motion.div
            variants={itemVariants}
            className={`grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 p-6 rounded-xl ${
              darkMode ? 'bg-white/5 border border-gray-700' : 'bg-black/5 border border-gray-200'
            } backdrop-blur-sm`}
          >
            <div className="text-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={inView ? { scale: 1 } : { scale: 0 }}
                transition={{ delay: 1.5, duration: 0.5 }}
                className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-2`}
              >
                {new Date().getFullYear() - 2022}+
              </motion.div>
              <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                Years of Study
              </div>
            </div>
            
            <div className="text-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={inView ? { scale: 1 } : { scale: 0 }}
                transition={{ delay: 1.7, duration: 0.5 }}
                className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-2`}
              >
                8.7
              </motion.div>
              <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                Current GPA
              </div>
            </div>
            
            <div className="text-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={inView ? { scale: 1 } : { scale: 0 }}
                transition={{ delay: 1.9, duration: 0.5 }}
                className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-2`}
              >
                IT
              </motion.div>
              <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                Specialization
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}

export default Education
