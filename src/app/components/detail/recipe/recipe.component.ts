import { Component, OnInit } from '@angular/core';
import {DrinksService} from '../../../_services/drinks.service';
import {IngredientsService} from "../../../_services/ingredients.service";

@Component({
  selector: 'app-recipe',
  templateUrl: './recipe.component.html',
  styleUrls: ['./recipe.component.css']
})
export class RecipeComponent implements OnInit {
  drinkData: any;

  constructor(private drinksService: DrinksService) { }

  ngOnInit() {
    this.drinksService.drinkSelected
      .subscribe(
        (data: any) => this.drinkData = data
      );
  }
}
