import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";

export interface BarChartData {
  value: Array<number>;
  date: Array<Label>;
}
