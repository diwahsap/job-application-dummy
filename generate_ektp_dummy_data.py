import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import json

# Initialize Indonesian Faker
fake = Faker('id_ID')

class EKTPGenerator:
    def __init__(self):
        self.fake = Faker('id_ID')
        
        # Indonesian provinces with their codes
        self.provinces = {
            "11": "ACEH", "12": "SUMATERA UTARA", "13": "SUMATERA BARAT", 
            "14": "RIAU", "15": "JAMBI", "16": "SUMATERA SELATAN", 
            "17": "BENGKULU", "18": "LAMPUNG", "19": "KEPULAUAN BANGKA BELITUNG",
            "21": "KEPULAUAN RIAU", "31": "DKI JAKARTA", "32": "JAWA BARAT",
            "33": "JAWA TENGAH", "34": "DI YOGYAKARTA", "35": "JAWA TIMUR",
            "36": "BANTEN", "51": "BALI", "52": "NUSA TENGGARA BARAT",
            "53": "NUSA TENGGARA TIMUR", "61": "KALIMANTAN BARAT",
            "62": "KALIMANTAN TENGAH", "63": "KALIMANTAN SELATAN",
            "64": "KALIMANTAN TIMUR", "65": "KALIMANTAN UTARA",
            "71": "SULAWESI UTARA", "72": "SULAWESI TENGAH",
            "73": "SULAWESI SELATAN", "74": "SULAWESI TENGGARA",
            "75": "GORONTALO", "76": "SULAWESI BARAT", "81": "MALUKU",
            "82": "MALUKU UTARA", "91": "PAPUA BARAT", "94": "PAPUA"
        }
        
        # Blood types
        self.blood_types = ["A", "B", "AB", "O", "-"]
        
        # Religions
        self.religions = ["ISLAM", "KRISTEN", "KATOLIK", "HINDU", "BUDDHA", "KHONGHUCU"]
        
        # Marital status
        self.marital_status = ["BELUM KAWIN", "KAWIN", "CERAI HIDUP", "CERAI MATI"]
        
        # Jobs
        self.jobs = [
            "KARYAWAN SWASTA", "PNS", "WIRASWASTA", "PETANI", "NELAYAN",
            "GURU", "DOSEN", "DOKTER", "PENGACARA", "INSINYUR", "MAHASISWA",
            "PELAJAR", "MENGURUS RUMAH TANGGA", "PENSIUNAN", "BELUM/TIDAK BEKERJA"
        ]

    def generate_nik(self, birth_date, gender, province_code):
        """Generate Indonesian NIK (16 digits)"""
        # Format: PPKKSSDDMMYYXXXX
        # PP = Province code (2 digits)
        # KK = Regency/City code (2 digits) 
        # SS = Sub-district code (2 digits)
        # DD = Birth date (2 digits, +40 for female)
        # MM = Birth month (2 digits)
        # YY = Birth year last 2 digits (2 digits)
        # XXXX = Sequence number (4 digits)
        
        regency_code = f"{random.randint(1, 99):02d}"
        subdistrict_code = f"{random.randint(1, 99):02d}"
        
        day = birth_date.day
        if gender == "PEREMPUAN":
            day += 40
            
        month = birth_date.month
        year = birth_date.year % 100
        sequence = f"{random.randint(1, 9999):04d}"
        
        nik = f"{province_code}{regency_code}{subdistrict_code}{day:02d}{month:02d}{year:02d}{sequence}"
        return nik

    def introduce_name_variation(self, original_name):
        """Introduce intentional variations in names"""
        variations = [
            # Letter substitutions
            lambda name: name.replace('i', 'y'),
            lambda name: name.replace('y', 'i'), 
            lambda name: name.replace('dh', 'd'),
            lambda name: name.replace('d', 'dh'),
            lambda name: name.replace('f', 'ph'),
            lambda name: name.replace('ph', 'f'),
            lambda name: name.replace('c', 'ch'),
            lambda name: name.replace('k', 'ck'),
            # Case variations
            lambda name: name.upper(),
            lambda name: name.lower(),
            lambda name: name.title(),
            # Extra spaces
            lambda name: name.replace(' ', '  '),
            # Missing middle name
            lambda name: ' '.join(name.split()[:2]) if len(name.split()) > 2 else name,
            # Adding/removing suffix
            lambda name: name + " S.Pd" if not any(suffix in name for suffix in ['.', 'S.', 'M.']) else name.replace(' S.Pd', '').replace(' M.', ' ').replace(' Dr.', ' '),
        ]
        
        return random.choice(variations)(original_name)

    def introduce_nik_variation(self, original_nik):
        """Introduce intentional variations in NIK"""
        nik_list = list(original_nik)
        variation_type = random.choice([
            'digit_change', 'digit_swap', 'extra_digit', 'missing_digit'
        ])
        
        if variation_type == 'digit_change':
            # Change one random digit
            pos = random.randint(0, 15)
            nik_list[pos] = str(random.randint(0, 9))
        elif variation_type == 'digit_swap':
            # Swap two adjacent digits
            pos = random.randint(0, 14)
            nik_list[pos], nik_list[pos + 1] = nik_list[pos + 1], nik_list[pos]
        elif variation_type == 'extra_digit':
            # Add extra digit
            pos = random.randint(0, 16)
            nik_list.insert(pos, str(random.randint(0, 9)))
        elif variation_type == 'missing_digit':
            # Remove one digit
            if len(nik_list) > 1:
                pos = random.randint(0, len(nik_list) - 1)
                nik_list.pop(pos)
        
        return ''.join(nik_list)

    def introduce_phone_variation(self, original_phone):
        """Introduce intentional variations in phone numbers"""
        phone_digits = ''.join(filter(str.isdigit, original_phone))
        variation_type = random.choice([
            'digit_change', 'extra_digit', 'missing_digit', 'format_change'
        ])
        
        if variation_type == 'digit_change':
            # Change one digit
            pos = random.randint(0, len(phone_digits) - 1)
            digits_list = list(phone_digits)
            digits_list[pos] = str(random.randint(0, 9))
            return ''.join(digits_list)
        elif variation_type == 'extra_digit':
            # Add extra digit
            pos = random.randint(0, len(phone_digits))
            return phone_digits[:pos] + str(random.randint(0, 9)) + phone_digits[pos:]
        elif variation_type == 'missing_digit':
            # Remove one digit
            if len(phone_digits) > 1:
                pos = random.randint(0, len(phone_digits) - 1)
                return phone_digits[:pos] + phone_digits[pos + 1:]
        elif variation_type == 'format_change':
            # Change format (+62 vs 08 vs 62)
            if phone_digits.startswith('62'):
                return '08' + phone_digits[2:]
            elif phone_digits.startswith('08'):
                return '+62' + phone_digits[1:]
        
        return original_phone

    def generate_ektp_data(self, job_application_data, mismatch_percentage=30):
        """Generate e-KTP data with intentional mismatches"""
        ektp_data = []
        
        for i, job_data in enumerate(job_application_data):
            # Determine if this record should have mismatches
            has_mismatch = random.random() < (mismatch_percentage / 100)
            
            # Basic data from job application
            province_code = random.choice(list(self.provinces.keys()))
            birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=65)
            gender = random.choice(["LAKI-LAKI", "PEREMPUAN"])
            
            # Generate base KTP data
            nik = self.generate_nik(birth_date, gender, province_code)
            full_name = job_data.get('full_name', self.fake.name())
            
            # Introduce mismatches with annotations
            annotations = []
            
            if has_mismatch:
                mismatch_types = []
                
                # Name mismatch (40% chance if mismatch enabled)
                if random.random() < 0.4:
                    original_name = full_name
                    full_name = self.introduce_name_variation(original_name)
                    mismatch_types.append(f"NAME_MISMATCH: '{original_name}' -> '{full_name}'")
                
                # NIK mismatch (30% chance if mismatch enabled)
                if random.random() < 0.3:
                    original_nik = nik
                    nik = self.introduce_nik_variation(original_nik)
                    mismatch_types.append(f"NIK_MISMATCH: '{original_nik}' -> '{nik}'")
                
                # Phone mismatch (25% chance if mismatch enabled)
                phone_number = job_data.get('phone_number', self.fake.phone_number())
                if random.random() < 0.25:
                    original_phone = phone_number
                    phone_number = self.introduce_phone_variation(original_phone)
                    mismatch_types.append(f"PHONE_MISMATCH: '{original_phone}' -> '{phone_number}'")
                else:
                    phone_number = job_data.get('phone_number', self.fake.phone_number())
                
                # Birth date mismatch (20% chance if mismatch enabled)
                if random.random() < 0.2:
                    original_date = birth_date
                    # Change birth date by 1-5 days/months/years
                    variation = random.choice(['day', 'month', 'year'])
                    if variation == 'day':
                        birth_date = birth_date + timedelta(days=random.randint(-5, 5))
                    elif variation == 'month':
                        month_diff = random.randint(-2, 2)
                        if month_diff != 0:
                            try:
                                birth_date = birth_date.replace(month=max(1, min(12, birth_date.month + month_diff)))
                            except ValueError:
                                birth_date = birth_date.replace(day=28, month=max(1, min(12, birth_date.month + month_diff)))
                    elif variation == 'year':
                        birth_date = birth_date.replace(year=birth_date.year + random.randint(-2, 2))
                    
                    mismatch_types.append(f"BIRTH_DATE_MISMATCH: '{original_date.strftime('%d-%m-%Y')}' -> '{birth_date.strftime('%d-%m-%Y')}'")
                
                annotations = mismatch_types
            else:
                # Use consistent data
                phone_number = job_data.get('phone_number', self.fake.phone_number())
                annotations = ["VALID_DATA"]
            
            # Generate address components
            rt_rw = f"{random.randint(1, 20):03d}/{random.randint(1, 15):03d}"
            village = self.fake.city()
            district = self.fake.city() 
            regency = random.choice([
                "JAKARTA PUSAT", "JAKARTA UTARA", "JAKARTA SELATAN", "JAKARTA TIMUR", "JAKARTA BARAT",
                "SURABAYA", "BANDUNG", "MEDAN", "SEMARANG", "MAKASSAR", "PALEMBANG", "TANGERANG",
                "DEPOK", "BEKASI", "BOGOR"
            ])
            province = self.provinces[province_code]
            
            ektp_record = {
                'record_id': i + 1,
                'nik': nik,
                'full_name': full_name,
                'birth_place': self.fake.city(),
                'birth_date': birth_date.strftime('%d-%m-%Y'),
                'gender': gender,
                'blood_type': random.choice(self.blood_types),
                'address': self.fake.street_address(),
                'rt_rw': rt_rw,
                'village_kelurahan': village,
                'district_kecamatan': district,
                'regency_city': regency,
                'province': province,
                'religion': random.choice(self.religions),
                'marital_status': random.choice(self.marital_status),
                'occupation': random.choice(self.jobs),
                'nationality': "WNI",
                'valid_until': "SEUMUR HIDUP",
                'issue_date': self.fake.date_between(start_date='-10y', end_date='today').strftime('%d-%m-%Y'),
                'issue_place': regency,
                'phone_number': phone_number,
                'data_quality': "MISMATCH" if has_mismatch else "VALID",
                'mismatch_annotations': '; '.join(annotations) if annotations else "NONE",
                'created_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'created_by': 'diwahsap'
            }
            
            ektp_data.append(ektp_record)
        
        return ektp_data

def load_job_application_data(filename='indonesian_job_applications.csv'):
    """Load job application data from CSV"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"⚠️  Warning: {filename} not found. Generating e-KTP data without job application reference.")
        return []

def save_ektp_to_csv(data, filename='indonesian_ektp_data.csv'):
    """Save e-KTP data to CSV file"""
    if not data:
        print("❌ No data to save!")
        return
    
    fieldnames = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ e-KTP data saved to {filename}")
    print(f"📊 Generated {len(data)} e-KTP records")
    
    # Show statistics
    valid_count = len([d for d in data if d['data_quality'] == 'VALID'])
    mismatch_count = len([d for d in data if d['data_quality'] == 'MISMATCH'])
    
    print(f"📈 Statistics:")
    print(f"   ✅ Valid records: {valid_count}")
    print(f"   ⚠️  Mismatch records: {mismatch_count}")
    print(f"   📊 Mismatch rate: {(mismatch_count/len(data)*100):.1f}%")

def generate_validation_report(ektp_data, filename='validation_report.json'):
    """Generate a detailed validation report"""
    report = {
        'generated_timestamp': datetime.now().isoformat(),
        'total_records': len(ektp_data),
        'valid_records': len([d for d in ektp_data if d['data_quality'] == 'VALID']),
        'mismatch_records': len([d for d in ektp_data if d['data_quality'] == 'MISMATCH']),
        'mismatch_types': {},
        'detailed_mismatches': []
    }
    
    # Analyze mismatch types
    for record in ektp_data:
        if record['data_quality'] == 'MISMATCH':
            annotations = record['mismatch_annotations']
            for annotation in annotations.split('; '):
                if annotation.startswith(('NAME_MISMATCH', 'NIK_MISMATCH', 'PHONE_MISMATCH', 'BIRTH_DATE_MISMATCH')):
                    mismatch_type = annotation.split(':')[0]
                    report['mismatch_types'][mismatch_type] = report['mismatch_types'].get(mismatch_type, 0) + 1
                    
                    report['detailed_mismatches'].append({
                        'record_id': record['record_id'],
                        'nik': record['nik'],
                        'name': record['full_name'],
                        'mismatch_type': mismatch_type,
                        'details': annotation
                    })
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
    
    print(f"📋 Validation report saved to {filename}")

if __name__ == "__main__":
    print("🇮🇩 Indonesian e-KTP Generator with Validation Testing")
    print("=" * 60)
    print(f"👤 Created by: diwahsap")
    print(f"📅 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load job application data
    job_data = load_job_application_data()
    
    if not job_data:
        # Generate sample job data if none exists
        print("🔄 Generating sample job application data for e-KTP reference...")
        fake = Faker('id_ID')
        job_data = [
            {
                'full_name': fake.name(),
                'phone_number': fake.phone_number(),
                'email': fake.email()
            }
            for _ in range(50)
        ]
    
    # Initialize e-KTP generator
    generator = EKTPGenerator()
    
    # Generate e-KTP data with 30% mismatch rate
    print(f"🏗️  Generating e-KTP data for {len(job_data)} records...")
    print("⚠️  30% of records will have intentional mismatches for validation testing")
    print()
    
    ektp_data = generator.generate_ektp_data(job_data, mismatch_percentage=30)
    
    # Save to CSV
    save_ektp_to_csv(ektp_data)
    
    # Generate validation report
    generate_validation_report(ektp_data)
    
    print()
    print("🎯 e-KTP Generation Complete!")
    print("📁 Files created:")
    print("   📄 indonesian_ektp_data.csv - e-KTP data with mismatches")
    print("   📋 validation_report.json - Detailed mismatch analysis")
    print()
    print("💡 Use this data to test your validation system!")
    print("   ✅ Valid records should pass validation")
    print("   ⚠️  Mismatch records should be flagged by your system")