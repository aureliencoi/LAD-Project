import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MediaDetail } from './media-detail';

describe('MediaDetail', () => {
  let component: MediaDetail;
  let fixture: ComponentFixture<MediaDetail>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MediaDetail]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MediaDetail);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
