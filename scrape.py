import os
import requests
import time

# Complete dataset of T2I Benchmarks (2022-2025)
# Sourced from the literature review app
benchmarks = [
    # 2024 Papers
    {"year": 2024, "name": "HRS-Bench", "url": "https://arxiv.org/abs/2304.05390"},
    {"year": 2024, "name": "RichHF-18K", "url": "https://arxiv.org/abs/2312.10240"},
    {"year": 2024, "name": "SafetyBench-T2I", "url": "https://arxiv.org/abs/2501.12612"},
    {"year": 2024, "name": "DesignBench", "url": "https://arxiv.org/abs/2310.15144"},
    {"year": 2024, "name": "GeomVerse", "url": "https://arxiv.org/abs/2312.12241"},
    {"year": 2024, "name": "VQAScore", "url": "https://arxiv.org/abs/2404.01291"},
    {"year": 2024, "name": "T2I-CompBench_PlusPlus", "url": "https://arxiv.org/abs/2307.06350"}, # ++ version often hosted on original link

    # 2025 Papers
    {"year": 2025, "name": "Logic-T2I", "url": "https://arxiv.org/abs/2510.00796"},
    {"year": 2025, "name": "Culture-Bench", "url": "https://arxiv.org/abs/2411.13962"},
    {"year": 2025, "name": "Phys-T2I", "url": "https://arxiv.org/abs/2406.11802"},
    {"year": 2025, "name": "Consistency-Story", "url": "https://arxiv.org/abs/2407.08683"},
    {"year": 2025, "name": "TIFF_Bench", "url": "https://arxiv.org/abs/2506.02161"},
    
    # Non-PDF / Website Links (Will be skipped or logged)
    {"year": 2025, "name": "Fine_Grain", "url": "https://finegrainbench.ai/"},
]

def get_pdf_url(original_url):
    """
    Converts an arXiv abstract URL to a direct PDF URL.
    Returns None if it's not a convertible arXiv link.
    """
    if "arxiv.org/abs/" in original_url:
        return original_url.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"
    elif "arxiv.org/pdf/" in original_url:
        return original_url
    elif original_url.endswith(".pdf"):
        return original_url
    return None

def download_file(url, filename, folder="papers"):
    """Downloads a file from a URL to a specific folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, filename)
    
    # Check if file already exists to avoid redownloading
    if os.path.exists(filepath):
        print(f"✅ [Exists] {filename}")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        print(f"⬇️  [Downloading] {filename}...")
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✨ [Saved] {filename}")
        
        # Be polite to servers
        time.sleep(1) 
        
    except Exception as e:
        print(f"❌ [Error] Could not download {filename}: {e}")

def main():
    print("--- Starting Paper Scraper (2024-2025) ---")
    
    for paper in benchmarks:
        # Filter for years 2024 and 2025
        if paper["year"] in [2024, 2025]:
            
            pdf_url = get_pdf_url(paper["url"])
            
            if pdf_url:
                # Sanitize filename
                safe_name = paper["name"].replace(" ", "_").replace("/", "-")
                filename = f"{paper['year']}_{safe_name}.pdf"
                download_file(pdf_url, filename)
            else:
                print(f"⚠️  [Skipped] {paper['name']} (URL is not a direct PDF/ArXiv link): {paper['url']}")

    print("\n--- Download Complete check the 'papers' folder ---")

if __name__ == "__main__":
    main()