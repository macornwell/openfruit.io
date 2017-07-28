import { Component, OnInit } from '@angular/core';
import {Response} from '@angular/http';
import { Router } from '@angular/router';

import { AuthenticationService } from '../_services/authentication.service';

@Component({
  moduleId: module.id,
  templateUrl: 'login.html'
})

export class LoginComponent implements OnInit {
  model: any = {};
  loading = false;
  error = '';

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService) { }

  ngOnInit() {
    // reset login status
    this.authenticationService.logout();
  }

  login() {
    this.loading = true;
    this.authenticationService.login(this.model.username, this.model.password)
      .catch(this.handleError)
      .subscribe(success => {
        console.log('success');
        this.router.navigate(['/dashboard']);
        this.loading = false;
      }, failure => {
        this.error = 'Username or password is incorrect';
        this.loading = false;
      });
  }

  private handleError (error: Response | any) {
    console.log('inside error');
    // In a real world app, we might use a remote logging infrastructure
    let errMsg: string;
    if (error instanceof Response) {
      const body = error.json() || '';
      const err = body.error || JSON.stringify(body);
      errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
    } else {
      errMsg = error.message ? error.message : error.toString();
    }
    console.error(errMsg);
    return Promise.reject(errMsg);
  }

  logout() {
    this.authenticationService.logout();
    this.router.navigate(['/']);
  }
}
