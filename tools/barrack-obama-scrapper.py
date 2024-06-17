import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def fetch_image_urls(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    images = []
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url and "http" in img_url:
            images.append(img_url)

    return images

def download_images(image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(os.path.join(folder_path, f"image_{i+1}{timestamp}.jpg"), "wb") as file:
                    file.write(response.content)
                print(f"Downloaded image {i+1}")
            else:
                print(f"Failed to download image {i+1} (status code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")

# Configuration
url = "https://www.bing.com/images/search?q=get+biden+image&form=HDRSC3&first=1"
headers = {"User-Agent": "Mozilla/5.0"}
folder_path = "../input/biden"

# Fetch image URLs
image_urls = fetch_image_urls(url, headers)

# Download images
download_images(image_urls, folder_path)

# Print JSON output
json_output = {"images": image_urls}
print(json_output)
