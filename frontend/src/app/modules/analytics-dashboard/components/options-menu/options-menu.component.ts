import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {AnalyticsDashboardDataService, Hashtag} from "../../services/analytics-dashboard-data.service";
import {FormControl, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-options-menu',
  templateUrl: './options-menu.component.html',
  styleUrls: ['./options-menu.component.scss']
})
export class OptionsMenuComponent implements OnInit {
  @Output() closeMenu = new EventEmitter();
  public hashtags: Array<Hashtag> = [];

  dataRange = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });

  constructor(
    public analyticsDashboardDataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.getInitialDataRange();
    this.getHashtags();
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

  private getHashtags(): void {
    this.hashtags = this.analyticsDashboardDataService.getHashtags();
  }

  // public toggleHashtag(hashtag: string): void {
  //   const hashtags = this.analyticsDashboardDataService.selectedHashtags;
  //   if (hashtags.includes(hashtag)) {
  //     hashtags.splice(hashtags.indexOf(hashtag), 1);
  //   } else {
  //     hashtags.push(hashtag);
  //   }
  //   console.log(hashtags);
  // }
}
