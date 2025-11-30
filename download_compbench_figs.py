import os
import requests
from bs4 import BeautifulSoup

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

def get_figures():
    url = "https://arxiv.org/html/2307.06350"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print("Failed to fetch HTML")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Figure 3
        # Look for id="S3.F3" or caption containing "Figure 3"
        fig3_url = None
        fig3 = soup.find(id="S3.F3")
        if not fig3:
            # Fallback search by caption
            for fig in soup.find_all('figure'):
                caption = fig.find('figcaption')
                if caption and "Figure 3" in caption.get_text():
                    fig3 = fig
                    break
        
        if fig3:
            img = fig3.find('img')
            if img:
                fig3_url = img.get('src')

        # Table 1
        # Look for id="S3.T1" or caption containing "Table 1"
        tab1_url = None
        tab1 = soup.find(id="S3.T1") # Tables in arXiv HTML are often images or HTML tables. 
        # If it's an HTML table, we can't easily screenshot it without a browser.
        # But often complex tables are images. Let's check.
        if not tab1:
             for fig in soup.find_all('figure'): # Tables are often wrapped in figure tags in arXiv HTML
                caption = fig.find('figcaption')
                if caption and "Table 1" in caption.get_text():
                    tab1 = fig
                    break
        
        if tab1:
            img = tab1.find('img')
            if img:
                tab1_url = img.get('src')
            else:
                print("Table 1 might be an HTML table, not an image.")

        # Download
        if fig3_url:
            if not fig3_url.startswith('http'):
                fig3_url = f"https://arxiv.org/html/2307.06350/{fig3_url}"
            download_image(fig3_url, "images/36.png") # Main image for card
            download_image(fig3_url, "images/36_fig3.png")

        if tab1_url:
            if not tab1_url.startswith('http'):
                tab1_url = f"https://arxiv.org/html/2307.06350/{tab1_url}"
            download_image(tab1_url, "images/36_tab1.png")

    except Exception as e:
        print(f"Error: {e}")

get_figures()
