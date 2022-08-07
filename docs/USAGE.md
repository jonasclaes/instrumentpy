# Usage

1. Install the library using pip:  
   `pip install instrumentpy`
2. Import the instrument you want to use from the library. This library features a couple of categories. Possible categories are:  
   - PSU
3. Create an instance of the instrument you want to use. This is done by calling the class constructor.  
   `instrument = PSU(...)`
4. Pass a configuration to the instrument during construction. For example a serial interface made using the PySerial library.
5. Done!
