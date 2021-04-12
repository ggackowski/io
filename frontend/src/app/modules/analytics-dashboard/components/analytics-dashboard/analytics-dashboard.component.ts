import { Component, OnInit } from '@angular/core';
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";
import {Label} from "ng2-charts";
import {ChartDataSets} from "chart.js";
import {faCog} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-analytics-dashboard',
  templateUrl: './analytics-dashboard.component.html',
  styleUrls: ['./analytics-dashboard.component.scss']
})
export class AnalyticsDashboardComponent implements OnInit {
  public dataSets: Array<ChartDataSets> = [];
  public labels: Array<Label> = [];
  public cogIcon = faCog;
  public dataLoaded = false;
  public open: boolean = false;

  constructor(
      private dataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.loadTweetsCountChartData();
  }

  private loadTweetsCountChartData(): void {
    this.dataService.getTweetsCountChartData().subscribe(data => {
      console.log(data);
      // this.dataSets = data.dataSets;
      // this.labels = data.date;
      // this.dataLoaded = true;
    })
  }

}
