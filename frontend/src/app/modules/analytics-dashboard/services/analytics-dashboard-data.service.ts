import { Injectable } from '@angular/core';
import {AnalyticsDashboardRestService} from "./analytics-dashboard-rest.service";
import {Observable, Subject} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";
import {tap} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardDataService {
  private infectionsData = new Subject<BarChartData>();
  private dataFirstLoaded = false;
  private loadingData = new Subject<void>();
  private startDate: Date =  new Date();
  private endDate: Date = new Date();

  constructor(
    private restService: AnalyticsDashboardRestService
  ) {
    this.setDefaultDataRange();
  }

  public getLoadingDataSubject(): Subject<void> {
    return this.loadingData;
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
    this.dataFirstLoaded = true;
    this.loadingData.next();
    this.restService.getInfectionsDataInRange(this.startDate, this.endDate).pipe(tap(console.log))
      .subscribe(data => this.infectionsData.next(data));
  }

  private setDefaultDataRange(): void {
    this.setDataRange(new Date('1.01.2021'), new Date());
  }

  public getAvailableHashtags(): Observable<Array<string>> {
    return this.restService.getAvailableHashtags();
  }
}
