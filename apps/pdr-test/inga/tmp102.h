/*
 * tmp102.h
 *
 *  Created on: 01.08.2013
 *      Author: ulf
 */

#ifndef TMP102_H_
#define TMP102_H_

/* Driver for the temperature sensor of the thermostat tmp102*/

#include "../dev/i2c.h"

/* Thermostat Sensor Definitions */
#define TMP102_SLAVE_ADDR_W 0x90 //0b10010000
#define TMP102_SLAVE_ADDR_R 0x91 //0b10010001
/* D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 
 *----------------------------------------
 * OS | R1 | R0 | F1 | F0 | POL| TM | SD
 */
#define TMP102_CONF_REG_1	0b01100000
/* D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 
 *----------------------------------------
 * CR1| CR0| AL | EM | 0  | 0  | 0  | 0
 */
#define TMP102_CONF_REG_2	0b01100000

/* 0 0 | Temperature Register (Read Only)
 * 0 1 | Configuration Register (Read/Write)
 * 1 0 | T_LOW Register (Read/Write)
 * 1 1 | T_HIGH Register (Read/Write
 */
#define TMP102_PNTR_ADDR_TEMP	0b00000000
#define TMP102_PNTR_ADDR_CONF	0b00000001
#define TMP102_PNTR_ADDR_T_L	0b00000010
#define TMP102_PNTR_ADDR_T_H	0b00000011

#define TMP102_TEMP_h 0x0F
#define TMP102_TEMP_l 0x0F

uint8_t tmp102_init(void);
/* Low accuracy, which is sufficient for the idealVolting implementation */
int8_t tmp102_read_temp_byte(void);
/* High accuracy with a resolution of 12bit*/
int16_t tmp102_read_temp_word(void);



#endif /* TEMPSENSOR_H_ */
