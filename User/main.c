/*
 BitzOS (BOS) V0.3.6 - Copyright (C) 2017-2024 Hexabitz
 All rights reserved

 File Name     : main.c
 Description   : Main program body.
 */
/* Includes ------------------------------------------------------------------*/
#include "BOS.h"

/* Private variables ---------------------------------------------------------*/
float eogSample;
float eogFilteredSample;
/* Private function prototypes -----------------------------------------------*/

/* Main function ------------------------------------------------------------*/

int main(void) {

	Module_Init();		//Initialize Module &  BitzOS

	//Don't place your code here.
	for (;;) {
	}
}

/*-----------------------------------------------------------*/

/* User Task */
void UserTask(void *argument) {
	EXG_Init(EOG);
	// put your code here, to run repeatedly.
	while (1) {
		uint8_t *temp = (uint8_t *)&eogFilteredSample;
	 Delay_s(0.1);
		EOG_Sample(& eogSample , & eogFilteredSample );
		writePxITMutex(P3, (char *)&temp[0], 4 * sizeof(uint8_t), 10);

	}
}

/*-----------------------------------------------------------*/
