# MRA Control

MRA Control is a command-line utility for controlling the gain and mute of MRA devices connected to your computer via USB. It uses the pyudev library to enumerate USB devices and identify MRA devices based on their vendor and product IDs.

## Requirements
Python 3.9 or higher
hidapi library

## Installation
Clone this repository and install the required packages:


    git clone https://github.com/geeks-r-us/mra-control.git
    cd mra_control
    python3 -m venv .venv
    source ./.venv/bin/activate
    pip install -r requirements.txt

To make the devices accessable for non root users you have to add a udev rule:

    sudo cp ./99-cm119-cmedia.rules /etc/udev/rules.d/99-cm119-cmedia.rules

## Usage

### List available devices
To list all available devices connected to the system, run:

    python ./mra_control.py list                    
    
### Mute / Unmute a device
To mute or unmute a device, run:

    python ./mra_control.py control --mute True/False /dev/hidraw<X>

### Standby / Activate
To put device to standby or make it active again, run:

    python ./mra_control.py control --standby True/False /dev/hidraw<X>

### Set gain factor
To change gain factor, run:

    python ./mra_control control --gain GAIN25_6dB /dev/hidraw<X>
    
Gain can beselected from the values GAIN25_6dB, GAIN31_6dB, GAIN35_6dB, GAIN37_6dB

### Http control
Devices are also controlable via http requests.

To use http requests, run:

    python ./server.py

Now you can control the device by GET requests like:

    wget http://localhost:8080/control?deviceid=<X>&mute=True

## Contributing
Feel free to contribute to this project by opening an issue or submitting a pull request.

Or support our work by buying one of our soundcards with or without amp in our online shop at [geeks-r-us](https://geeks-r-us.de/shop)
