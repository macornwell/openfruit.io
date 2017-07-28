import { Injectable } from '@angular/core';
import {Http, Response, Headers, RequestOptions} from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';


import {ConfigService} from '../config/config';

@Injectable()
export class AuthenticationService {
  public token: string;

  constructor(private http: Http, private _config: ConfigService) {
    // set token if saved in local storage
    let currentUser = JSON.parse(localStorage.getItem('currentUser'));
    this.token = currentUser && currentUser.token;
  }

  private get_options() {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    return options;
  }

  private cleanup() {
    this.token = null;
    localStorage.removeItem('currentUser');
  }

  is_logged_in() {
    if (!this.token) {
      console.log(this.token);
      console.log('no token');
      return false;
    }

    let options = this.get_options();
    this.http.post(this._config.apiUrl() + 'auth/verify/', '', options)
      .map((response: Response) => {
      console.log(response);
        let status = response.status;
        if (status === 200) {
          return true;
        } else {
          this.cleanup();
          return false;
        }
    });
  }

  refresh_token() {
    if (!this.token) {
      this.cleanup();
      return Observable.of(false);
    }
    let options = this.get_options();
    return this.http.post(this._config.apiUrl() + 'auth/refresh/', '', options)
      .map((response: Response) => {
        let status = response.status;
        if (status === 200) {
          return true;
        } else {
          this.cleanup();
          return false;
        }
      });
  }

  login(username: string, password: string): Observable<boolean> {
    let data = JSON.stringify({username: username, password: password});
    let options = this.get_options();
    return this.http.post(this._config.apiUrl() + 'auth/token/', data, options)
      .map((response: Response) => {
        // login successful if there's a jwt token in the response
        let token = response.json() && response.json().token;
        if (token) {
          // set token property
          this.token = token;

          // store username and jwt token in local storage to keep user logged in between page refreshes
          localStorage.setItem('currentUser', JSON.stringify({ username: username, token: token }));

          // return true to indicate successful login
          return true;
        } else {
          // return false to indicate failed login
          return false;
        }
      });
  }

  logout(): void {
    this.cleanup();
  }

}
