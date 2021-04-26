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

  public getAvailableHashtags(): Observable<Array<string>> {
    return this.httpClient.get<Array<string>>('/api/data/hashtags');
  }

  public getTweetsCountInRange(startDate: Date, endDate: Date, hashtags: Array<string>): Observable<BarChartData> {
    console.log(hashtags);
    return this.httpClient.get<Array<string>>('/api/data/tweets/count').pipe(tap(console.log));

    return of({
      date: ['1'],
      value: [10]
    }).pipe(delay(200));
  }

  public getInfectionsDataInRange(startDate: Date, endDate: Date): Observable<BarChartData> {
    // console.log(startDate, new Date(2021, 3, 1), startDate === new Date(2021, 3, 1));
    // if (startDate. new Date(2021, 3, 1))
      return of({
        date: ['10', '20'],
        value: [10, 20]
      }).pipe(delay(400))
    // return of({
    //   date: ['11', '22'],
    //   value: [13, 24]
    // }).pipe(delay(400))
    // return this.httpClient.get<BarChartData>('/api/data/active_cases',
    //   {params: {start: startDate.toISOString(), end: endDate.toISOString()}})
    //   .pipe(map(data => {
    //     data.date = data.date.map(x => dateTimeFormat.format(new Date(x as string)))
    //     return data
    // }), tap(console.log));
  }
}
