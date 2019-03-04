import {Component, ViewChild, HostListener, OnInit} from '@angular/core';
import 'rxjs/add/observable/of';
import {DrinksService} from '../../_services/drinks.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})


export class HomeComponent implements OnInit{
  @ViewChild('mynav') sidenav;
  resizeTimeout = setTimeout((() => {
    this.correctSidenav();
  }).bind(this), 100);

  @HostListener('window:resize')
  onWindowResize() {
    if (this.resizeTimeout) {
      clearTimeout(this.resizeTimeout);
    }
    this.resizeTimeout = setTimeout((() => {
      this.correctSidenav();
    }).bind(this), 200);
  }

  constructor(private drinkService: DrinksService) {
  }

  ngOnInit() {
    this.drinkService.drinksToggle
      .subscribe(
        (data) => {
          if (this.sidenav) {
            this.sidenav.toggle();
          }
        }
      )
  }

  correctSidenav() {
    if (this.sidenav) {
      if (window.innerWidth < 580) {
        this.sidenav.close();
        this.sidenav.mode = 'push'
      } else {
        this.sidenav.open();
        this.sidenav.mode = 'side'
      }
    }
  }
  onScroll() {
    console.log('Scrolling');
  }

}

