import {EventEmitter, Injectable} from '@angular/core';
import {Http, RequestOptions, URLSearchParams} from '@angular/http';
import {SharedDataService} from './shared-data.service';
import {Urls} from '../globals/urls'

@Injectable()
export class DrinksService {
  drinkSelected = new EventEmitter<any>();
  drinkChanged = new EventEmitter<any>();
  drinksToggle = new EventEmitter<any>();
  saveButton = new EventEmitter<any>();
  private query = '';

  constructor(private http: Http,
              private sharedData: SharedDataService) {}
  getDetailDrink(url: string) {
    return this.http.get(url, {headers: this.sharedData.headers})
      .map(res => res.json());
  }

  saveCurrentDrink(url: string) {
    const params: URLSearchParams = new URLSearchParams();
    params.set('changeUser', 'true');
    const options = new RequestOptions(
      {headers: this.sharedData.headers,
        search: params}
    );
    return this.http.get(url, options)
      .map(res => res.json());
  }
  setQuery(q: string) {
    this.query = q;
  }

  filterDrinks(filters: any[], ordering: string, user: string) {
    const params: URLSearchParams = new URLSearchParams();
    for (const filter of filters) {params.append('filter', filter);}
    if (ordering !== '') {params.append('ordering', ordering)};
    if (user !== '') {params.append('user', user)};
    params.set('q', this.query);
    const options = new RequestOptions(
      {headers: this.sharedData.headers,
        search: params}
    );
    return this.http.get(Urls.drinks, options)
      .map(res => res.json());
  }

  getNextPage(url: string) {
    return this.http.get(url, {headers: this.sharedData.headers})
      .map(res => res.json());
  }

  getPlaylists() {
    return this.http.get(Urls.playlists, {headers: this.sharedData.headers})
      .map(res => res.json());
  }
}
