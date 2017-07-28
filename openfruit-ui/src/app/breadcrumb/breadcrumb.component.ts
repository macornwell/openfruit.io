import { Component } from '@angular/core';
import {BreadCrumbService} from './breadcrumb.service';

@Component({
  selector: 'of-breadcrumb',
  templateUrl: './breadcrumb.html',
})

export class BreadCrumbComponent {
  constructor(private _breadcrumbService: BreadCrumbService) {
  }
}
