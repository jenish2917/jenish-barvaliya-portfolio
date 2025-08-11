import React from 'react'
import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { Calendar, MapPin, ExternalLink } from 'lucide-react'
import { useExperience } from '../../hooks/useApiData'
import { experience as fallbackExperience } from '../../data/portfolio'

const Experience = ({ darkMode }) => {
  const { data: experience, loading: experienceLoading } = useExperience(fallbackExperience);
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
    <section id="experience" className="py-20 relative pt-28">
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
              Professional Journey
            </motion.span>
            <h2 className={`text-4xl md:text-5xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-6`}>
              Experience
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
              {Array.isArray(experience) && experience.length > 0 ? (
                experience.map((exp, index) => (
                <motion.div
                  key={exp.id}
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
                      <h3 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-2`}>
                        {exp.title}
                      </h3>
                      <div className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-black'} mb-2`}>
                        {exp.company}
                      </div>
                      <div className={`flex flex-wrap items-center gap-4 text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                        <div className="flex items-center gap-1">
                          <Calendar size={16} />
                          <span>{exp.duration}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <MapPin size={16} />
                          <span>{exp.location}</span>
                        </div>
                      </div>
                    </div>

                    {/* Description */}
                    <div className="mb-6">
                      <ul className="space-y-2">
                        {exp.description.map((desc, descIndex) => (
                          <motion.li
                            key={descIndex}
                            initial={{ opacity: 0, x: -20 }}
                            animate={inView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
                            transition={{ delay: 0.8 + index * 0.2 + descIndex * 0.1, duration: 0.6 }}
                            className={`flex items-start space-x-2 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}
                          >
                            <span className={`w-1.5 h-1.5 rounded-full ${darkMode ? 'bg-white' : 'bg-black'} mt-2 flex-shrink-0`} />
                            <span>{desc}</span>
                          </motion.li>
                        ))}
                      </ul>
                    </div>

                    {/* Technologies */}
                    <div>
                      <div className={`text-sm font-semibold ${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-3`}>
                        Technologies Used:
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {exp.technologies.map((tech, techIndex) => (
                          <motion.span
                            key={techIndex}
                            initial={{ opacity: 0, scale: 0 }}
                            animate={inView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0 }}
                            transition={{ delay: 1 + index * 0.2 + techIndex * 0.05, duration: 0.4 }}
                            whileHover={{ scale: 1.1 }}
                            className={`px-3 py-1 text-xs rounded-full ${
                              darkMode 
                                ? darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                                : darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                            } font-medium`}
                          >
                            {tech}
                          </motion.span>
                        ))}
                      </div>
                    </div>
                  </motion.div>

                  {/* Spacer for alternating layout */}
                  <div className="hidden md:block w-5/12" />
                </motion.div>
              ))
              ) : (
                <motion.div
                  variants={itemVariants}
                  className="text-center py-12"
                >
                  <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Currently seeking internship opportunities in Machine Learning and AI.
                    <br />
                    Looking forward to gaining practical experience in the field.
                  </p>
                </motion.div>
              )}
            </div>
          </div>

          {/* Call to Action */}
          <motion.div
            variants={itemVariants}
            className="text-center pt-12"
          >
            <motion.div
              whileHover={{ scale: 1.02 }}
              className={`inline-block p-6 rounded-xl ${
                darkMode ? 'bg-gradient-to-r from-white/5 to-white/5 border border-white/10' : 'bg-gradient-to-r from-black/5 to-black/5 border border-black/10'
              } max-w-md mx-auto`}
            >
              <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} mb-4`}>
                Want to know more about my professional journey?
              </p>
              <motion.a
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                href="/resume.pdf"
                download
                className={`inline-flex items-center px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                  darkMode 
                    ? 'bg-white text-black hover:bg-gray-200' 
                    : 'bg-black text-white hover:bg-gray-800'
                }`}
              >
                <ExternalLink size={18} className="mr-2" />
                View Full Resume
              </motion.a>
            </motion.div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}

export default Experience
