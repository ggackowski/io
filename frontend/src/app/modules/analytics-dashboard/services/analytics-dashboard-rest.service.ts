import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardRestService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public getTweetsCountChartData(): Observable<BarChartData> {
    return of(
      {
      dataSets: [
        {
          data: [1, 2, 3, 4, 5],
          label: 'test'
        }
      ],
      labels: [
        'a', 'b', 'c', 'd', 'e'
      ]
    }
    );
    //return this.httpClient.get('');
  }
}
