import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { DrinksService } from '../../_services/drinks.service';
import {Urls} from '../../globals/urls'
import {environment} from "../../../environments/environment";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class DetailComponent implements OnInit {
  prefix = '';
  constructor(private route: ActivatedRoute,
              private drinksService: DrinksService) { }

  ngOnInit() {
    this.route.params
      .subscribe(
        (params: Params) => {
          const slug = params['slug'];
          this.getDetailDrink(slug);
        }
      )
  }

  getDetailDrink(slug: string) {
    const url = Urls.drinks + slug + '/';
    console.log(url);
    this.drinksService.getDetailDrink(url)
      .subscribe(
        (data) => {
          this.drinksService.drinkSelected.emit(data)
        }
      );
  }
}
