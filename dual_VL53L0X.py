import board, busio, adafruit_vl53l0x, time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need \
           superuser privileges.  You can achieve this by using 'sudo' to run \
           your script")


def setup(xshut0, xshut1, addr0=42, addr1=43):

    # assert addresses are not the same and default
    assert(addr0 != addr1)
    assert(addr0 != 41)
    assert(addr1 != 41)

    # initialize GPIO for XSHUT pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(xshut0, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(xshut1, GPIO.OUT, initial=GPIO.LOW)

    # reset both VL530X modules
    time.sleep(0.1)
    GPIO.output(xshut0, GPIO.HIGH)
    GPIO.output(xshut1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(xshut0, GPIO.LOW)
    GPIO.output(xshut1, GPIO.LOW)

    # initialize the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    i2c.scan()
    [hex(x) for x in i2c.scan()]

    # initialize one sensor and change the address
    print("Address Change")

    print("Address Change #1")
    GPIO.output(xshut0, GPIO.HIGH)
    time.sleep(0.1)

    i2c.scan()
    [hex(x) for x in i2c.scan()]

    print("Address Change #2")

    vl530 = adafruit_vl53l0x.VL53L0X(i2c)
    vl530.set_address(addr0)

    i2c.scan()
    [hex(x) for x in i2c.scan()]

    # initialize the next sensor and change the address
    GPIO.output(xshut1, GPIO.HIGH)
    time.sleep(0.1)
    vl531 = adafruit_vl53l0x.VL53L0X(i2c)
    vl531.set_address(addr1)

    # return I2C objects
    return (vl530, vl531)