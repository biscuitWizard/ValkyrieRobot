// There is a facility in the library to identify the most recent pin that triggered an interrupt. 
// Set the following definition '''before''' including the EnableInterrupt.h file in your sketch:
#define EI_ARDUINO_INTERRUPTED_PIN

#include <EnableInterrupt.h>

#define CHANNEL_1_PIN 2
#define CHANNEL_2_PIN 3
#define CHANNEL_3_PIN 4
#define CHANNEL_4_PIN 5

uint8_t channel_pins[] = {
  CHANNEL_1_PIN,
  CHANNEL_2_PIN,
  CHANNEL_3_PIN,
  CHANNEL_4_PIN
};

struct channel_pwm {
  uint8_t pin;
  volatile int pwm_value = 0;
  volatile int prev_time = 0;
};
 
channel_pwm* channel_values[16]; // The index of this array will be the pin #.
uint8_t latest_interrupted_pin;
 
void rising()
{
  enableInterrupt(arduinoInterruptedPin, &falling, FALLING);
  channel_pwm* channel_value = channel_values[arduinoInterruptedPin];
  channel_value->prev_time = micros();
}
 
void falling() {
  enableInterrupt(arduinoInterruptedPin, &rising, RISING);
  channel_pwm* channel_value = channel_values[arduinoInterruptedPin];
  channel_value->pwm_value = micros()-channel_value->prev_time;
}
 
void setup() {
  uint8_t pin = 0;
  for(int i=0;i < sizeof(channel_pins);i++) {  
    pin = channel_pins[i];
    
    pinMode(pin, INPUT);
    digitalWrite(pin, HIGH);

    struct channel_pwm *channel_value = (struct channel_pwm*) malloc(sizeof(struct channel_pwm));
    channel_value->pin = pin;
    channel_values[pin] = channel_value;
  }
   
  Serial.begin(115200);

  for(int i=0;i < sizeof(channel_pins);i++) {
    pin = channel_pins[i];
    enableInterrupt(pin, &rising, RISING);
  }
}

void loop() {
  // Just some debug code to see what the system is doing every second.
  Serial.println("---------------------------------------");
  delay(1000);
  for(int i=0;i < sizeof(channel_pins);i++) {
    uint8_t pin = channel_pins[i];
    struct channel_pwm *channel_value = channel_values[pin];
    Serial.print("Pin: ");
    Serial.print(pin);
    Serial.print(", load value: ");
    Serial.println(channel_value->pwm_value);
  }
}
