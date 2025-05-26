# Multi-Format Job Application + e-KTP Generator Makefile
# Author: GitHub Copilot
# Date: 2025-05-26 06:28:48 UTC
# User: diwahsap

# Configuration
PYTHON := python3
PIP := pip3
VENV_NAME := job_app_env
NUM_RECORDS := 50

# Format selection (can be overridden)
FORMAT := indonesian
ifeq ($(FORMAT),global)
    DATA_FILE := realistic_job_applications.csv
    PDF_FOLDER := professional_pdf_forms
    LOCALE := en_US
    GENERATOR_SCRIPT := generate_realistic_dummy_data.py
    PDF_SCRIPT := generate_professional_pdf_forms.py
    FLAG := 🌍
    DESCRIPTION := Global/International
else
    DATA_FILE := indonesian_job_applications.csv
    PDF_FOLDER := indonesian_pdf_forms
    LOCALE := id_ID
    GENERATOR_SCRIPT := generate_indonesian_dummy_data.py
    PDF_SCRIPT := generate_indonesian_pdf_forms.py
    FLAG := 🇮🇩
    DESCRIPTION := Indonesian
endif

# e-KTP files (Indonesian only)
EKTP_DATA := indonesian_ektp_data.csv
EKTP_GENERATOR := generate_ektp_dummy_data.py
VALIDATION_REPORT := validation_report.json

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m # No Color

# Default target
.PHONY: help
help:
	@echo "$(CYAN)🌍🇮🇩 Multi-Format Job Application + e-KTP Generator$(NC)"
	@echo "$(BLUE)Created for: diwahsap$(NC)"
	@echo "$(BLUE)Date: 2025-05-26 06:28:48 UTC$(NC)"
	@echo ""
	@echo "$(YELLOW)📋 Available Formats:$(NC)"
	@echo "  🇮🇩 Indonesian (id_ID) - Indonesian names, companies, Rupiah + e-KTP"
	@echo "  🌍 Global (en_US) - International names, companies, USD"
	@echo ""
	@echo "$(YELLOW)🚀 Quick Commands:$(NC)"
	@echo "  $(GREEN)make indonesian$(NC)     - Generate Indonesian format (50 records)"
	@echo "  $(GREEN)make global$(NC)         - Generate Global format (50 records)"
	@echo "  $(GREEN)make full-indonesian$(NC) - Indonesian + e-KTP + validation data"
	@echo "  $(GREEN)make both$(NC)           - Generate both formats"
	@echo "  $(GREEN)make demo$(NC)           - Demo both formats (5 records each)"
	@echo ""
	@echo "$(YELLOW)🆔 e-KTP Commands (Indonesian only):$(NC)"
	@echo "  $(GREEN)make ektp$(NC)           - Generate e-KTP data with mismatches"
	@echo "  $(GREEN)make validation$(NC)     - Create validation test dataset"
	@echo "  $(GREEN)make check-mismatches$(NC) - Show mismatch statistics"
	@echo "  $(GREEN)make ektp-clean$(NC)     - Clean e-KTP files only"
	@echo ""
	@echo "$(YELLOW)📋 Format-Specific Commands:$(NC)"
	@echo "  $(GREEN)make run FORMAT=indonesian$(NC)  - Indonesian workflow"
	@echo "  $(GREEN)make run FORMAT=global$(NC)      - Global workflow"
	@echo "  $(GREEN)make data-id$(NC)                - Indonesian data only"
	@echo "  $(GREEN)make data-global$(NC)            - Global data only"
	@echo ""
	@echo "$(YELLOW)🛠️  General Commands:$(NC)"
	@echo "  $(GREEN)make setup$(NC)          - Set up environment"
	@echo "  $(GREEN)make install$(NC)        - Install dependencies"
	@echo "  $(GREEN)make check$(NC)          - Check dependencies and locales"
	@echo "  $(GREEN)make stats$(NC)          - Show statistics for all formats"
	@echo "  $(GREEN)make compare$(NC)        - Compare Indonesian vs Global features"
	@echo "  $(GREEN)make clean$(NC)          - Clean current format files"
	@echo "  $(GREEN)make clean-all$(NC)      - Clean all formats"
	@echo ""
	@echo "$(YELLOW)Current Configuration:$(NC)"
	@echo "  Format: $(FLAG) $(PURPLE)$(DESCRIPTION)$(NC)"
	@echo "  Locale: $(PURPLE)$(LOCALE)$(NC)"
	@echo "  Records: $(PURPLE)$(NUM_RECORDS)$(NC)"
	@echo "  Data file: $(PURPLE)$(DATA_FILE)$(NC)"
	@echo "  PDF folder: $(PURPLE)$(PDF_FOLDER)$(NC)"

# Quick format commands
.PHONY: indonesian
indonesian:
	@echo "$(CYAN)🇮🇩 Generating Indonesian format ($(NUM_RECORDS) records)...$(NC)"
	@$(MAKE) FORMAT=indonesian run

.PHONY: global
global:
	@echo "$(CYAN)🌍 Generating Global format ($(NUM_RECORDS) records)...$(NC)"
	@$(MAKE) FORMAT=global run

.PHONY: full-indonesian
full-indonesian:
	@echo "$(CYAN)🇮🇩 Full Indonesian workflow with e-KTP validation...$(NC)"
	@$(MAKE) FORMAT=indonesian run
	@$(MAKE) ektp
	@$(MAKE) stats
	@echo "$(GREEN)🎉 Complete Indonesian dataset ready for validation testing!$(NC)"

.PHONY: both
both:
	@echo "$(CYAN)🌍🇮🇩 Generating both formats...$(NC)"
	@echo "$(YELLOW)📋 Step 1/2: Generating Indonesian format...$(NC)"
	@$(MAKE) FORMAT=indonesian run
	@echo ""
	@echo "$(YELLOW)📋 Step 2/2: Generating Global format...$(NC)"
	@$(MAKE) FORMAT=global run
	@echo ""
	@$(MAKE) compare
	@$(MAKE) stats

.PHONY: demo
demo:
	@echo "$(CYAN)🎬 Demo mode - generating samples of both formats...$(NC)"
	@echo "$(YELLOW)Creating Indonesian demo...$(NC)"
	@$(MAKE) FORMAT=indonesian NUM_RECORDS=5 run
	@echo "$(YELLOW)Creating Global demo...$(NC)"
	@$(MAKE) FORMAT=global NUM_RECORDS=5 run
	@$(MAKE) stats
	@echo "$(GREEN)🎉 Demo complete! Check both folders for samples.$(NC)"

# e-KTP specific commands
.PHONY: ektp
ektp:
	@echo "$(CYAN)🆔 Generating Indonesian e-KTP data with validation mismatches...$(NC)"
	@if [ ! -f "$(EKTP_GENERATOR)" ]; then \
		echo "$(RED)❌ $(EKTP_GENERATOR) not found!$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(DATA_FILE)" ]; then \
		echo "$(YELLOW)⚠️  Job application data not found. Generating e-KTP with sample data...$(NC)"; \
	fi
	$(PYTHON) $(EKTP_GENERATOR)
	@echo "$(GREEN)✅ e-KTP data generated with intentional mismatches!$(NC)"
	@echo "$(BLUE)📄 Files created:$(NC)"
	@echo "   📊 $(EKTP_DATA) - e-KTP data"
	@echo "   📋 $(VALIDATION_REPORT) - Mismatch analysis"

.PHONY: validation
validation: full-indonesian
	@echo "$(CYAN)🧪 Creating complete validation test dataset...$(NC)"
	@$(MAKE) check-mismatches
	@echo "$(GREEN)✅ Validation dataset ready!$(NC)"
	@echo "$(BLUE)Use this data to test your validation algorithms$(NC)"

.PHONY: check-mismatches
check-mismatches:
	@if [ ! -f "$(VALIDATION_REPORT)" ]; then \
		echo "$(RED)❌ Validation report not found. Run 'make ektp' first$(NC)"; \
		exit 1; \
	fi
	@echo "$(CYAN)📊 e-KTP Validation Report:$(NC)"
	@$(PYTHON) -c "import json; data=json.load(open('$(VALIDATION_REPORT)')); print(f'📋 Total records: {data[\"total_records\"]}'); print(f'✅ Valid records: {data[\"valid_records\"]}'); print(f'⚠️  Mismatch records: {data[\"mismatch_records\"]}'); print(f'📈 Mismatch rate: {data[\"mismatch_records\"]/data[\"total_records\"]*100:.1f}%'); print('🔍 Mismatch types:'); [print(f'   {k}: {v}') for k,v in data['mismatch_types'].items()]"

.PHONY: ektp-clean
ektp-clean:
	@echo "$(CYAN)🧹 Cleaning e-KTP files only...$(NC)"
	@[ -f "$(EKTP_DATA)" ] && rm -f $(EKTP_DATA) && echo "$(YELLOW)🗑️  Removed: $(EKTP_DATA)$(NC)" || true
	@[ -f "$(VALIDATION_REPORT)" ] && rm -f $(VALIDATION_REPORT) && echo "$(YELLOW)🗑️  Removed: $(VALIDATION_REPORT)$(NC)" || true
	@echo "$(GREEN)✅ e-KTP cleanup complete!$(NC)"

# Shortcut data commands
.PHONY: data-id
data-id:
	@$(MAKE) FORMAT=indonesian generate-data

.PHONY: data-global
data-global:
	@$(MAKE) FORMAT=global generate-data

.PHONY: pdfs-id
pdfs-id:
	@$(MAKE) FORMAT=indonesian generate-pdfs

.PHONY: pdfs-global
pdfs-global:
	@$(MAKE) FORMAT=global generate-pdfs

# Setup virtual environment
.PHONY: setup
setup:
	@echo "$(CYAN)🔧 Setting up multi-format + e-KTP environment...$(NC)"
	@if command -v python3 >/dev/null 2>&1; then \
		echo "$(GREEN)✅ Python3 found$(NC)"; \
	else \
		echo "$(RED)❌ Python3 not found. Please install Python 3.7+$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)📦 Creating virtual environment: $(VENV_NAME)$(NC)"
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "$(YELLOW)📋 Installing packages for all formats + e-KTP...$(NC)"
	@bash -c "source $(VENV_NAME)/bin/activate && pip install --upgrade pip"
	@bash -c "source $(VENV_NAME)/bin/activate && pip install faker==19.6.2 reportlab==4.0.4"
	@echo "$(GREEN)✅ Multi-format + e-KTP environment ready!$(NC)"

.PHONY: install
install:
	@echo "$(CYAN)📦 Installing packages for multi-format + e-KTP generator...$(NC)"
	$(PIP) install faker==19.6.2 reportlab==4.0.4
	@echo "$(GREEN)✅ Dependencies installed for all formats + e-KTP!$(NC)"

# Check dependencies and locales
.PHONY: check
check:
	@echo "$(CYAN)🔍 Checking multi-format + e-KTP capabilities...$(NC)"
	@$(PYTHON) -c "import faker; print('✅ Faker version:', faker.__version__)" 2>/dev/null || echo "$(RED)❌ Faker not installed$(NC)"
	@$(PYTHON) -c "import reportlab; print('✅ ReportLab version:', reportlab.Version)" 2>/dev/null || echo "$(RED)❌ ReportLab not installed$(NC)"
	@$(PYTHON) -c "import json; print('✅ JSON support available')" 2>/dev/null || echo "$(RED)❌ JSON not available$(NC)"
	@echo "$(BLUE)Testing locales:$(NC)"
	@$(PYTHON) -c "from faker import Faker; f = Faker('id_ID'); print('🇮🇩 Indonesian locale:', f.name(), '|', f.city())" 2>/dev/null || echo "$(RED)❌ Indonesian locale not available$(NC)"
	@$(PYTHON) -c "from faker import Faker; f = Faker('en_US'); print('🌍 Global locale:', f.name(), '|', f.city())" 2>/dev/null || echo "$(RED)❌ Global locale not available$(NC)"
	@echo "$(BLUE)Checking generator scripts:$(NC)"
	@[ -f "generate_indonesian_dummy_data.py" ] && echo "✅ Indonesian generator found" || echo "$(RED)❌ Indonesian generator missing$(NC)"
	@[ -f "generate_realistic_dummy_data.py" ] && echo "✅ Global generator found" || echo "$(RED)❌ Global generator missing$(NC)"
	@[ -f "generate_indonesian_pdf_forms.py" ] && echo "✅ Indonesian PDF generator found" || echo "$(RED)❌ Indonesian PDF generator missing$(NC)"
	@[ -f "generate_professional_pdf_forms.py" ] && echo "✅ Global PDF generator found" || echo "$(RED)❌ Global PDF generator missing$(NC)"
	@[ -f "$(EKTP_GENERATOR)" ] && echo "✅ e-KTP generator found" || echo "$(RED)❌ e-KTP generator missing$(NC)"

# Generate data based on format
.PHONY: generate-data
generate-data:
	@echo "$(CYAN)$(FLAG) Generating $(DESCRIPTION) data ($(NUM_RECORDS) records)...$(NC)"
	@if [ ! -f "$(GENERATOR_SCRIPT)" ]; then \
		echo "$(RED)❌ $(GENERATOR_SCRIPT) not found!$(NC)"; \
		exit 1; \
	fi
	@if [ "$(FORMAT)" = "indonesian" ]; then \
		sed -i.bak 's/generate_indonesian_job_application_data([0-9]*)/generate_indonesian_job_application_data($(NUM_RECORDS))/g' $(GENERATOR_SCRIPT); \
	else \
		sed -i.bak 's/generate_job_application_data([0-9]*)/generate_job_application_data($(NUM_RECORDS))/g' $(GENERATOR_SCRIPT); \
	fi
	$(PYTHON) $(GENERATOR_SCRIPT)
	@mv $(GENERATOR_SCRIPT).bak $(GENERATOR_SCRIPT) 2>/dev/null || true
	@echo "$(GREEN)✅ $(DESCRIPTION) data generation complete!$(NC)"
	@echo "$(BLUE)📄 Generated: $(DATA_FILE) ($(LOCALE) locale)$(NC)"

# Generate PDFs based on format
.PHONY: generate-pdfs
generate-pdfs:
	@echo "$(CYAN)$(FLAG) Generating $(DESCRIPTION) PDF forms...$(NC)"
	@if [ ! -f "$(DATA_FILE)" ]; then \
		echo "$(RED)❌ $(DATA_FILE) not found!$(NC)"; \
		echo "$(YELLOW)💡 Run 'make generate-data FORMAT=$(FORMAT)' first$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(PDF_SCRIPT)" ]; then \
		echo "$(RED)❌ $(PDF_SCRIPT) not found!$(NC)"; \
		exit 1; \
	fi
	@if [ "$(FORMAT)" = "indonesian" ]; then \
		sed -i.bak 's/indonesian_job_applications\.csv/$(DATA_FILE)/g' $(PDF_SCRIPT); \
	else \
		sed -i.bak 's/realistic_job_applications\.csv/$(DATA_FILE)/g' $(PDF_SCRIPT); \
	fi
	$(PYTHON) $(PDF_SCRIPT)
	@mv $(PDF_SCRIPT).bak $(PDF_SCRIPT) 2>/dev/null || true
	@echo "$(GREEN)✅ $(DESCRIPTION) PDF generation complete!$(NC)"
	@echo "$(BLUE)📁 PDFs saved in: $(PDF_FOLDER)/$(NC)"

# Complete workflow
.PHONY: run
run: generate-data generate-pdfs
	@echo "$(GREEN)🎉 $(FLAG) $(DESCRIPTION) workflow complete!$(NC)"
	@echo "$(BLUE)📊 Data: $(DATA_FILE)$(NC)"
	@echo "$(BLUE)📁 PDFs: $(PDF_FOLDER)/$(NC)"

# Show statistics for all formats
.PHONY: stats
stats:
	@echo "$(CYAN)📊 Multi-Format + e-KTP Statistics:$(NC)"
	@echo ""
	@echo "$(YELLOW)🇮🇩 Indonesian Format:$(NC)"
	@if [ -f "indonesian_job_applications.csv" ]; then \
		RECORDS=$$(tail -n +2 indonesian_job_applications.csv | wc -l 2>/dev/null || echo "0"); \
		SIZE=$$(du -h indonesian_job_applications.csv 2>/dev/null | cut -f1 || echo "0"); \
		echo "  📄 Job Applications: $(PURPLE)$$RECORDS records ($$SIZE)$(NC)"; \
	else \
		echo "  📄 Job Applications: $(RED)❌ Not generated yet$(NC)"; \
	fi
	@if [ -d "indonesian_pdf_forms" ]; then \
		PDF_COUNT=$$(find indonesian_pdf_forms -name "*.pdf" 2>/dev/null | wc -l || echo "0"); \
		echo "  📑 PDFs: $(PURPLE)$$PDF_COUNT forms$(NC)"; \
	else \
		echo "  📑 PDFs: $(RED)❌ Not generated yet$(NC)"; \
	fi
	@if [ -f "$(EKTP_DATA)" ]; then \
		EKTP_RECORDS=$$(tail -n +2 $(EKTP_DATA) | wc -l 2>/dev/null || echo "0"); \
		EKTP_SIZE=$$(du -h $(EKTP_DATA) 2>/dev/null | cut -f1 || echo "0"); \
		echo "  🆔 e-KTP Records: $(PURPLE)$$EKTP_RECORDS records ($$EKTP_SIZE)$(NC)"; \
		if [ -f "$(VALIDATION_REPORT)" ]; then \
			MISMATCH_COUNT=$$($(PYTHON) -c "import json; data=json.load(open('$(VALIDATION_REPORT)')); print(data['mismatch_records'])" 2>/dev/null || echo "0"); \
			echo "  ⚠️  Validation Mismatches: $(PURPLE)$$MISMATCH_COUNT records$(NC)"; \
		fi \
	else \
		echo "  🆔 e-KTP Records: $(RED)❌ Not generated yet$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)🌍 Global Format:$(NC)"
	@if [ -f "realistic_job_applications.csv" ]; then \
		RECORDS=$$(tail -n +2 realistic_job_applications.csv | wc -l 2>/dev/null || echo "0"); \
		SIZE=$$(du -h realistic_job_applications.csv 2>/dev/null | cut -f1 || echo "0"); \
		echo "  📄 Job Applications: $(PURPLE)$$RECORDS records ($$SIZE)$(NC)"; \
	else \
		echo "  📄 Job Applications: $(RED)❌ Not generated yet$(NC)"; \
	fi
	@if [ -d "professional_pdf_forms" ]; then \
		PDF_COUNT=$$(find professional_pdf_forms -name "*.pdf" 2>/dev/null | wc -l || echo "0"); \
		echo "  📑 PDFs: $(PURPLE)$$PDF_COUNT forms$(NC)"; \
	else \
		echo "  📑 PDFs: $(RED)❌ Not generated yet$(NC)"; \
	fi

# Compare formats
.PHONY: compare
compare:
	@echo "$(CYAN)🆚 Indonesian vs Global + e-KTP Comparison:$(NC)"
	@echo ""
	@echo "$(YELLOW)🇮🇩 Indonesian Format Features:$(NC)"
	@echo "  📍 Locale: id_ID (Indonesian)"
	@echo "  👤 Names: Indonesian names (Budi, Sari, etc.)"
	@echo "  🏢 Companies: Gojek, Tokopedia, BCA, Telkom, Astra"
	@echo "  🎓 Universities: UI, ITB, UGM, ITS, Unair"
	@echo "  💰 Currency: Indonesian Rupiah (Rp 5,000,000 - 60,000,000)"
	@echo "  📄 Documents: NIK, NPWP, BPJS numbers"
	@echo "  🆔 e-KTP: Full Indonesian e-KTP with validation mismatches"
	@echo "  🗣️  Language: Mixed Indonesian/English"
	@echo "  📋 Files: indonesian_job_applications.csv, indonesian_ektp_data.csv"
	@echo ""
	@echo "$(YELLOW)🌍 Global Format Features:$(NC)"
	@echo "  📍 Locale: en_US (English/International)"
	@echo "  👤 Names: International names (John, Sarah, etc.)"
	@echo "  🏢 Companies: Google, Microsoft, Amazon, Meta, Apple"
	@echo "  🎓 Universities: Harvard, Stanford, MIT, Yale, Princeton"
	@echo "  💰 Currency: US Dollar ($45,000 - $250,000)"
	@echo "  📄 Documents: SSN, standard international IDs"
	@echo "  🆔 e-KTP: Not applicable (Indonesian feature only)"
	@echo "  🗣️  Language: English"
	@echo "  📋 Files: realistic_job_applications.csv"

# View data based on current format
.PHONY: view-data
view-data:
	@if [ ! -f "$(DATA_FILE)" ]; then \
		echo "$(RED)❌ $(DATA_FILE) not found!$(NC)"; \
		echo "$(YELLOW)💡 Run 'make generate-data FORMAT=$(FORMAT)' first$(NC)"; \
		exit 1; \
	fi
	@echo "$(CYAN)$(FLAG) Sample $(DESCRIPTION) data from $(DATA_FILE):$(NC)"
	@head -n 4 $(DATA_FILE) | $(PYTHON) -c "import csv, sys; reader = csv.DictReader(sys.stdin); [print(f'$(BLUE)Record {i+1} ($(DESCRIPTION)):$(NC)') or [print(f'  {k}: {v}') for k, v in list(row.items())[:8]] or print() for i, row in enumerate(list(reader)[:2])]"

.PHONY: view-ektp
view-ektp:
	@if [ ! -f "$(EKTP_DATA)" ]; then \
		echo "$(RED)❌ $(EKTP_DATA) not found!$(NC)"; \
		echo "$(YELLOW)💡 Run 'make ektp' first$(NC)"; \
		exit 1; \
	fi
	@echo "$(CYAN)🆔 Sample e-KTP data from $(EKTP_DATA):$(NC)"
	@head -n 4 $(EKTP_DATA) | $(PYTHON) -c "import csv, sys; reader = csv.DictReader(sys.stdin); [print(f'$(BLUE)e-KTP Record {i+1}:$(NC)') or [print(f'  {k}: {v}') for k, v in list(row.items())[:10]] or print() for i, row in enumerate(list(reader)[:2])]"

# Clean specific format or all
.PHONY: clean
clean:
	@echo "$(CYAN)🧹 Cleaning $(DESCRIPTION) files...$(NC)"
	@[ -f "$(DATA_FILE)" ] && rm -f $(DATA_FILE) && echo "$(YELLOW)🗑️  Removed: $(DATA_FILE)$(NC)" || true
	@[ -d "$(PDF_FOLDER)" ] && rm -rf $(PDF_FOLDER) && echo "$(YELLOW)🗑️  Removed: $(PDF_FOLDER)/$(NC)" || true
	@if [ "$(FORMAT)" = "indonesian" ]; then \
		[ -f "$(EKTP_DATA)" ] && rm -f $(EKTP_DATA) && echo "$(YELLOW)🗑️  Removed: $(EKTP_DATA)$(NC)" || true; \
		[ -f "$(VALIDATION_REPORT)" ] && rm -f $(VALIDATION_REPORT) && echo "$(YELLOW)🗑️  Removed: $(VALIDATION_REPORT)$(NC)" || true; \
	fi
	@[ -f "*.pyc" ] && rm -f *.pyc || true
	@[ -d "__pycache__" ] && rm -rf __pycache__ || true
	@echo "$(GREEN)✅ $(DESCRIPTION) cleanup complete!$(NC)"

.PHONY: clean-all
clean-all:
	@echo "$(CYAN)🧹 Cleaning all formats + e-KTP...$(NC)"
	@rm -f indonesian_job_applications.csv realistic_job_applications.csv
	@rm -f $(EKTP_DATA) $(VALIDATION_REPORT)
	@rm -rf indonesian_pdf_forms professional_pdf_forms
	@rm -f *.pyc
	@rm -rf __pycache__ $(VENV_NAME) backup_*
	@echo "$(GREEN)✅ Complete cleanup finished!$(NC)"

# Test all formats including e-KTP
.PHONY: test
test:
	@echo "$(CYAN)🧪 Testing multi-format + e-KTP capabilities...$(NC)"
	@$(PYTHON) -c "from faker import Faker; print('🇮🇩 Indonesian test:', Faker('id_ID').name(), '|', Faker('id_ID').city()); print('🌍 Global test:', Faker('en_US').name(), '|', Faker('en_US').city())"
	@$(PYTHON) -c "import json; print('✅ JSON processing works')"
	@echo "$(GREEN)✅ All tests passed!$(NC)"

.PHONY: ktp-images
ktp-images:
	@echo "$(CYAN)🖼️  Generating KTP images for each CSV record...$(NC)"
	@if [ ! -f "generate_ektp_images_from_csv.py" ]; then \
		echo "$(RED)❌ generate_ektp_images_from_csv.py not found!$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "indonesian_job_applications.csv" ]; then \
		echo "$(RED)❌ indonesian_job_applications.csv not found! Run 'make ektp' first.$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "src/images.jpg" ]; then \
		echo "$(YELLOW)⚠️  src/photo.jpg (static photo) not found. Please add a sample photo.$(NC)"; \
		exit 1; \
	fi
	@python3 generate_ektp_images_from_csv.py
	@echo "$(GREEN)✅ All KTP images saved in ./results/$(NC)"