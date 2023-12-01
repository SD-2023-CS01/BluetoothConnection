#! /bin/bash
# sudo service ssh start
# pi's ip address = 10.0.0.177
# sudo apt install pulseaudio-module-bluetooth
# pulseaudio -k (might not be needed)
# pulseaudio --start

BLUETOOTH_MAC="F4:2B:7D:1C:17:C6"

# Connect to the Bluetooth device
bluetoothctl <<EOF
power on
agent on
connect $BLUETOOTH_MAC
EOF


aplay ./audio.wav

bluetoothctl <<EOF
disconnect $BLUETOOTH_MAC
power off
exit
EOF