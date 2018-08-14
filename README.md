rPi Project Controller
===
_Science and Learning_ Project 25

This is a extensible and hackable project controller that could form the basis of your project controlling needs. This repository contains an install script that automatically installs the dependencies for you, as well as sets up a `flask` app to run at log in.

With a mixture of _Javascript_ and _Python_, allow complete control of your `GPIO` pins through a web interface. This is meant to be more of an educational practice point, rather than a complete project in and of itself.

We've also provided an automatic touch screen set up in case you want to make a touch screen interface. This was originally going to be done using a python module called `appJar` which makes it easy to create software GUI applications. However when we had the web interface, we found it was easier and more consistent to use the chromium browser in `--kiosk` mode to render the web interface on the touch screen.

This is a simple project that is meant to be the bare bones for your project controlling needs. Definitely hackable, and comments have been provided in the code to help you form your own creations.

This software defaults to using 4 `GPIO` pins: `21`, `20`, `16`,`12` and sets up a fun interface to go with the Makeblock Neuron kit in this month's catalogue, (see also: [Makeblock Project]())

For any issues, suggestions or comments, feel free to message the project repository page, at http://github.com/duinotech/rPi-Project-controller/issues

# Bill of Materials:
| Qty | Code | Description |
|---|---|---|
|1 | [XC9000](jaycar.com.au/p/XC9000) | Raspberry Pi single board computer
|1 | [XC9024](jaycar.com.au/p/XC9024) | 5" Touch screen interface
|1 | [WC7724](jaycar.com.au/p/WC7724) | micro USB Lead
|1 | [MP3449](jaycar.com.au/p/MP3449) | 2.1A USB power supply.

Also a fresh Noobs Card if you do not have one already, or boot your own.

Note with the open-endedness of this project, you can easily substitute what you need. Additional ideas are presented at the bottom of this page.
# Assembly
If you are using the touch screen interface, be sure to connect the jumper wires before you attach the touch screen to the GPIO.

Boot up the rPi into a fresh raspbian install and type the following commands into a new terminal window:
```bash
git clone http://github.com/duinotech/rPi-Project-controller
./rPi-Project-Controller/install.py
```

this will prompt you if you are using the recommended touch screen, whether you want portrait or landscape mode, or if you will provide your own screen.

Note that the web-interface will still work regardless, accessed through the IP of the raspberry pi.

# Software Libraries and Downloads
The install script will download everything for you, but just as a reference:

|Git Repository|Author| Link |
| --- | --- | --- |
|LCD-show| goodtft| http://github.com/goodtft/LCD-show/ |

##### Python Libraries
* `flask` and dependencies
* `gitpython` and dependencies

# Programming - for the curious.
As the install script installs and sets up everything for you, I'll instead talk about the various technologies and layout of the system.

If you want to use the default "Feed the cat" program, you can just leave the project as it is, however if you are aiming to modify it to your own needs, here is a collection of information to start you out with your modifications. Remeber that [StackOverflow](https://stackoverflow.com/) and google are going to be your friends here.
#### System
* `./flaskapp/*` this folder is the folder containing the flask app module that is ran by python-flask.
  * [Flask](http://flask.pocoo.org/docs/0.12/quickstart/) is a python framework that provides an easy way to make HTTP routes in python program, or what's called a **Web Server Gateway Interface**


* `REST` The Rest API is actually more of an idea, or method, rather than a specific set of tools. You can read more about the specifics on the [Wikipedia Page](https://en.wikipedia.org/wiki/Representational_state_transfer) or some [Design Documents](https://www.mulesoft.com/resources/api/what-is-rest-api-design) but really all you need to know is that REST is a method that uses the standard HTTP protocol to communicate between services.
  * In our set up, the webpage is a "service" that connects to our flask app through a REST api, and then changes the page depending on the results.
  * This makes it easy to separate the rPi/Python application and the website, as we could easily create more apps, such as a phone application, that uses the same method to communicate to the flask app.


#### RestAPI Example
An example of a REST Api:

some service, such as a phone or web app, sends a HTTP request to `somewebsite`:
```javascript
GET api.somewebsite.com/users/436345645
```
the `api.somewebsite.com` then returns a bunch of data relating to a user (presumably) with the ID of `436345645` - it does not return a web-page.

```javascript
received: {'real name': 'Kevin Doe', 'age': 43}
```
Then if the app wants to change information, it can then `POST` the data back:
```javascript
POST api.somewebsite.com/users/436345645
BODY: { 'real name': 'John Doe'}
```
the web service (`api.somewebsite.com`) is responsible for managing data sent to and from the API.

* `JSON` ties in closely with REST, and stands for "JavaScript Object Notation" - it can bundle data together (much like a python dictionary, if you are familiar with Python) and is easy to convert between JSON and string objects. In the example above, the data sent back is a Javascript object: `{'real name': 'John Doe'}`, Note that Javascript objects are surrounded by `{}` characters, much like Python dictionaries.

In our example program "somewebsite" is our flask app, and we have a seperate HTML website that provides a Javascript web-application. (although, somewhat confusingly, it is also hosted by our flaskapp).


## About this 'Feed the Cat' Example Program

if you have a look through the source code of the flask app, you will find ( in `button.py`):

```python
@app.route('/pin/multi', methods=['POST'])
def multi():
  data = request.get_json(force=True)
```
This is the code relating to the 'http://localhost/pin/multi' route in our web service. We get the data in the form of a python dictionary by translating the request's json data.

The data that is sent to this particular point should be in the form of:
```javascript
{
  '12': true,
  '54': false,
  //etc
}
```
and will set the direction of the pins to what is specified in the JSON object. you can change this function to provide pin outputs (high or low as true or false)

the corresponding action on the javascript webapp is:
```JavaScript
//send multiple pins, as specified in the dictionary
function send_multi(dictionary){
	return fetch('pin/multi',{ //fetch the 'website/pin/multi' point
		method: 'POST', //post request
		body: JSON.stringify(dictionary), //note the body of the request is using JSON converted to string
		headers:{
			'Content-Type':'application/json; charset=utf-8'
		}
	}) //async response, we need a .then to tell it what to do when it's ready.
	.then(function(response){return response.json();})
}
```

it is used by:
```javascript
var data = {
  '14' = false;
};
//can also change data after variable creation
data['12'] = true;

//now data is a JS object, specifying two pins.
//we can use the send_multi as defined above:
send_multi(data).then(function(response){
  //do something with the response data
  console.log(response);
  //if the response has a status we could do something like
  if(response.status == 'OK'){
    //command completed ok
  }
  else{
    //command failed
  }
})
```

The individual pin route:
```python
@app.route('/pin/<int:pin_id>', methods=['GET','POST'])
def pin(pin_id):
```
is similarly set up, however we use both `GET` and `POST`

* `GET` is to return the status of the pin, or to read the pin.
* `POST` is to set the pin, high or low, depending on the data.

this route is also changeable, as the `<int:pin_id>` stands for any route that ends with a number. that number is then passed into our python function.

ie:

`POST localhost/pin/32 BODY: {'state':true}` - set pin 32 to high

`GET localhost/pin/43` - get the state of pin 43


Hopefully, reading through this quick run down and comments provided in the script files, you should have a basic understanding of what's going on, and have enough juice left in you to start hacking your own project controller.

# Future Improvements
* Use [YN8416 PoE splitter](http://jaycar.com.au/p/YN8416) in your projects so that you can power the Raspberry pi through a PoE router.
* The script is largely incomplete, but make more functions to read from different sensors and attach them to separate mount points in the interface, for instance you could attach a relay board, and then create a mount point in the form of:
```python
@app.route('/relay/<int:relay_number>', methods=['GET','POST'])
def activate_relay(relay_number):
    #your code here
```
