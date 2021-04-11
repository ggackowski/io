import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SimpleBarChartComponent } from './simple-bar-chart.component';
import {ChartsModule} from "ng2-charts";



@NgModule({
    declarations: [
        SimpleBarChartComponent
    ],
    exports: [
        SimpleBarChartComponent
    ],
  imports: [
    CommonModule,
    ChartsModule
  ]
})
export class SimpleBarChartModule { }
