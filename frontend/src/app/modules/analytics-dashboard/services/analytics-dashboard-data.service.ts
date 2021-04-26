import { Injectable } from '@angular/core';
import {AnalyticsDashboardRestService} from "./analytics-dashboard-rest.service";
import {Observable, Subject} from "rxjs";
import {BarChartData} from "../model/bar-chart-data.model";
import {map, tap} from "rxjs/operators";

export interface Hashtag {
  name: string;
  use: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardDataService {
  private infectionsData = new Subject<BarChartData>();
  private tweetsCount = new Subject<BarChartData>();
  private dataFirstLoaded = false;
  private loadingData = new Subject<void>();
  private hashtags: Array<Hashtag> = [];
  private startDate: Date =  new Date();
  private endDate: Date = new Date();

  constructor(
    private restService: AnalyticsDashboardRestService
  ) {
    this.setDefaultDataRange();
    this.getAvailableHashtags();
  }

  public getLoadingDataSubject(): Subject<void> {
    return this.loadingData;
  }

  public getHashtags(): Array<Hashtag> {
    return this.hashtags;
  }

  public getTweetsCountChartData(): Observable<BarChartData> {
    return this.tweetsCount.asObservable();
  }

  public getInfectionsData(): Observable<BarChartData> {
    return this.infectionsData.asObservable();
  }

  public getTweetsInRange(): Observable<BarChartData> {
    return this.tweetsCount.asObservable();
  }

  private getUsedHashtags(): Array<string> {
    return this.hashtags.filter(tag => tag.use).map(tag => tag.name);
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
    this.restService.getTweetsCountInRange(this.startDate, this.endDate, this.getUsedHashtags()).subscribe(
      data => this.tweetsCount.next(data)
    );
  }

  private setDefaultDataRange(): void {
    this.setDataRange(new Date('1.01.2021'), new Date());
  }

  public getAvailableHashtags(): void {
    this.restService.getAvailableHashtags()
      .pipe(map(hashtags => hashtags.map(hashtag => ({name: hashtag, use: false})))).subscribe(tags => {
        this.hashtags = tags;
      })
  }
}
