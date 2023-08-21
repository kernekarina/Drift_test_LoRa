import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def parse_datetime_from_filename(filename):
    try:
        # Split the file name by underscores to extract different parts
        filename_parts = os.path.splitext(os.path.basename(filename))[0].split('_')

        # Identify the part that contains the datetime information
        datetime_str = None
        for part in filename_parts:
            try:
                datetime_str = datetime.strptime(part, '%Y-%m-%d %H-%M-%S.%f')
                break
            except ValueError:
                continue

        if datetime_str is None:
            raise ValueError("Datetime information not found in the file name.")

        return datetime_str

    except Exception as e:
        print(f"Error parsing datetime from file name: {e}")
    return None

def get_max_frequency_values(folder_path):
    csv_files = glob.glob(os.path.join(folder_path, '*.CSV'))

    max_values = []
    timestamps = []
    max_frequency_values = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file, sep=";")
        if 'Frequency in Hz' in df.columns and 'Power in dBm' in df.columns:
            max_value = df['Power in dBm'].max()
            if max_value >= 0:  # Ignore data if max power is less than zero
                timestamp = parse_datetime_from_filename(csv_file)
                if timestamp is not None:
                    timestamps.append(timestamp)
                    max_frequency_idx = df['Power in dBm'].idxmax()
                    max_frequency_value = df.loc[max_frequency_idx, 'Frequency in Hz']
                    max_frequency_values.append(max_frequency_value)

    return timestamps, max_frequency_values

def plot_data(folder_path):
    subfolders = [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]

    all_time_seconds = []
    all_max_frequency_values = []
    all_subfolder_labels = []

    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        timestamps, max_frequency_values = get_max_frequency_values(subfolder_path)

        if timestamps and max_frequency_values:
            time_seconds = [(t - timestamps[0]).total_seconds() for t in timestamps]
            all_time_seconds.append(time_seconds)
            all_max_frequency_values.append(max_frequency_values)
            all_subfolder_labels.append(subfolder)

    plt.figure(figsize=(10, 6))
    for time_seconds, max_frequency_values, label in zip(all_time_seconds, all_max_frequency_values, all_subfolder_labels):
        plt.plot(time_seconds, max_frequency_values, marker='o', label=label)

    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency in Hz')
    plt.title('Frequency Corresponding to Maximum Power vs Time')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing the data you want to plot: ")
    plot_data(folder_path)
