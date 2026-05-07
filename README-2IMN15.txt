README for getting started with Leshan within the course 2IMN15 (IoT)

Leshan is the Java based LWM2M implementation of Eclipse.
For the 2IMN15 course, the Leshan client and server demo
applications are extended with scenario specific logic and
custom object definitions.  Modifications to the original
Leshan code are marked with "2IMN15" in a comment.


=== Assignment ===

For the 2IMN15 assignment, relevant code segments where
modifications are expected are marked with a comment

    // 2IMN15:  TODO  :  fill in

Modifications are required in the client and server applications.

In leshan-client-demo/src/main/java/org/eclipse/leshan/client/demo/
   Luminaire.java
	display the status of the luminaire.
   PresenceDetection.java
	implement a method to simulate presence detection.

In leshan-server-demo/src/main/java/org/course/
   RoomControl.java
	implement the application scenarios.


=== Compilation ===

To compile the Java code, use the command

	mvn install -P CompileOnly

Maven (mvn) is a Java build environment. If your system doesn't have
it, you can follow the general instructions on compiling Leshan.
After the compilation is finished, the server and client are
available in leshan-server-demo/target en leshan-client-demo/target.


=== Testing ===

To test the application, start a server and one or more clients.
In seperate terminals, use the commands

   java -jar leshan-server-demo/target/leshan-server-demo-2.0.0-SNAPSHOT-jar-with-dependencies.jar

   java -jar leshan-client-demo/target/leshan-client-demo-2.0.0-SNAPSHOT-jar-with-dependencies.jar -n client1 [-presence]  [-luminaire] [-demand]

For the client, the options -presence, -luminaire and -demand activate
those LWM2M objects.  Use the option -h to see which other options are
available.

For more convenient testing, you can put the relevant commands in
batch scripts for your preferred platform.

NOTE: the Java applications listen to network ports. Depending on your
      platform, the Java application might be blocked to open the network
      port (and print an error message) or the firewall might block
      the communication. 


=== Presence Detection Input Modes ===

The PresenceDetector client chooses its input interface automatically:

1. Sense HAT joystick (Raspberry Pi only)
   When "sensehat_joystick.py" is found in the working directory AND the
   sense-hat Python library is available, the Sense HAT joystick is used.
   - Press the centre/middle button to manually toggle presence ON/OFF.
   - Press up/down/left/right to simulate motion detection:
     presence turns ON and automatically turns OFF after 3 seconds without
     further movement (movement resets the 3-second timer).
   - During motion-triggered ON state, a heart is shown on the Sense HAT
     LED matrix (requires "sensehat_display.py" in the working directory).

2. Swing GUI button (desktop platforms: Mac, Windows, Linux with display)
   A small window with a "Toggle Presence" button appears automatically
   when no Sense HAT script is available but a graphical display is present.

3. Timed auto-toggle (headless / CI fallback)
   When neither a Sense HAT nor a graphical display is available, presence
   is toggled automatically every 10 seconds.


=== Running on Raspberry Pi with Sense HAT ===

--- Prerequisites ---

1. Java (JRE 11 or later):
      sudo apt update
      sudo apt install -y default-jre

2. Python sense-hat library (usually pre-installed on Raspberry Pi OS):
      sudo apt install -y sense-hat
   If not available via apt, use pip:
      pip3 install sense-hat

--- Copy files to the Pi ---

From your Mac/PC (replace <PI_IP> with the Pi's IP address, e.g. 10.30.32.227):

   scp leshan-client-demo/target/leshan-client-demo-2.0.0-SNAPSHOT-jar-with-dependencies.jar \
       pi@<PI_IP>:/home/pi/

   scp sensehat_joystick.py  pi@<PI_IP>:/home/pi/
   scp sensehat_display.py   pi@<PI_IP>:/home/pi/
   scp sensehat_lamp.py      pi@<PI_IP>:/home/pi/

--- Start the server on your Mac/PC ---

   java -jar leshan-server-demo/target/leshan-server-demo-2.0.0-SNAPSHOT-jar-with-dependencies.jar

Note your Mac/PC IP address (e.g. 10.30.51.20):
   macOS: ipconfig getifaddr en0
   Linux: hostname -I

--- Start the PresenceDetector client on the Pi ---

SSH into the Pi:
   ssh pi@<PI_IP>

Then run (replace <MAC_IP> with your server's IP):
   cd /home/pi
   java -jar leshan-client-demo-2.0.0-SNAPSHOT-jar-with-dependencies.jar \
        -n presencePi -presence -u coap://<MAC_IP>:5683

The client will print:
   [PresenceDetector] Sense HAT joystick active. Middle press toggles presence; movement triggers 3s motion mode.

--- Demo flow ---

1. Open the Leshan Web UI at http://<MAC_IP>:8080/
2. "presencePi" should appear in the client list.
3. Press the Sense HAT middle button → presence toggles true/false.
   Press up/down/left/right → presence turns true for 3 seconds after last movement.
4. Luminaire clients (lum1, lum2 …) will turn on/off automatically,
   and the Sense HAT LED matrix on the Pi will light up/dim/turn off.
5. Change the Demand Response "Total Allowed Peak Room Power" value in the
   UI → luminaire dim levels update automatically and the LED brightness
   changes accordingly.

--- Start the Luminaire client on the Pi ---

SSH into the Pi and run (replace <MAC_IP> with your server's IP):

   cd /home/pi
   java -jar leshan-client-demo-2.0.0-SNAPSHOT-jar-with-dependencies.jar \
        -n lumPi -luminaire -u coap://<MAC_IP>:5683

When sensehat_lamp.py is present in the working directory and the
sense-hat Python library is installed, the Sense HAT LED matrix will
automatically reflect the luminaire state:
  - Power ON  → full 8x8 matrix lit at the current dim brightness.
  - Power OFF → matrix cleared.
  - Dim level changed while ON → matrix brightness updated (0 = dark, 100 = full white).

--- Firewall notes ---

On macOS you may be prompted to allow incoming network connections for Java.
Click Allow.  If blocked, go to System Settings → Network → Firewall and
allow Java, or temporarily disable the firewall for testing.


=== Modifications to Leshan ===

For the 2IMN15 course, the following modifications were applied to
the standard Leshan code (compared to its git repository). If your
implementation requires additional modifications, you can check
those files first.

 * LeshanClientDemo.java  creates additional objects based on
   command line options.
 * LeshanClientDemoCLI.java  specifies additional command line
   options for luminaire, presence detector and demand response.
 * LwM2mDemoConstant.java  specifies application specific
   LWM2M objects.
 * ClientServlet.java  initializes the RoomControl.
 * EventServlet.java  passes on events to RoomControl.

In addition, the LWM2M object models (in XML format) for
Luminaire, PresenceDetector and DemandResponse are provided
in leshan-core-demo/src/main/resources/models/3300?.xml
and leshan-client-demo/src/main/resources/models/ .

Summaries of the modifications are provide in the files 
git-diff.txt and git-status.txt.
