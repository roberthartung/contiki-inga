#include "marker.h"
#include <avr/io.h>

void marker_init() {
	DDRA |= MARKER_MASK;
	// Disable all triggers
	PORTA &= ~MARKER_MASK;
}

void marker_high(uint8_t marker) {
	PORTA |= (1 << marker) & MARKER_MASK;
}

void marker_low(uint8_t marker) {
	PORTA &= ~((1 << marker) & MARKER_MASK);
}
