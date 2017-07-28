import { Component } from '@angular/core';
import {ConfigService} from '../config/config';
import {AuthGuard} from '../_guards/auth.guard';
import {AuthenticationService} from '../_services/authentication.service';
import {Router} from '@angular/router';
@Component({
  selector: 'of-navigation',
  templateUrl: './navigation.html',
})
export class NavigationComponent {
  public apiUrl: string;
  constructor(private _config: ConfigService,
              private _auth: AuthGuard,
              private auth: AuthenticationService,
              private router: Router) {
    this.apiUrl = _config.get('apiUrl');
  }

  userIsLoggedIn() {
    let result = this._auth.canActivate();
    console.log('Logged in?');
    console.log(result);
    return result;
  }


  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }
}
