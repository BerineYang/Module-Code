# AD7606_Raspberry_Pi User_guide
## Preparing
Before using this code, you should install RPi.GPIO, spidev, numpy in python.You can use the following instructions to download the above packages.
```bash
sudo pip install RPi.GPIO
sudo pip install spidev
sudo pip install numpy
```
## Wiring method
Before you run your Ppython files in your Raspberry_Pi, you should connect the wires correctly. In the next table, I will introduce the this method.  
|AD7606 Board |Raspberry Board|
| :-----------: | :-----------: |
|5V|4|
|GND|6|
|D7|21|
|RD|23|
|CS|3|
|RESET|5|
|CA|7|
|RANGE|11|
|OS0|13|
|OS1|15|
|OS2|31|
|BUSY|29|
