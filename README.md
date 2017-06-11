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
