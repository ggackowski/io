export interface Correlation {
  correlation: number;
  pValue: number;
}

export interface CorrelationData {
  correlation_matrix: Array<Array<Correlation>>;
  index_mapping: Array<string>;
}
