import csv
from faker import Faker
import random
from datetime import datetime, timedelta
import re

# Initialize Faker
fake = Faker('en_US')

def generate_realistic_job_application_data(num_records=50):
    """Generate comprehensive and realistic job application data"""
    data = []
    
    # More comprehensive job data
    job_categories = {
        "Technology": {
            "positions": ["Senior Software Engineer", "Full Stack Developer", "DevOps Engineer", 
                         "Data Scientist", "Machine Learning Engineer", "Cybersecurity Analyst",
                         "Cloud Solutions Architect", "Product Manager - Tech", "QA Engineer",
                         "Frontend Developer", "Backend Developer", "Mobile App Developer"],
            "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes",
                      "SQL", "MongoDB", "Git", "Agile", "Scrum", "REST APIs", "GraphQL"]
        },
        "Business": {
            "positions": ["Business Analyst", "Project Manager", "Operations Manager",
                         "Strategic Consultant", "Business Development Manager", "Process Improvement Specialist"],
            "skills": ["Project Management", "Data Analysis", "Strategic Planning", "Stakeholder Management",
                      "Process Optimization", "Budget Management", "Risk Assessment", "Excel", "PowerBI"]
        },
        "Marketing": {
            "positions": ["Digital Marketing Manager", "Content Marketing Specialist", "SEO Specialist",
                         "Social Media Manager", "Brand Manager", "Marketing Analytics Manager"],
            "skills": ["Google Analytics", "SEO/SEM", "Content Creation", "Social Media Marketing",
                      "Email Marketing", "Adobe Creative Suite", "Marketing Automation", "A/B Testing"]
        },
        "Finance": {
            "positions": ["Financial Analyst", "Senior Accountant", "Investment Analyst",
                         "Risk Manager", "Treasury Analyst", "Internal Auditor"],
            "skills": ["Financial Modeling", "Excel", "SAP", "QuickBooks", "Risk Analysis",
                      "Financial Reporting", "Budgeting", "Forecasting", "Compliance"]
        },
        "Healthcare": {
            "positions": ["Registered Nurse", "Medical Assistant", "Healthcare Administrator",
                         "Physical Therapist", "Medical Technologist", "Clinical Research Coordinator"],
            "skills": ["Patient Care", "Medical Records", "HIPAA Compliance", "Electronic Health Records",
                      "Clinical Documentation", "Medical Terminology", "Patient Safety"]
        }
    }
    
    # Education details
    universities = [
        "Harvard University", "Stanford University", "MIT", "University of California, Berkeley",
        "Yale University", "Princeton University", "Columbia University", "University of Pennsylvania",
        "Cornell University", "Northwestern University", "Duke University", "University of Chicago",
        "Carnegie Mellon University", "Johns Hopkins University", "University of Michigan",
        "New York University", "Boston University", "Georgetown University", "Vanderbilt University",
        "Emory University", "University of Southern California", "University of Virginia"
    ]
    
    majors_by_category = {
        "Technology": ["Computer Science", "Software Engineering", "Information Technology",
                      "Data Science", "Cybersecurity", "Computer Engineering"],
        "Business": ["Business Administration", "Finance", "Economics", "Management",
                    "International Business", "Marketing"],
        "Marketing": ["Marketing", "Communications", "Public Relations", "Advertising",
                     "Digital Media", "Journalism"],
        "Finance": ["Finance", "Accounting", "Economics", "Business Administration",
                   "Financial Engineering", "Statistics"],
        "Healthcare": ["Nursing", "Biology", "Pre-Med", "Health Administration",
                      "Public Health", "Biomedical Engineering"]
    }
    
    # Professional certifications by field
    certifications_by_field = {
        "Technology": ["AWS Certified Solutions Architect", "Google Cloud Professional",
                      "Certified Kubernetes Administrator", "PMP", "Scrum Master", "CISSP"],
        "Business": ["PMP", "Six Sigma Black Belt", "Certified Business Analyst",
                    "Lean Six Sigma", "Agile Certified Practitioner"],
        "Marketing": ["Google Ads Certified", "HubSpot Content Marketing",
                     "Facebook Blueprint", "Google Analytics Certified"],
        "Finance": ["CPA", "CFA", "FRM", "Chartered Financial Analyst"],
        "Healthcare": ["BLS Certification", "ACLS", "Certified Medical Assistant",
                      "HIPAA Certification"]
    }
    
    # Company names by industry
    companies_by_industry = {
        "Technology": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber",
                      "Salesforce", "Adobe", "Oracle", "IBM", "Intel", "NVIDIA"],
        "Business": ["McKinsey & Company", "Boston Consulting Group", "Deloitte",
                    "PwC", "EY", "KPMG", "Accenture"],
        "Marketing": ["Ogilvy", "WPP", "Publicis", "Omnicom", "Havas", "Dentsu"],
        "Finance": ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "Bank of America",
                   "Wells Fargo", "Citigroup", "BlackRock"],
        "Healthcare": ["Kaiser Permanente", "Mayo Clinic", "Cleveland Clinic",
                      "Johns Hopkins Medicine", "Pfizer", "Johnson & Johnson"]
    }
    
    # Salary ranges by experience and field
    salary_ranges = {
        "Entry Level": (45000, 65000),
        "1-3 years": (55000, 85000),
        "3-5 years": (70000, 110000),
        "5-8 years": (90000, 140000),
        "8-12 years": (120000, 180000),
        "12+ years": (150000, 250000)
    }
    
    for i in range(num_records):
        # Choose random category and related data
        category = random.choice(list(job_categories.keys()))
        position = random.choice(job_categories[category]["positions"])
        
        # Generate basic personal information
        gender = random.choice(['Male', 'Female', 'Non-binary'])
        if gender == 'Male':
            first_name = fake.first_name_male()
        elif gender == 'Female':
            first_name = fake.first_name_female()
        else:
            first_name = fake.first_name()
            
        last_name = fake.last_name()
        
        # Generate experience level and related salary
        experience_levels = ["Entry Level", "1-3 years", "3-5 years", "5-8 years", "8-12 years", "12+ years"]
        experience = random.choice(experience_levels)
        salary_min, salary_max = salary_ranges[experience]
        desired_salary = random.randint(salary_min, salary_max)
        
        # Education level based on experience
        if experience in ["Entry Level", "1-3 years"]:
            education_level = random.choice(["Bachelor's Degree", "Associate's Degree"])
        elif experience in ["3-5 years", "5-8 years"]:
            education_level = random.choice(["Bachelor's Degree", "Master's Degree"])
        else:
            education_level = random.choice(["Master's Degree", "PhD", "Bachelor's Degree"])
        
        # Generate work history
        previous_companies = random.sample(companies_by_industry.get(category, ["Generic Corp"]), 
                                         min(3, len(companies_by_industry.get(category, ["Generic Corp"]))))
        
        # Generate skills
        category_skills = job_categories[category]["skills"]
        general_skills = ["Leadership", "Communication", "Problem Solving", "Team Collaboration",
                         "Time Management", "Analytical Thinking", "Adaptability"]
        all_skills = category_skills + general_skills
        selected_skills = random.sample(all_skills, random.randint(5, 8))
        
        # Generate certifications
        certifications = certifications_by_field.get(category, [])
        num_certs = random.randint(0, min(3, len(certifications)))
        selected_certs = random.sample(certifications, num_certs) if certifications else []
        
        # Generate references
        references = []
        for _ in range(random.randint(2, 4)):
            ref_name = f"{fake.first_name()} {fake.last_name()}"
            ref_title = fake.job()
            ref_company = random.choice(previous_companies) if previous_companies else fake.company()
            ref_phone = fake.phone_number()
            ref_email = fake.email()
            references.append(f"{ref_name}, {ref_title} at {ref_company}, {ref_phone}, {ref_email}")
        
        # Generate application preferences
        work_authorization = random.choice(["US Citizen", "Permanent Resident", "Work Visa Required", "Green Card"])
        willing_to_relocate = random.choice(["Yes", "No", "Within State Only"])
        remote_work_preference = random.choice(["Fully Remote", "Hybrid", "On-site", "Flexible"])
        
        record = {
            # Application Info
            'application_id': f"APP{datetime.now().year}{str(i+1).zfill(4)}",
            'application_date': fake.date_between(start_date='-60d', end_date='today').strftime('%m/%d/%Y'),
            'application_status': random.choice(['Pending', 'Under Review', 'Interview Scheduled']),
            
            # Personal Information
            'first_name': first_name,
            'middle_name': fake.first_name() if random.choice([True, False]) else '',
            'last_name': last_name,
            'preferred_name': first_name if random.choice([True, False, False]) else '',
            'gender': gender,
            'date_of_birth': fake.date_of_birth(minimum_age=22, maximum_age=65).strftime('%m/%d/%Y'),
            'social_security_number': f"XXX-XX-{random.randint(1000, 9999)}",
            
            # Contact Information
            'email': f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
            'phone_primary': fake.phone_number(),
            'phone_secondary': fake.phone_number() if random.choice([True, False, False]) else '',
            'address_street': fake.street_address(),
            'address_city': fake.city(),
            'address_state': fake.state(),
            'address_zip': fake.zipcode(),
            'address_country': 'United States',
            'linkedin_profile': f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(100, 999)}",
            'personal_website': f"https://{first_name.lower()}{last_name.lower()}.com" if random.choice([True, False, False, False]) else '',
            
            # Position Information
            'position_applied': position,
            'department': category,
            'employment_type': random.choice(['Full-time', 'Part-time', 'Contract', 'Internship']),
            'desired_salary': f"${desired_salary:,}",
            'salary_negotiable': random.choice(['Yes', 'No']),
            'start_date_available': fake.date_between(start_date='today', end_date='+90d').strftime('%m/%d/%Y'),
            'notice_period': random.choice(['Immediate', '2 weeks', '1 month', '2 months']),
            
            # Work Authorization
            'work_authorization': work_authorization,
            'visa_status': 'H1-B' if work_authorization == 'Work Visa Required' else 'N/A',
            'willing_to_relocate': willing_to_relocate,
            'remote_work_preference': remote_work_preference,
            'travel_willingness': f"{random.randint(0, 50)}%",
            
            # Education
            'education_level': education_level,
            'university_name': random.choice(universities),
            'degree_major': random.choice(majors_by_category.get(category, ["General Studies"])),
            'degree_minor': random.choice(majors_by_category.get(category, [""])) if random.choice([True, False, False]) else '',
            'graduation_year': random.randint(2010, 2024),
            'gpa': round(random.uniform(3.0, 4.0), 2) if random.choice([True, False]) else '',
            'academic_honors': random.choice(['Magna Cum Laude', 'Cum Laude', 'Dean\'s List', '']) if random.choice([True, False, False]) else '',
            
            # Professional Experience
            'total_experience': experience,
            'current_employer': random.choice(companies_by_industry.get(category, [fake.company()])),
            'current_position': fake.job(),
            'current_salary': f"${random.randint(int(desired_salary * 0.8), int(desired_salary * 1.1)):,}",
            'previous_employer_1': previous_companies[0] if len(previous_companies) > 0 else '',
            'previous_position_1': fake.job() if len(previous_companies) > 0 else '',
            'previous_employer_2': previous_companies[1] if len(previous_companies) > 1 else '',
            'previous_position_2': fake.job() if len(previous_companies) > 1 else '',
            'reason_for_leaving': random.choice(['Career Growth', 'Better Opportunities', 'Relocation', 'Company Restructuring', 'Seeking New Challenges']),
            
            # Skills & Qualifications
            'technical_skills': ', '.join(selected_skills[:4]),
            'soft_skills': ', '.join(selected_skills[4:]),
            'programming_languages': ', '.join(random.sample(['Python', 'Java', 'JavaScript', 'C++', 'SQL', 'R'], random.randint(2, 4))) if category == 'Technology' else '',
            'certifications': ', '.join(selected_certs) if selected_certs else 'None',
            'languages_spoken': f"English (Native), {fake.language_name()}" if random.choice([True, False]) else "English (Native)",
            
            # Additional Information
            'cover_letter_submitted': random.choice(['Yes', 'No']),
            'portfolio_url': f"https://portfolio.{first_name.lower()}{last_name.lower()}.com" if category in ['Technology', 'Marketing'] and random.choice([True, False]) else '',
            'github_profile': f"https://github.com/{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}" if category == 'Technology' and random.choice([True, False]) else '',
            
            # Background Check
            'criminal_background': random.choice(['No', 'No', 'No', 'Yes']),  # Weighted towards No
            'drug_test_consent': random.choice(['Yes', 'No']),
            'reference_check_consent': 'Yes',
            
            # References
            'reference_1': references[0] if len(references) > 0 else '',
            'reference_2': references[1] if len(references) > 1 else '',
            'reference_3': references[2] if len(references) > 2 else '',
            'emergency_contact_name': f"{fake.first_name()} {fake.last_name()}",
            'emergency_contact_relationship': random.choice(['Spouse', 'Parent', 'Sibling', 'Friend']),
            'emergency_contact_phone': fake.phone_number(),
            
            # Preferences
            'preferred_work_schedule': random.choice(['Standard (9-5)', 'Flexible Hours', 'Early Start', 'Late Start']),
            'overtime_availability': random.choice(['Yes', 'Limited', 'No']),
            'weekend_availability': random.choice(['Yes', 'Occasionally', 'No']),
            
            # How they found the job
            'how_found_position': random.choice(['Company Website', 'LinkedIn', 'Indeed', 'Glassdoor', 'Referral', 'Job Fair', 'Recruiter']),
            'referral_source': f"{fake.first_name()} {fake.last_name()}" if random.choice([True, False, False]) else '',
            
            # Additional Questions
            'why_interested': f"I am excited about the opportunity to {fake.sentence()} and contribute to {fake.company()}'s mission.",
            'career_goals': f"My goal is to {fake.sentence()} and develop expertise in {random.choice(selected_skills)}.",
            'greatest_strength': random.choice(['Problem Solving', 'Leadership', 'Communication', 'Technical Expertise', 'Team Collaboration']),
            'biggest_weakness': random.choice(['Perfectionism', 'Public Speaking', 'Delegation', 'Time Management']),
            
            # Signature and Consent
            'electronic_signature': f"{first_name} {last_name}",
            'signature_date': datetime.now().strftime('%m/%d/%Y'),
            'terms_accepted': 'Yes',
            'privacy_policy_accepted': 'Yes'
        }
        
        data.append(record)
    
    return data

def save_to_csv(data, filename='realistic_job_applications.csv'):
    """Save data to CSV file"""
    if not data:
        print("No data to save!")
        return
    
    fieldnames = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ Generated {len(data)} realistic records and saved to {filename}")
    print(f"📊 Total columns: {len(fieldnames)}")

if __name__ == "__main__":
    # Generate realistic dummy data
    print("🔄 Generating comprehensive and realistic job application data...")
    print("📋 This includes detailed personal info, work history, education, skills, and more...")
    
    dummy_data = generate_realistic_job_application_data(50)  # Generate 50 records
    
    # Save to CSV
    save_to_csv(dummy_data)
    
    # Display sample data structure
    print(f"\n📋 Data structure overview:")
    sample_record = dummy_data[0]
    categories = {
        'Application Info': ['application_id', 'application_date', 'application_status'],
        'Personal Info': ['first_name', 'last_name', 'gender', 'date_of_birth'],
        'Contact Info': ['email', 'phone_primary', 'address_street', 'linkedin_profile'],
        'Position Info': ['position_applied', 'employment_type', 'desired_salary'],
        'Education': ['education_level', 'university_name', 'degree_major', 'gpa'],
        'Experience': ['total_experience', 'current_employer', 'current_position'],
        'Skills': ['technical_skills', 'soft_skills', 'certifications'],
        'References': ['reference_1', 'reference_2', 'reference_3']
    }
    
    for category, fields in categories.items():
        print(f"\n{category}:")
        for field in fields:
            if field in sample_record:
                print(f"  {field}: {sample_record[field]}")
    
    print(f"\n🎯 Sample complete record preview:")
    print(f"Name: {sample_record['first_name']} {sample_record['last_name']}")
    print(f"Position: {sample_record['position_applied']}")
    print(f"Experience: {sample_record['total_experience']}")
    print(f"Education: {sample_record['education_level']} in {sample_record['degree_major']}")
    print(f"Skills: {sample_record['technical_skills']}")