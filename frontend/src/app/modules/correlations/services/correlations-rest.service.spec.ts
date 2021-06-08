import { TestBed } from '@angular/core/testing';

import { CorrelationsRestService } from './correlations-rest.service';

describe('CorrelationsRestService', () => {
  let service: CorrelationsRestService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CorrelationsRestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
