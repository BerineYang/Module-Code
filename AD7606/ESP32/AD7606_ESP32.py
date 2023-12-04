from machine import Pin, SPI, PWM
import time, array, sys
SAMPLING_POINTS = 10
nums = 0
# Define all pin
SPI_MISO_PIN = 12
SPI_MOSI_PIN = 13
SPI_SCK_PIN = 14
AD_CS_PIN = 27
AD_RESET_PIN = 22
AD_CONVST_PIN = 21
AD_RANGE_PIN = 32
AD_OS0_PIN = 25
AD_OS1_PIN = 26
AD_OS2_PIN = 33
AD_BUSY_PIN = 23
CS_PIN = Pin(AD_CS_PIN, Pin.OUT)
RESET_PIN = Pin(AD_RESET_PIN, Pin.OUT)
OS0_PIN = Pin(AD_OS0_PIN, Pin.OUT)
OS1_PIN = Pin(AD_OS1_PIN, Pin.OUT)
OS2_PIN = Pin(AD_OS2_PIN, Pin.OUT)
RANGE_PIN = Pin(AD_RANGE_PIN, Pin.OUT)
CONVST_PIN = Pin(AD_CONVST_PIN, Pin.OUT)
BUSY_PIN = Pin(AD_BUSY_PIN, Pin.IN, Pin.PULL_UP)
#BUSY_PIN.irq(trigger = Pin.IRQ_FALLING, handler = call_back)
num_rows = 8
num_columns = SAMPLING_POINTS
HSPI = SPI(1, baudrate=8000000, sck=Pin(SPI_SCK_PIN), mosi=Pin(SPI_MOSI_PIN), miso=Pin(SPI_MISO_PIN))
ad7606SamplingDoneFlag = 0

# Define buffer
data = [array.array('d', [0] * num_columns) for _ in range(num_rows)]

def AD7606_ESP32(RANGE = 1, OS = 0):
    global CS_PIN, RESET_PIN, CONVST_PIN, OS0_PIN, OS1_PIN, OS2_PIN, RANGE_PIN, ad7606SamplingDoneFlag
    # Initialize CS pin
    CS_PIN.on()
    
    # Reset AD7606
    RESET_PIN.off()
    time.sleep(0.001)
    RESET_PIN.on()
    time.sleep(0.001)
    RESET_PIN.off()

    # Start AD7606
    PWM0 = PWM(CONVST_PIN)
    freq = PWM0.freq()
    PWM0.freq(100000) 
    duty = PWM0.duty()
    PWM0.duty(1014)
    
    # Define OS pin
    MODE = OS
    M = [0, 0, 0]
    for i in range(3):
        M[i] = MODE % 2
        MODE = MODE // 2
    if M[0] == 1:
        OS0_PIN.on()
    else:
        OS0_PIN.off()
    if M[1] == 1:
        OS1_PIN.on()
    else:
        OS1_PIN.off()
    if M[2] == 1:
        OS2_PIN.on()
    else:
        OS2_PIN.off()
    if RANGE == 1:
        RANGE_PIN.on()
    else:
        RANGE_PIN.off()
        
    while True:
        if ad7606SamplingDoneFlag:
            PWM0.duty(0)
            CS_PIN.on()
            ad7606SamplingDoneFlag = 1
            break
    
def call_back(pin):
    global CS_PIN, array, nums, ad7606SamplingDoneFlag
    if pin == Pin(23):
        if nums < SAMPLING_POINTS:
            ad7606SamplingDoneFlag = 0
            for i in range(8):
                CS_PIN.off()
                buf = bytearray(2)
                HSPI.readinto(buf)
                first_byte = buf[0]
                first_bit = (first_byte >> 7) & 1
                if first_bit == 1:
                    data[i][nums] = int.from_bytes(buf, 'big')/65535 * 2 * 10 - 20
                else:
                    data[i][nums] = int.from_bytes(buf, 'big')/65535 * 2 * 10
                if i == 0:
                    print(data[i][nums])
                CS_PIN.on()
            nums = nums + 1
        else:
            ad7606SamplingDoneFlag = 1
 
if __name__=="__main__":
    BUSY_PIN.irq(trigger = Pin.IRQ_FALLING, handler = call_back)
    AD7606_ESP32(RANGE = 1, OS = 0)    