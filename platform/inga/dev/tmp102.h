/*
 * Copyright (c) 2013, TU Braunschweig.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/**
 * \file
 *		TMP102 Temperature Sensor interface definitions
 * \author
 *      Ulf Kulau <kulau@ibr.cs.tu-bs.de>
 */

/**
 * \addtogroup inga_sensors_driver
 * @{
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
