import { Component, OnInit } from '@angular/core';
import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";
import {faCog} from "@fortawesome/free-solid-svg-icons";
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";
import {Subject, zip} from "rxjs";
import {BarChartData, GenericChartData} from "../../model/bar-chart-data.model";

@Component({
  selector: 'app-infections-data',
  templateUrl: './infections-data.component.html',
  styleUrls: ['./infections-data.component.scss']
})
export class InfectionsDataComponent implements OnInit {
  public data: Subject<GenericChartData>;
  public dataSets: Array<ChartDataSets> = [];
  public labels: Array<Label> = [];
  public cogIcon = faCog;
  public dataLoaded = false;

  constructor(
    private analyticsDashboardDataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.data = this.analyticsDashboardDataService.getDataByName('tweetsCount')
    this.subscribeToLoadingDataSubject();
    this.getData();
  }

  private subscribeToLoadingDataSubject(): void {
    this.analyticsDashboardDataService.getLoadingDataSubject().subscribe(() => {
      this.dataLoaded = false;
    });
  }

  private getData(): void {
    this.data.subscribe(data => {
      this.labels.length = 0;
      this.dataSets.length = 0;
      this.labels.push(...data.date);
      data.values.forEach(chartValue => {
        this.dataSets.push({label: chartValue.displayName, type: chartValue.type, data: chartValue.value})
      });
      this.dataLoaded = true;
    });
    // zip(this.analyticsDashboardDataService.getInfectionsData(), this.analyticsDashboardDataService.getNewCasesInDaysData())
    //   .subscribe(data => {
    //     console.log(data);
    //     this.dataSets =  [{ data: data[0].value, label: 'New cases' }, {data: data[1].value, label: 'New cases difference'}, {type: 'line', data: data[0].avg, label: 'Avg'}];
    //     this.labels.length = 0;
    //     this.labels.push(...data[0].date);
    //     this.dataLoaded = true;
    //   });
    // this.analyticsDashboardDataService.getInfectionsData().subscribe(data => {
    //   console.log(data);
    //   this.dataSets =  [{ data: data.value, label: '' }];
    //   this.labels.length = 0;
    //   this.labels.push(...data.date);
    //   this.dataLoaded = true;
    // })
  }

}
