# net_display
Simple web site for displaying sensor data, status information or other content.

The software is designed to be useful when implementing wireless displays; a networked screen that can be used to display sensor data or other content. The software can be run on a Raspberry Pi and used to make a networked display.

The software is written in python and uses the Tornado web framework (http://www.tornadoweb.org/en/stable/).

## Setup

Clone the repository to you desktop or Raspberry Pi, go to the root directory and run:

`pip install -r requirements.txt`

to install the dependencies (the tornado web framework).

## Usage

Start the application from the root directory using

`python display.py`

Startup messages similar to those shown below will be displayed.

![startup messages](https://github.com/sinoia/net_display/raw/master/documentation/startup_messages.png)

The hostname will be the name of you host where the software is running. Once the software is running open a browser and visit the URL shown in the startup messages. The default display will be shown and it looks something like this:

![default display](https://github.com/sinoia/net_display/raw/master/documentation/default_screen.png)

The connection status is indicated by the socket status indicator at the top of the screen on the right. Green shows the socket is connected and red not connected. The display will only be updated when the socket is connected (green).

## Using the display

Once the display is running messages can be sent to be displayed. Messages are strings and are sent using an http PUT method to the API end point `/msg`.

An easy way to use an http PUT is using curl, for example:

`curl -X PUT -d "Hello World" http://<hostname>:8888/msg`

Where `<hostname>` is the name of the host running the display.

This http PUT will display the message `"Hello World"` on the display.

![default display](https://github.com/sinoia/net_display/raw/master/documentation/send_message.png)

## How It Works

The `/msg` API end point is simply a synonym for this API call:

`curl -X PUT -d "Hello World" http://<hostname>:8888/update/message`

The display screen is an html document containing a few items that are displayed on the screen. Each of these items has an element `id`. The URL to the API contains the id of the element (`message`) and the contents for that element `"Hello World"`.

So the http PUT specifies that the item with the `id` of `message` should be changed (`update`) to the PUT value `"Hello World"`.

Updates are made to the display using a web socket connection between the server and the display. The red/green indicator shows the status of the web socket connection disconnected/connected.

There are only two elements that can be changed, they are:
* ``` <h2 id="page_title">Network Display</h2>```
* ``` <div id="message">```

So these two commands:
* `curl -X PUT -d "Raspberry Pi HyperPixel Display" http://<hostname>:8888/update/page_title`
* `curl -X PUT -d "Today will be mostly sunny!" http://<hostname>:8888/update/message`
will result in a display that looks like this:

![Raspberry Pi Hyperpixel!](https://github.com/sinoia/net_display/raw/master/documentation/hyperpixel_message.jpg)

The above image is a Raspberry PI 2 with a HyperPixel hat running Chromium in kiosk mode. With this device on the network it is a simple matter to display sensor data as it is collected.

By default the application runs on port 8888, but this can be changed by passing the port number on the start command:

`python display.py --port=9999`

The examples directory includes some examples of using the API to display various types of information.

## Examples
### send_msg.sh
A simple script to send any message to the display. The message is passed as the first parameter to the script. The script is assumed to be running on the same host as the display.

`send_msg.sh Hello World`
