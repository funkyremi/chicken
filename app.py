import RPi.GPIO as GPIO
import threading
from RpiMotorLib import RpiMotorLib
from flask import Flask, request
app = Flask(__name__)

is_moving = False

# Setup the motor
GpioPins = [18, 23, 24, 25]
motor = RpiMotorLib.BYJMotor("Motor", "28BYJ")

# Setup end button switch
def button_callback(channel):
    print("Stopping motor")
    motor.motor_stop()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(17, GPIO.RISING, callback=button_callback)


# Set and get state from file
def get_state():
    state_file = open("state.txt", "r")
    state = state_file.read()
    state_file.close()
    return state


def set_state(state):
    state_file = open("state.txt", "w")
    state_file.write(state)
    state_file.close()


def open_door(rotations_nb):
    global is_moving
    print('Opening')
    is_moving = True
    motor.motor_run(GpioPins, 0.002, -rotations_nb, False, False, "full", .05)
    is_moving = False
    print('Opened')


def close_door(rotations_nb):
    global is_moving
    print('Closing')
    is_moving = True
    motor.motor_run(GpioPins, 0.002, rotations_nb, True, False, "full", .05)
    is_moving = False
    print('Closed')


@app.route('/rotate')
def rotate():
    global is_moving
    if not is_moving:
        number = float(request.args.get('number'))
        rotations_nb = round(number * 512)
        if rotations_nb < 0:
            threading.Thread(target=open_door, args=[rotations_nb]).start()
            set_state("0")
            return 'Opening'
        elif rotations_nb >= 0:
            threading.Thread(target=close_door, args=[rotations_nb]).start()
            set_state("1")
            return 'Closing'
    else:
        return 'Please wait until the motor has stopped moving.'


@app.route('/open')
def open_door_url():
    global is_moving
    if not is_moving:
        if get_state() != '0':
            rotations_nb = round(-8 * 512)
            threading.Thread(target=open_door, args=[rotations_nb]).start()
            set_state("0")
            return 'Opening'
        else:
            return 'The door is already opened.'
    else:
        return 'Please wait until the motor has stopped moving.'


@app.route('/close')
def close_door_url():
    global is_moving
    if not is_moving:
        if get_state() != '1':
            rotations_nb = round(10 * 512)
            threading.Thread(target=close_door, args=[rotations_nb]).start()
            set_state("1")
            return 'Closing'
        else:
            return 'The door is already closed.'
    else:
        return 'Please wait until the motor has stopped moving.'


@app.route('/stop')
def stop_door_url():
    motor.motor_stop()
    return 'The motor is stopped'


@app.route('/state')
def state():
    return get_state()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
