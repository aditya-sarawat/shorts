import requests
import zipfile
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_FONTS_API_KEY')
OUTPUT_DIRECTORY = "./fonts/english/"


def download_and_extract_font(url, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    file_name = os.path.join(destination_folder, url.split("/")[-1])

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading font: {e}")
        return

    with open(file_name, "wb") as file:
        file.write(response.content)

    if zipfile.is_zipfile(file_name):
        with zipfile.ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall(destination_folder)
        os.remove(file_name)
        print(f"Font downloaded and extracted to {destination_folder}")
    else:
        print(f"Error: Downloaded file is not a valid ZIP archive.")


def list_all_fonts(fonts):
    for i, font in enumerate(fonts, start=1):
        print(f"{i}. {font['family']}")


def search_and_download_fonts_by_list(selected_ids, output_directory, fonts):
    try:
        selected_ids = [int(x) for x in selected_ids.split(",")]
        selected_fonts = [fonts[i - 1] for i in selected_ids]
    except (ValueError, IndexError):
        print("Invalid input. Please enter valid font IDs separated by commas.")
        return

    for font in selected_fonts:
        font_name = font["family"]

        if any(style.lower() == "regular" for style in font.get("variants", [])):
            files = {
                file_type: file_url
                for file_type, file_url in font["files"].items()
                if file_type.endswith("regular")
            }

            for file_type, file_url in files.items():
                download_and_extract_font(file_url, output_directory)

            print(
                f"Font '{font_name}' (regular style) downloaded and extracted to '{output_directory}'."
            )
        else:
            print(f"Font '{font_name}' does not have a 'regular' style.")


def search_and_download_fonts_by_name(font_name, output_directory, fonts):
    api_endpoint = f"https://www.googleapis.com/webfonts/v1/webfonts"

    params = {"key": API_KEY, "family": font_name}

    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving font information: {e}")
        return

    if response.status_code == 200:
        font_info = response.json()
        if "items" in font_info and len(font_info["items"]) > 0:
            selected_font = font_info["items"][0]["files"]["regular"]
            print(selected_font)
            download_and_extract_font(selected_font, output_directory)
        else:
            print(f"Font '{font_name}' not found.")
    else:
        print(f"Error retrieving font information for '{font_name}'.")


def get_all_fonts():
    api_endpoint = (
        f"https://www.googleapis.com/webfonts/v1/webfonts?key={API_KEY}&sort=trending"
    )
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving font information: {e}")
        return []

    if response.status_code == 200:
        font_info = response.json()
        return font_info.get("items", [])
    else:
        print(f"Error retrieving font information. Status code: {response.status_code}")
        return []


def print_menu():
    print("\nMenu:")
    print("1. Download fonts using the list")
    print("2. Download font by name")
    print("3. Exit")


def main():
    all_fonts = get_all_fonts()

    while True:
        print_menu()
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            list_all_fonts(all_fonts)
            selected_font_ids = input("Enter font IDs separated by commas: ")
            search_and_download_fonts_by_list(
                selected_font_ids, OUTPUT_DIRECTORY, all_fonts
            )
        elif choice == "2":
            font_name = input("Enter the font name: ")
            search_and_download_fonts_by_name(font_name, OUTPUT_DIRECTORY, all_fonts)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
