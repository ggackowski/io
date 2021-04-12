import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalyticsDashboardComponent } from './components/analytics-dashboard/analytics-dashboard.component';
import {RouterModule, Routes} from "@angular/router";
import {SimpleBarChartModule} from "../../commons/components/simple-bar-chart/simple-bar-chart.module";
import {MatCardModule} from "@angular/material/card";
import {HttpClientModule} from "@angular/common/http";
import {MatDividerModule} from "@angular/material/divider";
import {FontAwesomeModule} from "@fortawesome/angular-fontawesome";
import {MatButtonModule} from "@angular/material/button";
import {MatMenuModule} from "@angular/material/menu";
import { OptionsMenuComponent } from './components/options-menu/options-menu.component';
import {MatSelectModule} from "@angular/material/select";
import {MatRadioModule} from "@angular/material/radio";

const routes: Routes = [
  {
    path: '',
    component: AnalyticsDashboardComponent
  }
];

@NgModule({
  declarations: [
    AnalyticsDashboardComponent,
    OptionsMenuComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    SimpleBarChartModule,
    MatCardModule,
    MatDividerModule,
    MatButtonModule,
    FontAwesomeModule,
    MatMenuModule,
    MatRadioModule
  ]
})
export class AnalyticsDashboardModule { }
