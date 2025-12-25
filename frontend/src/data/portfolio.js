export const personalInfo = {
  name: "Jenish Barvaliya",
  title: "Information Technology Student",
  subtitle: "Seeking Internships in Machine Learning & Artificial Intelligence",
  location: "Surat, Gujarat, India",
  email: "jenishbarvaliya2012@gmail.com",
  phone: "+91 9510007247",
  linkedin: "https://linkedin.com/in/jenish-barvaliya-4b5312369",
  github: "https://github.com/jenish2917",
  resume: "/resume.pdf",
  profile_image: "/images/profile.jpg"
}

export const about = {
  summary: `Motivated Information Technology student in 8th semester with a strong passion for Machine Learning and Artificial Intelligence. 
Currently pursuing B.Tech in IT with 9.34/10.0 CGPA and seeking internship opportunities to apply theoretical knowledge in real-world ML/AI projects. 
Proficient in Python, TensorFlow, and data science libraries with hands-on experience in developing ML models through academic projects. 
Eager to contribute to innovative AI solutions while learning from industry professionals in a collaborative environment.`,
  
  vision: `To secure an internship in Machine Learning and Artificial Intelligence where I can apply my academic knowledge, 
contribute to meaningful projects, and gain practical industry experience that will help me grow into a skilled AI/ML professional.`,
  
  highlights: [
    "8th Semester B.Tech IT Student with 9.34/10.0 CGPA",
    "Strong foundation in Python, Machine Learning, and Data Science",
    "Academic projects in NLP, Recommendation Systems, and Predictive Analytics",
    "Seeking internships in Machine Learning and Artificial Intelligence",
    "Proficient in TensorFlow, Scikit-learn, and modern ML frameworks",
    "Passionate about AI-driven solutions and continuous learning"
  ]
}

export const experience = [
  {
    id: 1,
    title: "AI/ML Engineer Intern",
    company: "Elite Technocrats",
    duration: "May 2025 – June 2025",
    location: "Surat, Gujarat, India",
    type: "Internship",
    description: [
      "Developed and deployed AI-powered documentation automation tool using Django and React.js, reducing manual documentation time by 60%",
      "Architected robust data pipeline for preprocessing, validating, and transforming large-scale datasets, ensuring 99% data integrity for downstream NLP and machine learning workflows",
      "Integrated advanced machine learning, deep learning, and large language models (LLMs) to generate intelligent, context-aware technical content with 85% accuracy"
    ],
    technologies: ["Python", "Django", "React.js", "Machine Learning", "Deep Learning", "NLP", "LLMs", "Data Pipeline"],
    achievements: [
      "Reduced manual documentation time by 60%",
      "Achieved 99% data integrity in ML workflows",
      "Generated technical content with 85% accuracy using LLMs"
    ]
  }
]

export const projects = [
  {
    id: 1,
    title: "Fantasy Cricket Team Predictor | Machine Learning",
    description: "Engineered ML recommendation engine for Dream11 fantasy teams with 78% prediction accuracy using real-time player data",
    longDescription: "Engineered ML recommendation engine for Dream11 fantasy teams with 78% prediction accuracy using real-time player data. Implemented comprehensive data pipeline with web scraping using BeautifulSoup and Selenium. Deployed ensemble learning approach combining Random Forest, XGBoost, and logistic regression models for optimal team selection.",
    technologies: ["Python", "Machine Learning", "Random Forest", "XGBoost", "BeautifulSoup", "Selenium", "Data Analytics", "Web Scraping"],
    github: "https://github.com/jenish2917/dream11-team-predictor",
    demo: null,
    image: "/projects/cricket-predictor.jpg",
    featured: true,
    category: "Machine Learning"
  },
  {
    id: 2,
    title: "Spam Detection Classifier | Natural Language Processing",
    description: "Developed multi-class spam detection classifier achieving 94% accuracy and 92% F1-score using TF-IDF vectorization and supervised learning",
    longDescription: "Developed multi-class spam detection classifier achieving 94% accuracy and 92% F1-score using TF-IDF vectorization and supervised learning. Implemented comprehensive text preprocessing pipeline with regex-based cleaning, stopword removal. Compared performance of multiple algorithms including Naive Bayes, SVM, Random Forest, and Gradient Boosting for optimal model selection.",
    technologies: ["Python", "NLP", "TF-IDF", "Naive Bayes", "SVM", "Random Forest", "Gradient Boosting", "Scikit-learn", "Text Preprocessing"],
    github: "https://github.com/jenish2917/Email-sms-spam-detection",
    demo: null,
    image: "/projects/spam-detector.jpg",
    featured: true,
    category: "Natural Language Processing"
  },
  {
    id: 3,
    title: "Movie Recommendation System | Collaborative Filtering",
    description: "Built scalable recommendation system using collaborative filtering and content-based algorithms with 85% accuracy",
    longDescription: "Built scalable recommendation system using collaborative filtering and content-based algorithms. Implemented matrix factorization techniques (SVD, NMF) and cosine similarity algorithms for personalized movie suggestions. Developed hybrid recommendation approach combining user-based and item-based collaborative filtering with 85% accuracy.",
    technologies: ["Python", "Collaborative Filtering", "Content-Based Filtering", "SVD", "NMF", "Cosine Similarity", "Matrix Factorization", "Pandas", "NumPy"],
    github: "https://github.com/jenish2917/movie-recommendation-system",
    demo: null,
    image: "/projects/movie-recommender.jpg",
    featured: true,
    category: "Recommendation Systems"
  }
]

export const skills = {
  "Programming Languages": [
    { name: "Python", level: 90, icon: "Code" },
    { name: "Java", level: 80, icon: "Code" },
    { name: "C", level: 75, icon: "Code" },
    { name: "JavaScript", level: 85, icon: "Code" },
    { name: "SQL", level: 80, icon: "Database" }
  ],
  "Machine Learning & Data Science": [
    { name: "Scikit-learn", level: 90, icon: "Bot" },
    { name: "Pandas", level: 95, icon: "BarChart3" },
    { name: "NumPy", level: 90, icon: "Calculator" },
    { name: "Polars", level: 75, icon: "BarChart3" },
    { name: "Matplotlib", level: 85, icon: "LineChart" },
    { name: "Seaborn", level: 85, icon: "TrendingUp" },
    { name: "Natural Language Processing", level: 80, icon: "MessageSquare" }
  ],
  "Deep Learning Frameworks": [
    { name: "TensorFlow", level: 85, icon: "Brain" },
    { name: "Keras", level: 80, icon: "Brain" }
  ],
  "Web Technologies & Automation": [
    { name: "Django", level: 85, icon: "Globe" },
    { name: "React.js", level: 80, icon: "Globe" },
    { name: "Selenium", level: 75, icon: "Bot" },
    { name: "Playwright", level: 70, icon: "Bot" },
    { name: "REST APIs", level: 85, icon: "Zap" }
  ],
  "Development Tools & Platforms": [
    { name: "Git", level: 85, icon: "GitBranch" },
    { name: "GitHub", level: 85, icon: "Github" },
    { name: "Jupyter Notebooks", level: 90, icon: "FileText" }
  ]
}

export const certifications = [
  {
    id: 1,
    title: "Foundation Course on Green Skills and Artificial Intelligence",
    issuer: "Skills4Future Program - AICTE & Edunet Foundation",
    date: "March 2025",
    credentialId: "AICTE-AI-2025-JB",
    description: "Comprehensive foundation course covering Green Skills integration with Artificial Intelligence technologies",
    logo: "/certifications/aicte.png",
    link: "https://drive.google.com/file/d/1-Y9t-30E50JBxOdNqH-DiH6p8uGiFokG/view?usp=sharing"
  },
  {
    id: 2,
    title: "GenAI Powered Data Analytics Job Simulation",
    issuer: "Forage - Data Analytics & AI Collections Strategy",
    date: "June 2025",
    credentialId: "FORAGE-GENAI-2025-JB",
    description: "Practical job simulation focusing on Generative AI applications in data analytics and business strategy",
    logo: "/certifications/forage.png",
    link: "https://drive.google.com/file/d/1ugUh0pVpMiMgldPnV-DbVi7WWZvwQAip/view?usp=sharing"
  }
]

export const education = [
  {
    id: 1,
    degree: "Bachelor of Technology (B.Tech) in Information Technology",
    institution: "Sarvajanik College of Engineering and Technology",
    duration: "Expected Graduation: May 2026",
    gpa: "Cumulative GPA: 9.44/10.0",
    location: "Surat, Gujarat, India",
    description: "Specialized in Software Engineering, Data Structures, Algorithms, Database Systems, and Artificial Intelligence with focus on Machine Learning and Data Science",
    coursework: [
      "Data Structures and Algorithms",
      "Machine Learning",
      "Artificial Intelligence",
      "Database Management Systems",
      "Software Engineering",
      "Computer Networks",
      "Web Technologies",
      "Operating Systems",
      "Natural Language Processing",
      "Deep Learning"
    ]
  }
]

export const socialLinks = [
  {
    name: "GitHub",
    url: "https://github.com/jenish2917",
    icon: "Github",
    color: "#ffffff"
  },
  {
    name: "LinkedIn",
    url: "https://linkedin.com/in/jenish-barvaliya",
    icon: "Linkedin",
    color: "#0077b5"
  },
  {
    name: "Email",
    url: "mailto:jenishbarvaliya2012@gmail.com",
    icon: "Mail",
    color: "#ea4335"
  },
  {
    name: "Twitter",
    url: "https://twitter.com/jenish_barvaliya",
    icon: "Twitter",
    color: "#1da1f2"
  }
]
