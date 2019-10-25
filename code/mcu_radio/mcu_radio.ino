const int max_channels = 8;

struct Channel {
  // Final values.
  byte pin;
  byte channel_id;
  volatile short value;
  short friendly_value;

    // Temporary values.
  volatile long start;
  volatile long last;
};
struct Channel channels[max_channels] = {
  { .pin = 11, .channel_id = 1 },
  { .pin = 10, .channel_id = 2 },
  { .pin = 9, .channel_id = 3 },
  { .pin = 7, .channel_id = 4 },
  { .pin = 6, .channel_id = 5 },
  { .pin = 5, .channel_id = 6 },
  { .pin = 4, .channel_id = 7 },
  { .pin = 3, .channel_id = 8 }
};

void setup() {
  // put your setup code here, to run once:
  struct Channel *channel = &channels[0];
  for(int i=0; i < max_channels;i++) {
    channel = &channels[i];
    pinMode(channel->pin, INPUT_PULLUP);
  }
  
  attachInterrupt(digitalPinToInterrupt(channels[0].pin), channel_1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(channels[1].pin), channel_2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(channels[2].pin), channel_3, CHANGE);
  attachInterrupt(digitalPinToInterrupt(channels[3].pin), channel_4, CHANGE);
  attachInterrupt(digitalPinToInterrupt(channels[4].pin), channel_5, CHANGE);
  attachInterrupt(digitalPinToInterrupt(channels[5].pin), channel_6, CHANGE);
  attachInterrupt(digitalPinToInterrupt(channels[6].pin), channel_7, CHANGE);
  attachInterrupt(digitalPinToInterrupt(channels[7].pin), channel_8, CHANGE);

  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  struct Channel *channel = &channels[0];
  for(int i=0;i < max_channels;i++) {
    channel = &channels[i];
    Serial.print(channel->channel_id);
    Serial.print(":");
    // If we haven't heard from them in 2 seconds, set throttle to neutral.
    if(channel->value == 0) {
      channel->friendly_value = 0;
    } else {
      channel->friendly_value = constrain((((channel->value - 1000.0) / 1000.0) * 200.0) - 100.0, -100.0, 100.0);
    }
    
    Serial.print(channel->friendly_value);
    
    if(i + 1 < max_channels) {
      Serial.print("|");
    }
  }
  
  Serial.println("");
}

void channel_calc(struct Channel *channel) {
  if(digitalRead(channel->pin) == HIGH) {
    channel->start = micros();
    channel->last = micros();
  } else {
    if(channel->start == 0) {
      return;
    }
    
    channel->value = micros() - channel->start;
    channel->start = 0;
  }
}

void channel_1() {
  channel_calc(&channels[0]);
}

void channel_2() {
  channel_calc(&channels[1]);
}

void channel_3() {
  channel_calc(&channels[2]);
}

void channel_4() {
  channel_calc(&channels[3]);
}

void channel_5() {
  channel_calc(&channels[4]);
}

void channel_6() {
  channel_calc(&channels[5]);
}

void channel_7() {
  channel_calc(&channels[6]);
}

void channel_8() {
  channel_calc(&channels[7]);
}
