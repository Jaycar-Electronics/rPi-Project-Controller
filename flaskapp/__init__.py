from flask import Flask
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

red_pin = 12
yel_pin = 16
grn_pin = 20
blu_pin = 21
GPIO.setup(red_pin,GPIO.OUT)
GPIO.setup(yel_pin,GPIO.OUT)
GPIO.setup(grn_pin,GPIO.OUT)
GPIO.setup(blu_pin,GPIO.OUT)

GPIO.setup(red_pin,GPIO.IN)
GPIO.setup(yel_pin,GPIO.IN)
GPIO.setup(grn_pin,GPIO.IN)
GPIO.setup(blu_pin,GPIO.IN)
#GPIO.setup(5,GPIO.OUT)
#GPIO.setup(6,GPIO.IN, pull_up_down=GPIO.PUD_UP)

app = Flask(__name__)
from .button import *

# load up a homepage we have written elsewhere
@app.route('/')
def hello():
    return """
    Hello World!<br><br>
    This is the example page, we have other routes!:<br>
    <a href='test'>test page</a><br>
    <a href='neuron'>Neuron page</a>
    """
@app.route('/test')
def test():

    #return a homepage we have written elsewhere
    #flask has a better way to do this, but I'm racing the clock
    return app.send_static_file('homepage.html')


@app.route('/neuron')
def neuron():
    #this is our neuron home page, just to interface with the neuron project
    # as shown in our consumer flyer.
    return app.send_static_file('neuron.html')


