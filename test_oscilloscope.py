"""import numpy as np
import matplotlib.pyplot as plt
from oscilloscope_control import OscilloscopeControl

# Example usage
if __name__ == "__main__":
    osc = OscilloscopeControl('TCPIP::192.168.1.100::INSTR')
    osc.connect()
    osc.testConnectionToOscilloscope()
    #osc.setChannelCoupling(1, 'AC')
    osc.setAcquisitionTime(0.05)  # 50ms acquisition time

    # Set trigger settings
    #osc.setTrigger(1, 0.05, 'RISING')

    # Start acquisition
    osc.startAcquisition()

    # Acquire data from Channel 1
    data = osc.acquireData(1)
    print(len(data))
    osc.disconnect()

    # Generate time values
    total_time = 0.05  # 50 ms acquisition time
    num_points = len(data)
    time_array = np.linspace(0, total_time, num_points)

    # Plot the waveform
    plt.plot(time_array, data)
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Waveform from Channel 1")
    plt.grid(True)
    plt.show()

   # Save the data to a CSV file
    osc.saveDataToCSV('c:\\Users\\jtutu\\Desktop\\Oscilloscope\\measurement_results.csv', time_array, data)
"""
import time
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from RsInstrument import RsInstrument, BinFloatFormat

def main():
    try:
        # Initialize the connection to the oscilloscope
        instr = RsInstrument('TCPIP::192.168.1.100::INSTR', True, True)
        instr.visa_timeout = 10000  # Increased timeout to handle larger data transfer
        instr.opc_timeout = 20000

        # Clear status and reset the instrument
        instr.write_str('*CLS')
        time.sleep(0.5)
        instr.write_str_with_opc('*RST')

        # Set up single acquisition for 50ms
        instr.write_str("ACQ:POIN:AUTO RECL")  # Define Horizontal scale by number of points
        instr.write_str("TIM:RANG 10")  # 50ms Acquisition time
        instr.write_str("ACQ:POIN 1000000")  # Assuming a high number of points for high resolution
        instr.write_str("CHAN1:RANG 2")  # Horizontal range 2V
        instr.write_str("CHAN1:POS 0")  # Offset 0
        instr.write_str("CHAN1:COUP AC")  # Coupling AC 1MOhm
        instr.write_str("CHAN1:STAT ON")  # Switch Channel 1 ON

        # Trigger Settings
        instr.write_str("TRIG1:MODE NORMal")  # Trigger Auto mode in case of no signal is applied
        instr.write_str("TRIG1:SOUR CHAN1")  # Trigger source CH1
        instr.write_str("TRIG1:TYPE EDGE;:TRIG1:EDGE:SLOP POS")  # Trigger type Edge Positive
        instr.write_str("TRIG1:LEV1 0.04")  # Trigger level 40mV
        instr.query_opc()  # Using *OPC? query waits until all the instrument settings are finished

        # Arm the oscilloscope for single acquisition
        instr.visa_timeout = 20000  # Acquisition timeout - set it higher than the acquisition time
        instr.write_str("SING")
        instr.query_opc()  # Using *OPC? query waits until the instrument finished the Acquisition

        # Fetching the waveform in ASCII and BINary format
        trace = instr.query_bin_or_ascii_float_list('FORM ASC;:CHAN1:DATA?')  # Query ascii array of floats
        instr.bin_float_numbers_format = BinFloatFormat.Single_4bytes  # This tells the driver in which format to expect the binary float data
        trace = instr.query_bin_or_ascii_float_list('FORM REAL,32;:CHAN1:DATA?')  # Query binary array of floats
        max_points = instr.query_str("ACQ:POIN:MAX?")
        print(f"Maximum acquisition points supported: {max_points}")
        # Close the session
        instr.close()

        # Generate time values
        total_time = 0.05  # 50 ms acquisition time
        num_points = len(trace)
        time_array = np.linspace(0, total_time, num_points)


        # Plot the waveform
        plt.plot(time_array, trace)
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")
        plt.title("Waveform from Channel 1")
        plt.grid(True)
        plt.show()

        # Save the result to a CSV file
        csv_file_path = 'c:\\Users\\jtutu\\Desktop\\Oscilloscope\\measurement_results.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time (s)", "Voltage (V)"])
            for t, v in zip(time_array, trace):
                writer.writerow([t, v])

        print(f"Results saved to {csv_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
