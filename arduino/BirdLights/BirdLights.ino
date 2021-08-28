#include "FastLED.h"

#define NUM_LEDS 20
#define OUT_PIN 3
#define IN_PIN 2

#define BRIGHTNESS 0x80
#define FADE_TIME_MS 100000

CRGB leds[NUM_LEDS];
int state = 0;

void setup() {
  pinMode(IN_PIN, INPUT);

  // sanity check delay - allows reprogramming if accidently blowing power w/leds
  delay(2000);

  FastLED.addLeds<WS2812, OUT_PIN, RGB>(leds, NUM_LEDS);
  on();
  off();
}


void setBrightness(int brightness) {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB(brightness, brightness, brightness);
  }
  FastLED.show();
}

void on() {
  setBrightness(BRIGHTNESS);
}

void off() {
  setBrightness(0);
}

void _fade(unsigned long fadeTimeMillis, bool up) {
  int steps = BRIGHTNESS;
  int stepTimeMillis = fadeTimeMillis / steps;
  for (int b = 0; b <= BRIGHTNESS; b += 1) {
    if (up) {
      setBrightness(b);
    } else {
      setBrightness(BRIGHTNESS - b);
    }
    delay(stepTimeMillis);
  }
}

void fadeUp(unsigned long fadeTimeMillis) {
  _fade(fadeTimeMillis, true);
}

void fadeDown(unsigned long fadeTimeMillis) {
  _fade(fadeTimeMillis, false);
}

void loop() {
  int newState = digitalRead(IN_PIN);

  if (newState != state) {
    if (newState) {
      //on();
      fadeUp(FADE_TIME_MS);
    } else {
      fadeDown(FADE_TIME_MS);
      //off();
    }
  }
  state = newState;
  delay(1000);
}

