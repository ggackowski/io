import { Injectable } from '@angular/core';
import {AnalyticsDashboardRestService} from "./analytics-dashboard-rest.service";
import {Observable} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardDataService {

  constructor(
    private restService: AnalyticsDashboardRestService
  ) { }

  public getTweetsCountChartData(): Observable<BarChartData> {
    return this.restService.getTweetsCountChartData();
  }
}
