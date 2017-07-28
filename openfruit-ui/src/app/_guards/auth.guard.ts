import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import {AuthenticationService} from '../_services/authentication.service';

@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private auth: AuthenticationService) {
  }

  canActivate() {
    if (this.auth.is_logged_in()) {
      return true;
    }
    return false;
  }
}
