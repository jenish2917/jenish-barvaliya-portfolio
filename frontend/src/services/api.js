const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://jenish-barvaliya-portfolio.onrender.com/api';

class ApiService {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Personal Information
  static async getPersonalInfo() {
    return this.request('/personal-info/');
  }

  // About Information
  static async getAbout() {
    return this.request('/about/');
  }

  // Social Links
  static async getSocialLinks() {
    return this.request('/social-links/');
  }

  // Projects
  static async getProjects() {
    return this.request('/projects/');
  }

  static async getFeaturedProjects() {
    return this.request('/projects/?featured=true');
  }

  // Skills
  static async getSkills() {
    return this.request('/skills/');
  }

  // Experience
  static async getExperience() {
    return this.request('/experience/');
  }

  // Education
  static async getEducation() {
    return this.request('/education/');
  }

  // Certifications
  static async getCertifications() {
    return this.request('/certifications/');
  }

  // Contact
  static async submitContact(contactData) {
    return this.request('/contact/', {
      method: 'POST',
      body: JSON.stringify(contactData),
    });
  }

  // Portfolio Summary
  static async getPortfolioSummary() {
    return this.request('/portfolio-summary/');
  }
}

export default ApiService;
