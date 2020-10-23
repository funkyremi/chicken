import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from flask import Flask, request
app = Flask(__name__)

# Setup the motor
GpioPins = [18, 23, 24, 25]
motor = RpiMotorLib.BYJMotor("Motor", "28BYJ")

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

@app.route('/rotate')
def rotate():
    number = float(request.args.get('number'))
    rotations_nb = round(number * 512)
    if rotations_nb < 0:
        motor.motor_run(GpioPins , .0005, -rotations_nb, False, False, "half", .05)
        set_state("0")
    elif rotations_nb >= 0:
        motor.motor_run(GpioPins , .005, rotations_nb, True, False, "half", .05)
        set_state("1")
    return 'Done'

@app.route('/state')
def state():
    return get_state()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

