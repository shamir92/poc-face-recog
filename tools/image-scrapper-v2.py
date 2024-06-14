import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def fetch_image_urls(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    images = []
    # Target specific image tags within the gallery
    gallery_section = soup.find('ul', {'class': 'splide__list'})
    if gallery_section:
        img_tags = gallery_section.find_all('img')
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                # Ensure the URL is complete
                if img_url.startswith('/'):
                    img_url = "https://www.obamalibrary.gov" + img_url
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
                filename = f"image_{timestamp}_{i+1}.jpg"
                with open(os.path.join(folder_path, filename), "wb") as file:
                    file.write(response.content)
                print(f"Downloaded image {i+1} as {filename}")
            else:
                print(f"Failed to download image {i+1} (status code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")

# Configuration
url = "https://www.obamalibrary.gov/galleries/obama-family"
headers = {"User-Agent": "Mozilla/5.0"}
folder_path = "../input/barrack_family/family"

# Fetch image URLs
image_urls = fetch_image_urls(url, headers)

# Download images
download_images(image_urls, folder_path)

# Print JSON output
json_output = {"images": image_urls}
print(json_output)
