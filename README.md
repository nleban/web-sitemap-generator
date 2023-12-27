# Web Sitemap Generator

A Python asyncio-based web sitemap generator that crawls a website, extracts URLs, and generates an XML sitemap. The script uses the `aiohttp` library for asynchronous web requests, `BeautifulSoup` for HTML parsing, and regular expressions for URL extraction.

## Features

- **Asynchronous Crawling:** Utilizes `asyncio` and `aiohttp` for efficient, non-blocking web crawling.
- **Depth-Limited Crawling:** Limits the depth of crawling to prevent exhaustive exploration.
- **XML Sitemap Generation:** Generates an XML sitemap (`sitemap.xml`) conforming to the sitemaps.org protocol.
- **Error Handling:** Handles errors gracefully, logging encountered issues during the crawling process.

## Usage

1. **Installation:**
   - Install the required dependencies using:
     ```bash
     pip install aiohttp beautifulsoup4
     ```

2. **Run the Script:**
   - Execute the script by providing the starting URL when prompted:
     ```bash
     python script_name.py
     ```
     Replace `script_name.py` with the actual name of your Python script.

3. **Output:**
   - The script creates an `output` directory (if not exists) and generates a sitemap file (`sitemap.xml`) containing discovered URLs.

## Code Overview

- **`fetch_url` Function:** Asynchronously fetches a URL, extracts content, logs information, and writes the URL to the sitemap file.
- **`content_parser` Function:** Parses content using regular expressions to extract valid URLs under the specified base URL.
- **`main` Function:** Orchestrates the crawling process, initializes counters, and manages the overall flow.
- **`get_base_url` Function:** Extracts the base URL from a given URL.

## Requirements

- Python 3.7+
- `aiohttp` library
- `BeautifulSoup` library

## Notes

- Adjust the depth limit in the script based on your requirements.
- Ensure proper permissions for creating the output directory and writing to the sitemap file.

Feel free to customize the script according to your needs and explore additional enhancements. **Happy crawling!**