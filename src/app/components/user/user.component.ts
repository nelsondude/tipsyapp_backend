import { Component, OnInit } from '@angular/core';
import {SharedDataService} from '../../_services/shared-data.service';
import {AuthService} from '../../_services/auth.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  drinkActive = true;
  ingredientActive = false;

  constructor(private sharedData: SharedDataService,
              public auth: AuthService) { }

  ngOnInit() {
    this.sharedData.ingredientOrDrinkChanged.subscribe(
      (data: string) => {
        this.drinkActive = data === 'drink';
        this.ingredientActive = !this.drinkActive;
      }
    )
  }
}
