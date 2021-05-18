import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopDataComponent } from './top-data.component';

describe('TopDataComponent', () => {
  let component: TopDataComponent;
  let fixture: ComponentFixture<TopDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TopDataComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TopDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
