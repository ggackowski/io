import { Injectable } from '@angular/core';
import {AnalyticsDashboardRestService} from "./analytics-dashboard-rest.service";
import {BehaviorSubject, Observable, Subject} from "rxjs";
import {AvgChartData, BarChartData, GenericChartData} from "../model/bar-chart-data.model";
import {filter, map, tap} from "rxjs/operators";
import {TopData} from "../model/top-data.model";

export interface Hashtag {
  name: string;
  use: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDashboardDataService {
  private data = new Subject<GenericChartData>();
  // @ts-ignore
  private infectionsData = new BehaviorSubject<GenericChartData>(null);
  // @ts-ignore
  private deathsData = new BehaviorSubject<GenericChartData>(null);
  // @ts-ignore
  private quarantineData = new BehaviorSubject<GenericChartData>(null);
  // @ts-ignore
  private intenseData = new BehaviorSubject<GenericChartData>(null);
  // @ts-ignore
  private vaccinatedData = new BehaviorSubject<GenericChartData>(null);
  // @ts-ignore
  private curedData = new BehaviorSubject<GenericChartData>(null);
  // @ts-ignore
  private tweetsCount = new BehaviorSubject<GenericChartData>(null);
  // @ts-ignore
  private topData = new BehaviorSubject<Array<TopData>>(null);
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

  public getData(): Observable<GenericChartData> {
    return this.data.pipe(filter(x => x !== null));
  }

  public getLoadingDataSubject(): Subject<void> {
    return this.loadingData;
  }

  public getHashtags(): Array<Hashtag> {
    return this.hashtags;
  }

  public getTopData(): Observable<Array<TopData>> {
    return this.topData.pipe(filter(x => x !== null));
  }

  public getDataByName(dataName: string): BehaviorSubject<GenericChartData> {
    if (dataName === 'tweetsCount') return this.tweetsCount;
    if (dataName === 'infectionsCount') return this.infectionsData;
    if (dataName === 'deathsCount') return this.deathsData;
    if (dataName === 'quarantine') return this.quarantineData;
    if (dataName === 'intense') return this.intenseData;
    if (dataName === 'vaccinated') return this.vaccinatedData;
    if (dataName === 'cured') return this.curedData;
    // @ts-ignore
    return new BehaviorSubject<GenericChartData>(null);
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
      .subscribe(data => { this.infectionsData.next(data) });
    this.restService.getTweetsCountInRange(this.startDate, this.endDate, this.getUsedHashtags()).subscribe(
      data => this.tweetsCount.next(data)
    );
    this.restService.getDataInRange('/api/data/deaths', this.startDate, this.endDate)
      .subscribe(data => { this.deathsData.next(data) })
    this.restService.getDataInRange('/api/data/quarantine', this.startDate, this.endDate)
      .subscribe(data => { this.quarantineData.next(data) })
    this.restService.getDataInRange('/api/data/intense', this.startDate, this.endDate)
      .subscribe(data => { this.intenseData.next(data) })
    this.restService.getDataInRange('/api/data/vaccinated', this.startDate, this.endDate)
      .subscribe(data => { this.vaccinatedData.next(data) })
    this.restService.getDataInRange('/api/data/cured', this.startDate, this.endDate)
      .subscribe(data => { this.curedData.next(data) })
    this.restService.getTopDataInRange(this.startDate, this.endDate, this.getUsedHashtags())
      .subscribe(data => { this.topData.next(data); })
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
