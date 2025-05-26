import csv
from faker import Faker
import random
from datetime import datetime

# Initialize Faker with Indonesian locale
fake = Faker('id_ID')  # Indonesian locale
fake_en = Faker('en_US')  # Keep English for some fields like company names

def generate_indonesian_job_application_data(num_records=50):
    """Generate comprehensive and realistic Indonesian job application data"""
    data = []
    
    # Indonesian job categories with local context
    job_categories = {
        "Teknologi": {
            "positions": ["Senior Software Engineer", "Full Stack Developer", "DevOps Engineer", 
                         "Data Scientist", "Machine Learning Engineer", "Cybersecurity Analyst",
                         "Cloud Solutions Architect", "Product Manager - Tech", "QA Engineer",
                         "Frontend Developer", "Backend Developer", "Mobile App Developer",
                         "IT Support Specialist", "Database Administrator", "System Administrator"],
            "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes",
                      "SQL", "MongoDB", "Git", "Agile", "Scrum", "REST APIs", "GraphQL", "Laravel", "PHP"]
        },
        "Bisnis": {
            "positions": ["Business Analyst", "Project Manager", "Operations Manager",
                         "Strategic Consultant", "Business Development Manager", "Process Improvement Specialist",
                         "Account Manager", "Sales Manager", "Customer Success Manager"],
            "skills": ["Project Management", "Data Analysis", "Strategic Planning", "Stakeholder Management",
                      "Process Optimization", "Budget Management", "Risk Assessment", "Excel", "PowerBI",
                      "CRM", "Salesforce", "Negotiation"]
        },
        "Pemasaran": {
            "positions": ["Digital Marketing Manager", "Content Marketing Specialist", "SEO Specialist",
                         "Social Media Manager", "Brand Manager", "Marketing Analytics Manager",
                         "E-commerce Manager", "Growth Hacker", "Influencer Marketing Specialist"],
            "skills": ["Google Analytics", "SEO/SEM", "Content Creation", "Social Media Marketing",
                      "Email Marketing", "Adobe Creative Suite", "Marketing Automation", "A/B Testing",
                      "Instagram Marketing", "TikTok Marketing", "Facebook Ads", "Google Ads"]
        },
        "Keuangan": {
            "positions": ["Financial Analyst", "Senior Accountant", "Investment Analyst",
                         "Risk Manager", "Treasury Analyst", "Internal Auditor", "Tax Specialist",
                         "Budget Analyst", "Credit Analyst"],
            "skills": ["Financial Modeling", "Excel", "SAP", "QuickBooks", "Risk Analysis",
                      "Financial Reporting", "Budgeting", "Forecasting", "Compliance", "PSAK",
                      "Tax Regulation", "Banking"]
        },
        "Kesehatan": {
            "positions": ["Perawat", "Asisten Medis", "Healthcare Administrator",
                         "Physical Therapist", "Medical Technologist", "Clinical Research Coordinator",
                         "Dokter Umum", "Apoteker", "Radiographer"],
            "skills": ["Patient Care", "Medical Records", "Privacy Compliance", "Electronic Health Records",
                      "Clinical Documentation", "Medical Terminology", "Patient Safety", "Emergency Care"]
        },
        "Pendidikan": {
            "positions": ["Guru SD", "Guru SMP", "Guru SMA", "Dosen", "Academic Coordinator",
                         "Education Consultant", "Curriculum Developer", "Training Specialist"],
            "skills": ["Teaching", "Curriculum Development", "Student Assessment", "Classroom Management",
                      "Educational Technology", "Learning Management Systems", "Academic Research"]
        }
    }
    
    # Indonesian universities and institutions
    indonesian_universities = [
        "Universitas Indonesia", "Institut Teknologi Bandung", "Universitas Gadjah Mada",
        "Institut Teknologi Sepuluh Nopember", "Universitas Airlangga", "Universitas Padjadjaran",
        "Universitas Diponegoro", "Universitas Brawijaya", "Universitas Sebelas Maret",
        "Universitas Udayana", "Institut Pertanian Bogor", "Universitas Andalas",
        "Universitas Hasanuddin", "Universitas Sriwijaya", "Universitas Lampung",
        "Universitas Negeri Jakarta", "Universitas Pendidikan Indonesia", "Universitas Negeri Surabaya",
        "Universitas Bina Nusantara", "Universitas Pelita Harapan", "Universitas Trisakti",
        "Universitas Atmajaya", "Universitas Tarumanagara", "Universitas Katolik Indonesia"
    ]
    
    # Indonesian companies by industry
    indonesian_companies = {
        "Teknologi": ["Gojek", "Tokopedia", "Bukalapak", "Traveloka", "OVO", "DANA", "Blibli",
                     "Shopee Indonesia", "Grab Indonesia", "Ruangguru", "Zenius", "Kitabisa",
                     "Akulaku", "Kredivo", "Amartha", "PT Telkom Indonesia", "XL Axiata"],
        "Bisnis": ["PT Unilever Indonesia", "PT Astra International", "PT Gudang Garam",
                  "PT Bank Central Asia", "PT Bank Mandiri", "PT Bank Rakyat Indonesia",
                  "PT Indofood Sukses Makmur", "PT Semen Indonesia", "PT Pertamina"],
        "Pemasaran": ["PT Dentsu Indonesia", "PT Ogilvy Indonesia", "PT BBDO Indonesia",
                     "PT Grey Indonesia", "PT DDB Indonesia", "PT Leo Burnett Indonesia"],
        "Keuangan": ["PT Bank Central Asia", "PT Bank Mandiri", "PT Bank Rakyat Indonesia",
                    "PT Bank Negara Indonesia", "PT Bank CIMB Niaga", "PT Bank Danamon",
                    "PT Asuransi Jiwasraya", "PT Prudential Indonesia"],
        "Kesehatan": ["RS Cipto Mangunkusumo", "RS Fatmawati", "RS Persahabatan",
                     "Siloam Hospitals", "RS Pondok Indah", "Mayapada Healthcare",
                     "PT Kalbe Farma", "PT Kimia Farma", "PT Bio Farma"],
        "Pendidikan": ["Universitas Indonesia", "Institut Teknologi Bandung", "Universitas Gadjah Mada",
                      "Ruangguru", "Zenius", "Skill Academy", "Hacktiv8", "Binar Academy"]
    }
    
    # Indonesian-specific majors and fields
    majors_by_category = {
        "Teknologi": ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer",
                     "Teknik Elektro", "Teknik Industri", "Matematika"],
        "Bisnis": ["Manajemen", "Akuntansi", "Ekonomi", "Bisnis Internasional",
                  "Administrasi Bisnis", "Kewirausahaan"],
        "Pemasaran": ["Ilmu Komunikasi", "Public Relations", "Advertising",
                     "Desain Komunikasi Visual", "Digital Marketing", "Jurnalistik"],
        "Keuangan": ["Akuntansi", "Keuangan", "Ekonomi", "Manajemen Keuangan",
                    "Perbankan", "Asuransi"],
        "Kesehatan": ["Kedokteran", "Keperawatan", "Farmasi", "Kesehatan Masyarakat",
                     "Gizi", "Fisioterapi", "Radiologi"],
        "Pendidikan": ["Pendidikan Guru Sekolah Dasar", "Pendidikan Bahasa Indonesia",
                      "Pendidikan Matematika", "Pendidikan Fisika", "Pendidikan Kimia"]
    }
    
    # Indonesian certifications
    indonesian_certifications = {
        "Teknologi": ["AWS Certified Solutions Architect", "Google Cloud Professional",
                     "Microsoft Azure Certified", "Oracle Certified", "Cisco Certified",
                     "Certified Ethical Hacker", "ITIL Foundation"],
        "Bisnis": ["Project Management Professional (PMP)", "Six Sigma Black Belt",
                  "Certified Business Analyst", "Certified Scrum Master"],
        "Pemasaran": ["Google Ads Certified", "Facebook Blueprint Certified",
                     "HubSpot Content Marketing", "Google Analytics Certified"],
        "Keuangan": ["Certified Public Accountant (CPA)", "Certified Internal Auditor (CIA)",
                    "Financial Risk Manager (FRM)", "Certified Management Accountant (CMA)"],
        "Kesehatan": ["STR (Surat Tanda Registrasi)", "SIP (Surat Ijin Praktik)",
                     "BLS Certification", "ACLS Certification"],
        "Pendidikan": ["Sertifikat Pendidik", "TOEFL/IELTS Certificate", "Microsoft Office Specialist"]
    }
    
    # Indonesian cities for realistic addresses
    indonesian_cities = [
        "Jakarta", "Surabaya", "Bandung", "Bekasi", "Medan", "Tangerang", "Depok",
        "Semarang", "Palembang", "Makassar", "Batam", "Bogor", "Pekanbaru", "Bandar Lampung",
        "Malang", "Padang", "Denpasar", "Yogyakarta", "Samarinda", "Banjarmasin"
    ]
    
    # Salary ranges in Indonesian Rupiah by experience
    salary_ranges_idr = {
        "Entry Level": (5000000, 8000000),      # 5-8 million IDR
        "1-3 tahun": (7000000, 12000000),      # 7-12 million IDR
        "3-5 tahun": (10000000, 18000000),     # 10-18 million IDR
        "5-8 tahun": (15000000, 25000000),     # 15-25 million IDR
        "8-12 tahun": (20000000, 35000000),    # 20-35 million IDR
        "12+ tahun": (30000000, 60000000)      # 30-60 million IDR
    }
    
    # Indonesian languages
    indonesian_languages = [
        "Bahasa Indonesia (Native)", "Bahasa Jawa", "Bahasa Sunda", "Bahasa Batak",
        "Bahasa Minang", "Bahasa Bali", "English", "Mandarin", "Arabic", "Japanese"
    ]
    
    for i in range(num_records):
        # Choose random category and related data
        category = random.choice(list(job_categories.keys()))
        position = random.choice(job_categories[category]["positions"])
        
        # Generate Indonesian names
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()
            
        last_name = fake.last_name()
        
        # Generate experience level and related salary
        experience_levels = ["Entry Level", "1-3 tahun", "3-5 tahun", "5-8 tahun", "8-12 tahun", "12+ tahun"]
        experience = random.choice(experience_levels)
        salary_min, salary_max = salary_ranges_idr[experience]
        desired_salary = random.randint(salary_min, salary_max)
        
        # Education level based on experience
        if experience in ["Entry Level", "1-3 tahun"]:
            education_level = random.choice(["S1 (Sarjana)", "D3 (Diploma)"])
        elif experience in ["3-5 tahun", "5-8 tahun"]:
            education_level = random.choice(["S1 (Sarjana)", "S2 (Magister)"])
        else:
            education_level = random.choice(["S2 (Magister)", "S3 (Doktor)", "S1 (Sarjana)"])
        
        # Generate work history with Indonesian companies
        category_companies = indonesian_companies.get(category, ["PT Generic Indonesia"])
        previous_companies = random.sample(category_companies, min(3, len(category_companies)))
        
        # Generate skills
        category_skills = job_categories[category]["skills"]
        general_skills = ["Kepemimpinan", "Komunikasi", "Problem Solving", "Kerja Tim",
                         "Manajemen Waktu", "Analytical Thinking", "Adaptability", "Bahasa Inggris"]
        all_skills = category_skills + general_skills
        selected_skills = random.sample(all_skills, random.randint(5, 8))
        
        # Generate certifications
        certifications = indonesian_certifications.get(category, [])
        num_certs = random.randint(0, min(3, len(certifications)))
        selected_certs = random.sample(certifications, num_certs) if certifications else []
        
        # Generate references with Indonesian names
        references = []
        for _ in range(random.randint(2, 4)):
            ref_name = f"{fake.first_name()} {fake.last_name()}"
            ref_title = fake.job()
            ref_company = random.choice(previous_companies) if previous_companies else fake.company()
            ref_phone = fake.phone_number()
            ref_email = fake.email()
            references.append(f"{ref_name}, {ref_title} di {ref_company}, {ref_phone}, {ref_email}")
        
        # Indonesian-specific preferences
        work_authorization = random.choice(["WNI (Warga Negara Indonesia)", "WNA dengan Work Permit", "Permanent Resident"])
        willing_to_relocate = random.choice(["Ya", "Tidak", "Dalam Pulau Jawa saja", "Dalam kota saja"])
        remote_work_preference = random.choice(["Fully Remote", "Hybrid", "Work from Office", "Fleksibel"])
        
        # Indonesian city for address
        city = random.choice(indonesian_cities)
        
        # Generate Indonesian ID number format (NIK) - make it more realistic
        province_codes = ["11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "31", "32", "33", "34", "35", "36"]
        selected_province_code = random.choice(province_codes)
        nik = f"{selected_province_code}{random.randint(10, 99)}{random.randint(10, 99)}{random.randint(100000, 999999)}"
        
        # Indonesian phone number format
        phone_prefixes = ["08", "081", "082", "085", "087", "088", "089"]
        phone_primary = f"+62 {random.choice(phone_prefixes)[1:]}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        
        # Languages with Indonesian context
        num_languages = random.randint(2, 4)
        selected_languages = random.sample(indonesian_languages, num_languages)
        languages_str = ", ".join(selected_languages)
        
        record = {
            # Application Info
            'application_id': f"APP{datetime.now().year}{str(i+1).zfill(4)}",
            'application_date': fake.date_between(start_date='-60d', end_date='today').strftime('%d/%m/%Y'),
            'application_status': random.choice(['Pending', 'Under Review', 'Interview Scheduled']),
            
            # Personal Information (Indonesian format)
            'first_name': first_name,
            'middle_name': fake.first_name() if random.choice([True, False]) else '',
            'last_name': last_name,
            'preferred_name': first_name if random.choice([True, False, False]) else '',
            'gender': gender,
            'date_of_birth': fake.date_of_birth(minimum_age=22, maximum_age=65).strftime('%d/%m/%Y'),
            'nik': nik,  # Indonesian ID number
            
            # e-KTP specific fields (new additions)
            'full_name': f"{first_name} {last_name}",
            'birth_place': fake.city(),
            'birth_date': fake.date_of_birth(minimum_age=22, maximum_age=65).strftime('%d-%m-%Y'),
            'blood_type': random.choice(['A', 'B', 'AB', 'O', '-']),
            'address': fake.street_address(),
            'rt_rw': f"{random.randint(1, 20):03d}/{random.randint(1, 15):03d}",
            'village_kelurahan': fake.city_suffix() + " " + fake.city(),
            'district_kecamatan': "Kecamatan " + fake.city(),
            'religion': random.choice(['Islam', 'Kristen', 'Katolik', 'Hindu', 'Buddha', 'Konghucu', 'Lainnya']),
            'marital_status': random.choice(['Belum Menikah', 'Menikah', 'Duda/Janda']),
            'occupation': fake.job(),
            'nationality': 'WNI',
            'valid_until': 'SEUMUR HIDUP',
            'province': fake.state(),
            'regency_city': city,
            
            # Contact Information (Indonesian format)
            'email': f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
            'phone_primary': phone_primary,
            'phone_secondary': f"+62 {random.choice(phone_prefixes)[1:]}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}" if random.choice([True, False, False]) else '',
            'address_street': fake.street_address(),
            'address_city': city,
            'address_province': fake.state(),
            'address_postal_code': fake.postcode(),
            'address_country': 'Indonesia',
            'linkedin_profile': f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(100, 999)}",
            'personal_website': f"https://{first_name.lower()}{last_name.lower()}.com" if random.choice([True, False, False, False]) else '',
            
            # Position Information
            'position_applied': position,
            'department': category,
            'employment_type': random.choice(['Full-time', 'Part-time', 'Contract', 'Magang']),
            'desired_salary': f"Rp {desired_salary:,}",
            'salary_negotiable': random.choice(['Ya', 'Tidak']),
            'start_date_available': fake.date_between(start_date='today', end_date='+90d').strftime('%d/%m/%Y'),
            'notice_period': random.choice(['Segera', '2 minggu', '1 bulan', '2 bulan']),
            
            # Work Authorization
            'work_authorization': work_authorization,
            'visa_status': 'Work Permit' if work_authorization == 'WNA dengan Work Permit' else 'N/A',
            'willing_to_relocate': willing_to_relocate,
            'remote_work_preference': remote_work_preference,
            'travel_willingness': f"{random.randint(0, 50)}%",
            
            # Education
            'education_level': education_level,
            'university_name': random.choice(indonesian_universities),
            'degree_major': random.choice(majors_by_category.get(category, ["Umum"])),
            'degree_minor': random.choice(majors_by_category.get(category, [""])) if random.choice([True, False, False]) else '',
            'graduation_year': random.randint(2010, 2024),
            'gpa': round(random.uniform(3.0, 4.0), 2) if random.choice([True, False]) else '',
            'academic_honors': random.choice(['Magna Cum Laude', 'Cum Laude', 'Dean\'s List', 'Wisudawan Terbaik', '']) if random.choice([True, False, False]) else '',
            
            # Professional Experience
            'total_experience': experience,
            'current_employer': random.choice(category_companies),
            'current_position': fake.job(),
            'current_salary': f"Rp {random.randint(int(desired_salary * 0.8), int(desired_salary * 1.1)):,}",
            'previous_employer_1': previous_companies[0] if len(previous_companies) > 0 else '',
            'previous_position_1': fake.job() if len(previous_companies) > 0 else '',
            'previous_employer_2': previous_companies[1] if len(previous_companies) > 1 else '',
            'previous_position_2': fake.job() if len(previous_companies) > 1 else '',
            'reason_for_leaving': random.choice(['Pengembangan Karir', 'Peluang Lebih Baik', 'Relokasi', 'Restrukturisasi Perusahaan', 'Mencari Tantangan Baru']),
            
            # Skills & Qualifications
            'technical_skills': ', '.join(selected_skills[:4]),
            'soft_skills': ', '.join(selected_skills[4:]),
            'programming_languages': ', '.join(random.sample(['Python', 'Java', 'JavaScript', 'PHP', 'SQL', 'R'], random.randint(2, 4))) if category == 'Teknologi' else '',
            'certifications': ', '.join(selected_certs) if selected_certs else 'Tidak ada',
            'languages_spoken': languages_str,
            
            # Additional Information
            'cover_letter_submitted': random.choice(['Ya', 'Tidak']),
            'portfolio_url': f"https://portfolio.{first_name.lower()}{last_name.lower()}.com" if category in ['Teknologi', 'Pemasaran'] and random.choice([True, False]) else '',
            'github_profile': f"https://github.com/{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}" if category == 'Teknologi' and random.choice([True, False]) else '',
            
            # Background Check
            'criminal_background': random.choice(['Tidak', 'Tidak', 'Tidak', 'Ya']),  # Weighted towards No
            'drug_test_consent': random.choice(['Ya', 'Tidak']),
            'reference_check_consent': 'Ya',
            
            # References
            'reference_1': references[0] if len(references) > 0 else '',
            'reference_2': references[1] if len(references) > 1 else '',
            'reference_3': references[2] if len(references) > 2 else '',
            'emergency_contact_name': f"{fake.first_name()} {fake.last_name()}",
            'emergency_contact_relationship': random.choice(['Suami/Istri', 'Orang Tua', 'Saudara', 'Teman']),
            'emergency_contact_phone': f"+62 {random.choice(phone_prefixes)[1:]}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            
            # Preferences
            'preferred_work_schedule': random.choice(['Standar (9-17)', 'Jam Fleksibel', 'Mulai Pagi', 'Mulai Siang']),
            'overtime_availability': random.choice(['Ya', 'Terbatas', 'Tidak']),
            'weekend_availability': random.choice(['Ya', 'Kadang-kadang', 'Tidak']),
            
            # How they found the job
            'how_found_position': random.choice(['Website Perusahaan', 'LinkedIn', 'JobStreet', 'Karir.com', 'Referensi', 'Job Fair', 'Recruiter']),
            'referral_source': f"{fake.first_name()} {fake.last_name()}" if random.choice([True, False, False]) else '',
            
            # Additional Questions (in Indonesian)
            'why_interested': f"Saya tertarik dengan posisi ini karena {fake.sentence()} dan ingin berkontribusi untuk kemajuan perusahaan.",
            'career_goals': f"Tujuan karir saya adalah {fake.sentence()} dan mengembangkan keahlian dalam {random.choice(selected_skills)}.",
            'greatest_strength': random.choice(['Problem Solving', 'Kepemimpinan', 'Komunikasi', 'Keahlian Teknis', 'Kerja Tim']),
            'biggest_weakness': random.choice(['Perfeksionis', 'Public Speaking', 'Delegasi', 'Manajemen Waktu']),
            
            # Indonesian specific fields
            'bpjs_number': f"BPJS-{random.randint(10000000, 99999999)}" if random.choice([True, False]) else '',
            'npwp_number': f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(1, 9)}-{random.randint(100, 999)}.{random.randint(100, 999)}" if random.choice([True, False]) else '',
            
            # Signature and Consent
            'electronic_signature': f"{first_name} {last_name}",
            'signature_date': datetime.now().strftime('%d/%m/%Y'),
            'terms_accepted': 'Ya',
            'privacy_policy_accepted': 'Ya'
        }
        
        data.append(record)
    
    return data

def save_to_csv(data, filename='indonesian_job_applications.csv'):
    """Save data to CSV file"""
    if not data:
        print("No data to save!")
        return
    
    fieldnames = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ Generated {len(data)} realistic Indonesian records and saved to {filename}")
    print(f"📊 Total columns: {len(fieldnames)}")

if __name__ == "__main__":
    # Generate Indonesian dummy data
    print("🇮🇩 Generating comprehensive Indonesian job application data...")
    print("📋 This includes Indonesian names, addresses, companies, and cultural context...")
    
    dummy_data = generate_indonesian_job_application_data(50)  # Generate 50 records
    
    # Save to CSV
    save_to_csv(dummy_data)
    
    # Display sample data structure
    print("\n📋 Indonesian data structure overview:")
    sample_record = dummy_data[0]
    categories = {
        'Info Aplikasi': ['application_id', 'application_date', 'application_status'],
        'Info Personal': ['first_name', 'last_name', 'gender', 'date_of_birth', 'nik'],
        'Info Kontak': ['email', 'phone_primary', 'address_city', 'address_province'],
        'Info Posisi': ['position_applied', 'employment_type', 'desired_salary'],
        'Pendidikan': ['education_level', 'university_name', 'degree_major', 'gpa'],
        'Pengalaman': ['total_experience', 'current_employer', 'current_position'],
        'Keahlian': ['technical_skills', 'soft_skills', 'certifications', 'languages_spoken'],
        'Referensi': ['reference_1', 'reference_2', 'reference_3']
    }
    
    for category, fields in categories.items():
        print(f"\n{category}:")
        for field in fields:
            if field in sample_record:
                print(f"  {field}: {sample_record[field]}")
    
    print("\n🎯 Sample Indonesian record preview:")
    print(f"Nama: {sample_record['first_name']} {sample_record['last_name']}")
    print(f"Posisi: {sample_record['position_applied']}")
    print(f"Pengalaman: {sample_record['total_experience']}")
    print(f"Pendidikan: {sample_record['education_level']} - {sample_record['degree_major']}")
    print(f"Universitas: {sample_record['university_name']}")
    print(f"Kota: {sample_record['address_city']}")
    print(f"Gaji yang diinginkan: {sample_record['desired_salary']}")
    print(f"Bahasa: {sample_record['languages_spoken']}")