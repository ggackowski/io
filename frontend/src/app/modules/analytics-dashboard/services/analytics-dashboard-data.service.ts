import { Injectable } from '@angular/core';
import {AnalyticsDashboardRestService} from "./analytics-dashboard-rest.service";
import {Observable, Subject} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardDataService {
  private infectionsData = new Subject<BarChartData>();
  private startDate: Date =  new Date();
  private endDate: Date = new Date();

  constructor(
    private restService: AnalyticsDashboardRestService
  ) {
    this.setDataRange(new Date('1.01.2021'), new Date());
  }

  public getTweetsCountChartData(): Observable<BarChartData> {
    return this.restService.getTweetsCountChartData();
  }

  public getInfectionsData(): Observable<BarChartData> {
    return this.infectionsData.asObservable();
  }

  public getDataRange(): {begin: Date, end: Date} {
    return {
      begin: this.startDate,
      end: this.endDate
    };
  }

  public setDataRange(begin: Date, end: Date): void {
    this.startDate = begin;
    this.endDate = end;
    console.log(this.startDate, this.endDate);
    this.restService.getInfectionsDataInRange(this.startDate, this.endDate)
      .subscribe(data => this.infectionsData.next(data));
  }
}
