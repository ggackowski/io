import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {AvgChartData, BarChartData, GenericChartData} from "../model/bar-chart-data.model";
import {delay, map, tap} from "rxjs/operators";
const dateTimeFormat =  new Intl.DateTimeFormat()

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardRestService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public getAvailableHashtags(): Observable<Array<string>> {
    return this.httpClient.get<Array<string>>('/api/data/hashtags');
  }

  public getTweetsCountInRange(startDate: Date, endDate: Date, hashtags: Array<string>): Observable<GenericChartData> {
    console.log(hashtags);
    return this.httpClient.post<GenericChartData>('/api/data/tweets/count', {
      start: startDate.toISOString(),
      end: endDate.toISOString(),
      tags: hashtags
    }).pipe(map(data => this.mapData(data)));
  }

  public getInfectionsDataInRange(startDate: Date, endDate: Date): Observable<GenericChartData> {
    return this.httpClient.post<GenericChartData>('/api/data/active_cases',
      {
        start: startDate.toISOString(),
          end: endDate.toISOString(),
          avg: '7'
      }).pipe(map(data => this.mapData(data)));
  }

  public getDeathsDataInRange(startDate: Date, endDate: Date): Observable<GenericChartData> {
    return this.httpClient.post<GenericChartData>('/api/data/deaths',
      {
        start: startDate.toISOString(),
          end: endDate.toISOString(),
          avg: '7'
      }).pipe(map(data => this.mapData(data)));
  }

  public getDataInRange(endpoint: string, startDate: Date, endDate: Date): Observable<GenericChartData> {
    return this.httpClient.post<GenericChartData>(endpoint,
      {
        start: startDate.toISOString(),
          end: endDate.toISOString(),
          avg: '7'
      }).pipe(map(data => this.mapData(data)));
  }

  private mapData(data: any): any {
    data.date = data.date.map((x: any) => dateTimeFormat.format(new Date(x as string)))
    return data
  }
}
