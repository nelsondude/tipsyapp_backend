import { Component, OnInit } from '@angular/core';
import {DrinksService} from '../../../_services/drinks.service';
import {SharedDataService} from '../../../_services/shared-data.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-my-drinks',
  templateUrl: './my-drinks.component.html',
  styleUrls: ['./my-drinks.component.css']
})
export class MyDrinksComponent implements OnInit {
  myDrinks = [];

  constructor(private drinksService: DrinksService,
              private sharedData: SharedDataService,
              private router: Router) { }

  contains(drink) {
    for (const myDrink of this.myDrinks) {
      if (myDrink.name === drink.name) {
        return true;
      }
    }
    return false;
  }
  ngOnInit() {
    this.addMyDrinks();
    this.drinksService.drinkSelected
      .subscribe(
        (drink) => {
          const bool = this.contains(drink);
          let result = [true, 'Save'];
          if (bool) {
            result = [false, 'Remove'];
          }
          this.drinksService.saveButton.emit(result);
        }
      );
    this.drinksService.drinkChanged
      .subscribe(
        (data) => this.addMyDrinks()
      );
  }
  loadDrink(i: number) {
    const slug = this.myDrinks[i].slug;
    this.router.navigate([slug])
  }
  addMyDrinks() {
    this.drinksService.filterDrinks([], '', 'true')
      .subscribe(
        (data) => {
          this.myDrinks = data.results.slice();
          this.sharedData.ingredientOrDrinkChanged.emit('drink');
        }
      );
  }
  removeItem(index: number) {
    const drink = this.myDrinks[index];
    this.drinksService.saveButton.emit([true, 'Save']);
    this.drinksService.saveCurrentDrink(drink.url)
      .subscribe(
        (data) => this.drinksService.drinkChanged.emit(true)
      );
  }
}
