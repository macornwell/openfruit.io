import {Component, OnInit} from '@angular/core';

import { User } from '../_models/user';
import { UserService } from '../_services/user.service';
import {AuthenticationService} from '../_services/authentication.service';
import {Router} from '@angular/router';
import {BreadCrumbService} from '../breadcrumb/breadcrumb.service';
import {AuthGuard} from '../_guards/auth.guard';

@Component({
  selector: 'of-dashboard',
  templateUrl: './dashboard.html',
})

export class DashboardComponent implements OnInit {
  users: User[] = [];

  constructor(private userService: UserService,
              breadcrumb: BreadCrumbService,
              auth: AuthGuard
              ) {
    breadcrumb.reset();
    if (auth.canActivate()) {
      breadcrumb.addNode('Dashboard', '/dashboard');
    } else {
    }
  }

  ngOnInit() {
    this.userService.getUsers()
      .subscribe(users => {
        this.users = users;
      });
  }

}
