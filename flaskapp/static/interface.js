// this is the javascript code
// used to manage the site
// as well as send data to our flask back-end 
// it is designed to be used between both the test and neuron pages
//

function send_button(pin_id,state){

	//build a JS Object to store our data to send
	var data_obj = {};
	data_obj.pin = pin_id;
	data_obj.state = state;

	
	//fetch the response to our POST request to "pin/<id>"
	fetch('pin/'+pin_id,{
		method: 'POST',
		body: JSON.stringify(data_obj),
		headers:{
			'Content-Type':'application/json; charset=utf-8'
		}
	})
	.then(function(response){return response.json();})
	.then(function(response){
		//what to do with the response
		// here we would test that the command completed
		// or if there was a response coming from the rpi
		// such as other project params
		console.log(response);

		// have a look at the below async get pin status call
		// to see the similarities and what we're doing in this
		// block of code. notice the "then" function
	});

}

function send_multi(dictionary){

	//special 'multi' route
	return fetch('pin/multi',{
		method: 'POST',
		body: JSON.stringify(dictionary),
		headers:{
			'Content-Type':'application/json; charset=utf-8'
		}
	})
	.then(function(response){return response.json();})
}


// this is an ASYNC pin status. it will fire and then continue
// executing code, this is perfect for slow network connections
// it will return a "Promise" which you attach a "THEN" function
// in the form of Promis.then(function(){};)
// have a look at the below wrappers for get_button

function get_async_pin_status(pin_id){
	//fetch the GET data from the server, located at pin/<id>
	return fetch('pin/'+pin_id,{
		method: 'GET',
		headers:{
			'Content-Type':'application/json; charset=utf-8'
		},
		body: null
	}).then(function(response){return response.json();});
}

//simple wrapper just to demonstrate some concepts


//generic button function to attach to html buttons
function get_button(pin_id){
	get_async_pin_status(pin_id).then(function(data){
		document.getElementById('pin12_status').innerHTML = data.state;
	});
}

//wrapper function that we can then set an interval for, notice that this has no//arguments
function refresh_pin16(){
	get_async_pin_status(16).then(function(data){
		document.getElementById('pin16_status').innerHTML = data.state;
	});
}

