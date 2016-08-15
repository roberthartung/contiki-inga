#ifndef __MARKER_H__
#define __MARKER_H__

#include <stdint.h>

#define MARKER_MASK 0xF
#define MARKER_1 0
#define MARKER_2 1
#define MARKER_3 2
#define MARKER_4 3

void marker_init();
void marker_high(uint8_t marker);
void marker_low(uint8_t marker);

#endif
