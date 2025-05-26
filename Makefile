# Simple Indonesian Job Application + e-KTP Generator
PYTHON := python3
PIP := pip3
VENV_NAME := venv
NUM_RECORDS := 50

# File names
DATA_FILE := indonesian_job_applications.csv
EKTP_DATA := indonesian_ektp_data.csv
PDF_FOLDER := indonesian_pdf_forms
EKTP_IMAGES_FOLDER := indonesian_ktp

# Colors
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
CYAN := \033[0;36m
NC := \033[0m

# Default help
.PHONY: help
help:
	@echo "$(CYAN)🇮🇩 Indonesian Job Application + e-KTP Generator$(NC)"
	@echo ""
	@echo "$(YELLOW)🔧 Setup Commands:$(NC)"
	@echo "  $(GREEN)make venv$(NC)           - Create virtual environment"
	@echo "  $(GREEN)make install$(NC)        - Install requirements"
	@echo ""
	@echo "$(YELLOW)🚀 Generation Commands:$(NC)"
	@echo "  $(GREEN)make dummy-data$(NC)     - Generate job application data ($(NUM_RECORDS) records)"
	@echo "  $(GREEN)make pdf$(NC)            - Generate PDF forms"
	@echo "  $(GREEN)make ektp-images$(NC)    - Generate e-KTP images"
	@echo ""
	@echo "$(YELLOW)🧹 Cleanup Commands:$(NC)"
	@echo "  $(GREEN)make clean-all$(NC)      - Remove all generated files"
	@echo ""
	@echo "$(YELLOW)🎯 Quick Start:$(NC)"
	@echo "  $(GREEN)make start$(NC)          - Run all three generation commands"

# Setup commands
.PHONY: venv
venv:
	@echo "$(CYAN)🔧 Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "$(GREEN)✅ Virtual environment created: $(VENV_NAME)$(NC)"
	@echo "$(BLUE)💡 Activate with: source $(VENV_NAME)/bin/activate$(NC)"

.PHONY: install
install:
	@echo "$(CYAN)📦 Installing requirements...$(NC)"
	$(PIP) install faker==19.6.2 reportlab==4.0.4 Pillow
	@echo "$(GREEN)✅ Requirements installed!$(NC)"

# Generation commands
.PHONY: dummy-data
dummy-data:
	@echo "$(CYAN)📊 Generating Indonesian job application data...$(NC)"
	@if [ ! -f "src/generate_indonesian_dummy_data.py" ]; then \
		echo "❌ generate_indonesian_dummy_data.py not found!"; \
		exit 1; \
	fi
	$(PYTHON) src/generate_indonesian_dummy_data.py
	@echo "$(GREEN)✅ Job application data generated: $(DATA_FILE)$(NC)"

.PHONY: pdf
pdf:
	@echo "$(CYAN)📄 Generating PDF forms...$(NC)"
	@if [ ! -f "$(DATA_FILE)" ]; then \
		echo "❌ $(DATA_FILE) not found! Run 'make dummy-data' first"; \
		exit 1; \
	fi
	@if [ ! -f "src/generate_indonesian_pdf_forms.py" ]; then \
		echo "❌ generate_indonesian_pdf_forms.py not found!"; \
		exit 1; \
	fi
	$(PYTHON) src/generate_indonesian_pdf_forms.py
	@echo "$(GREEN)✅ PDF forms generated in: $(PDF_FOLDER)/$(NC)"

.PHONY: ektp-images
ektp-images:
	@echo "$(CYAN)🖼️  Generating e-KTP images...$(NC)"
	@if [ ! -f "$(DATA_FILE)" ]; then \
		echo "❌ $(DATA_FILE) not found! Run 'make dummy-data' first"; \
		exit 1; \
	fi
	@if [ ! -f "src/generate_ektp_images_from_csv.py" ]; then \
		echo "❌ generate_ektp_images_from_csv.py not found!"; \
		exit 1; \
	fi
	@if [ ! -f "src/assets/images.jpg" ]; then \
		echo "⚠️  src/assets/images.jpg not found. Please add a sample photo."; \
		exit 1; \
	fi
	$(PYTHON) src/generate_ektp_images_from_csv.py
	@echo "$(GREEN)✅ e-KTP images generated in: $(EKTP_IMAGES_FOLDER)/$(NC)"

# Combined commands
.PHONY: start
start: dummy-data pdf ektp-images
	@[ -f "src/result.png" ] && rm -f src/result.png && echo "🗑️ Removed: src/result.png" || true
	@[ -f "data.json" ] && rm -f data.json && echo "🗑️ Removed: data.json" || true
	@echo "$(GREEN)🎉 All generation complete!$(NC)"
	@echo "$(BLUE)📊 Data: $(DATA_FILE)$(NC)"
	@echo "$(BLUE)📄 PDFs: $(PDF_FOLDER)/$(NC)"
	@echo "$(BLUE)🖼️ Images: $(EKTP_IMAGES_FOLDER)/$(NC)"
	

# Cleanup
.PHONY: clean-all
clean-all:
	@echo "$(CYAN)🧹 Cleaning all generated files...$(NC)"
	@[ -f "$(DATA_FILE)" ] && rm -f $(DATA_FILE) && echo "🗑️ Removed: $(DATA_FILE)" || true
	@[ -f "$(EKTP_DATA)" ] && rm -f $(EKTP_DATA) && echo "🗑️ Removed: $(EKTP_DATA)" || true
	@[ -d "$(PDF_FOLDER)" ] && rm -rf $(PDF_FOLDER) && echo "🗑️ Removed: $(PDF_FOLDER)/" || true
	@[ -d "$(EKTP_IMAGES_FOLDER)" ] && rm -rf $(EKTP_IMAGES_FOLDER) && echo "🗑️ Removed: $(EKTP_IMAGES_FOLDER)/" || true
	@[ -f "validation_report.json" ] && rm -f validation_report.json && echo "🗑️ Removed: validation_report.json" || true
	@[ -f "data.json" ] && rm -f data.json && echo "🗑️ Removed: data.json" || true
	@[ -f "src/result.png" ] && rm -f src/result.png && echo "🗑️ Removed: src/result.png" || true
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"