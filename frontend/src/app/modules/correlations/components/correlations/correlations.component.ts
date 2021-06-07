import { Component, OnInit } from '@angular/core';
import {CorrelationsRestService} from "../../services/correlations-rest.service";
import {FormControl, FormGroup} from "@angular/forms";
import {CorrelationData} from "../../model/CorrelationData.model";

@Component({
  selector: 'app-correlations',
  templateUrl: './correlations.component.html',
  styleUrls: ['./correlations.component.scss']
})
export class CorrelationsComponent implements OnInit {
  correlationType = new FormControl();
  dataRange = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });
  correlation: CorrelationData;
  loaded = false;

  constructor(
    private restService: CorrelationsRestService
  ) { }

  ngOnInit(): void {

  }

  public showCorrelations(): void {
    this.restService.testGetCorrelation(
      new Date(this.dataRange.get('start')?.value), new Date(this.dataRange.get('end')?.value), this.correlationType.value
    ).subscribe(correlations => {
      console.log('got them', correlations);
      this.correlation = correlations;
      this.loaded = true;
    });
  }

}
