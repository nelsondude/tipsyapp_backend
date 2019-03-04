import {EventEmitter, Injectable, OnInit} from '@angular/core';
import {Http, RequestOptions, URLSearchParams} from '@angular/http';
import 'rxjs/add/operator/map'
import {SharedDataService} from './shared-data.service';
import {Urls} from '../globals/urls'

@Injectable()
export class IngredientsService implements OnInit {
  ingredientChanged = new EventEmitter<any>();
  constructor(private http: Http,
              private sharedData: SharedDataService) {}

  ngOnInit() { }

  getSearchIngredients(query: string) {
    const params: URLSearchParams = new URLSearchParams();
    params.set('q', query);
    const options = new RequestOptions(
      {headers: this.sharedData.headers,
       search: params}
       );
    return this.http.get(Urls.ingredients, options)
      .map(res => res.json().results);
  }

  addSearchedIngredient(objUrl: string) {
    return this.http.get(objUrl, {headers: this.sharedData.headers})
      .map(res => res.json());
  }

  getMyIngredients() {
    return this.http.get(Urls.ingredients, {headers: this.sharedData.headers})
      .map(res => res.json())
  }

  getSuggestedIngredients() {
    const params: URLSearchParams = new URLSearchParams();
    params.set('suggested', 'true');
    const options = new RequestOptions(
      {headers: this.sharedData.headers,
        search: params}
    );
    return this.http.get(Urls.ingredients, options)
      .map(res => res.json());
  }
}
