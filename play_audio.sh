#! /bin/bash

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