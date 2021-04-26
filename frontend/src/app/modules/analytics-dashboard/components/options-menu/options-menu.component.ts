import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";
import {FormControl, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-options-menu',
  templateUrl: './options-menu.component.html',
  styleUrls: ['./options-menu.component.scss']
})
export class OptionsMenuComponent implements OnInit {
  @Output() closeMenu = new EventEmitter();
  public hashtags = ['#koronawirus', '#szczepienia'];

  dataRange = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });

  constructor(
    private analyticsDashboardDataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.getInitialDataRange();
    this.subscribeToAvailableHashtags();
  }

  public saveSettings(): void {
    this.analyticsDashboardDataService.setDataRange
      (new Date(this.dataRange.get('start')?.value), new Date(this.dataRange.get('end')?.value));
    this.closeMenu.emit();
  }

  private getInitialDataRange(): void {
    const { begin, end } = this.analyticsDashboardDataService.getDataRange();
    this.dataRange.get('start')?.setValue(begin);
    this.dataRange.get('end')?.setValue(end);
  }

  private subscribeToAvailableHashtags(): void {
    this.analyticsDashboardDataService.getAvailableHashtags().subscribe(hashtags => {
      this.hashtags = hashtags;
    });
  }

}
