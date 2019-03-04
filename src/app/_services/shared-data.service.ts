import {EventEmitter, Injectable, OnInit} from '@angular/core';
import { Headers } from '@angular/http'

@Injectable()
export class SharedDataService {
  headers = new Headers();
  ingredientOrDrinkChanged = new EventEmitter<any>();

  constructor() {
    this.updateData();
  }
  updateData() {
    const token = localStorage.getItem('id_token');
    if (token) {
      this.headers.set('Authorization', 'JWT ' + token);
    }
  }
}
