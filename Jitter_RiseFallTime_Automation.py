"""
Alex Yazdani
05/03/2023
This file acts as an automation test run for jitter, rise and fall time transmitter testing.
The script connects to a Keysight oscilloscope via GPIB to query the instrument.
In an actual script for testing, a loop should be used to wait for full scope acquisition.

The full list of VISA commands can be found at the end of the file.
"""

import time
import pyvisa

scope_gpib = "GPIB0::7::INSTR"
scope_ip = "TCPIP0::___.___.___.___::____::SOCKET


"""
Open Instrument:
"""
scope_rm = pyvisa.ResourceManager()
oscilloscope = scope_rm.open_resource(scope_gpib)
time.sleep(1)


"""
Rise and Fall Time Test:
"""
oscilloscope.write(":ACQuire:STOP")
time.sleep(1)

oscilloscope.write(":SYSTem:MODE OSCilloscope")
time.sleep(1)

oscilloscope.write(":ACQuire:RUN")
time.sleep(1)

oscilloscope.write(":CHAN3A:FILTer OFF")
time.sleep(1)

oscilloscope.write(":CRECovery5:RELock")
time.sleep(1)

oscilloscope.write(":SYSTem:AUToscale")
time.sleep(1)

oscilloscope.write(":TRIGger:PLOCk ON")
time.sleep(1)

oscilloscope.write(":SYSTem:AUToscale")
time.sleep(1)

oscilloscope.write(":MEASure:OSCilloscope:FALLtime")
oscilloscope.write(":MEASure:OSCilloscope:RISetime")
time.sleep(10)

oscilloscope.write(":ACQuire:STOP")
time.sleep(1)

fall_time = oscilloscope.query(":MEASure:OSCilloscope:FALLtime:Mean?")
rise_time = oscilloscope.query(":MEASure:OSCilloscope:RISetime:Mean?")
time.sleep(1)

print(f"\nRise Time = {rise_time}\nFall Time = {fall_time}\n")

oscilloscope.write(":CHAN3A:FILTer ON")
time.sleep(1)

oscilloscope.write(":SYSTem:MODE EYE")
time.sleep(1)

oscilloscope.write(":TRIGger:PLOCk OFF")
time.sleep(1)
"""
End of Rise and Fall Time Test
"""


"""
Putting back in normal state:
"""
oscilloscope.write(":ACQuire:RUN")
time.sleep(5)


"""
Jitter Test:
"""
oscilloscope.write(":ACQuire:STOP")
time.sleep(1)

oscilloscope.write(":SYSTem:MODE JITTer")
time.sleep(1)

oscilloscope.write(":CRECovery5:RELock")
time.sleep(1)

oscilloscope.write(":SYSTem:AUToscale")
time.sleep(1)

oscilloscope.write(":TRIGger:PLOCk ON")
time.sleep(1)

oscilloscope.write(":ACQuire:RUN")
time.sleep(1)

oscilloscope.write(":MEASure:JITTer:DEFine:UNITs UINTerval")
time.sleep(1)

time.sleep(10)
oscilloscope.write(":ACQuire:STOP")
time.sleep(1)

tj = oscilloscope.query(":MEASure:JITTer:TJ?")
ddj = oscilloscope.query(":MEASure:JITTer:DDJ?")
time.sleep(1)

print(f"\nDDJ = {ddj}\nTJ = {tj}\n")

oscilloscope.write(":SYSTem:MODE EYE")
time.sleep(1)

oscilloscope.write(":TRIGger:PLOCk OFF")
time.sleep(1)

"""
End of Jitter Test
"""


"""
Putting back in normal state:
"""
oscilloscope.write(":ACQuire:RUN")
time.sleep(1)


"""
Close Instrument:
"""
oscilloscope.clear()
oscilloscope.close()
scope_rm.close()


"""
Sample Output:

Rise Time = 3.602E-11

Fall Time = 7.540E-11



DDJ = 1.06E-2

TJ = 5.24E-2
"""



"""
Full VISA Command List:


//Rise and Fall Time:

:ACQuire:STOP
:SYSTem:MODE OSCilloscope
:ACQuire:RUN
:CHAN3A:FILTer OFF
:CRECovery5:RELock
:SYSTem:AUToscale
:TRIGger:PLOCk ON
:SYSTem:AUToscale
:MEASure:OSCilloscope:FALLtime
:MEASure:OSCilloscope:RISetime

//Add in commands to wait for data collection to finish  --> -->  :MEASure:LTESt:ACQuire:COUNt?

:MEASure:OSCilloscope:FALLtime:Mean?    //QUERY 
:MEASure:OSCilloscope:RISetime:Mean?    //QUERY

//Take Screenshot

:CHAN3A:FILTer ON
:SYSTem:MODE EYE
:TRIGger:PLOCk OFF





//Jitter:

:ACQuire:STOP
:SYSTem:MODE JITTer
:CRECovery5:RELock
:SYSTem:AUToscale
:TRIGger:PLOCk ON
:ACQuire:RUN
:MEASure:JITTer:DEFine:UNITs UINTerval

//Add in commands to wait for data collection to finish -->  :MEASure:LTESt:ACQuire:COUNt?

:MEASure:JITTer:TJ?     //Query
:MEASure:JITTer:DDJ?    //Query

//Take Screenshot

:SYSTem:MODE EYE
:TRIGger:PLOCk OFF

"""
