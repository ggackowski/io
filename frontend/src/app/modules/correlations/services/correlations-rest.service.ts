import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {CorrelationData} from "../model/CorrelationData.model";
import {Observable} from "rxjs";
import {tap} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class CorrelationsRestService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public testGetCorrelation(from: Date, to: Date, correlationType: string): Observable<CorrelationData> {
    return this.httpClient.post<CorrelationData>(`/api/data/correlation_matrix`, {
      start: from.toISOString(),
      end: to.toISOString(),
      correlation: correlationType
    }).pipe(tap((x => console.log(x))));
  }
}
