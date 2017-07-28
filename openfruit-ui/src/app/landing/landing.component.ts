import {Component} from '@angular/core';
import {BreadCrumbService} from '../breadcrumb/breadcrumb.service';

@Component({
  selector: 'of-landing',
  templateUrl: './landing.html',
})

export class LandingComponent {
  constructor(breadcrumb: BreadCrumbService) {
    breadcrumb.reset();
  }
}
