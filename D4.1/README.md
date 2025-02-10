# RiseDatabase Python Library

The `RiseDatabase` Python library provides tools to download, process, and visualize accelerometer datasets collected from structural monitoring systems. The library interacts with a Flask-based API backend to securely fetch datasets stored in a private Google Drive repository. It includes features for downloading datasets, applying baseline correction to signals, and plotting time-series accelerometer data.

## Features

- **Dataset Management**: List available datasets and download them with a progress bar.
- **Signal Processing**: Perform baseline correction (mean subtraction or polynomial fitting).
- **Visualization**: Plot time-series data from accelerometer recordings.

## Flask API Backend

The API backend is built using Flask and is hosted on Heroku. It provides secure access to datasets stored in a private Google Drive folder. The API includes the following key endpoints:

- **`GET /list`**: Returns a list of available datasets, including their unique IDs and names.
- **`GET /download/<file_id>`**: Streams the requested dataset file based on its ID.

The backend uses a Google Cloud service account to authenticate with Google Drive. To protect the private repository, API access is restricted using API keys, rate limiting, and custom user-agent verification. The JSON key file for the service account is encoded and stored as a Heroku environment variable to ensure security.

### Example API Response (List Datasets)
```json
{
    "files": [
        {"id": "1-B6wOK-axIJ69-Wn46VimuF9S5oi6e9J", "name": "39R-Bridge.zip"},
        {"id": "1-7bd1YH4C2TpXOvkFX7oFA7JUDMJ4RZX", "name": "T7-Bridge.zip"}
    ]
}
```

## Installation

To install the library, run the following command:

```bash
pip install rise-database
```

The installation will automatically handle all necessary dependencies.

## Usage

### 1. Initialize the Library
```python
from rise_database import RiseDatabase

db = RiseDatabase()
```

### 2. List Available Datasets
```python
print("Available datasets:", db.databases)
```

Example output:
```python
{
    '1-B6wOK-axIJ69-Wn46VimuF9S5oi6e9J': '39R-Bridge.zip',
    '1-7bd1YH4C2TpXOvkFX7oFA7JUDMJ4RZX': 'T7-Bridge.zip'
}
```

### 3. Download and Extract a Dataset
```python
valid_id = list(db.databases.keys())[0]  # Get the first dataset ID
db.download_dataset(valid_id)
```
This will download and extract the dataset to the `data/` directory.

## API Setup Overview

The Flask API backend performs the following tasks:

1. **List Datasets**: Provides metadata about available datasets stored in Google Drive.
2. **Download Dataset**: Streams requested datasets directly from Google Drive to the client.
3. **Secure Access**: Utilizes Google Cloud service accounts for authentication and applies API keys, rate limiting, and user-agent verification to protect the data.

The backend is designed to be scalable and secure, leveraging Heroku for deployment and Google Cloud for storage integration.

## Contributing

Contributions are welcome! If you'd like to add features or fix issues, please submit a pull request.

