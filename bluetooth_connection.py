import subprocess
import time

BLUETOOTH_MAC = "F4:2B:7D:1C:17:C6"
CONNECT_RETRY_INTERVAL = 5  # seconds
MAX_CONNECT_ATTEMPTS = 10

def is_device_paired():
    command = f"bluetoothctl info {BLUETOOTH_MAC}"
    output = execute_command(command)
    return f"Device {BLUETOOTH_MAC}" in output

def is_device_connected():
    command = f"bluetoothctl info {BLUETOOTH_MAC}"
    output = execute_command(command)
    return "Connected: yes" in output

def connect_to_device():
    command = f"bluetoothctl <<EOF\npower on\nagent on\nconnect {BLUETOOTH_MAC}\nEOF"
    output = execute_command(command)
    return "Connection successful" in output

def play_audio():
    subprocess.run(["aplay", "./audio.wav"])

def execute_command(command):
    process = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

def main():
    if is_device_paired():
        connect_attempts = 0
        while connect_attempts < MAX_CONNECT_ATTEMPTS:
            if is_device_connected():
                print("Device is already connected.")
                play_audio()
                break
            else:
                connect_attempts += 1
                print(f"Attempting to connect (Attempt {connect_attempts})...")
                if connect_to_device():
                    print("Connected successfully.")
                    play_audio()
                    break
                else:
                    print("Failed to connect. Retrying in {} seconds...".format(CONNECT_RETRY_INTERVAL))
                    time.sleep(CONNECT_RETRY_INTERVAL)
        else:
            print(f"Max connection attempts reached ({MAX_CONNECT_ATTEMPTS}). Exiting.")
    else:
        print("Device is not paired. Please pair the device first.")

if __name__ == "__main__":
    main()