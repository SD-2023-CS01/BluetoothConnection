import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class BluetoothConnection {

    private static final String BLUETOOTH_MAC = "F4:2B:7D:1C:17:C6";

    public static void main(String[] args) {
        // Check if the device is already paired or connected
        if (!isDevicePairedOrConnected()) {
            // If not, try to connect
            if (connectToDevice()) {
                System.out.println("Connected successfully.");
                playAudio();
                disconnectDevice();
            } else {
                System.out.println("Failed to connect.");
            }
        } else {
            System.out.println("Device is already paired or connected.");
        }
    }

    private static boolean isDevicePairedOrConnected() {
        String command = "bluetoothctl info " + BLUETOOTH_MAC;
        return executeCommand(command).contains("Device " + BLUETOOTH_MAC);
    }

    private static boolean connectToDevice() {
        String command = "bluetoothctl <<EOF\npower on\nagent on\nconnect " + BLUETOOTH_MAC + "\nEOF";
        return executeCommand(command).contains("Connection successful");
    }

    private static void playAudio() {
        executeCommand("aplay ./audio.wav");
    }

    private static void disconnectDevice() {
        String command = "bluetoothctl <<EOF\ndisconnect " + BLUETOOTH_MAC + "\npower off\nexit\nEOF";
        executeCommand(command);
    }

    private static String executeCommand(String command) {
        StringBuilder output = new StringBuilder();

        try {
            Process process = new ProcessBuilder("bash", "-c", command).start();
            process.waitFor();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return output.toString();
    }
}