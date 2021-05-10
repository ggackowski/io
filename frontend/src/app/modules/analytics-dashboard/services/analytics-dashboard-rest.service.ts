import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";
import {delay, map, tap} from "rxjs/operators";
const dateTimeFormat =  new Intl.DateTimeFormat()

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardRestService {

  constructor(
    private httpClient: HttpClient
  ) { }

  // public getTweetsCountChartData(): Observable<BarChartData> {
  //   return this.httpClient.get<BarChartData>('/api/data/infections', {}).pipe(tap(console.log));
  // }

  public getNewCasesInDays(startDate: Date, endDate: Date): Observable<BarChartData> {
    return this.httpClient.get<BarChartData>('/api/data/active_cases/today',
      {params: {start: startDate.toISOString(), end: endDate.toISOString()}})
      .pipe(map(data => {
        data.date = data.date.map(x => dateTimeFormat.format(new Date(x as string)))
        return data
      }), tap(console.log));
  }

  public getNewTweetsDifference(startDate: Date, endDate: Date): Observable<BarChartData> {
    return this.httpClient.get<BarChartData>('/api/data/tweets/count/today',
      {params: {start: startDate.toISOString(), end: endDate.toISOString()}})
      .pipe(map(data => {
        data.date = data.date.map(x => dateTimeFormat.format(new Date(x as string)))
        return data
      }), tap(console.log));
  }

  public getAvailableHashtags(): Observable<Array<string>> {
    return this.httpClient.get<Array<string>>('/api/data/hashtags');
  }

  public getTweetsCountInRange(startDate: Date, endDate: Date, hashtags: Array<string>): Observable<BarChartData> {
    console.log(hashtags);
    return this.httpClient.post<BarChartData>('/api/data/tweets/count', {
      start: startDate.toISOString(),
      end: endDate.toISOString(),
      tags: hashtags
    }).pipe(map(data => {
      data.date = data.date.map(x => dateTimeFormat.format(new Date(x as string)))
      return data
    }), tap(console.log));
  }

  public getInfectionsDataInRange(startDate: Date, endDate: Date): Observable<BarChartData> {
    return this.httpClient.get<BarChartData>('/api/data/active_cases',
      {params: {start: startDate.toISOString(), end: endDate.toISOString()}})
      .pipe(map(data => {
        data.date = data.date.map(x => dateTimeFormat.format(new Date(x as string)))
        return data
    }), tap(console.log));
  }
}
