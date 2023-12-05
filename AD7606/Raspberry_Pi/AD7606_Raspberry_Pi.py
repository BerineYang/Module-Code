import RPi.GPIO as GPIO, numpy as np, spidev, time, sys
GPIO.setwarnings(False)
SAMPLING_POINTS = 10
nums = 0
# Define all pin
AD_CS_PIN = 3
AD_RESET_PIN = 5
AD_CONVST_PIN = 7
AD_RANGE_PIN = 11
AD_OS0_PIN = 13
AD_OS1_PIN = 15
AD_OS2_PIN = 31
AD_BUSY_PIN = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(AD_CS_PIN, GPIO.OUT)
GPIO.setup(AD_RESET_PIN, GPIO.OUT)
GPIO.setup(AD_OS0_PIN, GPIO.OUT)
GPIO.setup(AD_OS1_PIN, GPIO.OUT)
GPIO.setup(AD_OS2_PIN, GPIO.OUT)
GPIO.setup(AD_RANGE_PIN, GPIO.OUT)
GPIO.setup(AD_CONVST_PIN, GPIO.OUT)
GPIO.setup(AD_BUSY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
num_rows = 8
num_columns = SAMPLING_POINTS
#SPI COMMMUNICATION
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 8000000
spi.mode = 0b00

ad7606SamplingDoneFlag = 0

data2 = np.zeros((8, 1000))

def AD7606_Raspberry_Pi(RANGE = 1, OS = 0):
    global AD_CS_PIN, AD_RESET_PIN, AD_CONVST_PIN, AD_OS0_PIN, AD_OS1_PIN, AD_OS2_PIN, AD_RANGE_PIN, ad7606SamplingDoneFlag
    # Initialize CS pin
    GPIO.output(AD_CS_PIN, GPIO.LOW)

    # Reset AD7606
    GPIO.output(AD_RESET_PIN, GPIO.LOW)
    time.sleep(0.001)
    GPIO.output(AD_RESET_PIN, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(AD_RESET_PIN, GPIO.LOW)

    # PWM
    PWM0 = GPIO.PWM(AD_CONVST_PIN, 100000)  # 创建PWM0实例，并设置频率为50Hz
    PWM0.start(99)

    # Define OS pin
    MODE = OS
    M = [0, 0, 0]
    for i in range(3):
        M[i] = MODE % 2
        MODE = MODE // 2
    if M[0] == 1:
        GPIO.output(AD_OS0_PIN, GPIO.HIGH)
    else:
        GPIO.output(AD_OS0_PIN, GPIO.LOW)
    if M[1] == 1:
        GPIO.output(AD_OS0_PIN, GPIO.HIGH)
    else:
        GPIO.output(AD_OS0_PIN, GPIO.LOW)
    if M[2] == 1:
        GPIO.output(AD_OS0_PIN, GPIO.HIGH)
    else:
        GPIO.output(AD_OS0_PIN, GPIO.LOW)
    if RANGE == 1:
        GPIO.output(AD_RANGE_PIN, GPIO.HIGH)
    else:
        GPIO.output(AD_RANGE_PIN, GPIO.LOW)

    while True:
        if ad7606SamplingDoneFlag:
            PWM0.ChangeDutyCycle(0)
            GPIO.output(AD_CS_PIN, GPIO.HIGH)
            ad7606SamplingDoneFlag = 1
            GPIO.cleanup()
            break

def call_back(channel):
    global AD_CS_PIN, array, nums, ad7606SamplingDoneFlag
    if nums < SAMPLING_POINTS:
        ad7606SamplingDoneFlag = 0
        for i in range(8):
            GPIO.output(AD_CS_PIN, GPIO.LOW)
            rx_data = spi.xfer2([0x00, 0x00])
            first_bit = (rx_data[0] >> 7) & 1
            data = (rx_data[0] << 8) | rx_data[1]
            if first_bit == 1:
                data2[i][nums] = int(data) / 65535 * 2 * 10 - 20
            else:
                data2[i][nums] = int(data)  / 65535 * 2 * 10
            if i == 0:
                print(data2[i][nums])
            GPIO.output(AD_CS_PIN, GPIO.HIGH)
        nums = nums + 1
    else:
        ad7606SamplingDoneFlag = 1


if __name__ == "__main__":
    GPIO.add_event_detect(AD_BUSY_PIN, GPIO.FALLING, callback=call_back)
    AD7606_Raspberry_Pi(RANGE=1, OS=0)
