import React from 'react'
import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { 
  Code, Database, Brain, Bot, Eye, MessageSquare, Globe, Server, 
  Zap, Layout, Palette, BarChart3, Calculator, LineChart, 
  TrendingUp, PieChart, BarChart, GitBranch, Package, Cloud 
} from 'lucide-react'
import { useSkills } from '../../hooks/useApiData'
import { skills as fallbackSkills } from '../../data/portfolio'

const Skills = ({ darkMode }) => {
  const { data: skills, loading: skillsLoading } = useSkills(fallbackSkills);
  const [ref, inView] = useInView({
    threshold: 0.1,
    triggerOnce: true
  })

  // Map icon names to components
  const iconMap = {
    Code, Database, Brain, Bot, Eye, MessageSquare, Globe, Server,
    Zap, Layout, Palette, BarChart3, Calculator, LineChart,
    TrendingUp, PieChart, BarChart, GitBranch, Package, Cloud
  }

  const getIcon = (iconName) => {
    const IconComponent = iconMap[iconName]
    return IconComponent ? <IconComponent className="w-6 h-6" /> : <Code className="w-6 h-6" />
  }

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

  const skillVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  }

  return (
    <section id="skills" className="py-20 relative pt-28">
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
              Technical Expertise
            </motion.span>
            <h2 className={`text-4xl md:text-5xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-6`}>
              Skills & Technologies
            </h2>
            <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'} max-w-3xl mx-auto mb-6`}>
              A comprehensive overview of my technical skills across various domains including AI/ML, web development, and data science.
            </p>
            <div className={`w-20 h-1 ${darkMode ? 'bg-white' : 'bg-black'} mx-auto`} />
          </motion.div>

          {/* Skills Categories */}
          <div className="space-y-16">
            {Object.entries(skills).map(([category, categorySkills], categoryIndex) => (
              <motion.div
                key={category}
                variants={itemVariants}
                className="space-y-8"
              >
                {/* Category Header */}
                <div className="text-center">
                  <h3 className={`text-2xl md:text-3xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-4`}>
                    {category}
                  </h3>
                  <div className={`w-12 h-0.5 ${darkMode ? 'bg-white' : 'bg-black'} mx-auto`} />
                </div>

                {/* Skills Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {categorySkills.map((skill, skillIndex) => (
                    <motion.div
                      key={skill.name}
                      variants={skillVariants}
                      whileHover={{ scale: 1.05, y: -5 }}
                      className={`group p-6 rounded-xl ${
                        darkMode ? 'bg-white/5 border border-gray-700 hover:border-gray-600' : 'bg-black/5 border border-gray-200 hover:border-gray-300'
                      } backdrop-blur-sm transition-all duration-300`}
                    >
                      {/* Skill Header */}
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <span className={`${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                            {getIcon(skill.icon)}
                          </span>
                          <h4 className={`font-semibold ${darkMode ? 'text-white' : 'text-black'} group-hover:${darkMode ? 'text-gray-300' : 'text-gray-700'} transition-colors`}>
                            {skill.name}
                          </h4>
                        </div>
                        <span className={`text-sm font-mono ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                          {skill.level}%
                        </span>
                      </div>

                      {/* Progress Bar */}
                      <div className={`w-full h-2 ${darkMode ? 'bg-gray-800' : 'bg-gray-200'} rounded-full overflow-hidden`}>
                        <motion.div
                          initial={{ width: 0 }}
                          animate={inView ? { width: `${skill.level}%` } : { width: 0 }}
                          transition={{ 
                            delay: 0.5 + categoryIndex * 0.2 + skillIndex * 0.1, 
                            duration: 1.2, 
                            ease: "easeOut" 
                          }}
                          className={`h-full ${darkMode ? 'bg-gradient-to-r from-white to-gray-300' : 'bg-gradient-to-r from-black to-gray-700'} rounded-full relative`}
                        >
                          <motion.div
                            animate={{ x: [-10, 10, -10] }}
                            transition={{ duration: 2, repeat: Infinity }}
                            className="absolute inset-0 bg-white/20 rounded-full"
                          />
                        </motion.div>
                      </div>

                      {/* Skill Level Description */}
                      <div className="mt-3">
                        <span className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'} font-medium`}>
                          {skill.level >= 90 ? 'Expert' : 
                           skill.level >= 80 ? 'Advanced' : 
                           skill.level >= 70 ? 'Intermediate' : 'Beginner'}
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>

          {/* Skills Summary */}
          <motion.div
            variants={itemVariants}
            className={`p-8 rounded-xl ${
              darkMode ? 'bg-gradient-to-r from-white/5 to-white/5 border border-white/10' : 'bg-gradient-to-r from-black/5 to-black/5 border border-black/10'
            } text-center`}
          >
            <h3 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-4`}>
              Continuous Learning
            </h3>
            <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} mb-6 max-w-3xl mx-auto`}>
              I'm constantly expanding my skill set and staying updated with the latest technologies. 
              Currently exploring advanced topics in Deep Learning, MLOps, and Cloud Computing.
            </p>
            
            {/* Current Learning */}
            <div className="flex flex-wrap justify-center gap-3">
              {['PyTorch Lightning', 'Kubernetes', 'GraphQL', 'Rust', 'WebAssembly'].map((tech, index) => (
                <motion.span
                  key={tech}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={inView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0 }}
                  transition={{ delay: 2 + index * 0.1, duration: 0.5 }}
                  whileHover={{ scale: 1.1 }}
                  className={`px-4 py-2 rounded-full text-sm font-medium ${
                    darkMode 
                      ? darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                      : darkMode ? 'bg-white/20 text-white border border-white/30' : 'bg-black/20 text-black border border-black/30'
                  }`}
                >
                  🔄 {tech}
                </motion.span>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}

export default Skills
