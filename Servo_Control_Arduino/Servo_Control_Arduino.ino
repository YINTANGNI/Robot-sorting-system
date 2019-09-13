//*********************************************************************//
//*********************************************************************//
//******************3 DOF robot arm control program********************//
//******function: solve the inverse kinematics of 3 DOF robot arm******//
//*********************************************************************//
//*********************************************************************//
#include <Servo.h>

Servo Base;
Servo Bigarm;
Servo Smallarm;
Servo PumpFor;
Servo PumpBack;

#define numdata_length 6 //x,y,z,symbol,pump,forward/inverse
String comdata = "";
float pos_base = 0;
float pos_bigarm = 0;
float pos_smallarm = 0;
int numdata[numdata_length] = {0};
int flag = 0;
int pos_previous = 0;



void setup()
{ Serial.begin(9600);
  //pinMode(2,OUTPUT);
  //digitalWrite(2,LOW);
  Base.attach(2);
  Bigarm.attach(4);
  Smallarm.attach(3);
  PumpFor.attach(5);
  PumpBack.attach(6);
  pumpreset();
}



void loop()
{ int j = 0;
  while (Serial.available() > 0)
  { comdata += char(Serial.read());
    delay(2); 
    flag = 1;
  }
  if(flag == 1) {
    for(int i = 0; i < comdata.length() ; i++){
      if(comdata[i] == ' '){
        j++;
      }
      else{
        numdata[j] = numdata[j] * 10 + (comdata[i] - '0');
      }
  }
  comdata = String("");
  flag = 0;
  if (numdata[5]==1){
  int pos_temp = int(500+7.41*(numdata[0]+45));
  Base.writeMicroseconds(pos_temp);
  Bigarm.write(numdata[1]);
  Smallarm.write(numdata[2]);
  if(numdata[4] == 1){
    pickup();
  }
  else if(numdata[4] == 2){
    putdown();
  }
  }
  else{
  switch (numdata[3]) {
    case 1:
      numdata[0]=-numdata[0];
    break;
    case 2:
      numdata[1]=-numdata[1];
    break;
    case 3:
      numdata[2]=-numdata[2];
    break;
    case 12:
      numdata[0]=-numdata[0];
      numdata[1]=-numdata[1];
    break;    
    case 13:
      numdata[0]=-numdata[0];
      numdata[2]=-numdata[2];
    break;
    case 123:
      numdata[0]=-numdata[0];
      numdata[1]=-numdata[1];
      numdata[2]=-numdata[2];
    break;
  }
  float num0 = numdata[0]*0.1;
  float num1 = numdata[1]*0.1;
  float num2 = numdata[2]*0.1;
  
  //**************************************/
  //y > 0;
  
  float end_len_x = cos(atan2(num1,num0))*3.5;
  float end_len_y = sin(atan2(num1,num0))*3.5;
  float end_x = num0 - end_len_x;
  float end_y = num1 - end_len_y;

  
  
  
  
  
  pos_base = atan2(end_y,end_x)*57.3;
  float AC2 = end_x*end_x+end_y*end_y+num2*num2;
  if (num2 >= 0){
  pos_bigarm = (acos((AC2-31)/(30*sqrt(AC2)))+atan2(num2,sqrt(end_x*end_x+end_y*end_y)))*57.3;}
  else{
  pos_bigarm = (acos((AC2-31)/(30*sqrt(AC2)))-atan2(abs(num2),sqrt(end_x*end_x+end_y*end_y)))*57.3;}
  pos_smallarm = 270-pos_bigarm-(acos((481-AC2)/480)*57.3);

  //Serial.println(pos_previous);
  //Serial.println(pos_equal);
  //revolution(2,pos_base);
  int pos_equal = int(500+7.41*(pos_base+45));
  int pos_equal_low = 20000-pos_equal;
  Base.writeMicroseconds(pos_equal);
  Bigarm.write(pos_bigarm);
  Smallarm.write(pos_smallarm);

  if(numdata[4] == 1){
    pickup();
  }
  else if(numdata[4] == 2){
    putdown();
  }
  Serial.println('a');
  }
  }
  for(int i = 0; i < numdata_length; i++){
    numdata[i] = 0;
  }
}






void pickup()
{
  PumpFor.write(180);
  PumpBack.write(0);
  delay(1500);
  PumpFor.write(0);
  PumpBack.write(0);
  delay(500); 
}

void putdown()
{
  PumpFor.write(0);
  PumpBack.write(180);
  delay(1000);
  PumpFor.write(0);
  PumpBack.write(0);
  delay(500); 
}

void pumpreset()
{
  PumpFor.write(0);
  PumpBack.write(0);
  delay(1000);  
}

void revolution(int pin,float pos_base)
{ int pos_equal = int(500+7.41*(pos_base+43));
  int pos_equal_low = 20000-pos_equal;
  for(int i=0;i<5;i++){
  digitalWrite(pin,HIGH);
  delayMicroseconds(pos_equal);
  digitalWrite(pin,LOW);
  delayMicroseconds(pos_equal_low);
}
}


