#include <Servo.h>
#include <string.h>
#include <HardwareSerial.h>

//motor pins
#define leftMotorPin 9
#define rightMotorPin 10

//pins for the input from the RC reciever
#define throttlePin 18
#define elevatorPin 19
#define aileronPin 20

#define LEDPin 13
//Motors
Servo leftMotor;
Servo rightMotor;

int leftMotorInputROS = 0;
int rightMotorInputROS = 0;

//counter for how many throttle values were the same in a row, used to find if controller is disconnected
int throttleValueCounter = 0;
int throttlePreviousValue = 0;
int throttleCurrentValue = 0;
bool controllerConnect = true;

//pointers to reference above values
int *pTVC = &throttleValueCounter;
int *pTPV = &throttlePreviousValue;
int *pTCV = &throttleCurrentValue;

/*
CURRENT CONTROLLER DISCONNECT SOLUTION:
  On controller failsafe ch3 (throttle) is set to -100%
  If controller loses power it should force us into the 'else' condition of main loop

TO GET TO FAILSAFE SETTINGS ON CONTROLLER
  press and hold 'ok' button
  press 'ok' on picture of remote
  up/down to navigate to 'RX Setup
  'Failsafe'
*/
// TODO fix or remove.  Output is currently forced to 'True'
// OBSOLETE based on behavior of old controller that had a lot more signal inconsistency
// tests to find out if controller is connected or not
bool controllerConnected(int *tVC, int *tPV, int *tCV) {
  // if the previous value is the same as the current value, adds one counter
  // other condition is due to the fact that throttle staying at same value for too long when at the low position on the remote
  if(throttlePreviousValue == throttleCurrentValue && throttleCurrentValue > 1600) {
    *tVC += 1;
  }
  //otherwise it resets the counter to zero
  else
    *tVC = 0;
  //if the throttle is same for 25 times in a row, return false to signify controller is disconnected
  if(throttleValueCounter > 25) {
    // return false; // TODO UNCOMMENT IF/WHEN REPLACEMENT METHOD DETERMINED
  }
  //otherwise return true to signify controller is connected
  return true;
}

//output values for remote control mode
int leftMotorOutputRC = 0;
int rightMotorOutputRC = 0;

//output values from RC reciever once the input values are mapped
int elevatorOutput = 0;
int alieronOutput = 0;

//start time for measuring pulse of RC reciever inputs
volatile unsigned long timerStartT;
volatile unsigned long timerStartE;
volatile unsigned long timerStartA;

//pulse time of RC reciever inputs
int pulseTimeT;  // throttle
int pulseTimeE;  // elevator
int pulseTimeA;  // aileron

//previous time RC reciever got an input from RC remote
volatile int lastInteruptTimeT;
volatile int lastInteruptTimeE;
volatile int lastInteruptTimeA;

//calculates how long throttle pulse was
void calcSignalT() {
  //initializes current time in microseconds
  lastInteruptTimeT = micros();
  if(digitalRead(throttlePin) == HIGH)
    timerStartT = micros();
  else {
    if(timerStartT != 0) {
      pulseTimeT = ((volatile int)micros() - timerStartT);
      timerStartT = 0;
    }
  }
}

//calculates how long elevator pulse was
void calcSignalE() {
  lastInteruptTimeE = micros();
  if(digitalRead(elevatorPin) == HIGH)
    timerStartE = micros();
  else {
    if(timerStartE != 0) {
      pulseTimeE = ((volatile int)micros() - timerStartE);
      timerStartE = 0;
    }
  }
}

//calculates how long aileron pulse was
void calcSignalA() {
  lastInteruptTimeA = micros();
  if(digitalRead(aileronPin) == HIGH)
    timerStartA = micros();
  else {
    if(timerStartA != 0) {
      pulseTimeA = ((volatile int)micros() - timerStartA);
      timerStartA = 0;
    }
  }
}

//changes the direction the motor is spinning
//this is needed for our setup since the left motor's polarity needs to be reversed
int flipPolarity(int motorSpeed) {
  motorSpeed -= 1500;
  motorSpeed = -motorSpeed;
  motorSpeed += 1500;
  return motorSpeed;
}


/*************************** FOR HARD CODED PATHING ************************************************/
/*
  This code is for emergency use if the ROS/Jetson/Python code is non-functional.
  Sends commands directly to the motor controllers to execute the given path.  Use with caution.
  DOES NOT utilize external sensors.
  WILL NOT avoid cones.
  HAS NOT been thoroughly tested for safety.

IMPROVEMENTS TO MAKE
- Replace current mPerNinety calculations
  - Program IMU arduino to pipe euler x data to this arduino to use as a compass for better turn accuracy
  - Save "compass" orientation at start of auto functions to use as "base orientation"
  - Track 'target orientation' as base orientation +/- 90*n degrees
  - Turn functions changes target orientation, calls motors to turn until within +/-1(?) degree of target 
  - Consider decreasing turn speed when within +/- 10 degrees of target to increase accuracy
  - Implement helper function to wrap orientation values 0-360 degrees

Physical measurements for pathing considerations
  -Center of rotation to (angled) plow blade edge    ~= 1.30 m
  -Center of rotation to (angled) plow blade center  ~= 0.95 m
*/

/*
// Params for hard coded path functions 
int baseSpeed = 1800;        // Base speed value to send to motor controllers
int turnReduction = 100;     // Reduction to motor speed when turning, for increased turn accuracy
double mPerSec = 0.62;       // @ 1800 basespeed, measured speed in m/s
double mPerNinety = 0.1875;  // @ 1800 baseSpeed and 100 turnReduction, measure of "distance" to travel in meters to make a 90 degree turn 
double snowResistMult = 1.3; // Multiplier to compensate for pushing snow on forward movement.  Results may very.

// set both motors to 1500 -- no movement
void stop(){
  stop(0.1);
}
void stop(double seconds){  
  leftMotor.writeMicroseconds(1500);
  rightMotor.writeMicroseconds(1500);
  unsigned long timer = millis();
  double timerTarget = timer + (seconds * 1000);
  while(timer < timerTarget && pulseTimeT >= 1650){
    timer = millis();
  }
}

// moveForward with no snowOffset
void moveForward(double meters){ 
  moveForward(meters, 1.0);
}
// set motors to forward movement for ~X meters.  Second parameter optional.
// 'snowOffset' is to extend time to compensate for snow slowing movement
void moveForward(double meters, double snowOffset){  
  unsigned long timer = millis();
  double timerTarget = (double)timer + ((meters/mPerSec) * 1000.0 *snowOffset); 
  while(timer < timerTarget && pulseTimeT >= 1650){
    timer = millis();
    leftMotor.writeMicroseconds(flipPolarity(baseSpeed));
    rightMotor.writeMicroseconds(baseSpeed);
  }
}

// set both motors to backward movement for ~X meters.  Assumes no snow in path when reversing.
void moveBackward(double meters){                   
  unsigned long timer = millis();
  double timerTarget = (double)timer + ((meters/mPerSec) * 1000.0); 
  while(timer < timerTarget && pulseTimeT >= 1650){
    timer = millis();
    leftMotor.writeMicroseconds(baseSpeed);
    rightMotor.writeMicroseconds(flipPolarity(baseSpeed));
  }
}

// set leftMotor forward and rightMotor in reverse.  1 turns = ~90 degree rotation
void turnLeft(double turns){                        
  unsigned long timer = millis();
  double timerTarget = timer + ((turns/mPerSec) * 1000 * mPerNinety);
  while(timer < timerTarget && pulseTimeT >= 1650){
    timer = millis();
    leftMotor.writeMicroseconds(flipPolarity(baseSpeed-turnReduction));
    rightMotor.writeMicroseconds(flipPolarity(baseSpeed-turnReduction));
  }
}

// set rightMotor forward and leftMotor in reverse.  1 turns = ~90 degree rotation
void turnRight(double turns){                       
  unsigned long timer = millis();
  double timerTarget = timer + ((turns/mPerSec) * 1000 * mPerNinety);
  while(timer < timerTarget && pulseTimeT >= 1650){
    timer = millis();
    leftMotor.writeMicroseconds(baseSpeed-turnReduction);
    rightMotor.writeMicroseconds(baseSpeed-turnReduction);
  }
}

// Hard coded 'T' path for competition
// USE FOR COMPETITION ONLY AS A LAST RESORT
// ? use left turns only since plow blade would be angled inward-left, to avoid pushing snow under the bot while turning
void pathT(){
  // Assume starting position is 0.5(?) m in from left edge of T base at base of garage
  //  2.0 x 1.5 m 'T' base
  // 10.0 x 1.0 m 'T' top
  double stopShort=0; // account for distance between center of rotation and front of the plow blade.  IE: center of rotation is x distance from the starting line
  moveForward(2.5); 
  turnLeft(1.0);
  moveForward(4.5);
  turnRight(2.0);
  moveForward(10.5-stopShort);
  turnRight(2.0);
  moveForward(5.0-stopShort);
  turnLeft(1.0);
  moveForward(2.0 + 2.0);
}

// For testing/calibrating distance(mPerSec) and turn(mPerNinety) consistency.
// If the bot ends up right where it started then we're good to go.
void pathSquare(){
  double sideLength= 2.0;   // 2 meters per square side
  int i=0;
  for(i=0; i<4; ++i){       // 4 forward movements + 4 turns = complete square
    moveForward(sideLength);
    turnRight(1.0);
  }
}
*/
/**************************** END OF HARD CODED PATHING ******************************************************************* */


void setup(void)
{
  //sets pinmodes for motor pins
  pinMode(leftMotorPin, OUTPUT);
  pinMode(rightMotorPin, OUTPUT);
  pinMode(LEDPin, OUTPUT);
  //attaches the motors to defined pins
  leftMotor.attach(leftMotorPin);
  rightMotor.attach(rightMotorPin);

  //initializes start times for throttle, elevator, and aileron
  timerStartT = 0;
  timerStartE = 0;
  timerStartA = 0;

  //attaches the defined pins to call the respective functions anytime their value is changed
  attachInterrupt(digitalPinToInterrupt(throttlePin), calcSignalT, CHANGE);
  attachInterrupt(digitalPinToInterrupt(elevatorPin), calcSignalE, CHANGE);
  attachInterrupt(digitalPinToInterrupt(aileronPin), calcSignalA, CHANGE);

  Serial.begin(115200);
  Serial.setTimeout(50);

}
String lastInput="";
void loop(void)
{
  // !!!TALON MOTORCONTROLLER TAKES IN MICROSECONDS FROM 1000(FULL REVERSE) TO 2000 (FULL FORWARD)
  //on startup, set the previous throttle value to the actual value
  if(throttlePreviousValue == 0)
    throttlePreviousValue = pulseTimeT;
  //otherwise set the previous value variable to the current value, and set the current value variable to the actual value
  else {
    throttlePreviousValue = throttleCurrentValue;
    throttleCurrentValue = pulseTimeT;
  }

  //check if the controller is connected
  controllerConnect = controllerConnected(pTVC, pTPV, pTCV);
  
  //map the pulse times to the appropritate values
  /*
  Talon motor controllers take in values from 1000 to 2000, however, to account for steering left to right, the elevator will
  control the majority of the power (-60% to 60%) and the aileron will allow for small changes (-20% to 20%) which will allow for turns
  */
  elevatorOutput = map(pulseTimeE, 1280, 1700, 1200, 1800); 
  alieronOutput  = map(pulseTimeA, 1270, 1715, -100, 100);  

  //output values for the motors in RC mode, motors are controlled by both elevator and aileron as described above
  leftMotorOutputRC = elevatorOutput + alieronOutput;
  rightMotorOutputRC = elevatorOutput - alieronOutput;

if(Serial.available()) {
  String motorInputROS = Serial.readString();
  lastInput=motorInputROS;
  Serial.println("Found "+motorInputROS);
  int j=0;
  int val=0;
  int neg=1;
  for(int i=0;i<=motorInputROS.length();i++){
    if(i==motorInputROS.length()||motorInputROS[i]=='|'){
      if(j==0){
        leftMotorInputROS=val*neg;
      }else if(j==1){
        rightMotorInputROS=val*neg;
      }
      j++;
      val=0;
      neg=1;
    }else{
      if(motorInputROS[i]=='-'){
        neg=-1;
      }else if(((int)(motorInputROS[i]-'0'))>=0){
        val*=10;
        val+=motorInputROS[i]-'0';
      }
    }
  }
}

//Serial.print(lastInput);
if(leftMotorInputROS<=-50){
  digitalWrite(LEDPin,HIGH);
}else{
  digitalWrite(LEDPin,LOW);
}

// Debug print statements
if(0){
  Serial.print("pulseTimeT: ");
  Serial.print(pulseTimeT);
  Serial.print("  pulseTimeE: ");
  Serial.print(pulseTimeE);
  Serial.print("  pulseTimeA: ");
  Serial.print(pulseTimeA);
  Serial.print("  controllerConnect: ");
  Serial.print(controllerConnect);
  Serial.println();
}

//if the throttle is all the way up and the controller is connected, the arduino should be in ROS mode, listening to topics listed above over rosserial
  if(pulseTimeT >= 1650 && controllerConnect) {
    // AUTONOMOUS MODE

    // INPUT FROM JETSON/SERIAL
    if(0){ // toggle for debug printing values 
      Serial.print("Serial Vals: " );
      Serial.print(leftMotorInputROS);
      Serial.print(" | ");
      Serial.print(rightMotorInputROS);
      Serial.println();
    }
    // Write serial values to motors
    leftMotor.writeMicroseconds(flipPolarity(map(leftMotorInputROS, -100, 100, 1000, 2000)));
    rightMotor.writeMicroseconds(map(rightMotorInputROS, -100, 100, 1000, 2000));
  }
//If the throttle is in the middle, the arduino will be in RC mode and listen to input from elevator and aileron inputs
  else if (pulseTimeT < 1650 && pulseTimeT > 1350 && controllerConnect){
    // RC MANUAL MODE

    //Applying dead zones to both motor controllers since the RC remote being used isn't exact
    if(leftMotorOutputRC > 1460 && leftMotorOutputRC < 1540) 
      leftMotorOutputRC = 1500;
    if(rightMotorOutputRC > 1460 && rightMotorOutputRC < 1540)
      rightMotorOutputRC = 1500;
    leftMotor.writeMicroseconds(flipPolarity(leftMotorOutputRC));
    rightMotor.writeMicroseconds(rightMotorOutputRC);

  }
//Otherwise, if the throttle is all the way down, the controller will be in dead mode and will not move
  else {
    // STOP MODE
    leftMotor.writeMicroseconds(1500);
    rightMotor.writeMicroseconds(1500);
  }
}





