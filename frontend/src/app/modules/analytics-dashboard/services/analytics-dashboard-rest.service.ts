import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardRestService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public getTweetsCountChartData(): Observable<BarChartData> {
    return this.httpClient.get<BarChartData>('/api/data/infections');
  }
}
