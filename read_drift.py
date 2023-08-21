import os
import time
import shutil
from datetime import datetime
from RsInstrument import *

source_folder = r"C:\\Users\\adm_DesignCenter\\Desktop\\Rohde_Schwarz_measurements\\screenshot_drift"
destination_folder = r"C:\\Users\\adm_DesignCenter\\Desktop\\Rohde_Schwarz_measurements\\archive"
measurement_duration = 4 #0.4  # Duration of the measurement in seconds - tests on sx1262 uses 2s
start_time = time.time()  # Record the start time

fpl1007 = None  # Define fpl1007 as a global variable

def instrument_config():
    global fpl1007
    try:
        resource_string_1 = 'TCPIP::191.4.205.71::INSTR'
        fpl1007 = RsInstrument(resource_string_1, True, False)
        fpl1007.visa_timeout = 0.2
        fpl1007.opc_timeout = 0.2

        # FPL1007 Config:
        fpl1007.clear_status()
        fpl1007.reset()
        fpl1007.query_opc()
        fpl1007.write_str('SYST:DISP:UPD ON')
        fpl1007.write_str('DISP:WIND:TRAC:Y:RLEV 25.0')
        fpl1007.write_str('FREQ:CENT 915.2 MHz')
        fpl1007.write_str('FREQ:SPAN 125 KHz')
        fpl1007.write_str('BAND 1 kHz')
        fpl1007.write_str('SWE:POIN 7000')
    except Exception as e:
        print("Error configuring instrument:", e)


def trace_get(fpl1007, filename):
    try: 
        trace_data = fpl1007.query('Trace:DATA? TRACe1')
        csv_trace_data = trace_data.split(",")
        trace_len = len(csv_trace_data)
    except Exception as e:
        print("Error getting trace data:", e)

    start_freq = fpl1007.query_float('FREQuency:STARt?')
    span = fpl1007.query_float('FREQuency:SPAN?')
    step_size = span / (trace_len - 1)

    with open(filename, 'w') as file:
        file.write("Frequency in Hz;Power in dBm\n")
        for x in range(trace_len):
            freq = start_freq + x * step_size
            amp = float(csv_trace_data[x])
            file.write(f'{freq:.1f};{amp:.2f}\n')

#-------------------------------------------------------------------------------------------------------

# Instruments connection and functional config:
resource_string_1 = 'TCPIP::191.4.205.71::INSTR'  # Standard LAN connection (also called VXI-11)
fpl1007 = RsInstrument(resource_string_1, True, False)
fpl1007.visa_timeout = 0.2  # Timeout for VISA Read Operations (ms)
fpl1007.opc_timeout = 0.2  # Timeout for opc-synchronized operations(ms)
fpl1007.instrument_status_checking = True  # Error check after each command

# FPL1007 Config:
fpl1007.clear_status()
fpl1007.reset()
fpl1007.query_opc()
fpl1007.write_str('SYST:DISP:UPD ON')  # Display update ON - switch OFF after debugging
fpl1007.write_str('DISP:WIND:TRAC:Y:RLEV 25.0')  # Setting the Reference Level
fpl1007.write_str('FREQ:CENT 915 MHz')  # Setting the center frequency
fpl1007.write_str('FREQ:SPAN 125 KHz')  # Setting the span
fpl1007.write_str('BAND 1 kHz')  # Setting the RBW
fpl1007.write_str('SWE:POIN 7000')  # Setting the sweep points
#fpl1007.write_str('TRIG:DTIM 2ms')  

#-----------------------------------------------------------------------------------------------------------

# Data Acquisition
measurement_duration = 2 #0.4  # Duration of the measurement in seconds - tests on sx1262 uses 2s
start_time = time.time()  # Record the start time


def move_files_to_new_folder(source_folder, destination_folder):
    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d %H-%M-%S.%f")
    new_folder_path = os.path.join(destination_folder, folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    if not files:
        print("No files found in the source folder.")
        return

    for file in files:
        source_file_path = os.path.join(source_folder, file)
        destination_file_path = os.path.join(new_folder_path, file)
        shutil.move(source_file_path, destination_file_path)

    print(f"Successfully moved {len(files)} files to the new folder: {new_folder_path}")

def data_acquisition():
    while time.time() - start_time < measurement_duration:
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")
        filename = f"C:\\Users\\adm_DesignCenter\\Desktop\\Rohde_Schwarz_measurements\\screenshot_drift\\TraceFile_{timestamp}.CSV"
        trace_get(fpl1007, filename)

# Close the session
fpl1007.close()

#-----------------------------------------------------------------------------------------------------------

#Move files of test to a new folder - in this way, you can run the next test without worry about mix the data

def move_files_to_new_folder(source_folder, destination_folder):
    # Create the destination folder with the current date in the name
    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d %H-%M-%S.%f")
    new_folder_path = os.path.join(destination_folder, folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    # Get a list of all files in the source folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    if not files:
        print("No files found in the source folder.")
        return

    # Move each file to the new folder
    for file in files:
        source_file_path = os.path.join(source_folder, file)
        destination_file_path = os.path.join(new_folder_path, file)
        shutil.move(source_file_path, destination_file_path)

    print(f"Successfully moved {len(files)} files to the new folder: {new_folder_path}")

# Example usage:
source_folder = r"C:\Users\ADM_KARINAKERNE\Desktop\medir drift no rohde com spec 1\screenshot_drift"
destination_folder = r"C:\Users\ADM_KARINAKERNE\Desktop\medir drift no rohde com spec 1\archive"

move_files_to_new_folder(source_folder, destination_folder)


if __name__ == "__main__":
    instrument_config()
    data_acquisition()

    # Close the session
    if fpl1007 is not None:
        fpl1007.close()

    move_files_to_new_folder(source_folder, destination_folder)
    print('Program successfully ended.')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

