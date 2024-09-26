#include <IFCT.h>
#include <kinetis_flexcan.h>

int bitVar1 = 65535;
int bitVar2;
int bitVar3;

//int msg.buf[1];
int led = 13;
// create CAN object
IFCT CAN0(1000000);
static CAN_message_t msg;





// uint32_t make_duty_message_body(int dutypercent){

//   uint32_t val = ((uint32_t)dutypercent)*1000;
//   return val;
// }

// CAN_message_t craftMessageSpark(int typeofmsg,int val){

//   CAN_message_t new_msg;

//   new_msg.flags.extended = 1;

//   switch(typeofmsg){
//     case 0: //set duty cycle
//     {
//       new_msg.id = 0x0067;
//       new_msg.len = 4;

//       uint32_t duty_bytes = ((uint32_t)val)*1000;;
//       // uint32_t msg_bytes[4];

//       // new_msg.buf = duty_bytes;
//       new_msg.buf[0] = (duty_bytes & 0xff000000) >> 24;
//       new_msg.buf[1] = (duty_bytes & 0x00ff0000) >> 16;
//       new_msg.buf[2] = (duty_bytes & 0x0000ff00) >>  8;
//       new_msg.buf[3] = (duty_bytes & 0x000000ff)      ;


//       // return new_msg;

//       break;
//     }
//   }
// }


CAN_message_t craftMessage(uint8_t id = 01, int typeofmsg = 0, int val  = 0 ){

  CAN_message_t new_msg;


  new_msg.id = (0x140) + id;
  new_msg.len = 8;

  switch(typeofmsg){
    case 1: ///led
    {
      new_msg.buf[0] = 0x88;
      new_msg.buf[1] = 0x00;
      new_msg.buf[2] = 0x00;
      new_msg.buf[3] = 0x00;
      new_msg.buf[4] = 0x00;
      new_msg.buf[5] = 0x00;
      new_msg.buf[6] = 0x00;
      new_msg.buf[7] = 0x00;
      break;
    }
    case 2: //torque control
    {
      int16_t pos_bytes = (int16_t)(val);
      new_msg.buf[0] = 0xA1;
      new_msg.buf[1] = 0x00;
      new_msg.buf[2] = 0x00;
      new_msg.buf[3] = 0x00;
      new_msg.buf[4] = (pos_bytes & 0x00ff);
      new_msg.buf[5] = (pos_bytes & 0xff00) >>  8;
      new_msg.buf[6] = 0x00;
      new_msg.buf[7] = 0x00;
      break;
    }
    case 3: //position control
    {
      int32_t pos_bytes = (int32_t)(val);
      new_msg.buf[0] = 0xA3;
      new_msg.buf[1] = 0x00;
      new_msg.buf[2] = 0x00;
      new_msg.buf[3] = 0x00;
      new_msg.buf[7] = (pos_bytes & 0xff000000) >> 24;
      new_msg.buf[6] = (pos_bytes & 0x00ff0000) >> 16;
      new_msg.buf[5] = (pos_bytes & 0x0000ff00) >>  8;
      new_msg.buf[4] = (pos_bytes & 0x000000ff)      ;
      break;
    }
    default: //stop
    {
      new_msg.buf[0] = 0x80;
      new_msg.buf[1] = 0x00;
      new_msg.buf[2] = 0x00;
      new_msg.buf[3] = 0x00;
      new_msg.buf[4] = 0x00;
      new_msg.buf[5] = 0x00;
      new_msg.buf[6] = 0x00;
      new_msg.buf[7] = 0x00;
      break;
    }
  }
  return new_msg;

}



bool led_powered = 0;
unsigned led_curr_flash_duration = 0;
unsigned led_new_flash_duration = 0;
unsigned long led_curr_flash_start = 0;
unsigned long led_time = millis();
long led_curr_flash_left = 0;

void led_flash(int duration_ms){
  led_time = millis();  
  led_curr_flash_left =  led_curr_flash_start + led_curr_flash_duration - led_time; 
  led_new_flash_duration = max(duration_ms,led_curr_flash_left);

  if(led_new_flash_duration > 0 && !led_powered){
    led_curr_flash_start = millis();
    led_curr_flash_duration = led_new_flash_duration;
    led_powered = 1;
    digitalWrite(led, HIGH);   
  }
  else{
    led_powered = 0;
    digitalWrite(led, LOW);   
  }
}

void writeCANMessage(CAN_message_t to_send){
  CAN0.write(to_send);
  led_flash(100);
}


int sniffedIdsSize =  1000;

int sniffedIds[10] = { 0 } ;
int current_if_count = 0;

int isPresent(int * intarray, int len, int tofind){
  for(int i = 0; i < len; i++){
    if(intarray[i] == tofind){
      return 1;
    }
  }
  return 0;
}



void canSniff(const CAN_message_t &msg) {

  if(!isPresent(sniffedIds,current_if_count,msg.id)){
    Serial.print("NEW ID FOUND"); Serial.print(msg.id,HEX); Serial.println();
    sniffedIds[current_if_count] = msg.id;
    current_if_count += 1;
  }
}

unsigned read_period = 1; //100Hz
unsigned long time_last_read = millis();

unsigned send_period = 2000; // 0.5 Hz
unsigned long time_last_sent = millis();


unsigned long time_now = millis();

int sent_type_HI = 0;

#define knob 15

void setup() {
   Serial.begin(115200);
  // delay(3000);e
  // init CAN bus
  Serial.println("CAN BUS INIT");
 CAN0.begin();
  CAN0.enableFIFO();
  CAN0.setBaudRate(1000000);
  pinMode(led, OUTPUT);
  delay(1000);
  writeCANMessage(craftMessage(1,1));

  Serial.println("CAN BUS INIT COMPLETE");
  writeCANMessage(craftMessage(1,2,0));
  delay(5000);

}


int i = 0;

#define N 100
float V[N]={0};
int t = 0;


void loop() {
  time_now = millis();
  i++;
  t++;
  int val = analogRead(knob) ;
  // int val = analogRead(knob) ;

  int t_val = ((val - 500) / 10. - 2.)*80 ;


  V[t] = (val)*1000;

  int m_val = 0;

  for(int k = 0; k < N ; k++){
    m_val += V[k];
  }
  m_val /= N;


  Serial.println(t_val);

  // writeCANMessage(craftMessage(1,3,m_val));
  writeCANMessage(craftMessage(1,2,t_val));

  delay(100);

  t %= N;
  // if( time_now > time_last_read + read_period){
  //   time_last_read = millis();
  //   if(Can0.read(msg) ) {
  //     canSniff(msg);
  //     led_flash(10);
  //     Serial.println(msg.id);
  //   }else{
  //     // Serial.println("can-not read CAN");
  //   }
  // }

}
