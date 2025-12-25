# Generated migration to update portfolio data with latest information

from django.db import migrations
from datetime import date
import json

def update_portfolio_data(apps, schema_editor):
    # Get model classes
    PersonalInfo = apps.get_model('api', 'PersonalInfo')
    About = apps.get_model('api', 'About')
    Project = apps.get_model('api', 'Project')
    Experience = apps.get_model('api', 'Experience')
    Certification = apps.get_model('api', 'Certification')
    Education = apps.get_model('api', 'Education')
    SocialLink = apps.get_model('api', 'SocialLink')
    
    # Clear existing data
    PersonalInfo.objects.all().delete()
    About.objects.all().delete()
    Project.objects.all().delete()
    Experience.objects.all().delete()
    Certification.objects.all().delete()
    Education.objects.all().delete()
    
    # Update Personal Information
    personal_info = PersonalInfo.objects.create(
        name="Jenish Barvaliya",
        title="AI/ML Engineer",
        subtitle="Professional Machine Learning & AI Engineer",
        location="Surat, Gujarat, India",
        email="jenishbarvaliya2012@gmail.com",
        phone="+91 9510007247",
        linkedin="https://linkedin.com/in/jenish-barvaliya-4b5312369",
        github="https://github.com/jenish2917",
        resume="/resume.pdf",
        profile_image="/images/profile.jpg",
        is_active=True
    )
    
    # Update About Section
    about = About.objects.create(
        summary="Results-driven Information Technology student specializing in Machine Learning and Data Science with hands-on internship experience developing AI-driven solutions. Proficient in architecting and deploying end-to-end ML projects using Python, TensorFlow, and Scikit-learn. Demonstrated expertise in data pipeline development, model optimization, and predictive analytics. Seeking challenging international opportunities to apply strong foundation in data analysis and machine learning to solve complex business problems and deliver measurable impact in technology-driven organizations.",
        vision="To become a leading AI/ML engineer contributing to innovative solutions that bridge the gap between AI research and real-world applications, making technology accessible and beneficial for everyone.",
        highlights=[
            "AI/ML Engineer Intern with hands-on experience at Elite Technocrats",
            "Specialized in Machine Learning, Data Science, and AI-driven solutions",
            "Proficient in Python, TensorFlow, Scikit-learn, and modern ML frameworks",
            "Demonstrated expertise in data pipeline development and model optimization",
            "B.Tech IT student with 9.34/10.0 CGPA from SCET, Surat",
            "Proven track record in developing high-accuracy ML models (78-94% accuracy)"
        ],
        is_active=True
    )
    
    # Add Experience
    experience = Experience.objects.create(
        title="AI/ML Engineer Intern",
        company="Elite Technocrats",
        location="Surat, Gujarat, India",
        start_date=date(2025, 5, 1),
        end_date=date(2025, 6, 30),
        is_current=False,
        description=[
            "Developed and deployed AI-powered documentation automation tool using Django and React.js, reducing manual documentation time by 60%",
            "Architected robust data pipeline for preprocessing, validating, and transforming large-scale datasets, ensuring 99% data integrity for downstream NLP and machine learning workflows",
            "Integrated advanced machine learning, deep learning, and large language models (LLMs) to generate intelligent, context-aware technical content with 85% accuracy"
        ],
        technologies=["Python", "Django", "React.js", "Machine Learning", "Deep Learning", "NLP", "LLMs", "Data Pipeline"]
    )
    
    # Add Projects
    projects_data = [
        {
            "title": "Fantasy Cricket Team Predictor",
            "description": "Engineered ML recommendation engine for Dream11 fantasy teams with 78% prediction accuracy using real-time player data",
            "long_description": "Engineered ML recommendation engine for Dream11 fantasy teams with 78% prediction accuracy using real-time player data. Implemented comprehensive data pipeline with web scraping using BeautifulSoup and Selenium. Deployed ensemble learning approach combining Random Forest, XGBoost, and logistic regression models for optimal team selection.",
            "technologies": ["Python", "Machine Learning", "Random Forest", "XGBoost", "BeautifulSoup", "Selenium", "Data Analytics", "Web Scraping"],
            "github_url": "https://github.com/jenish2917/dream11-team-predictor",
            "is_featured": True
        },
        {
            "title": "Spam Detection Classifier",
            "description": "Developed multi-class spam detection classifier achieving 94% accuracy and 92% F1-score using TF-IDF vectorization and supervised learning",
            "long_description": "Developed multi-class spam detection classifier achieving 94% accuracy and 92% F1-score using TF-IDF vectorization and supervised learning. Implemented comprehensive text preprocessing pipeline with regex-based cleaning, stopword removal. Compared performance of multiple algorithms including Naive Bayes, SVM, Random Forest, and Gradient Boosting for optimal model selection.",
            "technologies": ["Python", "NLP", "TF-IDF", "Naive Bayes", "SVM", "Random Forest", "Gradient Boosting", "Scikit-learn", "Text Preprocessing"],
            "github_url": "https://github.com/jenish2917/Email-sms-spam-detection",
            "is_featured": True
        },
        {
            "title": "Movie Recommendation System",
            "description": "Built scalable recommendation system using collaborative filtering and content-based algorithms with 85% accuracy",
            "long_description": "Built scalable recommendation system using collaborative filtering and content-based algorithms. Implemented matrix factorization techniques (SVD, NMF) and cosine similarity algorithms for personalized movie suggestions. Developed hybrid recommendation approach combining user-based and item-based collaborative filtering with 85% accuracy.",
            "technologies": ["Python", "Collaborative Filtering", "Content-Based Filtering", "SVD", "NMF", "Cosine Similarity", "Matrix Factorization", "Pandas", "NumPy"],
            "github_url": "https://github.com/jenish2917/movie-recommendation-system",
            "is_featured": True
        }
    ]
    
    for project_data in projects_data:
        Project.objects.create(**project_data)
    
    # Add Certifications
    certifications_data = [
        {
            "title": "Foundation Course on Green Skills and Artificial Intelligence",
            "issuer": "Skills4Future Program - AICTE & Edunet Foundation",
            "date_issued": date(2025, 3, 1),
            "description": "Comprehensive foundation course covering Green Skills integration with Artificial Intelligence technologies",
            "verification_url": "https://drive.google.com/file/d/1-Y9t-30E50JBxOdNqH-DiH6p8uGiFokG/view?usp=sharing",
            "credential_id": "AICTE-AI-2025-JB"
        },
        {
            "title": "GenAI Powered Data Analytics Job Simulation",
            "issuer": "Forage - Data Analytics & AI Collections Strategy",
            "date_issued": date(2025, 6, 1),
            "description": "Practical job simulation focusing on Generative AI applications in data analytics and business strategy",
            "verification_url": "https://drive.google.com/file/d/1ugUh0pVpMiMgldPnV-DbVi7WWZvwQAip/view?usp=sharing",
            "credential_id": "FORAGE-GENAI-2025-JB"
        }
    ]
    
    for cert_data in certifications_data:
        Certification.objects.create(**cert_data)
    
    # Add Education
    Education.objects.create(
        degree="Bachelor of Technology (B.Tech) in Information Technology",
        institution="Sarvajanik College of Engineering and Technology",
        location="Surat, Gujarat, India",
        start_date=date(2022, 7, 1),
        end_date=date(2026, 5, 31),
        is_current=True,
        gpa="9.34/10.0",
        description="Specialized in Software Engineering, Data Structures, Algorithms, Database Systems, and Artificial Intelligence with focus on Machine Learning and Data Science",
        coursework=[
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
    )

def reverse_update_portfolio_data(apps, schema_editor):
    # This is a one-way migration - no reverse needed
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_personalinfo_profile_image'),
    ]

    operations = [
        migrations.RunPython(update_portfolio_data, reverse_update_portfolio_data),
    ]
