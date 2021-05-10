import { Component, OnInit } from '@angular/core';
import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";
import {faCog} from "@fortawesome/free-solid-svg-icons";
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";
import {zip} from "rxjs";

@Component({
  selector: 'app-infections-data',
  templateUrl: './infections-data.component.html',
  styleUrls: ['./infections-data.component.scss']
})
export class InfectionsDataComponent implements OnInit {
  public dataSets: Array<ChartDataSets> = [];
  public labels: Array<Label> = [];
  public cogIcon = faCog;
  public dataLoaded = false;

  constructor(
    private analyticsDashboardDataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.subscribeToLoadingDataSubject();
    this.getInfectionsData();
  }

  private subscribeToLoadingDataSubject(): void {
    this.analyticsDashboardDataService.getLoadingDataSubject().subscribe(() => {
      this.dataLoaded = false;
    });
  }

  private getInfectionsData(): void {
    zip(this.analyticsDashboardDataService.getInfectionsData(), this.analyticsDashboardDataService.getNewCasesInDaysData())
      .subscribe(data => {
        console.log(data);
        this.dataSets =  [{ data: data[0].value, label: 'New cases' }, {data: data[1].value, label: 'New cases difference'}];
        this.labels.length = 0;
        this.labels.push(...data[0].date);
        this.dataLoaded = true;
      });
    // this.analyticsDashboardDataService.getInfectionsData().subscribe(data => {
    //   console.log(data);
    //   this.dataSets =  [{ data: data.value, label: '' }];
    //   this.labels.length = 0;
    //   this.labels.push(...data.date);
    //   this.dataLoaded = true;
    // })
  }

}
