import { TestBed } from '@angular/core/testing';

import { Templates } from './templates';

describe('Templates', () => {
  let service: Templates;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Templates);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
