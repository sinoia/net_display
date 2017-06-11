# net_display
Simple web site for displaying sensor data, status information or other content.

The software is designed to be useful when implementing wireless displays; a networked screen that can be used to display sensor data or other content. The software runs well on a Raspberry Pi which can be used to make a good networked display.

The software is written in python and use the Tornado web framework (http://www.tornadoweb.org/en/stable/).

## Setup

Clone the repository to you desktop or Raspberry Pi, go to the root directory and run and run `pip install -r requirements.txt` to install the dependencies (the tornado web framework).

## Usage

Start the application from the root directory using `python display.py`, startup messages similar to those shown below will be displayed.

![startup messages](https://github.com/sinoia/net_display/raw/master/documentation/startup_messages.png)

The hostname will be the name of you host where the software is running. Once the software is running open a browser and enter the url shown. The default display will be displayed something like this:

![default display](https://github.com/sinoia/net_display/raw/master/documentation/default_screen.png)

By default the application runs on port 8888, but this can be changed by passing the port number on the start command: `python display.py --port=9999`

## Using the display

Once the display is running messages can be sent to be displayed. Messages are json strings and are sent using an http PUT method to the API end point `/msg`.

An easy way to use an http PUT is using curl, for example:

`curl http://<hostname>:8888/msg -XPUT -d '{"id": "message", "message": "Hello World"}'`

Where `<hostname>` is the name of the host running the display.

This http PUT will display the message `"Hello World"` on the display.

![default display](https://github.com/sinoia/net_display/raw/master/documentation/send_message.png)

## How It Works

The display screen is an html page containing a few items to be displayed on the screen. Each of these items has an element `id`. The json http PUT to the API contains the id of the element and the contents for that element.

There are only two elements that can be changed, they are:
* ```html <h2 id="page_title">Network Display</h2>```
* ```html <div id="message">```

So these two commands:
`curl http://<hostname>:8888/msg -XPUT -d '{"id": "page_title", "message": "Raspberry Pi HyperPixel Display"}'`
`curl http://<hostname>:8888/msg -XPUT -d '{"id": "message", "message": "Today will be mostly sunny!"}'`
will result in a display that looks like this:

![Raspberry Pi Hyperpixel!](https://github.com/sinoia/net_display/raw/master/documentation/hyperpixel_message.png)

The above image is of a Raspberry PI 2 with a HyperPixel hat running Chromium in kiosk mode. With this device on the network it is quick and easy to display sensor data as it is collected.

## Examples
The examples directory of the repository includes some examples of interacting with the display.
