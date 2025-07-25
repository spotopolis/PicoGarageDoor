from machine import Pin, reset, Timer
import network
import time
import usocket as socket

# Wi-Fi credentials
SSID = "YOUR_WIFI_NAME_HERE"
PASSWORD = "WIFI_PASSWORD_HERE"
GATEWAY_IP = "ROUTER_IP_ADDRESS_USUALLY_192.168.1.1_OR_SIMILAR"

# Relay and onboard LED setup
relay = Pin(18, Pin.OUT)
led = Pin("LED", Pin.OUT)

# Flash LED on boot
led.on()
time.sleep(0.5)
led.off()

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait up to 60s for Wi-Fi
start = time.time()
while wlan.status() != 3 and (time.time() - start) < 60:
    print("Waiting for Wi-Fi...")
    time.sleep(1)

if wlan.status() != 3:
    print("Wi-Fi failed. Soft rebooting...")
    reset()
else:
    print("Connected. IP:", wlan.ifconfig()[0])
time.sleep(5)

# Gateway ping check
def ping(ip=GATEWAY_IP, timeout=3):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, 80))
        sock.close()
        return True
    except:
        return False

# Schedule reboot
def delayed_reboot(timer):
    print("Soft rebooting...")
    s.close()
    reset()

# Web UI content
def web_server():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{font-family:Arial;text-align:center;margin:0;padding-top:30px;}
    .button{display:inline-block;width:200px;height:68px;background-color:#2196F3;
    color:white;border:none;border-radius:34px;font-size:24px;cursor:pointer}</style>
    <script>
    function pressButton() {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/?relay=off", true);
        xhr.send();
        setTimeout(function() {
            xhr.open("GET", "/?relay=on", true);
            xhr.send();
        }, 500);
    }
    </script></head><body>
    <h1>Garage Door Control</h1>
    <button class="button" onclick="pressButton()">Open/Close</button>
    </body></html>"""
    return html

# Start web server
s = socket.socket()
s.setblocking(False)
s.bind(('', 80))
s.listen(1)

fail_count = 0
max_failures = 3
last_ping = time.time()

try:
    while True:
        # Periodic ping
        if time.time() - last_ping > 30:
            if ping():
                print("Ping OK")
                fail_count = 0
            else:
                print("Ping failed")
                fail_count += 1
                if fail_count >= max_failures:
                    print("Too many failures. Reboot scheduled.")
                    Timer(-1).init(mode=Timer.ONE_SHOT, period=3000, callback=delayed_reboot)
            last_ping = time.time()

        try:
            conn, addr = s.accept()
            conn.settimeout(3)
            print("Connection from", addr)
            request = conn.recv(1024)
            print("Request:", request)

            if b"/?relay=on" in request:
                relay.value(0)
                print("RELAY ON")
            elif b"/?relay=off" in request:
                relay.value(1)
                print("RELAY OFF")

            response = web_server()
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            conn.sendall(response)
            conn.close()

        except OSError:
            pass

except KeyboardInterrupt:
    print("Interrupted by user. Closing socket...")
    s.close()
    raise
