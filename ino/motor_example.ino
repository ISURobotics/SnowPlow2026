/*
  Simple Example motor control for SRX. Try this test sketch with the Servo library to see how your
 ESC responds to different settings, type a speed (1000 - 2000)
 in the top of serial monitor and hit [ENTER], start at 1500
 and work your way toward 1000 50 micros at a time, then toward
 2000. 
*/
#include <Servo.h>
Servo esc;
void setup() {
  // initialize serial:
  Serial.begin(9600); //set serial monitor baud rate to match
  esc.writeMicroseconds(1500);
  esc.attach(9);
  prntIt();
}

void loop() {
  // if there's any serial available, read it:
  while (Serial.available() > 0) {

    // look for the next valid integer in the incoming serial stream:
    int speed = Serial.parseInt();
    speed = constrain(speed, 1000, 2000);
    esc.writeMicroseconds(speed);
    prntIt();
  }
}