import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
})
export class AboutComponent implements OnInit {
  technologies = [
    'Angular 2',
    'Django',
    'Django Rest Framework',
    'Google Material',
    'Python NLTK',

  ];

  constructor() { }

  ngOnInit() {
  }

}
