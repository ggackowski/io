import { Component, OnInit } from '@angular/core';
import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";
import {faCog} from "@fortawesome/free-solid-svg-icons";
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";

@Component({
  selector: 'app-tweets-count',
  templateUrl: './tweets-count.component.html',
  styleUrls: ['./tweets-count.component.scss']
})
export class TweetsCountComponent implements OnInit {
  public dataSets: Array<ChartDataSets> = [];
  public labels: Array<Label> = [];
  public cogIcon = faCog;
  public dataLoaded = false;

  constructor(
    private analyticsDashboardDataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.subscribeToLoadingDataSubject();
    this.getTweetsCountData();
  }

  private subscribeToLoadingDataSubject(): void {
    this.analyticsDashboardDataService.getLoadingDataSubject().subscribe(() => {
      this.dataLoaded = false;
    });
  }

  private getTweetsCountData(): void {
    this.analyticsDashboardDataService.getTweetsInRange().subscribe(data => {
      console.log(data);
      this.dataSets =  [{ data: data.value, label: 'Tweets' }];
      this.labels.length = 0;
      this.labels.push(...data.date);
      this.dataLoaded = true;
    })
  }

}
