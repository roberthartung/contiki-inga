/*
 * avs.c
 *
 *  Created on: 27.08.2013
 *      Author: ulf
 */

#include "tmp102.h"

uint8_t tmp102_init(void) {
	i2c_start(TMP102_SLAVE_ADDR_W);
	i2c_write(TMP102_PNTR_ADDR_CONF);
	i2c_write(TMP102_CONF_REG_1);
	i2c_write(TMP102_CONF_REG_2);
	i2c_stop();
	return 1;
}

int8_t tmp102_read_temp_byte(void){
	uint8_t ret;
	i2c_start(TMP102_SLAVE_ADDR_W);
	i2c_write(TMP102_PNTR_ADDR_TEMP);
	i2c_rep_start(TMP102_SLAVE_ADDR_R);
	i2c_read_nack(&ret);
	i2c_stop();
	return ret;
}

int16_t tmp102_read_temp_word(void){
	uint8_t ret1, ret2;
	i2c_start(TMP102_SLAVE_ADDR_W);
	i2c_write(TMP102_PNTR_ADDR_TEMP);
	i2c_rep_start(TMP102_SLAVE_ADDR_R);
	i2c_read_nack(&ret1);
	i2c_read_nack(&ret2);
	i2c_stop();
	return (((ret1 << 8) | ret2) >> 4);
}

