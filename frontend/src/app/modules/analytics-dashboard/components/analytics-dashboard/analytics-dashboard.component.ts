import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-analytics-dashboard',
  templateUrl: './analytics-dashboard.component.html',
  styleUrls: ['./analytics-dashboard.component.scss']
})
export class AnalyticsDashboardComponent implements OnInit {
  text: string = "There will be something soon"
  constructor() { }

  ngOnInit(): void {
    fetch('/api').then(res => res.json()).then(data => {
      this.text = data
    })
  }

}
