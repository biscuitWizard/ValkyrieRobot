const int max_channels = 8;

struct Channel {
  // Final values.
  byte pin;
  byte channel_id;
  short value;

    // Temporary values.
  long duration;
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

struct Channel *cur_chan;
void setup() {
  for(int i=0;i < max_channels;i++) {
    cur_chan = &channels[i];
    pinMode(cur_chan->pin, INPUT);
  }

  Serial.begin(19200);
}

void loop() {
  // Main loop for reading pulses.
  for(int i=0;i < max_channels;i++) {
    cur_chan = &channels[i];
    cur_chan->duration = pulseIn(cur_chan->pin, HIGH);
    if(cur_chan->duration != 0) {
      cur_chan->value = constrain((cur_chan->duration - 970.0) / 1000.0 * 200 - 100, -100, 100);
    } else {
      cur_chan->value = 0;
    }
  }

  // Main loop for reporting pulse results.
  for(int i=0;i < max_channels;i++) {
    cur_chan = &channels[i];
    Serial.print(cur_chan->channel_id);
    Serial.print(":");
    Serial.print(cur_chan->value);
    Serial.print("|");
  }
  Serial.println();
}
