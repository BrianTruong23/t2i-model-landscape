import os
import re
import requests
from bs4 import BeautifulSoup
import time

# Benchmark data extracted from index.html
benchmarks = [
    {"id": 1, "link": "https://arxiv.org/abs/2205.11487"},
    {"id": 2, "link": "https://arxiv.org/abs/2206.10789"},
    {"id": 3, "link": "https://arxiv.org/abs/2204.03162"},
    {"id": 4, "link": "https://arxiv.org/abs/2307.06350"},
    {"id": 5, "link": "https://arxiv.org/abs/2303.11897"},
    {"id": 6, "link": "https://arxiv.org/abs/2311.04287"},
    {"id": 7, "link": "https://arxiv.org/abs/2305.01749"},
    {"id": 8, "link": "https://arxiv.org/abs/2304.05977"},
    {"id": 9, "link": "https://arxiv.org/abs/2310.11513"},
    # {"id": 10, "link": "https://cdn.openai.com/papers/dall-e-3.pdf"}, # PDF, skip for now
    {"id": 11, "link": "https://arxiv.org/abs/2304.05390"},
    {"id": 12, "link": "https://arxiv.org/abs/2312.10240"},
    {"id": 13, "link": "https://arxiv.org/abs/2501.12612"},
    {"id": 14, "link": "https://arxiv.org/abs/2310.15144"},
    {"id": 15, "link": "https://arxiv.org/abs/2312.12241"},
    {"id": 16, "link": "https://arxiv.org/abs/2404.01291"},
    {"id": 17, "link": "https://arxiv.org/abs/2406.13743"},
    {"id": 18, "link": "https://arxiv.org/abs/2403.05135"},
    {"id": 19, "link": "https://arxiv.org/abs/2408.14339"},
    {"id": 20, "link": "https://arxiv.org/abs/2406.07546"},
    {"id": 21, "link": "https://arxiv.org/abs/2406.11802"},
    {"id": 22, "link": "https://arxiv.org/abs/2407.06863"},
    {"id": 23, "link": "https://arxiv.org/abs/2510.00796"},
    {"id": 24, "link": "https://arxiv.org/abs/2407.08683"},
    {"id": 25, "link": "https://arxiv.org/abs/2506.02161"},
    # {"id": 26, "link": "https://finegrainbench.ai/"}, # Not arXiv
    {"id": 27, "link": "https://arxiv.org/abs/2506.02161"},
    {"id": 28, "link": "https://arxiv.org/abs/2505.24787"},
    {"id": 29, "link": "https://arxiv.org/abs/2509.09680"},
    {"id": 30, "link": "https://arxiv.org/abs/2510.18701"},
    {"id": 31, "link": "https://arxiv.org/abs/2503.07265"},
    {"id": 32, "link": "https://arxiv.org/abs/2508.17472"},
    {"id": 33, "link": "https://arxiv.org/abs/2505.23493"},
    {"id": 34, "link": "https://arxiv.org/abs/2506.07977"},
    {"id": 35, "link": "https://arxiv.org/abs/2509.03516"},
]

os.makedirs("images", exist_ok=True)

def download_image(url, filename):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def process_arxiv(b):
    arxiv_id = b['link'].split('/')[-1]
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    
    print(f"Processing {b['id']}: {html_url}")
    
    try:
        response = requests.get(html_url, timeout=15)
        if response.status_code != 200:
            print(f"Failed to fetch HTML for {b['id']}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Strategy: Look for <figure> tags
        figures = soup.find_all('figure')
        target_img_url = None
        
        # Prioritize figures with "framework", "overview", "pipeline" in caption
        for fig in figures:
            caption = fig.find('figcaption')
            if caption:
                text = caption.get_text().lower()
                if any(k in text for k in ['framework', 'overview', 'pipeline', 'architecture']):
                    img = fig.find('img')
                    if img and img.get('src'):
                        target_img_url = img['src']
                        break
        
        # Fallback: First figure
        if not target_img_url and figures:
            img = figures[0].find('img')
            if img and img.get('src'):
                target_img_url = img['src']

        if target_img_url:
            # Handle relative URLs
            if not target_img_url.startswith('http'):
                target_img_url = f"https://arxiv.org/html/{arxiv_id}/{target_img_url}"
            
            download_image(target_img_url, f"images/{b['id']}.png")
        else:
            print(f"No suitable figure found for {b['id']}")

    except Exception as e:
        print(f"Error processing {b['id']}: {e}")

for b in benchmarks:
    if "arxiv.org" in b['link']:
        process_arxiv(b)
        time.sleep(1) # Be nice to arXiv
    else:
        print(f"Skipping non-arXiv: {b['link']}")
