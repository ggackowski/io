import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";

export interface BarChartData {
  dataSets: Array<ChartDataSets>;
  labels: Array<Label>;
}
