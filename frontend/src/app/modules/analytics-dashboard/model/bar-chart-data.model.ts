import {ChartDataSets} from "chart.js";
import {Label} from "ng2-charts";

export interface BarChartData {
  value: Array<number>;
  date: Array<Label>;
}

export interface AvgChartData extends BarChartData {
  avg: Array<number>;
}


export interface GenericChartData {
  date: Array<Label>;
  values: Array<ChartValue>;
}

export interface ChartValue {
  displayName: string;
  type: string;
  value: Array<number>;
  stats: Array<ChartStats>;
}

// export interface Interface {
//
// }

export interface ChartStats {
  displayName: string;
  value: number;
}
