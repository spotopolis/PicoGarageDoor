# PicoGarageDoor
Simple garage door opener controlled wirelessly via webpage



# Intro
This is a simple device that allows you to add wireless functionality to garage door control.
This project was a result of being a motorcycle rider and wanting to be able to open/close the garage to pull the bike in/out without having to either walk back into the house to open/close the garage or press the paired garage door controller button attached to the sun visor in my car. I do not have a garage door button panel outside of my garage, so I made this simple device to access the garage door from my phone while within my homes WiFi signal range.

# Parts list

Required:

Raspberry Pi Pico W [from Microcenter](https://www.microcenter.com/product/687384/raspberry-pi-pico-2-w) (( Should also work with a Pico 2W but has not been tested ) $6.99 USD at the time of writing )

Arduino v5 relay [from MicroCenter](https://www.microcenter.com/product/659887/inland-single-5v-relay-module-for-arduino) ($1.99 USD at the time of writing)

Project can be completed for under $10 USD with just these two components and some spare wire.
#

Optional:

To make the build a litle cleaner, use GPIO headers and some jumper wires.

Jumper wires [from Microcenter](https://www.microcenter.com/product/412198/leo-sales-ltd-jumpers,-premium-6-f-f,-50-wires) ( $14.99 USD at the time of writing )

GPIO right-angle header(s) [from Microcenter](https://www.microcenter.com/product/475249/schmartboard-inc-01-spacing-40-single-row-right-angle-headers-10-pack) ( $7.99 USD at the time of writing )



# Function
The PicoW hosts a small basic webserver via the code below:

<img width="778" height="339" alt="image" src="https://github.com/user-attachments/assets/5a957084-19fa-4740-9784-d78a803513ec" />


This in turn serves the following webpage:

![GDoor](https://github.com/user-attachments/assets/c784af8c-3046-4565-bc66-d1a3c445be5a)


The blue "Open/Close" button acts as a momentary switch to trigger a 5v relay attached directly to the PicoW via GPIO.

This function is handled here:

<img width="631" height="310" alt="image" src="https://github.com/user-attachments/assets/8188db1a-6afc-4cc0-a88d-2bcd92ab11a7" />

#

I discovered that during a power outage or power flicker during a storm, while the WiFi network and PicoW would come back online after power is restored, the PicoW would lose connection to the network and therefor could not host the webpage to interact with. It would only come back up if I power cycled the PicoW again by hand. So to try and fix this, I have also included some basic logic to test if the connection to the gateway is active, if it is not, it will reboot the PicoW to try and reestablish a connection.

The PicoW will wait initially 60 seconds on first boot before testing that the network is active to give the device time to connect. After 60 seconds, the PicoW will start to ping the gateway every 30 seconds. If the ping attempt fails, it will retry to ping the gateway 2 more times (3 in total) before triggering the reboot. This is to help mitigate any temp signals issues / interference along with the PicoW's lack of power to reboot on a false positive signal interruption. This code is handled here:


<img width="479" height="493" alt="image" src="https://github.com/user-attachments/assets/468694f3-ff66-4178-837e-e11f3e6af2cb" />


and here:


<img width="769" height="414" alt="image" src="https://github.com/user-attachments/assets/2e04e1c2-3d26-44ed-a260-3a1e1157ef9e" />



# Setup

Before uploading the main.py to the PicoW, edit the file at lines 7, 8, and 9. Fill in your SSID, password, and gateway IP. Thonny or NotePad++ can be used for the edits.

<img width="601" height="72" alt="image" src="https://github.com/user-attachments/assets/66652f99-039e-4cf9-b18e-fb3a100a82b4" />


Connections between the PicoW and relay are:

PicoW: VBUS <----> Relay: V

PicoW: GND  <----> Relay: G

PicoW: GP18 <----> Relay: S

#

Connect any 5v 1a USB charger to the PicoW's micro-USB port to power it on. Once the PicoW is powered on, it should get a local IP address assigned via DHCP from your firewall/router. You will want to log into your firewall/router and assign the PicoW a static IP address to make sure it doesn’t change on you and is always at the IP address you are expecting.

Once you select and set a static IP address for the PicoW in your firewall/router, power cycle the PicoW so it connects to your network with the newly assigned static IP.

Open a web browser on any device connected to the same WiFi network as the PicoW and browse to that static IP address. You should see the same page that I showed above under the "Function" section of this page. Tap or click the blue "Open/Close" button to verify the relay is triggering. You should hear it click on and then off while also getting an accompanying red LED to flash on the relay. If so, you are all set and ready to disconnect and attach it to your existing garage door button.

#

<img width="643" height="573" alt="gdoor3" src="https://github.com/user-attachments/assets/ee17f625-d70f-4c79-a007-7e4ff5784329" />

The relay can then be connected to your existing 2 wire garage door button via jumpers so that the button can still function while the relay is attached.
All this device is doing is acting like a 2nd garage door button attached to the same door. The garage door button is a momentary switch that seperates ( or bridges ) the connection between the two wires. By running jumper wires from the existing button to the relay, you are allowing a second button/switch ( the relay ) to trigger this function as well. Only instead of a physical button press, it is done via touchscreen on a mobile device on a private LAN hosted wepbage.


