# net_display
Simple web site for displaying sensor data, status information or other content.

The software is designed to be useful when implementing wireless displays; a networked screen that can be used to display sensor data or other content. The application could be run on a Raspberry Pi and used to make a networked display.

The software is written in python and uses the Tornado web framework (http://www.tornadoweb.org/en/stable/).

## Setup

Clone the repository to you desktop or Raspberry Pi, go to the root directory and run:

`pip install -r requirements.txt`

to install the dependencies - the tornado web framework and the requests module.

## Usage

Start the application from the root directory using

`python display.py`

Startup messages similar to those shown below will be displayed.

![startup messages](https://github.com/sinoia/net_display/raw/master/documentation/startup_messages.png)

The hostname will be the name of you host where the software is running. Once the software is running open a browser and visit the URL shown in the startup messages. The default display will be shown and it looks something like this:

![default display](https://github.com/sinoia/net_display/raw/master/documentation/default_screen.png)

The connection status is indicated by the socket status indicator at the top of the screen on the right. Green shows the socket is connected and red not connected. The display will only be updated when the socket is connected (green).

## Using the display

Once the display is running messages can be sent to be displayed. Messages are strings and are sent using an http PUT method to the API end point `/message`.

An easy way to use an http PUT is using curl, for example:

`curl -X PUT -d "Hello World" http://<hostname>:8888/message`

Where `<hostname>` is the name of the host running the display.

This http PUT will display the message `"Hello World"` on the display.

![default display](https://github.com/sinoia/net_display/raw/master/documentation/send_message.png)

## How It Works

The display screen is an html document containing two items that are displayed on the screen. These two items have an element `id`. The API URL contains the id of the element (`message`) and the PUT contains the contents for that element `"Hello World"`.

So the http PUT specifies that the item with the `id` of `message` should be changed (`put`) to the value `"Hello World"`.

Updates are made to the display using a web socket connection between the server and the display.

On the default page here are only two elements that can be changed, they are:
* ``` <h2 id="page_title">Network Display</h2>```
* ``` <div id="message"></div>```

So these two commands:
* `curl -X PUT -d "Weather Report" http://<hostname>:8888/page_title`
* `curl -X PUT -d "Today will be mostly sunny!" http://<hostname>:8888/message`
will result in a display that looks like this:

![Changing the title](https://github.com/sinoia/net_display/raw/master/documentation/title_change.png)

By default the application runs on port 8888, but this can be changed by passing the port number on the start command:

`python display.py --port=9999`

The examples directory includes some examples of using the API to display various types of information.

## Examples
### send_msg.sh
A simple script to send any message to the display. The message is passed as the first parameter to the script. The script is assumed to be running on the same host as the display.

`send_msg.sh Hello World`

## Display a Picture
The send_msg.sh script can be used to display images on your display. The message is set to an html image tag, the source being the URL to the image. The example below will show an nice landscape image from (https://www.pexels.com/)

`./send_msg.sh '<img src="https://images.pexels.com/photos/169738/pexels-photo-169738.jpeg?w=785&auto=compress&cs=tinysrgb" style="width:785px;">'`

![Raspberry Pi Hyperpixel!](https://github.com/sinoia/net_display/raw/master/documentation/hyperpixel_message.jpg)

The above net display is a Raspberry PI 2 with a HyperPixel hat running Chromium in kiosk mode. With this device on the local network it is a simple matter to display sensor data, images or notifications from any other host on the network.

## Build a Dashboard
It is possible to build dashboards using multiple updates to the `message` element. The example dashboard.py shows how this can be done.

First an html table is sent to the `/message` element. The element is updated with the html.

```python
html = '''
<table>
<tr><th>CPU</th><td id="cpu"></td></tr>
<tr><th>Memory</th><td id="mem"></td></tr>
<tr><th>Storage</th><td id="disc"></td></tr>
</table>
'''
r = requests.put(url+'/message', data = html)
```
This html creates three new element ids which can then be updated with values, like this:

```python
r = requests.put(url+'/cpu', data = '10')
r = requests.put(url+'/mem', data = '20')
r = requests.put(url+'/disc', data = '30')
```

The resulting display:

![Dashboard Example!](https://github.com/sinoia/net_display/raw/master/documentation/dashbooard_example.png)
