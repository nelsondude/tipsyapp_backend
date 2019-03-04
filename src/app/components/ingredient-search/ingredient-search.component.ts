import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {TypeaheadMatch} from 'ngx-bootstrap';
import {IngredientsService} from '../../_services/ingredients.service';
import {AuthService} from '../../_services/auth.service';

@Component({
  selector: 'app-ingredient-search',
  templateUrl: './ingredient-search.component.html',
  styleUrls: ['./ingredient-search.component.css']
})
export class IngredientSearchComponent implements OnInit {

  public asyncSelected: string;
  public typeaheadLoading: boolean;
  public typeaheadNoResults: boolean;
  public dataSource: Observable<any>;

  public ingredients: any[] = [];


  constructor(private ingredientsService: IngredientsService,
              public auth: AuthService) {
    this.dataSource = Observable
      .create((observer: any) => {
        observer.next(this.asyncSelected);
      })
      .flatMap((token: string) => this.getIngredientsAsObservable(token));
  }

  ngOnInit() {
  }

  public getIngredientsAsObservable(query: string): Observable<any> {
    return this.ingredientsService.getSearchIngredients(query);
  }

  public changeTypeaheadLoading(e: any): void {
    this.typeaheadLoading = e;
  }
  public changeTypeaheadNoResults(e: any): void {
    this.typeaheadNoResults = e;
  }
  public typeaheadOnSelect(e: TypeaheadMatch): void {
    const objUrl = e.item.url;
    this.addIngredient(objUrl);
  }

  addIngredient(objUrl: string) {
    this.ingredientsService.addSearchedIngredient(objUrl)
      .subscribe(
        () => this.ingredientsService.ingredientChanged.emit(true)
      );
  }
}
