from flask import request,make_response,jsonify
import RPi.GPIO as GPIO


from flaskapp import app


# this is a new route in our HTML webapp for a variable of pins
# for example:
# make a 'route' for localhost/pin/18 to point to the GPIO pin 18

@app.route('/pin/multi', methods=['POST']) # neuron only works one way so we won't worry about GET
def multi():
    data = request.get_json(force=True);
    print(data)

    #set a simple mood case, ideally you'd get a response from the system
    # but the makeblock can't respond to us, so we'll just set and forget

    for x in data.keys():
        GPIO.setup(int(x),GPIO.OUT if data[x] else GPIO.IN);



    pin = [x for x in data.keys() if data[x]][0] #get the true value

    if pin == '12':
        mood = 'angry'
        response = "I don't like this"
    elif pin == '16':
        mood = 'sad'
        response = "Too much sugar"
    elif pin == '20':
        mood = 'crazy'
        response = "Whoooop whoooooooop"
    elif pin == '21':
        mood = 'happy'
        response = "Yay I love bugs"

    else:
        print('unknown pin value') # shouldn't get here, but I'm sure you're playing around



    outgoing = {'mood': mood,'text':response} 
    return jsonify(outgoing);

@app.route('/pin/<int:pin_id>', methods=['GET','POST'])
def pin(pin_id):

    #simple check to see if it is actually a pin id
        # note that this doesn't check bounds, only for int

        try:
            pin_id = int(pin_id)
        except ValueError as e:
            return make_response(
                    jsonify({'error':str(e)},
                        404))


        ##############################################
        # check if the HTML request is a GET, which 
        # we then return the current state in a json response
        ##############################################
        if request.method =='GET':
            
            #python dict to represent data
            data = {
                    'pin': pin_id,
                    'state': GPIO.input(pin_id)
                    }

            print('request the pin from GPIO, sending back:')
            print(data)

            return make_response(jsonify(data),200)


        ##############################################
        # This is a html POST, which means the user has POSTED
        # data to the app, (simple bool) so we can set
        # the pin to what the bool is
        ##############################################
        if request.method == 'POST':
            incoming = request.get_json(force=True)

            print('set the data for GPIO pin:',pin_id)
            print(incoming) #this is a python dict
   
            GPIO.output(pin_id,incoming['state'])

            response = {
                    'pin': pin_id,
                    'state': GPIO.input(pin_id),
                    'status': 'command completed successfully'
                    }

            return make_response(jsonify(response),200)

