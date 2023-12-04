# AD7606_ESP32 User_guide
## Preparing
Before using this code, you should burn MicroPython firmware into ESP32. You could download in this website: https://micropython.org/download/ESP32_GENERIC/
## Wiring method
Before you send your Micropython files into your ESP32 boards, you should connect the wires correctly. In the next table, I will introduce the this method.  
AD7606 Board    ESP32 Board  
5V          ->  VIN  
GND         ->  GND  
D7          ->  D12  
RD          ->  D14  
CS          ->  D27  
RESET       ->  D22  
CA          ->  D21  
RANGE       ->  D32  
OS0         ->  D25  
OS1         ->  D26  
OS2         ->  D33  
BUSY        ->  D23  
