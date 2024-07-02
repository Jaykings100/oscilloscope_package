import time
import numpy as np
from RsInstrument import RsInstrument, BinFloatFormat

class OscilloscopeControl:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.instr = None

    def connect(self):
        """Establish a connection with the oscilloscope."""
        self.instr = RsInstrument(self.ip_address, True, True)
        self.instr.visa_timeout = 10000  # Default timeout
        self.instr.opc_timeout = 20000  # Default OPC timeout

    def disconnect(self):
        """Close the connection to the oscilloscope."""
        if self.instr:
            self.instr.close()

    def testConnectionToOscilloscope(self):
        """Test connection by querying the oscilloscope's identification information."""
        response = self.instr.query_str('*IDN?')
        print(f'Oscilloscope Identification: {response}')
        return response

    def setChannelCoupling(self, channel, coupling_type):
        """Set the input coupling of a specific channel."""
        if coupling_type not in ['50OHM', '1MOHM', 'AC']:
            raise ValueError("Invalid coupling type. Choose from '50OHM', '1MOHM', 'AC'")
        self.instr.write_str(f'CHAN{channel}:COUP {coupling_type}')

    def setAcquisitionTime(self, acquisition_time):
        """Set the acquisition time (timebase scale)."""
        self.instr.write_str(f'TIM:RANG {acquisition_time}')

    def startAcquisition(self):
        """Initiate the data acquisition process."""
        self.instr.write_str("SING")
        self.instr.query_opc()

    def changeDisplay(self, channel, display_state):
        """Enable or disable the display for specified channels."""
        if display_state not in ['ON', 'OFF']:
            raise ValueError("Invalid display state. Choose from 'ON' or 'OFF'")
        self.instr.write_str(f'CHAN{channel}:DISP {display_state}')

    def setTrigger(self, source_channel, level, slope):
        """Set the trigger settings."""
        slope_map = {'RISING': 'POS', 'FALLING': 'NEG'}
        if slope not in slope_map:
            raise ValueError("Invalid slope. Choose from 'RISING' or 'FALLING'")
        self.instr.write_str(f"TRIG:SOUR CHAN{source_channel}")
        self.instr.write_str(f"TRIG:LEV {level}")
        self.instr.write_str(f"TRIG:EDGE:SLOP {slope_map[slope]}")

    def acquireData(self, channel):
        """Retrieve waveform data from a specified channel."""
        self.instr.bin_float_numbers_format = BinFloatFormat.Single_4bytes
        data = self.instr.query_bin_or_ascii_float_list(f'FORM REAL,32;:CHAN{channel}:DATA?')
        return data
