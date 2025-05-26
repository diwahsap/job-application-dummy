# Indonesian Job Application + e-KTP Generator

This project generates dummy Indonesian job application data, PDF forms, and e-KTP images for testing and demo purposes.

## Features

- Generate CSV data for job applications
- Create personalized PDF forms
- Generate e-KTP images from data
- Easy setup with `make` commands

## Requirements

- Python 3.x
- Make
- (Optional) GitHub Actions for CI/CD

## Setup

1. **Clone the repo:**

   ```sh
   git clone https://github.com/diwahsap/job-application-dummy.git
   cd job-application-dummy
   ```

2. **Setup virtual environment:**

   ```sh
   make venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```sh
   make install
   ```

## Usage

### Generate Data

- **Generate dummy data:**  
  `make dummy-data`

- **Generate PDF forms:**  
  `make pdf`

- **Generate e-KTP images:**  
  `make ektp-images`

- **Quick Start (all at once):**  
  `make start`

### Cleanup

- **Remove all generated files:**  
  `make clean-all`

## Project Structure

- `src/` : Source scripts for generating data, PDFs, and images
- `indonesian_job_applications.csv` : Generated job application data
- `indonesian_pdf_forms/` : Generated PDF forms
- `indonesian_ktp/` : Generated e-KTP images

## CI/CD

This repo includes a GitHub Actions workflow to automatically run `make start` and save the output files as artifacts.

---

## License

MIT
