import os
import requests
import zipfile
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

class RiseDatabase:
    def __init__(self):
        self.api_url = "https://rise-data-api-3ecdb0861d7f.herokuapp.com"
        self.data = None

    def list_datasets(self):
        """List available datasets."""
        response = requests.get(f"{self.api_url}/list")
        if response.status_code == 200:
            return response.json()["files"]
        else:
            raise Exception("Failed to fetch dataset list.")

    def download_dataset(self, dataset_id, save_path="data"):
        """
        Download a specific dataset by its ID with a progress bar, unzip it, and delete the .zip file.

        Args:
            dataset_id (str): The ID of the dataset to download.
            save_path (str): The folder where the dataset will be saved and extracted.
        """
        # Create the folder if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Make the request to the API
        response = requests.get(f"{self.api_url}/download/{dataset_id}", stream=True)
        if response.status_code == 200:
            # Extract the dataset name from the headers
            dataset_name = response.headers.get(
                "Content-Disposition", "dataset.zip"
            ).split("filename=")[-1].strip('"')
            zip_file_path = os.path.join(save_path, dataset_name)

            # Get the total file size in bytes
            total_size = int(response.headers.get("content-length", 0))

            # Download the file with a progress bar
            with open(zip_file_path, "wb") as file, tqdm(
                desc=f"Downloading {dataset_name.split('.')[0]}",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    bar.update(len(chunk))
            print(f"\nDataset downloaded successfully: {zip_file_path}")
            # Unzip the file and delete the .zip file
            self._extract_and_cleanup(zip_file_path, save_path)
        else:
            raise Exception(
                f"Failed to download dataset. Status code: {response.status_code}"
            )

    def _extract_and_cleanup(self, zip_file_path, extract_to):
        """
        Extract a zip file and delete the zip file afterward.

        Args:
            zip_file_path (str): Path to the zip file.
            extract_to (str): Directory where the contents will be extracted.
        """
        print(f"Extracting {zip_file_path}...")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        # Delete the .zip file
        os.remove(zip_file_path)
        print(f"Extraction complete. Files extracted to: {extract_to}")


    def baseline_correction(self, method="mean"):
        """
        Perform baseline correction on accelerometer signals stored in self.data.

        Args:
            method (str): The method for baseline correction. Options are:
                - "mean": Subtract the mean of the signal.
                - "polynomial": Fit and subtract a 2nd-degree polynomial.

        Returns:
            pd.DataFrame: DataFrame with corrected signals.
        """
        if self.data is None:
            raise Exception("No data loaded. Please use the 'read_data' method to load data first.")

        # Perform baseline correction on each axis
        corrected_data = self.data.copy()
        for axis in ['Acc x', 'Acc y', 'Acc z']:
            if method == "mean":
                corrected_data[f'{axis} corrected'] = corrected_data[axis] - corrected_data[axis].mean()
            elif method == "polynomial":
                time = np.arange(len(corrected_data))
                coeffs = np.polyfit(time, corrected_data[axis], 2)
                trend = np.polyval(coeffs, time)
                corrected_data[f'{axis} corrected'] = corrected_data[axis] - trend
            else:
                raise ValueError(f"Unsupported method: {method}. Choose 'mean' or 'polynomial'.")

        self.data = corrected_data  # Update the data with corrected values
        return self.data

    def filter(self, lowcut, highcut, order=4):
        """
        Apply a Butterworth band-pass filter to the accelerometer signals in self.data.

        Args:
            lowcut (float): Low cutoff frequency (Hz).
            highcut (float): High cutoff frequency (Hz).
            order (int): Order of the filter.

        Returns:
            pd.DataFrame: DataFrame with filtered signals.
        """
        if self.data is None:
            raise Exception("No data loaded. Please use the 'read_data' method to load data first.")

        # Sampling rate estimation
        time_diff = self.data['Seconds (zeroed)'].diff().mean()
        fs = 1.0 / time_diff

        # Design the Butterworth band-pass filter
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')

        # Apply the filter to each accelerometer axis
        filtered_data = self.data.copy()
        for axis in ['Acc x', 'Acc y', 'Acc z']:
            filtered_data[f'{axis} filtered'] = filtfilt(b, a, filtered_data[axis])

        self.data = filtered_data  # Update the data with filtered values
        return self.data
    
    def read_data(self, file_path):
        """
        Read accelerometer data from a tab-separated file and store it in the class.

        Args:
            file_path (str): Path to the data file.

        Returns:
            pd.DataFrame: Parsed data.
        """
        try:
            data = pd.read_csv(file_path, sep="\t")
            expected_columns = ['Date', 'Time', 'Seconds (zeroed)', 'Seconds (synced)', 'Acc x', 'Acc y', 'Acc z']
            if not all(column in data.columns for column in expected_columns):
                raise ValueError("The file does not contain the expected columns.")
            self.data = data
            return self.data
        except Exception as e:
            raise Exception(f"Error reading data file: {e}")

    def plot(self):
        """
        Plot corrected x, y, and z axis signals from the data stored in self.data.

        Args:
            title (str): Title of the plot.
        """
        if self.data is None or not all(f'{axis} corrected' in self.data.columns for axis in ['Acc x', 'Acc y', 'Acc z']):
            raise Exception("No corrected data available. Please apply baseline correction first.")

        fig, axes = plt.subplots(3, 1, figsize=(12, 12))
        # Plot each axis on a separate subplot
        axes[0].plot(self.data['Seconds (zeroed)'], self.data['Acc x corrected'], color="red")
        axes[0].set_title("X-axis Corrected")
        axes[0].set_xlabel("Time (seconds)")
        axes[0].set_ylabel("Amplitude")
        axes[0].grid(True)

        axes[1].plot(self.data['Seconds (zeroed)'], self.data['Acc y corrected'], color="green")
        axes[1].set_title("Y-axis Corrected")
        axes[1].set_xlabel("Time (seconds)")
        axes[1].set_ylabel("Amplitude")
        axes[1].grid(True)

        axes[2].plot(self.data['Seconds (zeroed)'], self.data['Acc z corrected'], color="blue")
        axes[2].set_title("Z-axis Corrected")
        axes[2].set_xlabel("Time (seconds)")
        axes[2].set_ylabel("Amplitude")
        axes[2].grid(True)

        # Adjust layout for better spacing
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
