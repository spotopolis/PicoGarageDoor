# PicoGarageDoor
Simple garage door opener controlled wirelessly via webpage



# Intro
This is a simple device that allows you to add wireless functionality to garage door control.
This project was a result of being a motorcycle rider and wanting to be able to open/close the garage to pull the bike in/out without having to either walk back into the house to open/close the garage or press the paired garage door controller button attached to the sun visor in my car. I do not have a garage door button panel outside of my garage, so I made this simple device to access the garage door from my phone while within my homes WiFi signal range.



# Function
The PicoW host a small basic webserver via the code below:

<img width="778" height="339" alt="image" src="https://github.com/user-attachments/assets/5a957084-19fa-4740-9784-d78a803513ec" />


This in turn serves the following webpage:

![GDoor](https://github.com/user-attachments/assets/c784af8c-3046-4565-bc66-d1a3c445be5a)


The blue "Open/Close" button acts as a momentary switch to trigger a 5v relay attached directly to the PicoW via GPIO.

This function is handled here:

<img width="631" height="310" alt="image" src="https://github.com/user-attachments/assets/8188db1a-6afc-4cc0-a88d-2bcd92ab11a7" />


I discovered that during a power outage or power flicker during a storm, while the WiFi network and PicoW would come back online after power is restored, the PicoW would lose connection to the network and therefor could not host the webpage to interact with. It would only come back up if I power cycled the PicoW again by hand. So to try and fix this, I have also included some basic logic to test if the connection to the gateway is active, if it is not, it will reboot the PicoW to try and reestablish a connection.

The PicoW will wait initially 60 seconds on first boot before testing that the network is active to give the device time to connect. After 60 seconds, the PicoW will start to ping the gateway every 30 seconds. If the ping attempt fails, it will retry to ping the gateway 2 more times (3 in total) before triggering the reboot. This is to help mitigate any temp signals issues / interference along with the PicoW's lack of power to reboot on a false positive signal interruption. This code is handled here:


<img width="479" height="493" alt="image" src="https://github.com/user-attachments/assets/468694f3-ff66-4178-837e-e11f3e6af2cb" />


and here:


<img width="769" height="414" alt="image" src="https://github.com/user-attachments/assets/2e04e1c2-3d26-44ed-a260-3a1e1157ef9e" />



# Setup / How to use
Before uploading the main.py to the PicoW, edit the file at lines 7, 8, and 9. Fill in your SSID, password, and gateway IP.

<img width="601" height="72" alt="image" src="https://github.com/user-attachments/assets/66652f99-039e-4cf9-b18e-fb3a100a82b4" />

The relay module used was a single Arduino v5 relay from MicroCenter

![SRD-05VDC-SL-C](https://github.com/user-attachments/assets/a32ba4f3-7a18-4d65-876f-cc1dd4f3ca5d)

Connections between the PicoW and relay are:
PicoW: VBUS <----> Relay: V
PicoW: GND  <----> Relay: G
PicoW: GP18 <----> Relay: S

The relay can then be connected to your existing 2 wire garage door button via jumpers so that the button can still function while the relay is attached.

