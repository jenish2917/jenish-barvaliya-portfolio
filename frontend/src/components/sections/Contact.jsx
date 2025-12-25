import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { Send, Mail, Phone, MapPin, Github, Linkedin, MessageSquare, CheckCircle, AlertCircle } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { usePersonalInfo, useSocialLinks } from '../../hooks/useApiData'
import { personalInfo as fallbackPersonalInfo, socialLinks as fallbackSocialLinks } from '../../data/portfolio'
import ApiService from '../../services/api'

const Contact = ({ darkMode }) => {
  const { data: personalInfo } = usePersonalInfo(fallbackPersonalInfo);
  const { data: socialLinks } = useSocialLinks(fallbackSocialLinks);
  const [ref, inView] = useInView({
    threshold: 0.1,
    triggerOnce: true
  })

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [formStatus, setFormStatus] = useState(null) // 'success' | 'error' | null

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
    hidden: { opacity: 0, y: 30 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.8, ease: "easeOut" }
    }
  }

  const cardVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    // Clear status when user starts typing again
    if (formStatus) setFormStatus(null)
  }

  const validateForm = () => {
    const { name, email, subject, message } = formData
    if (!name.trim() || !email.trim() || !subject.trim() || !message.trim()) {
      toast.error('Please fill in all fields')
      return false
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      toast.error('Please enter a valid email address')
      return false
    }
    
    return true
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Basic form validation
    if (!formData.name.trim() || !formData.email.trim() || !formData.message.trim()) {
      toast.error('Please fill in all required fields')
      return
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(formData.email)) {
      toast.error('Please enter a valid email address')
      return
    }
    
    setIsSubmitting(true)

    try {
      // Try to submit to backend first
      console.log('Submitting contact form:', formData)
      console.log('API endpoint:', 'http://127.0.0.1:8000/api/contact/')
      
      const result = await ApiService.submitContact(formData);
      console.log('Contact form submission successful:', result)
      
      toast.success('Message sent successfully! I\'ll get back to you soon.')
      setFormData({ name: '', email: '', subject: '', message: '' })
    } catch (error) {
      console.error('Error sending message:', error)
      console.error('Error details:', {
        message: error.message,
        status: error.status,
        response: error.response
      })
      
      // Fallback: Create mailto link with pre-filled content
      const subject = encodeURIComponent(formData.subject || 'Portfolio Contact')
      const body = encodeURIComponent(
        `Name: ${formData.name}\nEmail: ${formData.email}\n\nMessage:\n${formData.message}`
      )
      const mailtoLink = `mailto:${personalInfo.email}?subject=${subject}&body=${body}`
      
      // Open mailto link
      window.open(mailtoLink, '_blank')
      
      toast.success('Redirected to your email client. Please send the message from there.')
      setFormData({ name: '', email: '', subject: '', message: '' })
    } finally {
      setIsSubmitting(false)
    }
  }

  const contactInfo = [
    {
      icon: Mail,
      label: 'Email',
      value: personalInfo.email,
      href: `mailto:${personalInfo.email}`,
      color: darkMode ? 'text-white' : 'text-black'
    },
    {
      icon: Phone,
      label: 'Phone',
      value: personalInfo.phone,
      href: `tel:${personalInfo.phone}`,
      color: darkMode ? 'text-white' : 'text-black'
    },
    {
      icon: MapPin,
      label: 'Location',
      value: personalInfo.location,
      href: '#',
      color: darkMode ? 'text-white' : 'text-black'
    }
  ]

  return (
    <section id="contact" className="py-20 relative pt-28">
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
              Get In Touch
            </motion.span>
            <h2 className={`text-3xl sm:text-4xl md:text-5xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-4 sm:mb-6`}>
              Contact Me
            </h2>
            <p className={`text-sm sm:text-base md:text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'} max-w-3xl mx-auto mb-4 sm:mb-6 px-6 text-center leading-relaxed`}>
              I'm always open to discussing new opportunities, collaborations, or just having a chat about AI/ML and technology. 
              Feel free to reach out!
            </p>
            <div className={`w-20 h-1 ${darkMode ? 'bg-white' : 'bg-black'} mx-auto`} />
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16">
            {/* Contact Information */}
            <motion.div variants={itemVariants} className="space-y-8">
              <div>
                <h3 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-6`}>
                  Let's Connect
                </h3>
                <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} leading-relaxed mb-8`}>
                  Whether you're looking for a collaborator on an exciting AI project, need consultation on machine learning solutions, 
                  or just want to discuss the latest developments in technology, I'd love to hear from you.
                </p>
              </div>

              {/* Contact Details */}
              <div className="space-y-6">
                {contactInfo.map((contact, index) => (
                  <motion.a
                    key={contact.label}
                    href={contact.href}
                    initial={{ opacity: 0, x: -30 }}
                    animate={inView ? { opacity: 1, x: 0 } : { opacity: 0, x: -30 }}
                    transition={{ delay: 0.8 + index * 0.2, duration: 0.6 }}
                    whileHover={{ scale: 1.02, x: 10 }}
                    className={`flex items-center space-x-4 p-4 rounded-xl ${
                      darkMode ? 'bg-white/5 hover:bg-white/10 border border-gray-700' : 'bg-black/5 hover:bg-black/10 border border-gray-200'
                    } transition-all duration-300 group`}
                  >
                    <div className={`p-3 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-gray-100'} group-hover:scale-110 transition-transform`}>
                      <contact.icon size={24} className={contact.color} />
                    </div>
                    <div>
                      <div className={`font-semibold ${darkMode ? 'text-white' : 'text-black'} group-hover:${darkMode ? 'text-gray-300' : 'text-gray-700'} transition-colors`}>
                        {contact.label}
                      </div>
                      <div className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} text-sm`}>
                        {contact.value}
                      </div>
                    </div>
                  </motion.a>
                ))}
              </div>

              {/* Social Links */}
              <div>
                <h4 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-black'} mb-4`}>
                  Follow Me
                </h4>
                <div className="flex space-x-4">
                  {socialLinks.map((social, index) => {
                    const IconComponent = social.icon === 'Github' ? Github : 
                                         social.icon === 'Linkedin' ? Linkedin : 
                                         social.icon === 'Mail' ? Mail : MessageSquare
                    
                    return (
                      <motion.a
                        key={social.name}
                        href={social.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        initial={{ opacity: 0, scale: 0 }}
                        animate={inView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0 }}
                        transition={{ delay: 1.2 + index * 0.1, duration: 0.5 }}
                        whileHover={{ scale: 1.1, y: -5 }}
                        whileTap={{ scale: 0.9 }}
                        className={`p-3 rounded-xl ${darkMode ? 'bg-white/5 hover:bg-white/10' : 'bg-black/5 hover:bg-black/10'} transition-all duration-300`}
                        style={{ 
                          borderColor: social.color,
                          borderWidth: '1px',
                          borderStyle: 'solid',
                          borderOpacity: 0.3
                        }}
                      >
                        <IconComponent size={24} style={{ color: social.color }} />
                      </motion.a>
                    )
                  })}
                </div>
              </div>

              {/* Quote */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
                transition={{ delay: 1.5, duration: 0.8 }}
                className={`p-6 rounded-xl ${
                  darkMode ? 'bg-gradient-to-r from-white/5 to-white/5 border border-white/10' : 'bg-gradient-to-r from-black/5 to-black/5 border border-black/10'
                }`}
              >
                <div className={`text-3xl ${darkMode ? 'text-white' : 'text-black'} mb-3`}>
                  "
                </div>
                <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} italic mb-3`}>
                  The best way to predict the future is to create it. Let's build something amazing together.
                </p>
                <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'} font-semibold`}>
                  - Jenish Barvaliya
                </div>
              </motion.div>
            </motion.div>

            {/* Contact Form */}
            <motion.div variants={itemVariants}>
              <div className={`p-6 sm:p-8 rounded-xl ${
                darkMode ? 'bg-white/5 border border-gray-700' : 'bg-black/5 border border-gray-200'
              } backdrop-blur-sm`}>
                <h3 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-black'} mb-6`}>
                  Send Message
                </h3>

                <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                    <div>
                      <label className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>
                        Name *
                      </label>
                      <motion.input
                        whileFocus={{ scale: 1.02 }}
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        required
                        className={`w-full px-4 py-3 rounded-lg border ${
                          darkMode 
                            ? 'bg-white/5 border-gray-600 text-white placeholder-gray-400 focus:border-blue-400' 
                            : 'bg-white border-gray-300 text-black placeholder-gray-500 focus:border-blue-500'
                        } focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300`}
                        placeholder="Your Name"
                      />
                    </div>
                    <div>
                      <label className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>
                        Email *
                      </label>
                      <motion.input
                        whileFocus={{ scale: 1.02 }}
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                        className={`w-full px-4 py-3 rounded-lg border ${
                          darkMode 
                            ? 'bg-white/5 border-gray-600 text-white placeholder-gray-400 focus:border-blue-400' 
                            : 'bg-white border-gray-300 text-black placeholder-gray-500 focus:border-blue-500'
                        } focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300`}
                        placeholder="your.email@example.com"
                      />
                    </div>
                  </div>

                  <div>
                    <label className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>
                      Subject *
                    </label>
                    <motion.input
                      whileFocus={{ scale: 1.02 }}
                      type="text"
                      name="subject"
                      value={formData.subject}
                      onChange={handleInputChange}
                      required
                      className={`w-full px-4 py-3 rounded-lg border ${
                        darkMode 
                          ? 'bg-white/5 border-gray-600 text-white placeholder-gray-400 focus:border-blue-400' 
                          : 'bg-white border-gray-300 text-black placeholder-gray-500 focus:border-blue-500'
                      } focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300`}
                      placeholder="What's this about?"
                    />
                  </div>

                  <div>
                    <label className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>
                      Message *
                    </label>
                    <motion.textarea
                      whileFocus={{ scale: 1.02 }}
                      name="message"
                      value={formData.message}
                      onChange={handleInputChange}
                      required
                      rows={6}
                      className={`w-full px-4 py-3 rounded-lg border ${
                        darkMode 
                          ? 'bg-white/5 border-gray-600 text-white placeholder-gray-400 focus:border-blue-400' 
                          : 'bg-white border-gray-300 text-black placeholder-gray-500 focus:border-blue-500'
                      } focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300 resize-none`}
                      placeholder="Tell me about your project, idea, or just say hello..."
                    />
                  </div>

                  <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    type="submit"
                    disabled={isSubmitting}
                    className={`w-full flex items-center justify-center px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 ${
                      isSubmitting
                        ? 'opacity-50 cursor-not-allowed'
                        : darkMode 
                          ? 'bg-white text-black hover:bg-gray-200' 
                          : 'bg-black text-white hover:bg-gray-800'
                    }`}
                  >
                    {isSubmitting ? (
                      <div className="flex items-center space-x-2">
                        <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
                        <span>Sending...</span>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2">
                        <Send size={20} />
                        <span>Send Message</span>
                      </div>
                    )}
                  </motion.button>
                </form>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>

    </section>
  )
}

export default Contact
