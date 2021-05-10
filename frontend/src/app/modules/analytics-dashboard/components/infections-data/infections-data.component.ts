import { Component, OnInit } from '@angular/core';
import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";
import {faCog} from "@fortawesome/free-solid-svg-icons";
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";
import {BehaviorSubject, Observable, Subject, zip} from "rxjs";
import {BarChartData, GenericChartData} from "../../model/bar-chart-data.model";
import {filter} from "rxjs/operators";

@Component({
  selector: 'app-infections-data',
  templateUrl: './infections-data.component.html',
  styleUrls: ['./infections-data.component.scss']
})
export class InfectionsDataComponent implements OnInit {
  public possibleDataSources = [
    'infectionsCount', 'tweetsCount'
  ];
  public data: BehaviorSubject<GenericChartData>;
  public dataSets: Array<ChartDataSets> = [];
  public labels: Array<Label> = [];
  public cogIcon = faCog;
  public dataLoaded = false;

  constructor(
    private analyticsDashboardDataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.data = this.analyticsDashboardDataService.getDataByName('infectionsCount');
    this.subscribeToLoadingDataSubject();
    this.getData();
    // setTimeout(() => {  }, 500);
  }

  public changeGraph(name: string): void {
      this.data = this.analyticsDashboardDataService.getDataByName(name);
      this.dataLoaded = false;
      this.updateChartData(this.data.getValue());
  }

  private subscribeToLoadingDataSubject(): void {
    this.analyticsDashboardDataService.getLoadingDataSubject().subscribe(() => {
      this.dataLoaded = false;
    });
  }

  private getData(): void {
    this.data.pipe(filter(x => x !== null)).subscribe(data => {
      this.updateChartData(data);
    });
  }

  private updateChartData(data: GenericChartData): void {
    console.log('get');
    this.labels.length = 0;
    this.dataSets.length = 0;
    const temp: ChartDataSets[] | { label: string; type: string; data: number[]; }[] = [];

    data.values.forEach(chartValue => {
      temp.push({label: chartValue.displayName, type: chartValue.type, data: chartValue.value})
    });

    this.dataSets = temp;
    this.labels.push(...data.date);
    setTimeout(() => this.dataLoaded = true, 100);
  }

}
