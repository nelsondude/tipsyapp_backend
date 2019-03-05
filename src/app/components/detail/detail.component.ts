import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import { DrinksService } from '../../_services/drinks.service';
import {Urls} from '../../globals/urls'
import {environment} from "../../../environments/environment";
import {IngredientsService} from "../../_services/ingredients.service";
import {SharedDataService} from "../../_services/shared-data.service";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class DetailComponent implements OnInit {
  prefix = '';
  slug = '';

  constructor(private route: ActivatedRoute,
              private router: Router,
              private drinksService: DrinksService,
              private ingredientsService: IngredientsService) { }

  ngOnInit() {
    this.route.params
      .subscribe(
        (params: Params) => {
          const slug = params['slug'];
          this.getDetailDrink(slug);
        }
      );
    this.ingredientsService.ingredientChanged
      .subscribe(
        () => {
          const slug = this.router.url.replace('/', '');
          this.getDetailDrink(slug);
        }
      )
  }

  getDetailDrink(slug: string) {
    const url = Urls.drinks + slug + '/';
    this.drinksService.getDetailDrink(url)
      .subscribe(
        (data) => {
          this.drinksService.drinkSelected.emit(data)
        }
      );
  }
}
