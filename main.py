import aiohttp
import asyncio
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
import time
import re
import os

async def fetch_url(session, base_url, url, depth, seen_urls, counter, counter_lock, sitemap_file):
    if url in seen_urls or not url.startswith(base_url) or depth > 10:
        return None

    seen_urls.add(url)

    try:
        async with session.get(url) as response:
            content = await response.text()

            elapsed_time = time.time() - counter['start_time']

            async with counter_lock:
                counter['total'] += 1
                pages_per_minute = counter['total'] / (elapsed_time / 60)

            print(f'{url}: {len(content)} bytes ({depth} depth) - '
                  f'\nTotal Pages: {counter["total"]}\nPages/Minute: {pages_per_minute:.2f}')

            # Write the URL to the sitemap file
            sitemap_file.write(f'<url><loc>{url}</loc></url>\n')

            # Parse content with the updated content_parser function
            links = content_parser(content, base_url)

            # Recursive crawling with the updated start time
            tasks = [
                fetch_url(session, base_url, link, depth + 1, seen_urls, counter, counter_lock, sitemap_file)
                for link in links
            ]
            await asyncio.gather(*tasks)

    except Exception as e:
        print(f'Error fetching {url}: {str(e)}')

    await asyncio.sleep(1)

def content_parser(content, base_url):
    try:
        # Use a regular expression to find all URLs in the content
        urls = re.findall(r'href=["\']((?:https?://|m\.|www\.)[^"\']+?)["\']', content)

        # Filter URLs to include only those under the base_url and exclude those with #
        urls = [urljoin(base_url, url) for url in urls if url.startswith(base_url) and '#' not in url]

        return urls
    except Exception as e:
        print(f'Error parsing content: {str(e)}')
        return []

async def main(start_url):
    base_url = get_base_url(start_url)
    seen_urls = set()
    counter = {'total': 0, 'start_time': time.time()}
    counter_lock = asyncio.Lock()

    # Create the output directory if it doesn't exist
    output_directory = 'output'
    os.makedirs(output_directory, exist_ok=True)

    # Create an XML sitemap file
    sitemap_filename = os.path.join(output_directory, 'sitemap.xml')
    with open(sitemap_filename, 'w') as sitemap_file:
        sitemap_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sitemap_file.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        async with aiohttp.ClientSession() as session:
            await fetch_url(session, base_url, start_url, 1, seen_urls, counter, counter_lock, sitemap_file)

        sitemap_file.write('</urlset>\n')

def get_base_url(url):
    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

if __name__ == '__main__':
    start_url = input("Enter the starting URL (without 'http://'): ")
    asyncio.run(main(f'https://{start_url}'))
