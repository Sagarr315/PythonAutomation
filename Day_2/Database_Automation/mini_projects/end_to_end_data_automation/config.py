
from pathlib import Path

# Mini-project root directory
PROJECT_ROOT = Path(__file__).resolve().parent

# Output and logging directories
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

# Create directories automatically
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# API configuration
API_BASE_URL = "https://dummyjson.com"

# Website configuration
SCRAPING_BASE_URL = "https://books.toscrape.com/"

# API settings
REQUEST_TIMEOUT = 30

# Database configuration
# Reuse the existing Database_Automation connection module.
DATABASE_PROJECT_ROOT = PROJECT_ROOT.parents[1]

print("Project configuration loaded!")
print("Project root:", PROJECT_ROOT)
print("Output directory:", OUTPUT_DIR)
print("Logs directory:", LOG_DIR)
