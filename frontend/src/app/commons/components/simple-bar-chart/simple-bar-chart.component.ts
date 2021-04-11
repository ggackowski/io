import {Component, Input, OnInit} from '@angular/core';
import {ChartDataSets, ChartOptions, ChartType} from "chart.js";
import {Label} from "ng2-charts";


interface ChartData {
  options: ChartOptions;
  labels: Array<Label>;
  type: ChartType;
  showLegend: boolean;
  plugins: Array<any>;
  dataSets: Array<ChartDataSets>;
}


@Component({
  selector: 'app-simple-bar-chart',
  templateUrl: './simple-bar-chart.component.html',
  styleUrls: ['./simple-bar-chart.component.scss']
})
export class SimpleBarChartComponent implements OnInit {
  @Input() labels: Array<Label> = [];
  @Input() dataSets: Array<ChartDataSets> = [];

  public chartData: ChartData;

  public constructor() { }

  public ngOnInit(): void {
    this.chartData = {
      options: { responsive: true },
      labels: this.labels,
      type: 'bar',
      showLegend: true,
      plugins: [],
      dataSets: this.dataSets
    };
  }

}
