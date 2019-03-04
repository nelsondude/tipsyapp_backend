var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
import { Component } from '@angular/core';
import { AuthService } from './_services/auth.service';
import { DrinksService } from './_services/drinks.service';
import { IngredientsService } from './_services/ingredients.service';
import { SharedDataService } from './_services/shared-data.service';
var AppComponent = (function () {
    function AppComponent(auth, drinksService, ingredientsService, shareDataService) {
        this.auth = auth;
        this.drinksService = drinksService;
        this.ingredientsService = ingredientsService;
        this.shareDataService = shareDataService;
        this.isIn = false; // store state
        auth.handleAuthentication();
        auth.scheduleRenewal();
        this.shareDataService.updateData();
    }
    AppComponent.prototype.ngOnInit = function () {
    };
    AppComponent.prototype.toggleDrinks = function () {
        this.drinksService.drinksToggle.emit(true);
    };
    AppComponent.prototype.toggleState = function () {
        var bool = this.isIn;
        this.isIn = bool === false;
    };
    AppComponent.prototype.onSubmit = function (form) {
        this.drinksService.setQuery(form.value.search);
        this.ingredientsService.ingredientChanged.emit(true);
        console.log(form.value.search);
    };
    AppComponent = __decorate([
        Component({
            selector: 'app-root',
            templateUrl: './app.component.html',
            styleUrls: ['./app.component.css'],
        }),
        __metadata("design:paramtypes", [AuthService,
            DrinksService,
            IngredientsService,
            SharedDataService])
    ], AppComponent);
    return AppComponent;
}());
export { AppComponent };
//# sourceMappingURL=app.component.js.map