/*
 * global_variables.h
 *
 *  Created on: Mar 2, 2020
 *      Author: Johannes
 */

#ifndef INC_GLOBAL_VARIABLES_H_
#define INC_GLOBAL_VARIABLES_H_

#include <stdlib.h>
#include <stdio.h>

#define Rec_Button HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_5)
#define Button_1 HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_8)
#define Button_2 HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_7)
#define Button_3 HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_9)
#define Stop_Button HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_6)


#endif /* INC_GLOBAL_VARIABLES_H_ */
