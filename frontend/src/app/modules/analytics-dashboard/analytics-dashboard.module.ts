import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalyticsDashboardComponent } from './components/analytics-dashboard/analytics-dashboard.component';
import {RouterModule, Routes} from "@angular/router";

const routes: Routes = [
  {
    path: '',
    component: AnalyticsDashboardComponent
  }
];

@NgModule({
  declarations: [
    AnalyticsDashboardComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes)
  ]
})
export class AnalyticsDashboardModule { }
