# Day 2 – Python Web, API & Database Automation

---

## 1. Overview

Day 2 focuses on **Web Automation**, **Web Scraping**, **REST API Automation**, and **MySQL Database Automation** using Python.

The goal is to build reusable modules, understand how external systems exchange data, and integrate multiple data sources into one working automation pipeline.

---

## 2. Learning Objectives

- [x] Learn browser automation fundamentals with Selenium.
- [x] Learn web scraping fundamentals with Requests and BeautifulSoup.
- [x] Practice REST API methods, JSON responses, and pagination.
- [x] Connect Python to MySQL and perform database operations.
- [x] Integrate CSV and Excel data with MySQL.
- [x] Build and execute an end-to-end data automation mini-project.
- [ ] Finish advanced browser automation and scraping topics.
- [ ] Finish advanced API integration topics.
- [ ] Verify all remaining database exercises.
- [ ] Complete database backup and restore practicals.

---

## 3. Day 2 Modules

### Module 1: Web Automation

**Objective:** Automate browser navigation and user interactions using Python.

**Topics Covered:**

1. Selenium and browser setup.
2. Opening websites and navigating pages.
3. Locating elements using ID, name, XPath, and CSS selectors.
4. Clicking buttons, typing into fields, and submitting forms.
5. Handling dropdowns, checkboxes, and dynamic elements.
6. Explicit waits, browser sessions, and screenshots.
7. Basic exception handling for browser workflows.

**Libraries Used:**

- `selenium`
- Python standard library

**Practical Work:** Browser interaction and basic web workflow exercises.

**Status:** Fundamentals covered; advanced topics and final verification pending.

---

### Module 2: Web Scraping

**Objective:** Extract and process structured information from websites.

**Topics Covered:**

1. HTTP GET requests and status codes.
2. HTML structure and parsing.
3. Finding elements with BeautifulSoup.
4. Extracting text, links, prices, and other attributes.
5. Multi-page scraping and pagination.
6. Cleaning and validating extracted records.
7. Handling network errors and request timeouts.
8. Preparing data for CSV or database storage.

**Libraries Used:**

- `requests`
- `beautifulsoup4`
- `lxml`
- `csv`

**Practical Work:** Scraped book information from [Books to Scrape](https://books.toscrape.com/) as part of the integrated project.

**Status:** Fundamentals covered; advanced topics pending.

---

### Module 3: API Automation

**Objective:** Automate HTTP communication with REST APIs and process JSON data.

**Topics Covered:**

1. REST API and HTTP fundamentals.
2. `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` requests.
3. Request headers, query parameters, and JSON payloads.
4. Response status codes and error handling.
5. Authentication concepts and API sessions.
6. Pagination, filtering, sorting, and searching.
7. Timeouts, retries, and rate limiting.
8. File uploads and downloads.

**Libraries Used:**

- `requests`
- `json`
- `pathlib`
- `python-dotenv`

**Practical Work:** Used [DummyJSON](https://dummyjson.com/) for API exercises and product extraction.

**Important Note:** DummyJSON write operations are simulated and do not permanently save changes. Microsoft Entra OAuth 2.0 integration and other advanced topics remain pending.

**Status:** Core topics covered; advanced topics pending.

---

### Module 4: Database Automation

**Objective:** Use Python to connect to MySQL, process data, and automate reporting.

**Topics Covered:**

1. MySQL connection and configuration.
2. Creating databases and tables.
3. CRUD operations: `INSERT`, `SELECT`, `UPDATE`, `DELETE`.
4. SQL joins, grouping, sorting, and filtering.
5. Transactions, commit, rollback, and bulk operations.
6. CSV and Excel database integration.
7. Parameterized queries and input validation.
8. Indexes, query plans, and performance concepts.
9. Health checks, audit logs, and incremental synchronization.
10. Schema version management.
11. Backup and restore concepts.
12. Integration of multiple data sources.

**Libraries Used:**

- `mysql-connector-python`
- `openpyxl`
- `csv`
- `python-dotenv`
- `logging`
- `decimal`

**Module Progress:**

| Database Module | Status |
| --- | --- |
| 1. Connection and Setup | Completed and verified |
| 2. CRUD Operations | Completed and verified |
| 3. Advanced SQL | Code prepared; execution confirmation pending |
| 4. Transactions and Bulk Operations | Code prepared; execution confirmation pending |
| 5. CSV and Excel Integration | Completed |
| 6. SQLAlchemy and Pandas | Blocked by Windows Application Control |
| 7. Security and Performance | Completed and verified |
| 8. Advanced Database Automation | Mostly verified; backup/restore pending |
| 9. Integration Mini-Project | Pipeline executed successfully |

**Important Note:** The environment blocks compiled components needed by Pandas and SQLAlchemy. The working project uses `csv` and `openpyxl` instead. Do not bypass organizational Windows security restrictions.

---

## 4. Integrated Mini-Project

### End-to-End Data Automation

**Objective:** Combine API extraction, web scraping, CSV, Excel, and MySQL in a single workflow.

**Data Sources:**

1. DummyJSON REST API – products.
2. Books to Scrape – books.
3. CSV input – employee records.
4. Excel input – employee records.

**Architecture:**

```text
DummyJSON API -----------+
                         |
Books to Scrape ---------+--> Extract --> Validate --> MySQL
                         |                            |
CSV Employee File -------+                            +--> CSV Report
                         |                            |
Excel Employee File -----+                            +--> Excel Report
```

**Completed Work:**

- [x] API product extraction and pagination.
- [x] Multi-page book scraping.
- [x] CSV employee validation and deduplication.
- [x] Excel employee validation and deduplication.
- [x] MySQL table creation and data loading.
- [x] Parameterized SQL upsert operations.
- [x] CSV report export.
- [x] Multi-sheet Excel report export.
- [x] Final database summary verification.

**Verified Pipeline Results:**

| Source or Database Table | Records |
| --- | ---: |
| API products | 194 |
| Scraped books | 60 |
| CSV employee input | 3 |
| Excel employee input | 4 |
| `integration_products` | 194 |
| `integration_books` | 60 |
| `integration_employees` | 7 |
| **Total records stored in MySQL** | **261** |

*The API and website counts may change on future runs.*

**Detailed Documentation:** See `Database_Automation/mini_projects/end_to_end_data_automation/README.md`.

---

## 5. Project Structure

```text
PythonAutomation/
├── .venv/
├── Day_1/
│   └── README.md
├── Day_2/
│   ├── README.md
│   ├── Web_Automation/
│   ├── Web_Scraping/
│   ├── API_Automation/
│   └── Database_Automation/
│       ├── config/
│       │   └── settings.py
│       ├── database/
│       │   └── connection.py
│       ├── exercises/
│       ├── utils/
│       ├── output/
│       ├── logs/
│       ├── mini_projects/
│       │   └── end_to_end_data_automation/
│       │       ├── api/
│       │       ├── scraping/
│       │       ├── database/
│       │       ├── files/
│       │       ├── integration/
│       │       ├── output/
│       │       ├── logs/
│       │       ├── config.py
│       │       ├── main.py
│       │       ├── requirements.txt
│       │       └── README.md
│       ├── .env
│       ├── .gitignore
│       ├── requirements.txt
│       └── main.py
├── README.md
└── .gitignore
```

*The tree highlights the main module folders and the verified mini-project structure; individual exercise files are omitted for readability.*

---

## 6. Installation & Environment Setup

**Development Environment:**

- **Operating System:** Windows
- **IDE:** Visual Studio Code
- **Python:** 3.14.10
- **Virtual Environment:** `.venv`
- **Database:** MySQL 8.0

### Activate the Virtual Environment

From the `PythonAutomation/Day_2` directory:

```powershell
..\.venv\Scripts\Activate.ps1
```

### Install Mini-Project Dependencies

```powershell
python -m pip install -r Database_Automation/mini_projects/end_to_end_data_automation/requirements.txt
```

### Database Configuration

The shared database settings are read from `Database_Automation/.env`.

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

**Security:** Never commit `.env`, passwords, tokens, or other secrets to Git.

---

## 7. Execution Instructions

Run the commands below from the `PythonAutomation/Day_2` directory.

### Run the Verified Mini-Project Pipeline

```powershell
python -m Database_Automation.mini_projects.end_to_end_data_automation.integration.pipeline
```

### Run the Mini-Project Main Entry Point

```powershell
python -m Database_Automation.mini_projects.end_to_end_data_automation.main
```

### Run the Shared Database Entry Point

```powershell
python -m Database_Automation.main
```

**Note:** The mini-project pipeline was successfully tested. The main entry point was created afterward and should be verified separately. Other web/API modules have their own exercises; use their actual filenames rather than assuming an entry point exists.

---

## 8. Development Practices

- Separate modules by responsibility.
- Use reusable Python functions.
- Keep configuration and credentials separate from application logic.
- Use parameterized SQL for database operations.
- Validate and deduplicate imported data.
- Handle network and database errors.
- Write logs for troubleshooting.
- Organize input, output, and report files into dedicated folders.
- Track source code using Git and meaningful commit messages.

---

## 9. Day 2 Learning Outcomes

After completing the covered work, the learner can:

1. Automate browser interactions with Selenium.
2. Extract website data using Requests and BeautifulSoup.
3. Communicate with REST APIs and process JSON responses.
4. Use API pagination and error handling.
5. Connect Python applications to MySQL.
6. Execute SQL queries and manage transactions.
7. Import and export CSV and Excel records.
8. Validate and deduplicate data.
9. Generate database-backed reports.
10. Integrate several Python automation modules into one workflow.

---

## 10. Overall Progress

| Module | Status |
| --- | --- |
| Web Automation | Fundamentals covered |
| Web Scraping | Fundamentals covered |
| API Automation | Core topics covered |
| Database Automation | Core and several advanced topics covered; remaining items pending |
| End-to-End Data Automation Mini-Project | Pipeline successfully executed |

**Project:** Python Automation – Day 2  
**Category:** Web Automation / Web Scraping / API Automation / Database Automation  
**Status:** Core learning and integrated mini-project pipeline completed; 
