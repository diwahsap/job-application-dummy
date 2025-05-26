# Multi-Format Job Application Form Generator Makefile
# Author: GitHub Copilot
# Date: 2025-05-26 06:10:45 UTC
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
	@echo "$(CYAN)🌍🇮🇩 Multi-Format Job Application Form Generator$(NC)"
	@echo "$(BLUE)Created for: diwahsap$(NC)"
	@echo "$(BLUE)Date: 2025-05-26 06:10:45 UTC$(NC)"
	@echo ""
	@echo "$(YELLOW)📋 Available Formats:$(NC)"
	@echo "  🇮🇩 Indonesian (id_ID) - Indonesian names, companies, Rupiah, local context"
	@echo "  🌍 Global (en_US) - International names, companies, USD, global context"
	@echo ""
	@echo "$(YELLOW)🚀 Quick Commands:$(NC)"
	@echo "  $(GREEN)make indonesian$(NC)     - Generate Indonesian format (50 records)"
	@echo "  $(GREEN)make global$(NC)         - Generate Global format (50 records)"
	@echo "  $(GREEN)make both$(NC)           - Generate both formats consecutively"
	@echo "  $(GREEN)make quick-id$(NC)       - Quick Indonesian (10 records)"
	@echo "  $(GREEN)make quick-global$(NC)   - Quick Global (10 records)"
	@echo "  $(GREEN)make demo$(NC)           - Demo both formats (5 records each)"
	@echo ""
	@echo "$(YELLOW)📋 Format-Specific Commands:$(NC)"
	@echo "  $(GREEN)make run FORMAT=indonesian$(NC)  - Indonesian workflow"
	@echo "  $(GREEN)make run FORMAT=global$(NC)      - Global workflow"
	@echo "  $(GREEN)make data-id$(NC)                - Indonesian data only"
	@echo "  $(GREEN)make data-global$(NC)            - Global data only"
	@echo "  $(GREEN)make pdfs-id$(NC)                - Indonesian PDFs only"
	@echo "  $(GREEN)make pdfs-global$(NC)            - Global PDFs only"
	@echo ""
	@echo "$(YELLOW)🛠️  General Commands:$(NC)"
	@echo "  $(GREEN)make setup$(NC)          - Set up environment"
	@echo "  $(GREEN)make install$(NC)        - Install dependencies"
	@echo "  $(GREEN)make check$(NC)          - Check dependencies and locales"
	@echo "  $(GREEN)make stats$(NC)          - Show statistics for both formats"
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

.PHONY: quick-id
quick-id:
	@echo "$(CYAN)⚡🇮🇩 Quick Indonesian (10 records)...$(NC)"
	@$(MAKE) FORMAT=indonesian NUM_RECORDS=10 run

.PHONY: quick-global
quick-global:
	@echo "$(CYAN)⚡🌍 Quick Global (10 records)...$(NC)"
	@$(MAKE) FORMAT=global NUM_RECORDS=10 run

.PHONY: demo
demo:
	@echo "$(CYAN)🎬 Demo mode - generating samples of both formats...$(NC)"
	@echo "$(YELLOW)Creating Indonesian demo...$(NC)"
	@$(MAKE) FORMAT=indonesian NUM_RECORDS=5 run
	@echo "$(YELLOW)Creating Global demo...$(NC)"
	@$(MAKE) FORMAT=global NUM_RECORDS=5 run
	@$(MAKE) stats
	@echo "$(GREEN)🎉 Demo complete! Check both folders for samples.$(NC)"

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
	@echo "$(CYAN)🔧 Setting up multi-format environment...$(NC)"
	@if command -v python3 >/dev/null 2>&1; then \
		echo "$(GREEN)✅ Python3 found$(NC)"; \
	else \
		echo "$(RED)❌ Python3 not found. Please install Python 3.7+$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)📦 Creating virtual environment: $(VENV_NAME)$(NC)"
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "$(YELLOW)📋 Installing packages for both formats...$(NC)"
	@bash -c "source $(VENV_NAME)/bin/activate && pip install --upgrade pip"
	@bash -c "source $(VENV_NAME)/bin/activate && pip install faker==19.6.2 reportlab==4.0.4"
	@echo "$(GREEN)✅ Multi-format environment ready!$(NC)"
	@echo "$(BLUE)💡 Supports both Indonesian (id_ID) and Global (en_US) formats$(NC)"

.PHONY: install
install:
	@echo "$(CYAN)📦 Installing packages for multi-format generator...$(NC)"
	$(PIP) install faker==19.6.2 reportlab==4.0.4
	@echo "$(GREEN)✅ Dependencies installed for both formats!$(NC)"

# Check dependencies and locales
.PHONY: check
check:
	@echo "$(CYAN)🔍 Checking multi-format capabilities...$(NC)"
	@$(PYTHON) -c "import faker; print('✅ Faker version:', faker.__version__)" 2>/dev/null || echo "$(RED)❌ Faker not installed$(NC)"
	@$(PYTHON) -c "import reportlab; print('✅ ReportLab version:', reportlab.Version)" 2>/dev/null || echo "$(RED)❌ ReportLab not installed$(NC)"
	@echo "$(BLUE)Testing locales:$(NC)"
	@$(PYTHON) -c "from faker import Faker; f = Faker('id_ID'); print('🇮🇩 Indonesian locale:', f.name(), '|', f.city())" 2>/dev/null || echo "$(RED)❌ Indonesian locale not available$(NC)"
	@$(PYTHON) -c "from faker import Faker; f = Faker('en_US'); print('🌍 Global locale:', f.name(), '|', f.city())" 2>/dev/null || echo "$(RED)❌ Global locale not available$(NC)"
	@echo "$(BLUE)Checking generator scripts:$(NC)"
	@[ -f "generate_indonesian_dummy_data.py" ] && echo "✅ Indonesian generator found" || echo "$(RED)❌ Indonesian generator missing$(NC)"
	@[ -f "generate_realistic_dummy_data.py" ] && echo "✅ Global generator found" || echo "$(RED)❌ Global generator missing$(NC)"
	@[ -f "generate_indonesian_pdf_forms.py" ] && echo "✅ Indonesian PDF generator found" || echo "$(RED)❌ Indonesian PDF generator missing$(NC)"
	@[ -f "generate_professional_pdf_forms.py" ] && echo "✅ Global PDF generator found" || echo "$(RED)❌ Global PDF generator missing$(NC)"

# Generate data based on format
.PHONY: generate-data
generate-data:
	@echo "$(CYAN)$(FLAG) Generating $(DESCRIPTION) data ($(NUM_RECORDS) records)...$(NC)"
	@if [ ! -f "$(GENERATOR_SCRIPT)" ]; then \
		echo "$(RED)❌ $(GENERATOR_SCRIPT) not found!$(NC)"; \
		echo "$(YELLOW)💡 Required scripts:$(NC)"; \
		echo "  Indonesian: generate_indonesian_dummy_data.py"; \
		echo "  Global: generate_realistic_dummy_data.py"; \
		exit 1; \
	fi
	@# Update the number of records in the script
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
		echo "$(YELLOW)💡 Required scripts:$(NC)"; \
		echo "  Indonesian: generate_indonesian_pdf_forms.py"; \
		echo "  Global: generate_professional_pdf_forms.py"; \
		exit 1; \
	fi
	@# Update CSV filename in PDF script if needed
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

# Show statistics for both formats
.PHONY: stats
stats:
	@echo "$(CYAN)📊 Multi-Format Statistics:$(NC)"
	@echo ""
	@echo "$(YELLOW)🇮🇩 Indonesian Format:$(NC)"
	@if [ -f "indonesian_job_applications.csv" ]; then \
		RECORDS=$$(tail -n +2 indonesian_job_applications.csv | wc -l 2>/dev/null || echo "0"); \
		COLUMNS=$$(head -n 1 indonesian_job_applications.csv | tr ',' '\n' | wc -l 2>/dev/null || echo "0"); \
		SIZE=$$(du -h indonesian_job_applications.csv 2>/dev/null | cut -f1 || echo "0"); \
		echo "  📄 Records: $(PURPLE)$$RECORDS Indonesian applicants$(NC)"; \
		echo "  📋 Columns: $(PURPLE)$$COLUMNS fields$(NC)"; \
		echo "  💾 File size: $(PURPLE)$$SIZE$(NC)"; \
	else \
		echo "  $(RED)❌ Not generated yet$(NC)"; \
	fi
	@if [ -d "indonesian_pdf_forms" ]; then \
		PDF_COUNT=$$(find indonesian_pdf_forms -name "*.pdf" 2>/dev/null | wc -l || echo "0"); \
		PDF_SIZE=$$(du -sh indonesian_pdf_forms 2>/dev/null | cut -f1 || echo "0"); \
		echo "  📑 PDFs: $(PURPLE)$$PDF_COUNT forms ($$PDF_SIZE)$(NC)"; \
	else \
		echo "  📑 PDFs: $(RED)❌ Not generated yet$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)🌍 Global Format:$(NC)"
	@if [ -f "realistic_job_applications.csv" ]; then \
		RECORDS=$$(tail -n +2 realistic_job_applications.csv | wc -l 2>/dev/null || echo "0"); \
		COLUMNS=$$(head -n 1 realistic_job_applications.csv | tr ',' '\n' | wc -l 2>/dev/null || echo "0"); \
		SIZE=$$(du -h realistic_job_applications.csv 2>/dev/null | cut -f1 || echo "0"); \
		echo "  📄 Records: $(PURPLE)$$RECORDS global applicants$(NC)"; \
		echo "  📋 Columns: $(PURPLE)$$COLUMNS fields$(NC)"; \
		echo "  💾 File size: $(PURPLE)$$SIZE$(NC)"; \
	else \
		echo "  $(RED)❌ Not generated yet$(NC)"; \
	fi
	@if [ -d "professional_pdf_forms" ]; then \
		PDF_COUNT=$$(find professional_pdf_forms -name "*.pdf" 2>/dev/null | wc -l || echo "0"); \
		PDF_SIZE=$$(du -sh professional_pdf_forms 2>/dev/null | cut -f1 || echo "0"); \
		echo "  📑 PDFs: $(PURPLE)$$PDF_COUNT forms ($$PDF_SIZE)$(NC)"; \
	else \
		echo "  📑 PDFs: $(RED)❌ Not generated yet$(NC)"; \
	fi
	@echo ""
	@TOTAL_RECORDS=0; \
	[ -f "indonesian_job_applications.csv" ] && TOTAL_RECORDS=$$((TOTAL_RECORDS + $$(tail -n +2 indonesian_job_applications.csv | wc -l 2>/dev/null || echo "0"))); \
	[ -f "realistic_job_applications.csv" ] && TOTAL_RECORDS=$$((TOTAL_RECORDS + $$(tail -n +2 realistic_job_applications.csv | wc -l 2>/dev/null || echo "0"))); \
	echo "$(BLUE)📈 Total Records Generated: $(PURPLE)$$TOTAL_RECORDS$(NC)"

# Compare formats
.PHONY: compare
compare:
	@echo "$(CYAN)🆚 Indonesian vs Global Format Comparison:$(NC)"
	@echo ""
	@echo "$(YELLOW)🇮🇩 Indonesian Format Features:$(NC)"
	@echo "  📍 Locale: id_ID (Indonesian)"
	@echo "  👤 Names: Indonesian names (Budi, Sari, etc.)"
	@echo "  🏢 Companies: Gojek, Tokopedia, BCA, Telkom, Astra"
	@echo "  🎓 Universities: UI, ITB, UGM, ITS, Unair"
	@echo "  💰 Currency: Indonesian Rupiah (Rp 5,000,000 - 60,000,000)"
	@echo "  📄 Documents: NIK, NPWP, BPJS numbers"
	@echo "  🗣️  Language: Mixed Indonesian/English"
	@echo "  🏙️  Cities: Jakarta, Surabaya, Bandung, Medan"
	@echo "  📋 File: indonesian_job_applications.csv"
	@echo "  📁 PDFs: indonesian_pdf_forms/"
	@echo ""
	@echo "$(YELLOW)🌍 Global Format Features:$(NC)"
	@echo "  📍 Locale: en_US (English/International)"
	@echo "  👤 Names: International names (John, Sarah, etc.)"
	@echo "  🏢 Companies: Google, Microsoft, Amazon, Meta, Apple"
	@echo "  🎓 Universities: Harvard, Stanford, MIT, Yale, Princeton"
	@echo "  💰 Currency: US Dollar ($45,000 - $250,000)"
	@echo "  📄 Documents: SSN, standard international IDs"
	@echo "  🗣️  Language: English"
	@echo "  🏙️  Cities: New York, Los Angeles, Chicago, Houston"
	@echo "  📋 File: realistic_job_applications.csv"
	@echo "  📁 PDFs: professional_pdf_forms/"

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

# Clean specific format or all
.PHONY: clean
clean:
	@echo "$(CYAN)🧹 Cleaning $(DESCRIPTION) files...$(NC)"
	@[ -f "$(DATA_FILE)" ] && rm -f $(DATA_FILE) && echo "$(YELLOW)🗑️  Removed: $(DATA_FILE)$(NC)" || true
	@[ -d "$(PDF_FOLDER)" ] && rm -rf $(PDF_FOLDER) && echo "$(YELLOW)🗑️  Removed: $(PDF_FOLDER)/$(NC)" || true
	@[ -f "*.pyc" ] && rm -f *.pyc || true
	@[ -d "__pycache__" ] && rm -rf __pycache__ || true
	@echo "$(GREEN)✅ $(DESCRIPTION) cleanup complete!$(NC)"

.PHONY: clean-all
clean-all:
	@echo "$(CYAN)🧹 Cleaning all formats...$(NC)"
	@rm -f indonesian_job_applications.csv realistic_job_applications.csv
	@rm -rf indonesian_pdf_forms professional_pdf_forms
	@rm -f *.pyc
	@rm -rf __pycache__ $(VENV_NAME) backup_*
	@echo "$(GREEN)✅ Complete cleanup finished!$(NC)"

# Create backup for specific format
.PHONY: backup
backup:
	@BACKUP_DIR="backup_$(FORMAT)_$(shell date +%Y%m%d_%H%M%S)"; \
	echo "$(CYAN)💾 Creating $(DESCRIPTION) backup: $$BACKUP_DIR$(NC)"; \
	mkdir -p $$BACKUP_DIR; \
	[ -f "$(DATA_FILE)" ] && cp $(DATA_FILE) $$BACKUP_DIR/ || true; \
	[ -d "$(PDF_FOLDER)" ] && cp -r $(PDF_FOLDER) $$BACKUP_DIR/ || true; \
	cp *.py $$BACKUP_DIR/ 2>/dev/null || true; \
	echo "$(GREEN)✅ $(DESCRIPTION) backup created: $$BACKUP_DIR$(NC)"

# Test both formats
.PHONY: test
test:
	@echo "$(CYAN)🧪 Testing multi-format capabilities...$(NC)"
	@$(PYTHON) -c "from faker import Faker; print('🇮🇩 Indonesian test:', Faker('id_ID').name(), '|', Faker('id_ID').city()); print('🌍 Global test:', Faker('en_US').name(), '|', Faker('en_US').city())"
	@echo "$(GREEN)✅ Multi-format tests passed!$(NC)"

# Show current format info
.PHONY: info
info:
	@echo "$(CYAN)ℹ️  Current Format Information:$(NC)"
	@echo "  Format: $(FLAG) $(PURPLE)$(DESCRIPTION)$(NC)"
	@echo "  Locale: $(PURPLE)$(LOCALE)$(NC)"
	@echo "  Generator: $(PURPLE)$(GENERATOR_SCRIPT)$(NC)"
	@echo "  PDF Generator: $(PURPLE)$(PDF_SCRIPT)$(NC)"
	@echo "  Data file: $(PURPLE)$(DATA_FILE)$(NC)"
	@echo "  PDF folder: $(PURPLE)$(PDF_FOLDER)$(NC)"
	@echo "  Records to generate: $(PURPLE)$(NUM_RECORDS)$(NC)"

# Quick switch between formats
.PHONY: switch-id
switch-id:
	@echo "$(CYAN)🔄 Switching to Indonesian format...$(NC)"
	@$(MAKE) FORMAT=indonesian info

.PHONY: switch-global
switch-global:
	@echo "$(CYAN)🔄 Switching to Global format...$(NC)"
	@$(MAKE) FORMAT=global info

# Show available files
.PHONY: list
list:
	@echo "$(CYAN)📂 Available Files:$(NC)"
	@echo "$(YELLOW)Generator Scripts:$(NC)"
	@ls -la generate_*.py 2>/dev/null || echo "  No generator scripts found"
	@echo "$(YELLOW)Data Files:$(NC)"
	@ls -la *.csv 2>/dev/null || echo "  No CSV files found"
	@echo "$(YELLOW)PDF Folders:$(NC)"
	@ls -ld *pdf_forms 2>/dev/null || echo "  No PDF folders found"