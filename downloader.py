import os
import requests
import time
import logging
import hashlib
from tqdm import tqdm
from requests.exceptions import RequestException, Timeout
from time import sleep
import argparse
import threading

logging.basicConfig(filename="download_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(message)s")


def download_file(url, filename, output_dir, retries=3):
    try:
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, filename) if output_dir else filename

        if os.path.exists(file_path):
            print(f"{filename} already exists in {output_dir or 'the current directory'}.")
            return

        response = requests.head(url)
        response.raise_for_status()
        file_size = int(response.headers.get('Content-Length', 0))

        with tqdm(total=file_size, unit="B", unit_scale=True, desc="Downloading") as download_bar:
            try:
                with requests.get(url, stream=True, timeout=30) as response:
                    response.raise_for_status()
                    with open(file_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                            download_bar.update(len(chunk))

                logging.info(f"File successfully downloaded: {file_path}")
                print(f"File successfully downloaded and saved as {file_path}")
            except (RequestException, Timeout) as e:
                logging.error(f"Error downloading the file: {e}")
                handle_error(url, file_path, retries)

        if response.headers.get('X-Checksum-SHA256'):
            server_hash = response.headers['X-Checksum-SHA256']
            downloaded_hash = compute_hash(file_path)
            if server_hash != downloaded_hash:
                logging.error(f"Hash mismatch: {file_path}")
                raise ValueError("Downloaded file hash does not match the expected hash.")

    except RequestException as e:
        print(f"Error: {e}")
        logging.error(f"Error during download: {e}")
        handle_error(url, file_path, retries)
    except Timeout as e:
        print(f"Timeout Error: {e}")
        logging.error(f"Timeout during download: {e}")
        handle_error(url, file_path, retries)


def compute_hash(filename):
    hash_sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def handle_error(url, filename, retries):
    if retries <= 0:
        print("Maximum retries reached. Exiting.")
        logging.error(f"Maximum retries reached for {url}")
        exit()

    print("\nDownload interrupted or failed.")
    choice = input("Retry (r) or exit (e): ").lower()

    if choice == 'r':
        print("Retrying download...")
        download_file(url, filename, retries=retries-1)
    elif choice == 'e':
        print("Exiting download.")
        logging.info(f"Download exited by user: {url}")
        exit()
    else:
        print("Invalid choice. Exiting.")
        logging.info(f"Download exited due to invalid choice: {url}")
        exit()


def download_file_parallel(url, filename, output_dir, retries=3):
    download_file(url, filename, output_dir, retries)


def download_files_parallel(urls, filenames, output_dir, retries=3, parallel=2):
    threads = []
    for i in range(len(urls)):  # FIXED
        thread = threading.Thread(target=download_file_parallel, args=(urls[i], filenames[i], output_dir, retries))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a file with progress tracking and error handling.")
    parser.add_argument("urls", help="Comma-separated list of URLs of the files to download")
    parser.add_argument("filenames", help="Comma-separated list of filenames to save the downloaded files")
    parser.add_argument("--retries", type=int, default=3, help="Number of retry attempts on failure")
    parser.add_argument("--output", type=str, default="", help="Directory to download the file into")
    parser.add_argument("--parallel", type=int, default=2, help="Number of parallel downloads")

    args = parser.parse_args()
    
    urls = args.urls.split(",")
    filenames = args.filenames.split(",")
    
    if len(urls) != len(filenames):
        print("The number of URLs must match the number of filenames.")
        exit()
    
    download_files_parallel(urls, filenames, args.output, retries=args.retries, parallel=args.parallel)
