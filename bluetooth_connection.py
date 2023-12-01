# sudo service ssh start
# pi's ip address = 10.0.0.177


# sudo apt install pulseaudio-module-bluetooth
# pulseaudio -k (might not be needed)
# pulseaudio --start


import subprocess
import time

BLUETOOTH_MAC = "F4:2B:7D:1C:17:C6"
CONNECT_RETRY_INTERVAL = 5  # seconds
MAX_CONNECT_ATTEMPTS = 10

def is_device_paired():
    command = f"bluetoothctl info {BLUETOOTH_MAC}"
    output = execute_command(command)

    return not f"Device {BLUETOOTH_MAC} not available" in output

def is_device_connected():
    command = f"bluetoothctl info {BLUETOOTH_MAC}"
    output = execute_command(command)
    return "Connected: yes" in output

def connect_to_device():
    command = f"bluetoothctl <<EOF\npower on\nagent on\nconnect {BLUETOOTH_MAC}\nEOF"
    output = execute_command(command)
    return "Connection successful" in output

def play_audio():
    subprocess.run(["aplay", "./audio_messages/*"])
    subprocess.run(["rm", "./audio_messages/*"])

def execute_command(command):
    process = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

def is_device_in_paired_list():
    command = "bluetoothctl paired-devices"
    output = execute_command(command)
    return BLUETOOTH_MAC in output

def main():
    connect_attempts = 0
    if not is_device_in_paired_list():
        while connect_attempts < MAX_CONNECT_ATTEMPTS:
            print("Device is not paired. Attempting to pair...")
            print(connect_attempts)
            if connect_attempts == 0:
                pair_command = f"bluetoothctl <<EOF\npower on\nagent on\nscan on\npair {BLUETOOTH_MAC}\nEOF"
            else:
                pair_command = f"bluetoothctl <<EOF\npair {BLUETOOTH_MAC}\nEOF"
            pair_output = execute_command(pair_command)
            connect_attempts = connect_attempts + 1
            print(pair_command)

            time.sleep(CONNECT_RETRY_INTERVAL)
            if is_device_in_paired_list():
                print("Device paired successfully.")
                break
            else:
                print("Failed to pair the device.")
            
    connect_attempts = 0
    while connect_attempts < MAX_CONNECT_ATTEMPTS:
        if is_device_connected():
            print("Device connected, playing audio...")
            play_audio()
            break
        else:
            connect_attempts += 1
            print(f"Attempting to connect (Attempt {connect_attempts})...")
            if connect_to_device():
                print("Connected successfully, playing audio...")
                play_audio()
                break
            else:
                print("Failed to connect. Retrying in {} seconds...".format(CONNECT_RETRY_INTERVAL))
                time.sleep(CONNECT_RETRY_INTERVAL)
    else:
        print(f"Max connection attempts reached ({MAX_CONNECT_ATTEMPTS}). Exiting.")



if __name__ == "__main__":
    main()