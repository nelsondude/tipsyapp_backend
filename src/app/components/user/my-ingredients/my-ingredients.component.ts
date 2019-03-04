import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {IngredientsService} from '../../../_services/ingredients.service';
import {SharedDataService} from '../../../_services/shared-data.service';
import {
  trigger,
  state,
  style,
  transition,
  animate,
} from '@angular/animations';


@Component({
  selector: 'app-my-ingredients',
  templateUrl: './my-ingredients.component.html',
  styleUrls: ['./my-ingredients.component.css'],
  animations: []
})
export class MyIngredientsComponent implements OnInit {
  myIngredients = [];
  constructor(private ingredientsService: IngredientsService,
              private sharedData: SharedDataService) { }

  ngOnInit() {
    this.ingredientsService.ingredientChanged
      .subscribe(
        (value: boolean) => {
          if (value) {
            this.updateMyIngredients()
          }
        }
      );
    this.updateMyIngredients()
  }

  updateMyIngredients() {
    this.ingredientsService.getMyIngredients()
      .subscribe(
        data => {
          this.myIngredients = data.results;
          this.sharedData.ingredientOrDrinkChanged.emit('ingredient');
        }
      );
  }

  removeItem(index: string) {
    const item = this.myIngredients[index];
    this.myIngredients.splice(+index, 1)
    const objUrl = item.url;
    console.log(objUrl);
    this.ingredientsService.addSearchedIngredient(objUrl)
      .subscribe(
        () => {
          this.ingredientsService.ingredientChanged.emit(true);
          this.updateMyIngredients();
        }
      );
  }
}
