# End-to-End Data Automation – Python Mini-Project

---

## 1. Overview

This mini-project combines **REST API automation**, **web scraping**, **CSV processing**, **Excel automation**, and **MySQL database operations** in one Python pipeline.

The workflow extracts data from multiple sources, validates records, saves the results to MySQL, and generates database-backed CSV and Excel reports.

---

## 2. Project Objectives

- [x] Extract products from a REST API.
- [x] Scrape books from a multi-page website.
- [x] Create and read CSV employee records.
- [x] Create and read Excel employee records.
- [x] Validate data and remove duplicates within each file source.
- [x] Connect to MySQL and create tables.
- [x] Insert or update extracted records.
- [x] Export cleaned employee records to CSV.
- [x] Generate a three-worksheet Excel report.
- [x] Log execution and handle common errors.
- [x] Execute and verify the integrated pipeline.

---

## 3. Technology Stack

| Technology | Purpose |
| --- | --- |
| Python 3.14.10 | Application logic |
| `requests` | HTTP and REST API requests |
| `beautifulsoup4` | HTML extraction |
| `lxml` | HTML parsing support |
| `mysql-connector-python` | MySQL connection and queries |
| MySQL 8.0 | Data storage |
| `csv` | CSV reading and writing |
| `openpyxl` | Excel reading, writing, and reporting |
| `python-dotenv` | Database configuration |
| `logging` | Execution and error logs |
| `pathlib` | File and folder paths |

---

## 4. Data Sources

### REST API – DummyJSON

**URL:** https://dummyjson.com/

**Extracted product fields:**

- External product ID
- Title
- Category
- Brand
- Price
- Stock
- Rating
- Source

### Website – Books to Scrape

**URL:** https://books.toscrape.com/

**Extracted book fields:**

- Title
- Price
- Currency
- Rating
- Availability
- Product URL
- Source

### CSV and Excel Employee Files

**Employee fields:**

1. Name
2. Email
3. Department
4. Salary

The project creates sample input files and validates their contents before database insertion.

---

## 5. System Architecture

```text
                  INPUT SOURCES
                       |
       +---------------+----------------+
       |               |                |
   DummyJSON       Books Website     CSV / Excel
       |               |                |
       v               v                v
  API Extractor    Web Scraper      File Handlers
       |               |                |
       +---------------+----------------+
                       |
                       v
              DATA VALIDATION
                       |
                       v
               MYSQL DATABASE
                       |
                       v
               DATA RETRIEVAL
                       |
                +------+------+
                |             |
                v             v
             CSV REPORT    EXCEL REPORT
                              |
                    +---------+---------+
                    |         |         |
                 Employees  Department  Import
                            Summary     Summary
```

---

## 6. Project Structure

```text
Database_Automation/
├── config/
│   └── settings.py
├── database/
│   └── connection.py
├── mini_projects/
│   └── end_to_end_data_automation/
│       ├── api/
│       │   ├── __init__.py
│       │   └── api_extractor.py
│       ├── scraping/
│       │   ├── __init__.py
│       │   └── web_scraper.py
│       ├── database/
│       │   ├── __init__.py
│       │   └── data_repository.py
│       ├── files/
│       │   ├── __init__.py
│       │   ├── csv_handler.py
│       │   └── excel_handler.py
│       ├── integration/
│       │   ├── __init__.py
│       │   └── pipeline.py
│       ├── output/
│       │   ├── csv_input/
│       │   ├── csv_output/
│       │   ├── excel_input/
│       │   └── excel_output/
│       ├── logs/
│       ├── config.py
│       ├── main.py
│       ├── requirements.txt
│       └── README.md
└── .env
```

---

## 7. Module Responsibilities

### API Extraction – `api/api_extractor.py`

- Request product data from DummyJSON.
- Handle paginated API responses.
- Clean and validate product records.
- Return structured product data.

### Web Scraping – `scraping/web_scraper.py`

- Request pages from Books to Scrape.
- Parse HTML using BeautifulSoup.
- Extract titles, prices, ratings, availability, and links.
- Follow pagination for a configured number of pages.

### Database Repository – `database/data_repository.py`

- Create or verify database tables.
- Validate records before insertion.
- Save products, books, and employees using parameterized SQL.
- Update existing records using unique keys.
- Retrieve records and display summary counts.

### CSV Handler – `files/csv_handler.py`

- Create sample CSV input.
- Read and validate employee records.
- Filter invalid and duplicate rows.
- Export cleaned records to CSV.

### Excel Handler – `files/excel_handler.py`

- Create sample Excel input.
- Read and validate employee records.
- Filter invalid and duplicate rows.
- Generate a multi-sheet Excel report.

### Integration Pipeline – `integration/pipeline.py`

- Coordinate all data sources.
- Load available records into MySQL.
- Retrieve stored employee data.
- Export CSV and Excel reports.
- Log errors and close database resources.

### Application Entry Point – `main.py`

- Configure application logging.
- Start the integration pipeline.
- Display application execution messages.

---

## 8. Database Design

### `integration_products`

| Column | Description |
| --- | --- |
| `id` | Primary key |
| `external_id` | Unique product ID from the API |
| `title` | Product title |
| `category` | Category |
| `brand` | Brand |
| `price` | Price |
| `stock` | Available stock |
| `rating` | Rating |
| `source` | Data source |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

### `integration_books`

| Column | Description |
| --- | --- |
| `id` | Primary key |
| `title` | Unique book title in this demo schema |
| `price` | Price |
| `currency` | Currency |
| `rating` | Rating |
| `availability` | Availability status |
| `product_url` | Book URL |
| `source` | Data source |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

### `integration_employees`

| Column | Description |
| --- | --- |
| `id` | Primary key |
| `name` | Employee name |
| `email` | Employee email |
| `department` | Department |
| `salary` | Salary |
| `source_file` | `CSV` or `Excel` |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

**Important:** Employee uniqueness uses the combination of `email` and `source_file`. The same email in CSV and Excel can therefore be represented by separate source records.

---

## 9. Installation & Configuration

### Prerequisites

- Python 3.14 or compatible version.
- MySQL Server 8.0.
- Visual Studio Code or another Python editor.
- Working internet connection.
- Existing project virtual environment.

### Step 1: Open the Day 2 Directory

```powershell
cd C:\Users\sagar\Desktop\PythonAutomation\Day_2
```

### Step 2: Activate the Virtual Environment

```powershell
..\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
python -m pip install -r Database_Automation/mini_projects/end_to_end_data_automation/requirements.txt
```

### Step 4: Configure MySQL

The project reuses `Database_Automation/config/settings.py` and `Database_Automation/database/connection.py`.

**Environment file:** `Database_Automation/.env`

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

Replace the placeholders with your local configuration.

**Security:** Never commit `.env` or real credentials to GitHub.

---

## 10. Running the Project

Run these commands from `PythonAutomation/Day_2`.

### Verified Integration Pipeline

```powershell
python -m Database_Automation.mini_projects.end_to_end_data_automation.integration.pipeline
```

### Main Application Entry Point

```powershell
python -m Database_Automation.mini_projects.end_to_end_data_automation.main
```

**Note:** The pipeline command was successfully executed and verified. The `main.py` entry point was created subsequently and should also be tested.

### Execution Flow

1. Load project settings.
2. Fetch products from DummyJSON.
3. Scrape books from Books to Scrape.
4. Create, read, and validate CSV employee input.
5. Create, read, and validate Excel employee input.
6. Connect to MySQL.
7. Create or verify three database tables.
8. Insert or update source records.
9. Retrieve employee records from MySQL.
10. Export cleaned CSV and multi-sheet Excel reports.
11. Display database summary counts.
12. Close database resources.

---

## 11. Generated Outputs

```text
output/
├── csv_input/
│   └── employees.csv
├── csv_output/
│   └── employees_cleaned.csv
├── excel_input/
│   └── employees.xlsx
└── excel_output/
    └── employees_report.xlsx

logs/
├── pipeline.log
└── application.log
```

### CSV Report

**File:** `output/csv_output/employees_cleaned.csv`

Contains cleaned employee records retrieved from MySQL.

### Excel Report

**File:** `output/excel_output/employees_report.xlsx`

**Worksheets:**

1. `Employees` – employee details.
2. `Department Summary` – department-level statistics.
3. `Import Summary` – overall import information.

---

## 12. Verified Execution Results

The integrated pipeline completed successfully during testing.

| Data Source | Records Processed |
| --- | ---: |
| DummyJSON products | 194 |
| Scraped books | 60 |
| Valid CSV employees | 3 |
| Valid Excel employees | 4 |

**MySQL Summary:**

| Table | Stored Records |
| --- | ---: |
| `integration_products` | 194 |
| `integration_books` | 60 |
| `integration_employees` | 7 |
| **Total** | **261** |

**Report Verification:**

- [x] CSV sample input created.
- [x] Excel sample input created.
- [x] MySQL connection established.
- [x] Product records saved.
- [x] Book records saved.
- [x] CSV employee records saved.
- [x] Excel employee records saved.
- [x] Cleaned CSV report generated.
- [x] Three-sheet Excel report generated.
- [x] Database summary displayed.
- [x] Database connection closed.

*Counts from live sources may vary on future runs.*

---

## 13. Validation, Error Handling & Security

- Validate required fields before database insertion.
- Filter invalid employee records.
- Deduplicate CSV and Excel input records.
- Use decimal types for monetary values.
- Use parameterized SQL queries.
- Commit successful database writes and roll back failed operations.
- Catch request and database errors.
- Log pipeline failures for troubleshooting.
- Keep credentials in environment variables.

---

## 14. Limitations

- DummyJSON is a public test API, not a production data source.
- Books to Scrape is a practice website.
- External sources depend on internet and website availability.
- Source counts may change between runs.
- The pipeline does not implement distributed transactions across every source.
- Production-grade monitoring, comprehensive retries, and automated testing are future improvements.

---

## 15. Learning Outcomes

1. Build modular Python automation programs.
2. Integrate REST APIs with pagination.
3. Scrape multi-page websites.
4. Process CSV and Excel records.
5. Validate and deduplicate imported data.
6. Connect to MySQL and perform upsert operations.
7. Generate reports from stored database records.
8. Handle common execution errors and log failures.
9. Coordinate multiple modules in one end-to-end pipeline.

---

## 16. Project Completion Checklist

- [x] API extraction module developed.
- [x] Web scraping module developed.
- [x] CSV handler developed.
- [x] Excel handler developed.
- [x] Database repository developed.
- [x] Integration pipeline developed.
- [x] Complete pipeline successfully executed.
- [x] Database records verified.
- [x] CSV and Excel reports generated.
- [ ] Confirm the separate `main.py` entry point run.

**Project:** End-to-End Data Automation  
**Category:** Python / API / Web Scraping / CSV / Excel / MySQL  
**Status:** Integration pipeline successfully executed and verified.  
**Purpose:** Practical demonstration of multi-source Python data automation.
