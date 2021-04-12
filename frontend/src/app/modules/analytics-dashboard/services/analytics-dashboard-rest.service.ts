import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";
import {tap} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardRestService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public getTweetsCountChartData(): Observable<BarChartData> {
    return this.httpClient.get<BarChartData>('/api/data/infections', {}).pipe(tap(console.log));
  }

  public getInfectionsDataInRange(startDate: Date, endDate: Date): Observable<BarChartData> {
    return this.httpClient.get<BarChartData>('/api/data/active_cases', {params: {start: startDate.toISOString(), end: endDate.toISOString()}});
  }
}
