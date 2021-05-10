import { Component, OnInit } from '@angular/core';
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";
import {Label} from "ng2-charts";
import {ChartDataSets} from "chart.js";
import {faCog} from '@fortawesome/free-solid-svg-icons';
import {zip} from "rxjs";

@Component({
  selector: 'app-analytics-dashboard',
  templateUrl: './analytics-dashboard.component.html',
  styleUrls: ['./analytics-dashboard.component.scss']
})
export class AnalyticsDashboardComponent implements OnInit {
  public newCasesToday: number = 0;
  public newTweetsToday: number = 0;
  public newCasesDifference: number = 0;
  public newTweetsDifference: number = 0;
  public newTweetsLoaded = false;
  public newCasesLoaded = false;
  public labels: Array<Label> = [];
  public cogIcon = faCog;
  public dataLoaded = false;
  public open: boolean = false;

  constructor(
      private dataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    // this.loadNewCasesToday();
    // this.loadTweetsCountToday();
  }

  // private loadTweetsCountToday(): void {
  //   zip(this.dataService.getTweetsCountChartData()).subscribe(data => {
  //     // console.log(data);
  //     this.newTweetsToday = data[0].value[data[0].value.length - 1];
  //     // this.dataSets = data.dataSets;
  //     // this.labels = data.labels;
  //     // this.dataLoaded = true;
  //     this.newTweetsLoaded = true;
  //   });
  // }

  // private loadNewCasesToday(): void {
  //   zip(this.dataService.getInfectionsData(), this.dataService.getNewCasesInDaysData()).subscribe(data => {
  //     // console.log(data);
  //     this.newCasesToday = data[0].value[data[0].value.length - 1];
  //     this.newCasesDifference = data[1].value[data[1].value.length - 1];
  //     // this.dataSets = data.dataSets;
  //     // this.labels = data.labels;
  //     // this.dataLoaded = true;
  //     this.newCasesLoaded = true;
  //   });
  // }

}
