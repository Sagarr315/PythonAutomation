
# Day 1 – Python Desktop & Office Automation

## 1. Overview

Day 1 focuses on learning Python for desktop automation, office automation, file management, document processing and email automation.

The objective is to understand how Python can automate repetitive business tasks that are normally performed manually.

We will build individual automation modules using reusable Python functions and integrate them into practical business automation workflows.

## 2. Learning Objectives

- [x] Learn file and folder automation.
- [x] Learn Excel and CSV automation.
- [x] Learn PDF and Word document automation.
- [ ] Complete desktop automation testing.
- [ ] Complete email automation setup and testing.


---

# 3. Day 1 Modules

## Module 1: File & Folder Automation

### Objective

Automate file and folder management operations using Python.

### Topics Covered

1. File listing – List files available inside a directory.
2. File creation – Create new files.
3. File reading – Read content from text files.
4. File writing – Write and append data to files.
5. File copying – Copy files from one location to another.
6. File moving – Move files between directories.
7. File renaming – Rename existing files.
8. File deletion – Delete files safely.
9. Folder management – Create, list and manage directories.
10. File metadata – Retrieve file size, extension and timestamps.
11. File organizer – Automatically organize files according to their extensions.

### Libraries Used

- `os`
- `pathlib`
- `shutil`
- `datetime`

### Practical Project: File Organizer Bot

Created a file organizer that:

- Scans an input directory.
- Identifies files based on their extensions.
- Creates categorized output folders.
- Copies files into their respective folders.
- Verifies copied files.
- Generates an automation log.
- Displays execution statistics.

### Expected Output

- Excel folder
- PDF folder
- Word folder
- Images folder
- Text folder
- Other Files folder
- Automation log

**Status:** Completed at basic practical level.

---

## Module 2: Excel & CSV Automation

### Objective

Automate Excel workbook and CSV operations using Python.

### Topics Covered

1. Excel reading.
2. Excel writing.
3. Worksheet creation and management.
4. Data filtering and sorting.
5. Duplicate removal.
6. Data merging.
7. CSV reading.
8. CSV writing.
9. Excel to CSV conversion.
10. CSV to Excel conversion.
11. Excel report generation.
12. Excel formatting.

### Libraries Used

- `openpyxl`
- `pandas`
- `csv`
- `pathlib`

### Practical Project: Excel Data Processing Automation

Created an Excel automation application that:

- Generates sample employee and sales data.
- Reads Excel workbooks.
- Writes data into worksheets.
- Creates and manages multiple worksheets.
- Processes and filters records.
- Removes duplicate records.
- Merges data.
- Converts Excel files into CSV.
- Converts CSV files into Excel.
- Generates formatted Excel reports.

### Expected Output

- `Employees.xlsx`
- `Sales.xlsx`
- `Employees.csv`
- `Converted_From_Excel.csv`
- Processed Excel reports

**Status:** Completed at basic practical level.

---

## Module 3: PDF & Word Automation

### Objective

Automate PDF and Microsoft Word document operations using Python.

### PDF Automation Topics

1. PDF reading – Extract text from PDF documents.
2. PDF creation – Generate PDF documents.
3. PDF merging – Combine multiple PDF files.
4. PDF splitting – Split a PDF into multiple documents.
5. PDF metadata – Extract PDF information and metadata.
6. PDF table extraction – Extract tables from PDF documents.
7. PDF image processing – Render pages and extract embedded images.
8. PDF form handling – Read and fill supported PDF form fields.

### Word Automation Topics

1. Word creation – Create DOCX documents.
2. Word reading – Read paragraphs and tables.
3. Word editing – Update document content.
4. Document formatting – Apply basic formatting.

### Libraries Used

- `pypdf`
- `pdfplumber`
- `reportlab`
- `pymupdf`
- `python-docx`

### Practical Project: PDF & Word Document Automation

Created an application that:

- Generates sample PDF documents.
- Generates sample Word documents.
- Reads PDF and Word content.
- Creates PDF reports.
- Merges multiple PDFs.
- Splits PDF documents.
- Extracts PDF metadata.
- Extracts tables into CSV and Excel.
- Renders PDF pages into images.
- Extracts embedded images.
- Reads and fills supported PDF forms.
- Creates and edits Word documents.

### Expected Output

- `Sample_Report.pdf`
- `Sample_Form.pdf`
- `Sample_Document.docx`
- Merged PDF documents
- Split PDF documents
- Extracted tables in CSV/Excel
- Generated Word and PDF reports

**Important Notes:**

- Scanned PDFs may require OCR.
- PDF form editing requires supported form fields.
- Flattened PDF forms cannot be filled directly.

**Status:** Completed at basic practical level.

---

## Module 4: Desktop Automation

### Objective

Automate desktop applications and user interactions using Python.

### Topics Covered

1. Application automation – Launch desktop applications.
2. Mouse automation – Move, click, double-click and scroll.
3. Keyboard automation – Type text and perform keyboard shortcuts.
4. Screenshot automation – Capture full-screen and selected screen regions.
5. Clipboard automation – Copy, read and clear clipboard content.
6. Window automation – Identify and interact with application windows.
7. Process management – List running processes.
8. Image recognition – Locate visual elements on the screen.
9. Desktop workflow – Combine multiple desktop actions into one workflow.

### Libraries Used

- `pyautogui`
- `pyperclip`
- `pywinauto`
- `psutil`
- `pillow`
- `subprocess`

### Practical Project: Desktop Automation Bot

Created a desktop automation application that can:

- Launch Notepad.
- Launch Calculator.
- Launch Paint.
- Open File Explorer.
- Perform mouse operations.
- Perform keyboard operations.
- Copy and paste clipboard content.
- Capture screenshots.
- List active windows.
- Identify visual elements using image recognition.
- Automate a basic Notepad workflow.

### Expected Output

- Automated desktop interactions.
- Screenshots saved in the Output directory.
- Text files created through automation.
- Application and window information.

**Important Note:** Desktop automation depends on the active Windows session, application state and screen configuration.

**Status:** Testing pending confirmation.

---

## Module 5: Email Automation

### Objective

Automate email creation, sending, reading, searching and attachment handling using Python.

### Topics Covered

1. Email creation.
2. Email simulation.
3. SMTP email sending.
4. IMAP email reading.
5. Email searching.
6. Email filtering.
7. Email attachment handling.
8. Gmail API integration.
9. Microsoft Graph API integration.
10. OAuth 2.0 authentication.

### Libraries and Technologies Used

- `smtplib`
- `imaplib`
- `email`
- `ssl`
- `python-dotenv`
- `google-api-python-client`
- `google-auth-httplib2`
- `google-auth-oauthlib`
- `msal`
- `requests`

### Practical Project: Email Automation Application

Created an email automation application that supports:

- Creating email messages.
- Saving simulated emails as `.eml` files.
- Sending emails through SMTP.
- Reading emails through IMAP.
- Searching emails.
- Filtering unread messages.
- Downloading email attachments.
- Sending emails with attachments.
- Sending emails through Gmail API.
- Reading Gmail inbox through Gmail API.
- Sending and reading Outlook emails through Microsoft Graph API.

### Authentication and Security

- Store credentials in environment variables.
- Use `.env` for local configuration.
- Use OAuth 2.0 for API-based authentication.
- Keep credentials and token files private.
- Never commit credentials, tokens or application secrets to GitHub.

### Expected Output

- Generated `.eml` files.
- Sent emails.
- Retrieved email messages.
- Downloaded attachments.
- Gmail API integration.
- Microsoft Graph API integration.

**Important Note:** Email simulation does not send real emails. Real sending and reading require valid account configuration, network access and appropriate permissions.

**Status:** Setup and testing pending confirmation.

---



# 4. Project Structure

```text
PythonAutomation/
│
├── .venv/
│
├── Day_1/
│   │
│   ├── README.md
│   │
│   ├── File_Automation/
│   │   ├── Input/
│   │   ├── Output/
│   │   ├── Archive/
│   │   ├── file_utils.py
│   │   ├── 01_file_listing.py
│   │   ├── 02_file_creation.py
│   │   ├── 03_file_reading.py
│   │   ├── 04_file_writing.py
│   │   ├── 05_file_copy.py
│   │   ├── 06_file_move.py
│   │   ├── 07_file_rename.py
│   │   ├── 08_file_delete.py
│   │   ├── 09_folder_management.py
│   │   ├── 10_file_metadata.py
│   │   └── 11_file_organizer.py
│   │
│   ├── EXCEL & CSV AUTOMATION/
│   │   ├── Input/
│   │   ├── Output/
│   │   ├── Archive/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── sample_data.py
│   │   ├── excel_reading.py
│   │   ├── excel_writing.py
│   │   ├── worksheet_management.py
│   │   ├── excel_processing.py
│   │   ├── csv_automation.py
│   │   ├── excel_report.py
│   │   └── main.py
│   │
│   ├── PDF_Word_Automation/
│   │   ├── Input/
│   │   ├── Output/
│   │   ├── Archive/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── sample_data.py
│   │   ├── pdf_reading.py
│   │   ├── pdf_creation.py
│   │   ├── pdf_merging.py
│   │   ├── pdf_splitting.py
│   │   ├── pdf_metadata.py
│   │   ├── pdf_table_extraction.py
│   │   ├── pdf_images.py
│   │   ├── pdf_forms.py
│   │   ├── word_creation.py
│   │   ├── word_reading.py
│   │   ├── word_editing.py
│   │   └── main.py
│   │
│   ├── Desktop_Automation/
│   │   ├── Input/
│   │   ├── Output/
│   │   ├── Archive/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── mouse_automation.py
│   │   ├── keyboard_automation.py
│   │   ├── screenshot_automation.py
│   │   ├── application_automation.py
│   │   ├── window_automation.py
│   │   ├── clipboard_automation.py
│   │   ├── image_recognition.py
│   │   ├── desktop_workflow.py
│   │   └── main.py
│   │
│   ├── Email_Automation/
│   │   ├── Input/
│   │   ├── Output/
│   │   ├── Archive/
│   │   ├── __init__.py
│   │   ├── .env
│   │   ├── .gitignore
│   │   ├── config.py
│   │   ├── email_creation.py
│   │   ├── email_sending.py
│   │   ├── email_reading.py
│   │   ├── email_search.py
│   │   ├── email_attachments.py
│   │   ├── email_filtering.py
│   │   ├── email_simulation.py
│   │   ├── email_outlook.py
│   │   ├── email_gmail_api.py
│   │   └── main.py
│   │
│   └
│       
│           
│       
│       
│       
│       
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 5. Installation & Environment Setup

## Python Environment

- Python Version: `3.14.10`
- Virtual Environment: `.venv`
- IDE: Visual Studio Code
- Operating System: Windows

### Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
python -m pip install openpyxl pandas pypdf pdfplumber reportlab pymupdf python-docx pyautogui pyperclip pywinauto psutil pillow python-dotenv google-api-python-client google-auth-httplib2 google-auth-oauthlib msal requests
```

### Save Dependencies

```powershell
python -m pip freeze > requirements.txt
```

---

# 6. Execution Instructions

Run commands from the main `PythonAutomation` project directory.

### File Automation

```powershell
python Day_1/File_Automation/11_file_organizer.py
```

### Excel & CSV Automation

```powershell
python -m "Day_1.EXCEL & CSV AUTOMATION.main"
```

### PDF & Word Automation

```powershell
python -m Day_1.PDF_Word_Automation.main
```

### Desktop Automation

```powershell
python -m Day_1.Desktop_Automation.main
```

### Email Automation

```powershell
python -m Day_1.Email_Automation.main
```

---

# 7. Development Practices

- Each module has separate responsibilities.
- Reusable functions are maintained in separate Python files.
- Main application files provide menu-based execution.
- Input, Output and Archive directories separate source and generated files.
- Environment variables are used for sensitive configuration.
- Error handling is included in automation workflows.
- Logs are generated to understand execution results.
- Dependencies are managed through `requirements.txt`.

---

# 8. Day 1 Learning Outcomes

After completing Day 1, the learner should understand:

1. How Python interacts with files and folders.
2. How to process Excel and CSV data.
3. How to work with PDF and Word documents.
4. How Python interacts with Windows desktop applications.
5. How to automate mouse, keyboard and clipboard operations.
6. How to create and manage emails programmatically.
7. How SMTP, IMAP, Gmail API and Microsoft Graph API work.
8. How to build reusable automation modules.
9. How to combine different Python libraries into one workflow.
10. How to structure a practical Python automation project.

---

