import { Component, OnInit } from '@angular/core';
import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";
import {faCog} from "@fortawesome/free-solid-svg-icons";
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";

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
    this.getInfectionsData();
  }


  private getInfectionsData(): void {
    this.analyticsDashboardDataService.getInfectionsData().subscribe(data => {
      console.log('new data');
      this.dataSets = data.dataSets;
      this.labels = data.labels;
      this.dataLoaded = true;
    })
  }

}