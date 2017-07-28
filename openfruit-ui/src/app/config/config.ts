import {Http} from '@angular/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import 'rxjs/Rx';

@Injectable()
export class ConfigService {
  private _config: Object;
  private _env: Object;

  constructor(private http: Http) {
  }

  load() {
    return new Promise((resolve, reject) => {
      this.http.get('assets/config/env.json')
      .map(res => res.json())
        .subscribe((env_data) => {
          this._env = env_data;
          this.http.get('assets/config/' + env_data.env + '.json')
          .map(res => res.json())
            .catch((error: any) => {
              console.error(error);
              return Observable.throw(error.json().error || 'Server error');
            })
            .subscribe((data) => {
              this._config = data;
              resolve(true);
            });
        });
    });
  }

  getEnv(key: any) {
    return this._env[key];
  }

  apiUrl() {
    return this.get('apiUrl');
  }

  adminUrl() {
    return this.get('adminUrl');
  }

  get(key: any) {
    return this._config[key];
  }
}
