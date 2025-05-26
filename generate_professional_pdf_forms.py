import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import os
from datetime import datetime

class ApplicationFormCanvas(canvas.Canvas):
    """Custom canvas for adding headers and footers"""
    
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
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.darkblue)
        self.drawString(50, letter[1] - 30, f"Job Application Form - {self.applicant_name}")
        self.drawRightString(letter[0] - 50, letter[1] - 30, f"App ID: {self.app_id}")
        
        # Draw line under header
        self.setStrokeColor(colors.darkblue)
        self.setLineWidth(1)
        self.line(50, letter[1] - 35, letter[0] - 50, letter[1] - 35)
        self.restoreState()
    
    def _draw_footer(self):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.grey)
        footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y')} | Page {self._pageNumber}"
        self.drawCentredText(letter[0]/2, 30, footer_text)
        
        # Draw line above footer
        self.setStrokeColor(colors.lightgrey)
        self.setLineWidth(0.5)
        self.line(50, 40, letter[0] - 50, 40)
        self.restoreState()

def create_comprehensive_pdf(applicant_data, output_folder='professional_pdf_forms'):
    """Create a comprehensive PDF job application form"""
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Generate filename
    safe_name = "".join(c for c in f"{applicant_data['last_name']}_{applicant_data['first_name']}" if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{applicant_data['application_id']}_{safe_name}.pdf"
    filepath = os.path.join(output_folder, filename)
    
    # Create custom canvas
    doc = SimpleDocTemplate(
        filepath, 
        pagesize=letter, 
        topMargin=0.7*inch, 
        bottomMargin=0.7*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    
    # Override the canvas class
    doc.canvasmaker = lambda *args, **kwargs: ApplicationFormCanvas(
        *args, 
        applicant_name=f"{applicant_data['first_name']} {applicant_data['last_name']}",
        app_id=applicant_data['application_id'],
        **kwargs
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=15,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        spaceAfter=6,
        spaceBefore=10,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.darkblue,
        borderPadding=3,
        backColor=colors.lightblue
    )
    
    subsection_style = ParagraphStyle(
        'SubsectionHeader',
        parent=styles['Heading3'],
        fontSize=11,
        spaceAfter=4,
        spaceBefore=8,
        textColor=colors.darkred,
        fontName='Helvetica-Bold'
    )
    
    # Build content
    content = []
    
    # Title
    content.append(Paragraph("COMPREHENSIVE JOB APPLICATION FORM", title_style))
    content.append(Spacer(1, 0.1*inch))
    
    # Company logo placeholder and application info
    app_info_data = [
        ['Application ID:', applicant_data['application_id'], 'Date Submitted:', applicant_data['application_date']],
        ['Status:', applicant_data.get('application_status', 'Pending'), 'Position:', applicant_data['position_applied']],
        ['Department:', applicant_data.get('department', 'N/A'), 'Employment Type:', applicant_data.get('employment_type', 'Full-time')]
    ]
    
    app_table = Table(app_info_data, colWidths=[1.2*inch, 1.8*inch, 1.2*inch, 1.8*inch])
    app_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(app_table)
    content.append(Spacer(1, 0.15*inch))
    
    # Personal Information Section
    content.append(Paragraph("1. PERSONAL INFORMATION", section_style))
    
    personal_data = [
        ['Full Legal Name:', f"{applicant_data['first_name']} {applicant_data.get('middle_name', '')} {applicant_data['last_name']}".replace('  ', ' '),
         'Preferred Name:', applicant_data.get('preferred_name', 'Same as legal')],
        ['Date of Birth:', applicant_data['date_of_birth'], 'Gender:', applicant_data.get('gender', 'Prefer not to say')],
        ['SSN (Last 4):', applicant_data.get('social_security_number', 'XXXX'), 'Work Authorization:', applicant_data.get('work_authorization', 'US Citizen')]
    ]
    
    personal_table = Table(personal_data, colWidths=[1.3*inch, 2.2*inch, 1.2*inch, 1.3*inch])
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
    content.append(Spacer(1, 0.1*inch))
    
    # Contact Information
    content.append(Paragraph("Contact Information", subsection_style))
    
    contact_data = [
        ['Primary Email:', applicant_data['email'], 'Primary Phone:', applicant_data['phone_primary']],
        ['Secondary Phone:', applicant_data.get('phone_secondary', 'N/A'), 'LinkedIn:', applicant_data.get('linkedin_profile', 'N/A')],
        ['Address:', f"{applicant_data['address_street']}, {applicant_data['address_city']}, {applicant_data['address_state']} {applicant_data['address_zip']}", '', ''],
        ['Portfolio/Website:', applicant_data.get('personal_website', 'N/A'), 'GitHub:', applicant_data.get('github_profile', 'N/A')]
    ]
    
    contact_table = Table(contact_data, colWidths=[1.3*inch, 2.2*inch, 1.2*inch, 1.3*inch])
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
    content.append(Spacer(1, 0.15*inch))
    
    # Position Information
    content.append(Paragraph("2. POSITION DETAILS", section_style))
    
    position_data = [
        ['Desired Salary:', applicant_data['desired_salary'], 'Negotiable:', applicant_data.get('salary_negotiable', 'Yes')],
        ['Start Date Available:', applicant_data.get('start_date_available', 'Immediate'), 'Notice Period:', applicant_data.get('notice_period', '2 weeks')],
        ['Remote Work Preference:', applicant_data.get('remote_work_preference', 'Flexible'), 'Travel Willingness:', applicant_data.get('travel_willingness', '0%')],
        ['Willing to Relocate:', applicant_data.get('willing_to_relocate', 'No'), 'Overtime Available:', applicant_data.get('overtime_availability', 'Yes')]
    ]
    
    position_table = Table(position_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch])
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
    content.append(Spacer(1, 0.15*inch))
    
    # Education Section
    content.append(Paragraph("3. EDUCATION BACKGROUND", section_style))
    
    education_data = [
        ['Highest Degree:', applicant_data['education_level'], 'Graduation Year:', str(applicant_data['graduation_year'])],
        ['University/Institution:', applicant_data['university_name'], 'GPA:', applicant_data.get('gpa', 'N/A')],
        ['Major/Field of Study:', applicant_data['degree_major'], 'Minor:', applicant_data.get('degree_minor', 'N/A')],
        ['Academic Honors:', applicant_data.get('academic_honors', 'N/A'), 'Languages:', applicant_data.get('languages_spoken', 'English')]
    ]
    
    education_table = Table(education_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch])
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
    content.append(Spacer(1, 0.15*inch))
    
    # Professional Experience
    content.append(Paragraph("4. PROFESSIONAL EXPERIENCE", section_style))
    
    experience_data = [
        ['Total Experience:', applicant_data['total_experience'], 'Current Salary:', applicant_data.get('current_salary', 'N/A')],
        ['Current Employer:', applicant_data['current_employer'], 'Current Position:', applicant_data['current_position']],
        ['Previous Employer 1:', applicant_data.get('previous_employer_1', 'N/A'), 'Position:', applicant_data.get('previous_position_1', 'N/A')],
        ['Previous Employer 2:', applicant_data.get('previous_employer_2', 'N/A'), 'Position:', applicant_data.get('previous_position_2', 'N/A')],
        ['Reason for Leaving:', applicant_data.get('reason_for_leaving', 'Career Growth'), '', '']
    ]
    
    experience_table = Table(experience_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch])
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
    content.append(Spacer(1, 0.15*inch))
    
    # Skills and Certifications
    content.append(Paragraph("5. SKILLS & QUALIFICATIONS", section_style))
    
    skills_data = [
        ['Technical Skills:', applicant_data.get('technical_skills', 'N/A')],
        ['Soft Skills:', applicant_data.get('soft_skills', 'N/A')],
        ['Programming Languages:', applicant_data.get('programming_languages', 'N/A')],
        ['Certifications:', applicant_data.get('certifications', 'None')],
        ['Greatest Strength:', applicant_data.get('greatest_strength', 'N/A')],
        ['Area for Improvement:', applicant_data.get('biggest_weakness', 'N/A')]
    ]
    
    skills_table = Table(skills_data, colWidths=[1.7*inch, 4.3*inch])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    content.append(skills_table)
    content.append(Spacer(1, 0.15*inch))
    
    # References
    content.append(Paragraph("6. PROFESSIONAL REFERENCES", section_style))
    
    ref_data = []
    for i in range(1, 4):
        ref_key = f'reference_{i}'
        if applicant_data.get(ref_key):
            ref_info = applicant_data[ref_key].split(', ')
            if len(ref_info) >= 4:
                ref_data.append([f'Reference {i}:', ref_info[0], 'Title:', ref_info[1]])
                ref_data.append(['Company:', ref_info[2], 'Contact:', f"{ref_info[3]} / {ref_info[4] if len(ref_info) > 4 else 'N/A'}"])
            else:
                ref_data.append([f'Reference {i}:', applicant_data[ref_key], '', ''])
        else:
            ref_data.append([f'Reference {i}:', 'Available upon request', '', ''])
    
    if ref_data:
        ref_table = Table(ref_data, colWidths=[1.2*inch, 2.3*inch, 1*inch, 1.5*inch])
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
    content.append(Spacer(1, 0.1*inch))
    
    # Emergency Contact
    emergency_data = [
        ['Emergency Contact:', applicant_data.get('emergency_contact_name', 'N/A'), 
         'Relationship:', applicant_data.get('emergency_contact_relationship', 'N/A')],
        ['Emergency Phone:', applicant_data.get('emergency_contact_phone', 'N/A'), '', '']
    ]
    
    emergency_table = Table(emergency_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch])
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
    content.append(Spacer(1, 0.15*inch))
    
    # Additional Information
    content.append(Paragraph("7. ADDITIONAL INFORMATION", section_style))
    
    additional_data = [
        ['How did you find this position?', applicant_data.get('how_found_position', 'N/A')],
        ['Referral Source:', applicant_data.get('referral_source', 'N/A')],
        ['Cover Letter Submitted:', applicant_data.get('cover_letter_submitted', 'No')],
        ['Background Check Consent:', applicant_data.get('reference_check_consent', 'Yes')],
        ['Drug Test Consent:', applicant_data.get('drug_test_consent', 'Yes')]
    ]
    
    additional_table = Table(additional_data, colWidths=[2*inch, 4*inch])
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
    content.append(Paragraph("8. APPLICANT CERTIFICATION", section_style))
    
    certification_text = """I certify that the information provided in this application is true and complete to the best of my knowledge. 
    I understand that false information may lead to dismissal if I am employed. I authorize the company to contact my references and verify information."""
    
    content.append(Paragraph(certification_text, styles['Normal']))
    content.append(Spacer(1, 0.1*inch))
    
    signature_data = [
        ['Electronic Signature:', applicant_data.get('electronic_signature', ''), 'Date:', applicant_data.get('signature_date', '')],
        ['Print Name:', f"{applicant_data['first_name']} {applicant_data['last_name']}", 'Terms Accepted:', applicant_data.get('terms_accepted', 'Yes')]
    ]
    
    signature_table = Table(signature_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1*inch])
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
    
    # Build PDF
    doc.build(content)
    return filepath

def process_csv_and_generate_professional_pdfs(csv_filename='realistic_job_applications.csv'):
    """Read CSV data and generate comprehensive PDF forms for each applicant"""
    
    if not os.path.exists(csv_filename):
        print(f"❌ Error: {csv_filename} not found! Please run generate_realistic_dummy_data.py first.")
        return
    
    generated_files = []
    
    try:
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            print("🔄 Generating comprehensive PDF job application forms...")
            print("📋 Each form includes detailed sections for personal info, experience, skills, and references...")
            
            for i, row in enumerate(reader, 1):
                try:
                    pdf_path = create_comprehensive_pdf(row)
                    generated_files.append(pdf_path)
                    print(f"✅ Generated: {os.path.basename(pdf_path)}")
                    
                    # Progress indicator
                    if i % 10 == 0:
                        print(f"📊 Progress: {i} forms completed...")
                        
                except Exception as e:
                    print(f"❌ Error generating PDF for {row.get('first_name', 'Unknown')} {row.get('last_name', '')}: {e}")
            
        print(f"\n🎉 Successfully generated {len(generated_files)} comprehensive PDF job application forms!")
        print(f"📁 Files saved in 'professional_pdf_forms' folder")
        print(f"📄 Each PDF contains 8 detailed sections with professional formatting")
        
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")

if __name__ == "__main__":
    process_csv_and_generate_professional_pdfs()