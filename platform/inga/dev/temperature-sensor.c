/*
 * Copyright (c) 2012, TU Braunschweig.
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
 *      Temperature sensor interface source
 * \author
 *     Ulf Kulau <kulau@ibr.cs.tu-bs.de>
 */

#include "contiki.h"
#include "dev/temperature-sensor.h"
#if INGA_CONF_REVISION == INGA_V161
#include "dev/tmp102.h"
#else
#include "bmp085.h"
#endif

const struct sensors_sensor temperature_sensor;

/*---------------------------------------------------------------------------*/
static int
value(int type)
{
  switch (type) {
    case TEMP:
#if INGA_CONF_REVISION == INGA_V161
      return tmp102_read_temp_byte();
#else
      return bmp085_read_temperature();
#endif
      break;
    case TEMP_H:
#if INGA_CONF_REVISION == INGA_V161
      return tmp102_read_temp_word();
#else
      return bmp085_read_temperature();
#endif
      break;
  }
}
/*---------------------------------------------------------------------------*/
static int
configure(int type, int c)
{
#if INGA_CONF_REVISION == INGA_V161
  return tmp102_init(); //TODO return =1 (OK) =0 (Failure)
#else
  return bmp085_init();
#endif
}
/*---------------------------------------------------------------------------*/
static int
status(int type)
{
  return 1; //TODO status
}
/*---------------------------------------------------------------------------*/
SENSORS_SENSOR(temperature_sensor, TEMPERATURE_SENSOR,
               value, configure, status);