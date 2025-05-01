# BookScraper

This project scrapes book data from [books.tobscraped.com](https://books.tobscraped.com) and stores the relevant information into a MySQL database. The data is collected and processed through Scrapy, then refactored and stored in a MySQL server for easy querying and analysis.

## Features

- Scrapes book details from a specified website.
- Uses Scrapy for web scraping and MySQL for data storage.
- Integrates with ScrapeOps Fake User-Agent API for rotating user agents, improving request anonymity and reducing blocks.
- The database credentials are securely handled using environment variables stored in a `.env` file.
- Data includes information like book title, URL, price, category, reviews, and more.

## Installation

### Prerequisites
- Python 3.12+
- MySQL Server 8.0+
- Git

### Step-by-Step Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/book-scraper.git
cd book-scraper
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure MySQL**:
```sql
-- Run in MySQL shell:
CREATE DATABASE bookscraper;
CREATE USER 'scraper'@'localhost' IDENTIFIED BY 'securepassword123';
GRANT ALL PRIVILEGES ON bookscraper.* TO 'scraper'@'localhost';
FLUSH PRIVILEGES;
```

5. **Set up environment variables**:
```bash
echo "MYSQL_USER=scraper" > .env
echo "MYSQL_PASSWORD=securepassword123" >> .env
echo "MYSQL_DATABASE=bookscraper" >> .env
echo "MYSQL_HOST=localhost" >> .env
echo ".env" >> .gitignore
```
## Usage

### Running the Scraper
```bash
# Start the spider (from project root directory)
scrapy crawl bookscraper

# To save output to JSON (optional):
scrapy crawl bookscraper -o books.json
```

### Checking the Database
```sql
-- Connect to MySQL:
mysql -u scraper -p

-- Then query your data:
USE bookscraper;
SELECT title, price FROM books LIMIT 10;
```

## Project Structure
```
bookscraper/
├── spiders/
│   ├── __init__.py
│   └── bookscraper.py         # Main spider implementation
├── items.py                   # Data container definitions
├── middlewares.py             # Optional middleware
├── pipelines.py               # MySQL storage pipeline
├── settings.py                # Project settings
├── requirements.txt           # Dependencies
scrapy.cfg                     # Scrapy config
```

## Troubleshooting

### Common Issues
1. **MySQL Connection Errors**:
   ```bash
   # Verify MySQL is running:
   sudo systemctl status mysql  # Linux
   # or
   mysqladmin -u root -p status
   ```

2. **Missing Dependencies**:
   ```bash
   # Reinstall requirements if needed:
   pip install --force-reinstall -r requirements.txt
   ```

3. **Environment Variables Not Loading**:
   ```bash
   # Manually test env variables:
   python -c "import os; print(os.environ.get('MYSQL_USER'))"
   ```

## License
MIT License - See [LICENSE](LICENSE) file for details.


