import requests
import zipfile
import os

def download_and_extract_font(url, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    file_name = os.path.join(destination_folder, url.split("/")[-1])
    response = requests.get(url)
    with open(file_name, 'wb') as file:
        file.write(response.content)
    if zipfile.is_zipfile(file_name):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        os.remove(file_name)
    print(f"Font downloaded and extracted to {destination_folder}")

font_urls = [
    "https://example.com/font1.zip",
]

destination_folder = "./hindi"

for font_url in font_urls:
    download_and_extract_font(font_url, destination_folder)
