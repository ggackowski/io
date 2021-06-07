import { ViewChild } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { ColumnMode, DatatableComponent } from '@swimlane/ngx-datatable';
import {AnalyticsDashboardDataService} from "../../services/analytics-dashboard-data.service";



@Component({
  selector: 'app-top-data',
  templateUrl: './top-data.component.html',
  styleUrls: ['./top-data.component.scss']
})
export class TopDataComponent implements OnInit {
  rows: any = [];
  temp: any = [];
  loadingIndicator = true;
  reorderable = true;
  @ViewChild(DatatableComponent) table: DatatableComponent;
  columns = [{ prop: 'Username' }, { prop: 'Count' }, { prop: 'Likes' }, {prop: "Replies" }, {prop: "Retweets"}];

  ColumnMode = ColumnMode;

  constructor(
    private analyticsDashboardDataService: AnalyticsDashboardDataService
  ) { }

  ngOnInit(): void {
    this.analyticsDashboardDataService.getTopData().subscribe(data => {
      console.log('ok', data);
      this.loadingIndicator = false;
      this.rows = data;
    });
    // setTimeout(() => {
    //
    //   // this.rows = [{
    //   //   Username: 'rzeczpospolita',
    //   //   Count: 12206,
    //   //   Likes: 45343,
    //   //   Replies: 3454,
    //   //   Retweets:3445
    //   // },
    //   //   {
    //   //     Username: 'tvp_info',
    //   //     Count: 7791,
    //   //     Likes: 3454,
    //   //     Replies: 3445,
    //   //     Retweets:2223
    //   //   },
    //   //   {
    //   //     Username: 'polskiegoradio24',
    //   //     Count: 7110,
    //   //     Likes: 5433,
    //   //     Replies: 2345,
    //   //     Retweets:4554
    //   //   },
    //   //   {
    //   //     Username: 'marekzadecki',
    //   //     Count: 4809,
    //   //     Likes: 2345,
    //   //     Replies: 4534,
    //   //     Retweets:333
    //   //   },
    //   //   {
    //   //     Username: 'int_wydarzenia',
    //   //     Count: 4754,
    //   //     Likes: 2378,
    //   //     Replies: 876,
    //   //     Retweets:236
    //   //   },
    //   //   {
    //   //     Username: 'republikatv',
    //   //     Count: 3875,
    //   //     Likes: 6775,
    //   //     Replies: 9865,
    //   //     Retweets:786
    //   //   }];
    //
    // }, 500);
  }

  updateFilter(event: any) {
    const val = event.target.value.toLowerCase();

    // filter our data
    const temp = this.temp.filter(function (d: any) {
      return d.Username.toLowerCase().indexOf(val) !== -1 || !val;
    });

    // update the rows
    this.rows = temp;
    // Whenever the filter changes, always go back to the first page
    this.table.offset = 0;
  }

}
