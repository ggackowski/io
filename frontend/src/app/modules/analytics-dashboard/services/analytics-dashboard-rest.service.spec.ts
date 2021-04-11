import { TestBed } from '@angular/core/testing';

import { AnalyticsDashboardRestService } from './analytics-dashboard-rest.service';

describe('AnalyticsDashboardRestService', () => {
  let service: AnalyticsDashboardRestService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnalyticsDashboardRestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
