import os
import csv
import json
import shutil
from datetime import datetime

# CONFIGURATION
CSV_FILE = "./indonesian_job_applications.csv"  # Input CSV with e-KTP data
STATIC_PHOTO = "src/assets/images.jpg"         # Path to static photo
OUTPUT_DIR = "indonesian_ktp/"                 # Where to save generated images
CREATE_SCRIPT = "src/create.py"            # The image generator script

TEMPLATE_JSON = "./data.json"            # The temp data file for create.py

def make_data_json(row, photo_path, out_path):
    data = {
        "application_id": row["application_id"],
        "nik": row["nik"],
        "nama": row["first_name"] + " " + row["middle_name"] + " " + row["last_name"],
        "ttl": f"{row['birth_place']}, {row['date_of_birth']}",
        "jenis_kelamin": row["gender"],
        "golongan_darah": row["blood_type"],
        "alamat": row["address_street"],
        "rt/rw": row["rt_rw"],
        "kel/desa": row["address_city"],
        "kecamatan": row["address_city"],
        "agama": row["religion"],
        "status": row["marital_status"],
        "pekerjaan": row["current_position"],
        "kewarganegaraan": "Indonesia",
        "masa_berlaku": datetime.now().strftime('%d-%m-%Y'),
        "provinsi": row["address_province"],
        "kota": row["address_city"],
        "terbuat": datetime.now().strftime('%d-%m-%Y'),
        "pas_photo": photo_path
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            make_data_json(row, STATIC_PHOTO, TEMPLATE_JSON)
            # Run the image generator
            os.system(f"python3 {CREATE_SCRIPT}")
            # Move result to unique file
            dest_img = os.path.join(OUTPUT_DIR, f"ktp_{row['application_id']}.png")
            shutil.copy("src/result.png", dest_img)
            print(f"✅ Generated {dest_img}")
    print(f"\nAll KTP images generated in ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()