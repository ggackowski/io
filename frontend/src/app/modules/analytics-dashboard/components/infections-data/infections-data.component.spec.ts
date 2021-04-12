import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfectionsDataComponent } from './infections-data.component';

describe('InfectionsDataComponent', () => {
  let component: InfectionsDataComponent;
  let fixture: ComponentFixture<InfectionsDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InfectionsDataComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InfectionsDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
