#include<TimeLib.h>


/*Force Sensor Resistance to Arduino's Analog Ports*/
int fsrAnalogPin1 = 0; //FSR1 is connected to analog 0
int fsrAnalogPin2 = 1; //FSR2 is connected to analog 1
int fsrAnalogPin3 = 2; //FSR3 is connected to analog 2
int fsrAnalogPin4 = 3; //FSR4 is connected to analog 3
int fsrAnalogPin5 = 4; //FSR5 is connected to analog 4

/*LED connections to Arduino's Digital Ports*/
int LEDpin1 = 11; //1.Green LED to pin 11 (PWM pin)
int LEDpin2 = 10; //2.Yellow LED to pin 10 (PWM pin)
int LEDpin3 = 9; //3.Blue LED to pin 9 (PWM pin)
int LEDpin4 = 8 ; //4.White LED to pin 8 (PWM pin)
int LEDpin5 = 12; //5. Orange LED to pin 12 (PWM pin)

/*The analog reading from the FSR resistor divider*/
int fsrReading1;
int fsrReading2;
int fsrReading3;
int fsrReading4;
int fsrReading5;
int LEDbrightness1;
int LEDbrightness2;
int LEDbrightness3;
int LEDbrightness4;
int LEDbrightness5;
 
void setup(void) {
  Serial.begin(9600);   /*Send debugging information via the Serial monitor*/
  pinMode(LEDpin1, OUTPUT);
  pinMode(LEDpin2, OUTPUT);
  pinMode(LEDpin3, OUTPUT);
  pinMode(LEDpin4, OUTPUT);
  pinMode(LEDpin5, OUTPUT);
}
 
void loop(void) {  
 
   fsrReading1 = analogRead(fsrAnalogPin1);
   Serial.print("A0  ");
   Serial.println(fsrReading1);
   //Serial.println("");

   fsrReading2 = analogRead(fsrAnalogPin2);
   Serial.print("A1  ");
   Serial.println(fsrReading2);
   //Serial.println("");

   fsrReading3 = analogRead(fsrAnalogPin3);
   Serial.print("A2  ");
   Serial.println(fsrReading3);
   //Serial.println("");

   fsrReading4 = analogRead(fsrAnalogPin4);
   Serial.print("A3  ");
   Serial.println(fsrReading4);
   //Serial.println("");

   fsrReading5 = analogRead(fsrAnalogPin5);
   Serial.print("A4  ");
   Serial.println(fsrReading5);
   //Serial.println("");
 
   /* We'll need to change the range from the analog reading (0-1023) down to the range used by analogWrite (0-255) with map! */  
   /* LED gets brighter or harder depending on how it is pressed by the user */
   LEDbrightness1 = map(fsrReading1, 0, 1023, 0, 255);
   analogWrite(LEDpin1, LEDbrightness1);
     
   LEDbrightness2 = map(fsrReading2, 0, 1023, 0, 255);
   analogWrite(LEDpin2, LEDbrightness2);

   LEDbrightness3 = map(fsrReading3, 0, 1023, 0, 255);
   analogWrite(LEDpin3, LEDbrightness3);

   LEDbrightness4 = map(fsrReading4, 0, 1023, 0, 255);
   analogWrite(LEDpin4, LEDbrightness4);

   LEDbrightness5 = map(fsrReading5, 0, 1023, 0, 255);
   analogWrite(LEDpin5, LEDbrightness5);

   delay(1000);
}
