import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalyticsDashboardComponent } from './components/analytics-dashboard/analytics-dashboard.component';
import {RouterModule, Routes} from "@angular/router";
import {SimpleBarChartModule} from "../../commons/components/simple-bar-chart/simple-bar-chart.module";
import {MatCardModule} from "@angular/material/card";
import {MatDividerModule} from "@angular/material/divider";
import {FontAwesomeModule} from "@fortawesome/angular-fontawesome";
import {MatButtonModule} from "@angular/material/button";
import {MatMenuModule} from "@angular/material/menu";
import { OptionsMenuComponent } from './components/options-menu/options-menu.component';
import {MatCheckboxModule} from "@angular/material/checkbox";
import {OverlayModule} from "@angular/cdk/overlay";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatInputModule} from "@angular/material/input";
import {MatNativeDateModule} from "@angular/material/core";
import { InfectionsDataComponent } from './components/infections-data/infections-data.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import { TweetsCountComponent } from './components/tweets-count/tweets-count.component';

const routes: Routes = [
  {
    path: '',
    component: AnalyticsDashboardComponent
  }
];

@NgModule({
  declarations: [
    AnalyticsDashboardComponent,
    OptionsMenuComponent,
    InfectionsDataComponent,
    TweetsCountComponent
  ],
  providers: [
    MatDatepickerModule
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
    MatCheckboxModule,
    OverlayModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatInputModule,
    ReactiveFormsModule,
    MatProgressSpinnerModule,
    FormsModule
  ]
})
export class AnalyticsDashboardModule { }
