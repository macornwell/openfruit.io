import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import { AuthenticationService } from '../_services/authentication.service';
import { User } from '../_models/user';
import {ConfigService} from '../config/config';
import {Router} from '@angular/router';

@Injectable()
export class UserService {
  constructor(
    private http: Http,
    private router: Router,
    private authenticationService: AuthenticationService,
    private _config: ConfigService) {
  }

  getUsers(): Observable<User[]> {
    this.authenticationService.refresh_token().map((wasRefreshed: boolean) => {
      if (wasRefreshed) {
        let headers = new Headers({ 'Authorization': 'JWT ' + this.authenticationService.token });
        let options = new RequestOptions({ headers: headers });
        return this.http.get(this._config.apiUrl() + 'users/', options)
          .map((response: Response) => response.json());
      } else {
        this.router.navigate(['/login']);
      }
    });
    return Observable.of([]);
  }
}
