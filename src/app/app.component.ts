import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {AuthService} from './_services/auth.service';
import {DrinksService} from './_services/drinks.service';
import {NgForm} from '@angular/forms';
import {IngredientsService} from './_services/ingredients.service';
import {SharedDataService} from './_services/shared-data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  isIn = false;   // store state

  constructor(public auth: AuthService,
              private drinksService: DrinksService,
              private ingredientsService: IngredientsService,
              private shareDataService: SharedDataService) {
    auth.handleAuthentication();
    auth.scheduleRenewal();
    this.shareDataService.updateData();
  }

  ngOnInit() {
  }

  toggleDrinks() {
    this.drinksService.drinksToggle.emit(true);
  }
  toggleState() { // click handler
    const bool = this.isIn;
    this.isIn = bool === false;
  }
  onSubmit(form: NgForm) {
    this.drinksService.setQuery(form.value.search);
    this.ingredientsService.ingredientChanged.emit(true);
    console.log(form.value.search);
  }

}
