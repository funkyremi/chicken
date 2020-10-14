import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from flask import Flask, request

# Setting the motor
GpioPins = [18, 23, 24, 25]
motor = RpiMotorLib.BYJMotor("Motor", "28BYJ")

# Init app
app = Flask(__name__)

@app.route('/rotate')
def rotate():
    number = float(request.args.get('number'))
    rotations_nb = round(number * 512)
    if rotations_nb < 0:
        motor.motor_run(GpioPins , .001, -rotations_nb, False, False, "half", .05)
    elif rotations_nb >= 0:
        motor.motor_run(GpioPins , .001, rotations_nb, True, False, "half", .05)
    return 'Done'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

