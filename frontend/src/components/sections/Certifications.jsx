import React from 'react'
import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { Award, Calendar, ExternalLink, CheckCircle, Badge, Building2, Shield } from 'lucide-react'
import { useCertifications } from '../../hooks/useApiData'
import { certifications as fallbackCertifications } from '../../data/portfolio'

const Certifications = ({ darkMode }) => {
  const { data: certifications, loading: certificationsLoading } = useCertifications(fallbackCertifications);
  const [ref, inView] = useInView({
    threshold: 0.1,
    triggerOnce: true
  })

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        duration: 0.8
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.8, ease: "easeOut" }
    }
  }

  const cardVariants = {
    hidden: { opacity: 0, scale: 0.9, rotateY: -30 },
    visible: { 
      opacity: 1, 
      scale: 1,
      rotateY: 0,
      transition: { duration: 0.8, ease: "easeOut" }
    }
  }

  return (
    <section id="certifications" className="py-20 relative pt-28">
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
              Achievements
            </motion.span>
            <h2 className={`text-4xl md:text-5xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-6`}>
              Certifications
            </h2>
            <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'} max-w-3xl mx-auto mb-6`}>
              Professional certifications that validate my expertise in AI/ML, cloud computing, and data science.
            </p>
            <div className={`w-20 h-1 ${darkMode ? 'bg-white' : 'bg-black'} mx-auto`} />
          </motion.div>

          {/* Certifications Grid */}
          <motion.div
            variants={containerVariants}
            className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 lg:gap-8"
          >
            {Array.isArray(certifications) && certifications.length > 0 ? (
              certifications.map((cert, index) => (
              <motion.div
                key={cert.id}
                variants={cardVariants}
                whileHover={{ 
                  scale: 1.03, 
                  y: -10,
                  rotateY: 5,
                  boxShadow: darkMode ? "0 20px 40px rgba(255,255,255,0.1)" : "0 20px 40px rgba(0,0,0,0.1)"
                }}
                className={`group relative overflow-hidden rounded-xl ${
                  darkMode ? 'bg-white/5 border border-gray-700' : 'bg-black/5 border border-gray-200'
                } backdrop-blur-sm shadow-lg transform-gpu`}
                style={{ perspective: "1000px" }}
              >
                {/* Background Gradient */}
                <div className={`absolute inset-0 bg-gradient-to-br ${
                  'from-white/5 to-white/5'
                } opacity-0 group-hover:opacity-100 transition-opacity duration-300`} />

                <div className="relative p-6 space-y-4">
                  {/* Header */}
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-4">
                      {/* Logo Placeholder */}
                      <motion.div
                        whileHover={{ rotate: 360 }}
                        transition={{ duration: 0.8 }}
                        className={`w-12 h-12 rounded-lg ${
                          darkMode ? 'bg-gray-800' : 'bg-gray-200'
                        } flex items-center justify-center text-2xl`}
                      >
                        <Award className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`} size={24} />
                      </motion.div>
                      <div>
                        <h3 className={`text-lg font-bold ${darkMode ? 'text-white' : 'text-black'} group-hover:${darkMode ? 'text-gray-300' : 'text-gray-700'} transition-colors`}>
                          {cert.title}
                        </h3>
                        <p className={`text-sm font-semibold ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                          {cert.issuer}
                        </p>
                      </div>
                    </div>

                    {/* Date */}
                    <div className={`flex items-center space-x-1 text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                      <Calendar size={14} />
                      <span>{cert.date}</span>
                    </div>
                  </div>

                  {/* Description */}
                  <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} text-sm leading-relaxed`}>
                    {cert.description}
                  </p>

                  {/* Credential ID */}
                  <div className={`text-xs font-mono ${darkMode ? 'text-gray-500' : 'text-gray-400'} bg-gray-500/10 px-2 py-1 rounded`}>
                    ID: {cert.credentialId}
                  </div>

                  {/* Action Button */}
                  <motion.a
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    href={cert.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`inline-flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300 ${
                      darkMode 
                        ? 'bg-white/10 hover:bg-white/20 text-white border border-white/20 hover:border-white/40' 
                        : 'bg-black/10 hover:bg-black/20 text-black border border-black/20 hover:border-black/40'
                    }`}
                  >
                    <span>Verify Certificate</span>
                    <ExternalLink size={14} />
                  </motion.a>
                </div>

                {/* Floating Elements */}
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <motion.div
                    animate={{ rotate: [0, 360] }}
                    transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                    className={`w-8 h-8 border-2 ${
                      darkMode ? 'border-gray-400' : 'border-gray-600'
                    } border-dashed rounded-full`}
                  />
                </div>
              </motion.div>
            ))
            ) : (
              <motion.div
                variants={cardVariants}
                className="col-span-full text-center py-12"
              >
                <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  Certifications are currently being updated.
                  <br />
                  Check back soon for my latest achievements!
                </p>
              </motion.div>
            )}
          </motion.div>

          {/* Call to Action */}
          <motion.div
            variants={itemVariants}
            className={`text-center p-8 rounded-xl ${
              darkMode ? 'bg-gradient-to-r from-white/5 to-white/5 border border-white/10' : 'bg-gradient-to-r from-black/5 to-black/5 border border-black/10'
            }`}
          >
            <h3 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-4`}>
              Continuous Professional Development
            </h3>
            <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} mb-6 max-w-2xl mx-auto`}>
              I'm committed to staying current with industry trends and continuously expanding my knowledge through 
              professional certifications and hands-on learning.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}

export default Certifications
