import requests
import json

BASE_URL = "http://127.0.0.1:5011"  

def upload_file(file_path):
    url = f"{BASE_URL}/upload"
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'action': 'upload'}
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print("Upload successful:", response.json())
    else:
        print("Failed to upload file:", response.text)

def download_file(file_name):
    url = f"{BASE_URL}/download"
    data = {'action': 'download', 'file_name': file_name}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Download successful:", response.json())
    else:
        print("Failed to download file:", response.text)

if __name__ == "__main__":
    # Example usage:
    upload_file("C:\\Users\\Sonam\\Desktop\\text.txt")
    #download_file("text.txt")
