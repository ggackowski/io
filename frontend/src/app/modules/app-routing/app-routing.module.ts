import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'analyticsDashboard',
    pathMatch: 'full'
  },
  {
    path: 'analyticsDashboard',
    loadChildren: () => import('../analytics-dashboard/analytics-dashboard.module')
      .then(m => m.AnalyticsDashboardModule)
  },
  {
    path: 'correlations',
    loadChildren: () => import('../correlations/correlations.module')
      .then(m => m.CorrelationsModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
