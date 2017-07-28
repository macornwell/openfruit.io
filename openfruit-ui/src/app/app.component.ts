import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'my-app',
  templateUrl: './app.html',
})
export class AppComponent  {
  constructor(titleService: Title) {
    titleService.setTitle('Open Fruit - The Community Fruit Source');
  }
}
