# tasker
A task distribution system based on rabbitmq message queue. Assigned tasks are asynchronously performed by subscribed endpoints (worker).
For every task type (configurable) the api takes a customers request, create a new task and send the task to the endpoints by the amqp publish/subscribe pattern. On receiving the task, the endpoints create a task-response in the database, perform the task and update the task-response after finishing the task. The customer can get the tasks status and responses by request the api.

## Installation (currently untested!)

Prerequisite:
* mysql user/database named tasker
* rabbitmq user/vhost named tasker 

Clone to an arbitrary folder
 
	git clone git@github.com:MatthiasWiesner/tasker.git 


In the folder run:

	python bootstrap.py


An executable script `bin/buildout` should be created. After run this script all necessary libraries should be downloaded. Further, some executable scripts are created:

* `bin/initialize`: run this script to initialize (or reset) the database tables and rabbitmq vhost
* `bin/supervisord`: run this script to start the supervisor daemon. The supervisord daemon will start and control the api and the manager according to the configuration in `buildout.cfg` (supervisord section)
* `bin/supervisorctl`: supervisor control (for more information see [supervisord.org](http://supervisord.org/))
* `bin/api`: run this script to start the api (for debug running)
* `bin/manager`: run this script to start the task manager (for debug running)

## Configuration
To configure tasker you have to edit the configuration yaml file according to the run mode. The configuration file is located in `config/<run_mode>.config.yaml`.

In this file are the settings:
* task type: For each task type a separate exchange and api handler will be created. Furthermore, for each task type can have multiple workers subscribe on to the exchange. Set this as a list of strings
* `api.port`: set the port
* `api.wait_for_endpoints_timeout`: time in which all endpoints should received the task
* `manager.db.verbose`: verbose flag (unused)
* `manager.db.uri`: mysql uri
* `manager.message_queue.*`: several rabbitmq preferences
* `rabbitmq.*`: rabbitmq settings to initialize/reset the rabbitmq user/vhost (superuser permissions required!).

## Api
The requests api url is `http://<host>:<port>/<task_type>`

A task can be assigned by POST requesting the restful api. 
The requests content-type has to be "application/json". The requests body has to be a json object (example data):

	{
	   "identifier":"e7bd91d0-16ad-11e2-892e-0800200c9a66",
	   "payload":{
		  "foo":"bar"
	   },
	   "endpoints":[
		  "loadbalancer-1",
		  "loadbalancer-2"
	   ]
	}

* identifier: is a mandatory customers task identifier
* payload: are optional customers data to perform the task
* endpoints: are a optional list of known endpoints they perform the task.
  If the list is given, then it is checked whether all endpoints have been received the task. If an endpoint has not been given the task, then the task is marked as incomplete. At the current status, there is no retry mechanism.

The response is the created task as json object.


The tasks status can be retrieved with a GET request `http://<host>:<port>/<task_type>/<task_id>`. The responses content-type is "application/json", the body contains the task and the endpoints responses (after perform the task) as a json object. 

## Endpoint
On the endpoint the handler must be implemented according to the customer needs. For it in the `manager.handler` package, a module with the task-types name must be created and the `handle_task` function implemented.

## Use case
* Your web based administration software requires to do a long time job (> webservers timeout).
* you have to do an application update on a greater list of server


# Author
Matthias Wiesner (matthias.wiesner@googlemail.com)
