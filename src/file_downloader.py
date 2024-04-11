import requests
import zipfile


class EpwFileDownloader:
    @staticmethod
    def download_epw_file(url: str, save_path: str) -> None:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)


class ZipFileExtractor:
    @staticmethod
    def extract_zip_file(zip_path: str, extract_to: str) -> None:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)




