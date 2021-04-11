import { TestBed } from '@angular/core/testing';

import { AnalyticsDashboardDataService } from './anaytical-dashboard-data.service';

describe('AnayticalDashboardDataService', () => {
  let service: AnalyticsDashboardDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnalyticsDashboardDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
