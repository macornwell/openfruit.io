import {APP_INITIALIZER, NgModule}      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {AlertModule, BsDropdownModule} from 'ngx-bootstrap';
import { HttpModule, JsonpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';

import { BaseRequestOptions } from '@angular/http';

import { AppComponent }  from './app.component';
import { routing } from './app.routing';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NavigationComponent } from './navigation/navigation.component';
import { BreadCrumbComponent } from './breadcrumb/breadcrumb.component';
import { BreadCrumbService } from './breadcrumb/breadcrumb.service';

import { AuthGuard } from './_guards/auth.guard';
import { AuthenticationService } from './_services/authentication.service';
import { UserService } from './_services/user.service';
import { LoginComponent } from './login/login.component';

import { ConfigService } from './config/config';
import {LandingComponent} from './landing/landing.component';

@NgModule({
  imports:      [
    BrowserModule,
    HttpModule,
    JsonpModule,
    FormsModule,
    AlertModule.forRoot(),
    BsDropdownModule.forRoot(),
    routing,
  ],
  declarations: [
    AppComponent,
    LandingComponent,
    DashboardComponent,
    NavigationComponent,
    BreadCrumbComponent,
    LoginComponent,
  ],
  bootstrap:    [ AppComponent ],
  providers: [
    AuthGuard,
    AuthenticationService,
    BreadCrumbService,
    UserService,
    BaseRequestOptions,
    ConfigService,
    {
      provide: APP_INITIALIZER,
      useFactory: (config: ConfigService) => () => config.load(),
      deps: [ConfigService],
      multi: true
    }
  ]
})
export class AppModule { }
