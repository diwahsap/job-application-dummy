import csv
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

class IndonesianApplicationFormCanvas(canvas.Canvas):
    """Custom canvas for Indonesian job application forms with headers and footers"""
    
    def __init__(self, *args, **kwargs):
        self.applicant_name = kwargs.pop('applicant_name', '')
        self.app_id = kwargs.pop('app_id', '')
        canvas.Canvas.__init__(self, *args, **kwargs)
    
    def showPage(self):
        self._draw_header()
        self._draw_footer()
        canvas.Canvas.showPage(self)
    
    def _draw_header(self):
        self.saveState()
        self.setFont("Helvetica-Bold", 11)
        self.setFillColor(colors.darkred)
        self.drawString(50, A4[1] - 30, f"FORMULIR LAMARAN KERJA - {self.applicant_name}")
        self.drawRightString(A4[0] - 50, A4[1] - 30, f"ID Aplikasi: {self.app_id}")
        
        # Draw Indonesian flag colors line under header
        self.setStrokeColor(colors.red)
        self.setLineWidth(2)
        self.line(50, A4[1] - 35, A4[0]/2 - 10, A4[1] - 35)
        self.setStrokeColor(colors.white)
        self.setLineWidth(1)
        self.line(A4[0]/2 - 10, A4[1] - 35, A4[0]/2 + 10, A4[1] - 35)
        self.setStrokeColor(colors.red)
        self.setLineWidth(2)
        self.line(A4[0]/2 + 10, A4[1] - 35, A4[0] - 50, A4[1] - 35)
        self.restoreState()
    
    def _draw_footer(self):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.grey)
        footer_text = f"Dibuat pada {datetime.now().strftime('%d %B %Y')} | Halaman {self._pageNumber} | diwahsap@2025"
        self.drawCentredText(A4[0]/2, 30, footer_text)
        
        # Draw line above footer
        self.setStrokeColor(colors.lightgrey)
        self.setLineWidth(0.5)
        self.line(50, 40, A4[0] - 50, 40)
        self.restoreState()

def create_indonesian_pdf(applicant_data, output_folder='indonesian_pdf_forms'):
    """Create a comprehensive Indonesian PDF job application form"""
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Generate filename
    safe_name = "".join(c for c in f"{applicant_data['last_name']}_{applicant_data['first_name']}" if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{applicant_data['application_id']}_{safe_name}.pdf"
    filepath = os.path.join(output_folder, filename)
    
    # Create custom canvas with A4 size (more common in Indonesia)
    doc = SimpleDocTemplate(
        filepath, 
        pagesize=A4, 
        topMargin=0.8*inch, 
        bottomMargin=0.8*inch,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch
    )
    
    # Override the canvas class
    doc.canvasmaker = lambda *args, **kwargs: IndonesianApplicationFormCanvas(
        *args, 
        applicant_name=f"{applicant_data['first_name']} {applicant_data['last_name']}",
        app_id=applicant_data['application_id'],
        **kwargs
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom Indonesian styles
    title_style = ParagraphStyle(
        'IndonesianTitle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=15,
        alignment=TA_CENTER,
        textColor=colors.darkred,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'IndonesianSection',
        parent=styles['Heading2'],
        fontSize=13,
        spaceAfter=6,
        spaceBefore=12,
        textColor=colors.darkred,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.darkred,
        borderPadding=4,
        backColor=colors.lightcoral
    )
    
    subsection_style = ParagraphStyle(
        'IndonesianSubsection',
        parent=styles['Heading3'],
        fontSize=11,
        spaceAfter=4,
        spaceBefore=8,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    # Build content
    content = []
    
    # Title with Indonesian flag motif
    content.append(Paragraph("FORMULIR LAMARAN KERJA", title_style))
    content.append(Paragraph("(JOB APPLICATION FORM)", styles['Normal']))
    content.append(Spacer(1, 0.15*inch))
    
    # Company info and application details
    app_info_data = [
        ['ID Aplikasi:', applicant_data['application_id'], 'Tanggal Submit:', applicant_data['application_date']],
        ['Status:', applicant_data.get('application_status', 'Pending'), 'Posisi:', applicant_data['position_applied']],
        ['Departemen:', applicant_data.get('department', 'N/A'), 'Tipe Kerja:', applicant_data.get('employment_type', 'Full-time')]
    ]
    
    app_table = Table(app_info_data, colWidths=[1.4*inch, 2*inch, 1.4*inch, 2*inch])
    app_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightcoral),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightcoral),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(app_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Personal Information Section
    content.append(Paragraph("1. DATA PRIBADI (PERSONAL INFORMATION)", section_style))
    
    personal_data = [
        ['Nama Lengkap:', f"{applicant_data['first_name']} {applicant_data.get('middle_name', '')} {applicant_data['last_name']}".replace('  ', ' '),
         'Nama Panggilan:', applicant_data.get('preferred_name', 'Sama dengan nama lengkap')],
        ['Tanggal Lahir:', applicant_data['date_of_birth'], 'Jenis Kelamin:', applicant_data.get('gender', 'Tidak disebutkan')],
        ['NIK:', applicant_data.get('nik', 'XXXXXXXXXXXX'), 'Status Kewarganegaraan:', applicant_data.get('work_authorization', 'WNI')],
        ['Agama:', applicant_data.get('religion', 'N/A'), 'Status Pernikahan:', applicant_data.get('marital_status', 'Belum Menikah')]
    ]
    
    personal_table = Table(personal_data, colWidths=[1.5*inch, 2.4*inch, 1.4*inch, 1.5*inch])
    personal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(personal_table)
    content.append(Spacer(1, 0.15*inch))
    
    # Contact Information
    content.append(Paragraph("Informasi Kontak (Contact Information)", subsection_style))
    
    contact_data = [
        ['Email Utama:', applicant_data['email'], 'Telepon Utama:', applicant_data['phone_primary']],
        ['Telepon Kedua:', applicant_data.get('phone_secondary', 'Tidak ada'), 'LinkedIn:', applicant_data.get('linkedin_profile', 'Tidak ada')],
        ['Alamat Lengkap:', f"{applicant_data['address_street']}, {applicant_data['address_city']}, {applicant_data['address_province']} {applicant_data['address_postal_code']}", '', ''],
        ['Website/Portfolio:', applicant_data.get('personal_website', 'Tidak ada'), 'GitHub:', applicant_data.get('github_profile', 'Tidak ada')]
    ]
    
    contact_table = Table(contact_data, colWidths=[1.5*inch, 2.4*inch, 1.4*inch, 1.5*inch])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 2), (3, 2)),  # Span address across columns
    ]))
    content.append(contact_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Position Information
    content.append(Paragraph("2. INFORMASI POSISI (POSITION DETAILS)", section_style))
    
    position_data = [
        ['Gaji yang Diinginkan:', applicant_data['desired_salary'], 'Dapat Dinegosiasi:', applicant_data.get('salary_negotiable', 'Ya')],
        ['Tanggal Mulai Kerja:', applicant_data.get('start_date_available', 'Segera'), 'Notice Period:', applicant_data.get('notice_period', '2 minggu')],
        ['Preferensi Remote:', applicant_data.get('remote_work_preference', 'Fleksibel'), 'Kesediaan Travel:', applicant_data.get('travel_willingness', '0%')],
        ['Bersedia Relokasi:', applicant_data.get('willing_to_relocate', 'Tidak'), 'Kesediaan Lembur:', applicant_data.get('overtime_availability', 'Ya')]
    ]
    
    position_table = Table(position_data, colWidths=[1.7*inch, 2.2*inch, 1.5*inch, 1.4*inch])
    position_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(position_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Education Section
    content.append(Paragraph("3. RIWAYAT PENDIDIKAN (EDUCATION BACKGROUND)", section_style))
    
    education_data = [
        ['Jenjang Pendidikan:', applicant_data['education_level'], 'Tahun Lulus:', str(applicant_data['graduation_year'])],
        ['Universitas/Institusi:', applicant_data['university_name'], 'IPK/GPA:', applicant_data.get('gpa', 'Tidak disebutkan')],
        ['Jurusan Utama:', applicant_data['degree_major'], 'Jurusan Sampingan:', applicant_data.get('degree_minor', 'Tidak ada')],
        ['Penghargaan Akademik:', applicant_data.get('academic_honors', 'Tidak ada'), 'Bahasa yang Dikuasai:', applicant_data.get('languages_spoken', 'Bahasa Indonesia')]
    ]
    
    education_table = Table(education_data, colWidths=[1.7*inch, 2.2*inch, 1.5*inch, 1.4*inch])
    education_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(education_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Professional Experience
    content.append(Paragraph("4. PENGALAMAN KERJA (PROFESSIONAL EXPERIENCE)", section_style))
    
    experience_data = [
        ['Total Pengalaman:', applicant_data['total_experience'], 'Gaji Saat Ini:', applicant_data.get('current_salary', 'Tidak disebutkan')],
        ['Perusahaan Saat Ini:', applicant_data['current_employer'], 'Posisi Saat Ini:', applicant_data['current_position']],
        ['Perusahaan Sebelumnya 1:', applicant_data.get('previous_employer_1', 'Tidak ada'), 'Posisi:', applicant_data.get('previous_position_1', 'Tidak ada')],
        ['Perusahaan Sebelumnya 2:', applicant_data.get('previous_employer_2', 'Tidak ada'), 'Posisi:', applicant_data.get('previous_position_2', 'Tidak ada')],
        ['Alasan Keluar:', applicant_data.get('reason_for_leaving', 'Pengembangan Karir'), '', '']
    ]
    
    experience_table = Table(experience_data, colWidths=[1.7*inch, 2.2*inch, 1.5*inch, 1.4*inch])
    experience_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 4), (3, 4)),  # Span reason for leaving
    ]))
    content.append(experience_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Skills and Certifications
    content.append(Paragraph("5. KEAHLIAN & KUALIFIKASI (SKILLS & QUALIFICATIONS)", section_style))
    
    skills_data = [
        ['Keahlian Teknis:', applicant_data.get('technical_skills', 'Tidak disebutkan')],
        ['Soft Skills:', applicant_data.get('soft_skills', 'Tidak disebutkan')],
        ['Bahasa Pemrograman:', applicant_data.get('programming_languages', 'Tidak ada')],
        ['Sertifikasi:', applicant_data.get('certifications', 'Tidak ada')],
        ['Kelebihan Utama:', applicant_data.get('greatest_strength', 'Tidak disebutkan')],
        ['Area Pengembangan:', applicant_data.get('biggest_weakness', 'Tidak disebutkan')]
    ]
    
    skills_table = Table(skills_data, colWidths=[2*inch, 4.8*inch])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    content.append(skills_table)
    content.append(Spacer(1, 0.2*inch))
    
    # References
    content.append(Paragraph("6. REFERENSI PROFESIONAL (PROFESSIONAL REFERENCES)", section_style))
    
    ref_data = []
    for i in range(1, 4):
        ref_key = f'reference_{i}'
        if applicant_data.get(ref_key):
            ref_info = applicant_data[ref_key].split(', ')
            if len(ref_info) >= 4:
                ref_data.append([f'Referensi {i}:', ref_info[0], 'Jabatan:', ref_info[1].replace(' di ', ' - ')])
                ref_data.append(['Perusahaan:', ref_info[2], 'Kontak:', f"{ref_info[3]} / {ref_info[4] if len(ref_info) > 4 else 'N/A'}"])
            else:
                ref_data.append([f'Referensi {i}:', applicant_data[ref_key], '', ''])
        else:
            ref_data.append([f'Referensi {i}:', 'Tersedia bila diminta', '', ''])
    
    if ref_data:
        ref_table = Table(ref_data, colWidths=[1.4*inch, 2.4*inch, 1.2*inch, 1.8*inch])
        ref_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(ref_table)
    content.append(Spacer(1, 0.15*inch))
    
    # Emergency Contact
    emergency_data = [
        ['Kontak Darurat:', applicant_data.get('emergency_contact_name', 'Tidak disebutkan'), 
         'Hubungan:', applicant_data.get('emergency_contact_relationship', 'Tidak disebutkan')],
        ['Telepon Darurat:', applicant_data.get('emergency_contact_phone', 'Tidak disebutkan'), '', '']
    ]
    
    emergency_table = Table(emergency_data, colWidths=[1.7*inch, 2.2*inch, 1.5*inch, 1.4*inch])
    emergency_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightyellow),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 1), (3, 1)),
    ]))
    content.append(emergency_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Additional Information
    content.append(Paragraph("7. INFORMASI TAMBAHAN (ADDITIONAL INFORMATION)", section_style))
    
    additional_data = [
        ['Bagaimana mengetahui lowongan ini?', applicant_data.get('how_found_position', 'Tidak disebutkan')],
        ['Sumber Referensi:', applicant_data.get('referral_source', 'Tidak ada')],
        ['Cover Letter Dilampirkan:', applicant_data.get('cover_letter_submitted', 'Tidak')],
        ['Nomor BPJS:', applicant_data.get('bpjs_number', 'Tidak disebutkan')],
        ['Nomor NPWP:', applicant_data.get('npwp_number', 'Tidak disebutkan')],
        ['Persetujuan Background Check:', applicant_data.get('reference_check_consent', 'Ya')],
        ['Persetujuan Drug Test:', applicant_data.get('drug_test_consent', 'Ya')]
    ]
    
    additional_table = Table(additional_data, colWidths=[2.2*inch, 4.6*inch])
    additional_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(additional_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Signature section
    content.append(Paragraph("8. PERNYATAAN DAN TANDA TANGAN (DECLARATION & SIGNATURE)", section_style))
    
    declaration_text = """Saya menyatakan bahwa informasi yang saya berikan dalam formulir aplikasi ini adalah benar dan lengkap. 
    Saya memahami bahwa informasi yang salah dapat menyebabkan penolakan atau pemutusan hubungan kerja jika saya diterima. 
    Saya mengizinkan perusahaan untuk menghubungi referensi dan memverifikasi informasi yang saya berikan."""
    
    content.append(Paragraph(declaration_text, styles['Normal']))
    content.append(Spacer(1, 0.15*inch))
    
    signature_data = [
        ['Tanda Tangan Elektronik:', applicant_data.get('electronic_signature', ''), 'Tanggal:', applicant_data.get('signature_date', '')],
        ['Nama Lengkap:', f"{applicant_data['first_name']} {applicant_data['last_name']}", 'Syarat & Ketentuan:', applicant_data.get('terms_accepted', 'Ya')]
    ]
    
    signature_table = Table(signature_data, colWidths=[1.8*inch, 2.5*inch, 1.2*inch, 1.3*inch])
    signature_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(signature_table)
    
    # Footer note
    content.append(Spacer(1, 0.15*inch))
    footer_note = "Terima kasih telah melamar di perusahaan kami. Kami akan menghubungi Anda dalam waktu 2-3 minggu."
    content.append(Paragraph(footer_note, styles['Normal']))
    
    # Build PDF
    doc.build(content)
    return filepath

def process_csv_and_generate_indonesian_pdfs(csv_filename='indonesian_job_applications.csv'):
    """Read CSV data and generate Indonesian PDF forms for each applicant"""
    
    if not os.path.exists(csv_filename):
        print(f"❌ Error: {csv_filename} not found! Please run generate_indonesian_dummy_data.py first.")
        return
    
    generated_files = []
    
    try:
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            print("🇮🇩 Generating Indonesian PDF job application forms...")
            print("📋 Each form includes Indonesian formatting, language, and cultural context...")
            
            for i, row in enumerate(reader, 1):
                try:
                    pdf_path = create_indonesian_pdf(row)
                    generated_files.append(pdf_path)
                    print(f"✅ Generated: {os.path.basename(pdf_path)}")
                    
                    # Progress indicator
                    if i % 10 == 0:
                        print(f"📊 Progress: {i} forms completed...")
                        
                except Exception as e:
                    print(f"❌ Error generating PDF for {row.get('first_name', 'Unknown')} {row.get('last_name', '')}: {e}")
            
        print(f"\n🎉 Successfully generated {len(generated_files)} Indonesian PDF job application forms!")
        print(f"📁 Files saved in 'indonesian_pdf_forms' folder")
        print(f"📄 Each PDF contains Indonesian formatting with cultural context")
        print(f"🇮🇩 Features: Indonesian names, addresses, companies, and terminology")
        
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")

if __name__ == "__main__":
    process_csv_and_generate_indonesian_pdfs()