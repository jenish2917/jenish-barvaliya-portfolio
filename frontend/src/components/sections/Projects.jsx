import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { ExternalLink, Github, Eye, X, Folder } from 'lucide-react'
import { useProjects } from '../../hooks/useApiData'
import { projects as fallbackProjects } from '../../data/portfolio'

const Projects = ({ darkMode }) => {
  const { data: projects, loading: projectsLoading } = useProjects(fallbackProjects);
  const [selectedProject, setSelectedProject] = useState(null)
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
    hidden: { opacity: 0, scale: 0.9 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  }

  return (
    <section id="projects" className="py-16 sm:py-20 relative pt-20 sm:pt-28">
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
              Portfolio
            </motion.span>
            <h2 className={`text-3xl sm:text-4xl md:text-5xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-4 sm:mb-6`}>
              Featured Projects
            </h2>
            <p className={`text-sm sm:text-base md:text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'} max-w-3xl mx-auto mb-4 sm:mb-6 px-6 text-center leading-relaxed`}>
              A collection of my most impactful projects showcasing expertise in AI/ML, web development, and data science.
            </p>
            <div className={`w-20 h-1 ${darkMode ? 'bg-white' : 'bg-black'} mx-auto`} />
          </motion.div>

          {/* Projects Grid */}
          <motion.div
            variants={containerVariants}
            className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8"
          >
            {Array.isArray(projects) && projects.length > 0 ? (
              projects.map((project, index) => (
              <motion.div
                key={project.id}
                variants={cardVariants}
                whileHover={{ y: -10, scale: 1.02 }}
                className={`group relative overflow-hidden rounded-xl ${
                  darkMode ? 'bg-white/5 border border-gray-700' : 'bg-black/5 border border-gray-200'
                } backdrop-blur-sm shadow-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-white/20`}
                onClick={() => setSelectedProject(project)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    setSelectedProject(project);
                  }
                }}
                tabIndex={0}
                role="button"
                aria-label={`View details for ${project.title} project`}
              >
                {/* Project Image */}
                <div className="relative h-40 sm:h-48 overflow-hidden">
                  <div className={`w-full h-full ${
                    darkMode ? 'bg-gradient-to-br from-gray-800 to-gray-900' : 'bg-gradient-to-br from-gray-100 to-gray-200'
                  } flex items-center justify-center`}>
                    <div className={`text-4xl ${darkMode ? 'text-gray-600' : 'text-gray-400'}`}>
                      <Folder size={48} className={darkMode ? 'text-white/60' : 'text-black/60'} />
                    </div>
                  </div>
                  
                  {/* Overlay */}
                  <div className={`absolute inset-0 ${
                    darkMode ? 'bg-black/60' : 'bg-white/60'
                  } opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center space-x-4`}>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={(e) => {
                        e.stopPropagation()
                        setSelectedProject(project)
                      }}
                      className={`p-2 rounded-full ${darkMode ? 'bg-white text-black' : 'bg-black text-white'}`}
                    >
                      <Eye size={20} />
                    </motion.button>
                    {project.github && (
                      <motion.a
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        href={project.github}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className={`p-2 rounded-full ${darkMode ? 'bg-white text-black' : 'bg-black text-white'}`}
                      >
                        <Github size={20} />
                      </motion.a>
                    )}
                    {project.live && (
                      <motion.a
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        href={project.live}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className={`p-2 rounded-full ${darkMode ? 'bg-white text-black' : 'bg-black text-white'}`}
                      >
                        <ExternalLink size={20} />
                      </motion.a>
                    )}
                  </div>

                  {/* Status Badge */}
                  <div className="absolute top-4 right-4">
                    <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                      project.status === 'Completed' 
                        ? darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                        : darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                    }`}>
                      {project.status}
                    </span>
                  </div>
                </div>

                {/* Project Info */}
                <div className="p-6 space-y-4">
                  <h3 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-black'} group-hover:${darkMode ? 'text-gray-300' : 'text-gray-700'} transition-colors`}>
                    {project.title}
                  </h3>
                  
                  <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} text-sm leading-relaxed line-clamp-3`}>
                    {project.description}
                  </p>

                  {/* Technologies */}
                  <div className="flex flex-wrap gap-1">
                    {project.technologies.slice(0, 4).map((tech, techIndex) => (
                      <span
                        key={techIndex}
                        className={`px-2 py-1 text-xs rounded-md ${
                          darkMode 
                            ? darkMode ? 'bg-white/10 text-white border border-white/20' : 'bg-black/10 text-black border border-black/20'
                            : darkMode ? 'bg-white/10 text-white border border-white/20' : 'bg-black/10 text-black border border-black/20'
                        } font-medium`}
                      >
                        {tech}
                      </span>
                    ))}
                    {project.technologies.length > 4 && (
                      <span className={`px-2 py-1 text-xs rounded-md ${
                        darkMode ? 'text-gray-400' : 'text-gray-500'
                      }`}>
                        +{project.technologies.length - 4}
                      </span>
                    )}
                  </div>
                </div>
              </motion.div>
            ))
            ) : (
              <motion.div
                variants={cardVariants}
                className="col-span-full text-center py-12"
              >
                <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  Projects are currently being updated.
                  <br />
                  Check back soon for my latest work!
                </p>
              </motion.div>
            )}
          </motion.div>

          {/* Call to Action */}
          <motion.div variants={itemVariants} className="text-center">
            <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-6`}>
              Want to see more of my work?
            </p>
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="https://github.com/jenish2917"
              target="_blank"
              rel="noopener noreferrer"
              className={`inline-flex items-center px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                darkMode 
                  ? 'border-2 border-gray-500 text-white hover:border-white hover:bg-white/10' 
                  : 'border-2 border-gray-400 text-black hover:border-black hover:bg-black/10'
              }`}
            >
              <Github size={18} className="mr-2" />
              View All Projects
            </motion.a>
          </motion.div>
        </motion.div>
      </div>

      {/* Project Modal */}
      <AnimatePresence>
        {selectedProject && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[60] flex items-center justify-center p-2 sm:p-4 bg-black/80"
            onClick={() => setSelectedProject(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className={`relative max-w-4xl w-full max-h-[95vh] sm:max-h-[90vh] overflow-y-auto rounded-lg sm:rounded-xl ${
                darkMode ? 'bg-gray-900 border border-gray-700' : 'bg-white border border-gray-200'
              } shadow-2xl`}
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close Button */}
              <button
                onClick={() => setSelectedProject(null)}
                className={`absolute top-4 right-4 z-10 p-2 rounded-full ${
                  darkMode ? 'bg-white/10 hover:bg-white/20 text-white' : 'bg-black/10 hover:bg-black/20 text-black'
                }`}
              >
                <X size={20} />
              </button>

              {/* Modal Content */}
              <div className="p-4 sm:p-6 lg:p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
                  {/* Project Image */}
                  <div className="space-y-4">
                    <div className={`h-48 sm:h-64 rounded-lg ${
                      darkMode ? 'bg-gradient-to-br from-gray-800 to-gray-900' : 'bg-gradient-to-br from-gray-100 to-gray-200'
                    } flex items-center justify-center`}>
                      <div className={`text-6xl ${darkMode ? 'text-gray-600' : 'text-gray-400'}`}>
                        <Folder size={80} className={darkMode ? 'text-white/60' : 'text-black/60'} />
                      </div>
                    </div>
                    
                    {/* Action Buttons */}
                    <div className="flex space-x-4">
                      {selectedProject.github && (
                        <motion.a
                          whileHover={{ scale: 1.05 }}
                          href={selectedProject.github}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={`flex-1 inline-flex items-center justify-center px-4 py-3 rounded-lg font-semibold ${
                            darkMode ? 'bg-white text-black hover:bg-gray-200' : 'bg-black text-white hover:bg-gray-800'
                          }`}
                        >
                          <Github size={18} className="mr-2" />
                          GitHub
                        </motion.a>
                      )}
                      {selectedProject.live && (
                        <motion.a
                          whileHover={{ scale: 1.05 }}
                          href={selectedProject.live}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={`flex-1 inline-flex items-center justify-center px-4 py-3 rounded-lg font-semibold border-2 ${
                            darkMode 
                              ? 'border-gray-500 text-white hover:border-white hover:bg-white/10' 
                              : 'border-gray-400 text-black hover:border-black hover:bg-black/10'
                          }`}
                        >
                          <ExternalLink size={18} className="mr-2" />
                          Live Demo
                        </motion.a>
                      )}
                    </div>
                  </div>

                  {/* Project Details */}
                  <div className="space-y-6">
                    <div>
                      <h3 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-2`}>
                        {selectedProject.title}
                      </h3>
                      <span className={`px-3 py-1 text-sm rounded-full font-medium ${
                        selectedProject.status === 'Completed' 
                          ? darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                          : darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                      }`}>
                        {selectedProject.status}
                      </span>
                    </div>

                    <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} leading-relaxed`}>
                      {selectedProject.longDescription}
                    </p>

                    {/* Features */}
                    {selectedProject.features && (
                      <div>
                        <h4 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-black'} mb-3`}>
                          Key Features:
                        </h4>
                        <ul className="space-y-2">
                          {selectedProject.features.map((feature, index) => (
                            <li key={index} className={`flex items-start space-x-2 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                              <span className={`w-1.5 h-1.5 rounded-full ${darkMode ? 'bg-white' : 'bg-black'} mt-2 flex-shrink-0`} />
                              <span>{feature}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Technologies */}
                    <div>
                      <h4 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-black'} mb-3`}>
                        Technologies Used:
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {selectedProject.technologies.map((tech, index) => (
                          <span
                            key={index}
                            className={`px-3 py-1 text-sm rounded-full ${
                              darkMode 
                                ? darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                                : darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                            } font-medium`}
                          >
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  )
}

export default Projects
