from django.db import migrations
from datetime import date


def populate_portfolio_content(apps, schema_editor):
    # Get model classes
    Project = apps.get_model('api', 'Project')
    Skill = apps.get_model('api', 'Skill')
    Experience = apps.get_model('api', 'Experience')
    Education = apps.get_model('api', 'Education')
    Certification = apps.get_model('api', 'Certification')
    
    # Projects data
    projects_data = [
        {
            'title': 'Fantasy Cricket Team Predictor',
            'description': 'Engineered ML recommendation engine for Dream11 fantasy teams with 78% prediction accuracy using real-time player data',
            'long_description': 'Built a comprehensive fantasy cricket prediction system that analyzes player statistics, pitch conditions, weather data, and historical performance to recommend the best team combinations. Implemented comprehensive data pipeline with web scraping using BeautifulSoup and Selenium. Deployed ensemble learning approach combining Random Forest, XGBoost, and logistic regression models for optimal team selection.',
            'technologies': ['Python', 'Machine Learning', 'Random Forest', 'XGBoost', 'BeautifulSoup', 'Selenium', 'Data Analytics'],
            'github_url': 'https://github.com/jenish2917/dream11-team-predictor',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Spam Detection Classifier',
            'description': 'Developed multi-class spam detection classifier achieving 94% accuracy and 92% F1-score using TF-IDF vectorization and supervised learning',
            'long_description': 'Built an advanced Natural Language Processing system for email and SMS spam detection. Implemented comprehensive text preprocessing pipeline with regex-based cleaning and stopword removal. Compared performance of multiple algorithms including Naive Bayes, SVM, Random Forest, and Gradient Boosting for optimal model selection.',
            'technologies': ['Python', 'NLP', 'TF-IDF', 'Naive Bayes', 'SVM', 'Random Forest', 'Gradient Boosting', 'Scikit-learn'],
            'github_url': 'https://github.com/jenish2917/Email-sms-spam-detection',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Movie Recommendation System',
            'description': 'Built scalable recommendation system using collaborative filtering and content-based algorithms with 85% accuracy',
            'long_description': 'Developed a hybrid movie recommendation system using collaborative filtering and content-based algorithms. Implemented matrix factorization techniques (SVD, NMF) and cosine similarity algorithms for personalized movie suggestions. Created a Streamlit web application for easy user interaction and real-time recommendations.',
            'technologies': ['Python', 'Collaborative Filtering', 'Content-Based Filtering', 'SVD', 'NMF', 'Streamlit', 'Pandas', 'NumPy'],
            'github_url': 'https://github.com/jenish2917/movie-recommendation-system',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Smart Grievance System',
            'description': 'A comprehensive grievance management system for efficient complaint handling and resolution tracking',
            'long_description': 'Developed a smart grievance management platform that streamlines the complaint registration and resolution process. The system includes automated categorization, priority assignment, and real-time tracking capabilities.',
            'technologies': ['Python', 'Django', 'Database Management', 'Web Development'],
            'github_url': 'https://github.com/jenish2917/smartgriev',
            'is_featured': False,
            'status': 'completed'
        },
        {
            'title': 'Daily News Reels',
            'description': 'An automated news aggregation and summarization platform for daily news consumption',
            'long_description': 'Built a news aggregation platform that automatically collects, processes, and summarizes daily news from multiple sources. Implemented NLP techniques for content summarization and categorization.',
            'technologies': ['Python', 'NLP', 'Web Scraping', 'Text Summarization', 'News API'],
            'github_url': 'https://github.com/jenish2917/daily-news-reels',
            'is_featured': False,
            'status': 'completed'
        }
    ]
    
    # Create projects
    for project_data in projects_data:
        Project.objects.get_or_create(
            title=project_data['title'],
            defaults=project_data
        )
    
    # Experience data
    Experience.objects.get_or_create(
        title='AI/ML Engineer Intern',
        company='Elite Technocrats',
        defaults={
            'location': 'Surat, Gujarat, India',
            'start_date': date(2025, 5, 1),
            'end_date': date(2025, 6, 30),
            'is_current': False,
            'description': [
                'Developed and deployed AI-powered documentation automation tool using Django and React.js, reducing manual documentation time by 60%',
                'Architected robust data pipeline for preprocessing, validating, and transforming large-scale datasets, ensuring 99% data integrity for downstream NLP and machine learning workflows',
                'Integrated advanced machine learning, deep learning, and large language models (LLMs) to generate intelligent, context-aware technical content with 85% accuracy',
                'Collaborated with cross-functional teams to deliver production-ready AI solutions'
            ],
            'technologies': ['Python', 'Django', 'React.js', 'TensorFlow', 'NLP', 'LLMs', 'Data Pipelines', 'Machine Learning']
        }
    )
    
    # Education data
    Education.objects.get_or_create(
        degree='Bachelor of Technology (B.Tech) in Information Technology',
        institution='Sarvajanik College of Engineering and Technology',
        defaults={
            'location': 'Surat, Gujarat, India',
            'start_date': date(2022, 7, 1),
            'end_date': date(2026, 5, 31),
            'is_current': True,
            'gpa': '9.34/10.0',
            'description': 'Specialized in Software Engineering, Data Structures, Algorithms, Database Systems, and Artificial Intelligence with focus on Machine Learning and Data Science',
            'coursework': [
                'Data Structures and Algorithms',
                'Machine Learning',
                'Artificial Intelligence',
                'Database Management Systems',
                'Software Engineering',
                'Computer Networks',
                'Web Technologies',
                'Operating Systems',
                'Natural Language Processing',
                'Deep Learning'
            ]
        }
    )
    
    # Certifications data
    certifications_data = [
        {
            'title': 'Foundation Course on Green Skills and Artificial Intelligence',
            'issuer': 'Skills4Future Program - AICTE & Edunet Foundation',
            'date_issued': date(2025, 3, 1),
            'credential_id': 'AICTE-AI-2025-JB',
            'description': 'Comprehensive foundation course covering Green Skills integration with Artificial Intelligence technologies'
        },
        {
            'title': 'GenAI Powered Data Analytics Job Simulation',
            'issuer': 'Forage - Data Analytics & AI Collections Strategy',
            'date_issued': date(2025, 6, 1),
            'credential_id': 'FORAGE-GENAI-2025-JB',
            'description': 'Practical job simulation focusing on Generative AI applications in data analytics and business strategy'
        }
    ]
    
    for cert_data in certifications_data:
        Certification.objects.get_or_create(
            title=cert_data['title'],
            defaults=cert_data
        )


def reverse_populate_portfolio_content(apps, schema_editor):
    # Get model classes
    Project = apps.get_model('api', 'Project')
    Skill = apps.get_model('api', 'Skill')
    Experience = apps.get_model('api', 'Experience')
    Education = apps.get_model('api', 'Education')
    Certification = apps.get_model('api', 'Certification')
    
    # Delete the data
    Project.objects.all().delete()
    Experience.objects.all().delete()
    Education.objects.all().delete()
    Certification.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0004_populate_portfolio_data'),
    ]

    operations = [
        migrations.RunPython(populate_portfolio_content, reverse_populate_portfolio_content),
    ]
