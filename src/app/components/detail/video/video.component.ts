import { Component, OnInit } from '@angular/core';
import {DrinksService} from '../../../_services/drinks.service';

@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.css']
})
export class VideoComponent implements OnInit {
  embedUrl = '';
  currentDrink: any;
  saveButton = [true, 'Save'];
  description = '';
  showDescription = false;
  public max  = 5;
  public rate  = 3;
  public isReadonly = true;


  constructor(private drinksService: DrinksService) { }

  ngOnInit() {
    this.drinksService.drinkSelected
      .subscribe(
        (data: any) => {
          this.currentDrink = data;
          this.embedUrl = data.embed_url;
          this.rate = data.rating;
          this.description = data.webpage_url.description;
        }
      );

    this.drinksService.saveButton
      .subscribe(
        (data) => this.saveButton = data
      );
  }

  saveDrink() {
    console.log(this.currentDrink.url);
    if (this.saveButton[0]) {
      this.saveButton = [false, 'Remove'];
    } else {
      this.saveButton = [true, 'Save'];
    }

    this.drinksService.saveCurrentDrink(this.currentDrink.url)
      .subscribe(
        (data) => this.drinksService.drinkChanged.emit(true)
      );
  }

}
