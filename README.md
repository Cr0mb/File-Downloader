# File Downloader with Parallel Support

This script allows you to download files from given URLs with progress tracking, error handling, and retry capabilities. You can also download multiple files in parallel, making it more efficient for large sets of downloads.

## Features

- **File Downloading**: Downloads files with progress shown using `tqdm` for a better user experience.
- **Error Handling**: Handles HTTP request errors (timeouts, server errors) and gives the user an option to retry or exit the download process.
- **Hash Verification**: Ensures that the downloaded file matches the expected SHA256 hash (if provided by the server).
- **Parallel Downloads**: Supports downloading multiple files simultaneously with configurable parallelism to speed up large batch downloads.
- **Logging**: Keeps a log of the download process in a `download_log.txt` file.
- **Command-Line Interface**: Easily configurable via command-line arguments.

## Requirements

- Python 3.x
- `requests` library
- `tqdm` library

You can install the required libraries using `pip`:

```bash
pip install requests tqdm
```

## Usage

### Command-Line Arguments

- `urls`: Comma-separated list of file URLs to download
- `filenames`: Comma-separated list of filenames to save the downloaded files
- `--retries`: Number of retry attempts on failure (default: 3).
- `--output`: Directory to download the files into (default: current directory).
- `--parallel`: Number of parallel downloads (default: 2).

![image](https://github.com/user-attachments/assets/e4676eef-ea78-4f59-abc6-093d166b3670)


## Example Command
To download files in parallel:
```
python downloader.py "http://example.com/file1.zip,http://example.com/file2.zip" "file1.zip,file2.zip" --output "./downloads" --retries 5 --parallel 4
```

## Error Handling
If a download fails (due to network issues, timeouts, etc.), the script will:

1. Log the error.
2. Ask the user if they want to retry the download or exit the process.
3. If retries are exhausted, it will exit automatically.

# Log File
All logs are saved in a file named download_log.txt. This includes download successes, errors, and retries.

