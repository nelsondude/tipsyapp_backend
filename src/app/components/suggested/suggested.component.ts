import {Component, Injectable, OnInit} from '@angular/core';
import {IngredientsService} from '../../_services/ingredients.service';
import {AuthService} from '../../_services/auth.service';

@Component({
  selector: 'app-suggested',
  templateUrl: './suggested.component.html',
  styleUrls: ['./suggested.component.css']
})

export class SuggestedComponent implements OnInit {
  suggestedIngredients = [];
  loading = -1;

  checked = false;
  indeterminate = false;
  align = 'start';

  constructor(private ingredientsService: IngredientsService,
              public auth: AuthService) { }

  ngOnInit() {
    this.addSuggestedIngredients();
    this.ingredientsService.ingredientChanged
      .subscribe(
        (data: any) => this.addSuggestedIngredients()
      );
  }

  addSuggestedIngredients() {
    this.ingredientsService.getSuggestedIngredients()
      .subscribe(
        (data: any) => this.suggestedIngredients = data.results
      );
  }
  addIngredient(index: number) {
    this.loading = index;
    const url = this.suggestedIngredients[index].url;
    this.ingredientsService.addSearchedIngredient(url)
      .subscribe(
        () => {
          this.ingredientsService.ingredientChanged.emit(true);
          this.loading = -1;
        }
      );
  }
}
