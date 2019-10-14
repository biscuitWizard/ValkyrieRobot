#include <Wire.h>

const short channels = 8;
const byte slave_address = 42;

short pwm_value[channels];
int channel_pins[channels] = {
  7, 9, 10, 11, 12, 13, 4, 6
};

unsigned long duration; 
int index = 0;

void setup() {
  Wire.begin(); // join i2c bus as master
  
  Serial.begin(19200);

  for(index=0;index < channels;index++) {
    pinMode(channel_pins[index], INPUT);
  }
}

void loop() { 
  Wire.beginTransmission(slave_address);
  byte current_channel = 0x00;
  for(index=0;index < channels;index++) { 
    current_channel = index + 1;
    Wire.write(current_channel); // Channel #
    Serial.write(current_channel);
    
    duration = 0;
    duration = pulseIn(channel_pins[index], HIGH, 36000);
    if(duration != 0) {
      pwm_value[index] = constrain((((duration - 970.0) / 1000.0) * 200.0) - 100.0, -100, 100);
    } else {
      pwm_value[index] = 0;
    }

    Wire.write(pwm_value[index]); // PWM Value.
    Serial.write(pwm_value[index]);    
  }
  
  Wire.write(0xFF); // Break/EOF.
  Serial.write(0xFF);
  Serial.println();
}
