import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TweetsCountComponent } from './tweets-count.component';

describe('TweetsCountComponent', () => {
  let component: TweetsCountComponent;
  let fixture: ComponentFixture<TweetsCountComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TweetsCountComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TweetsCountComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
