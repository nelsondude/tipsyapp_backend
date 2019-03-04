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
import { DrinksService } from '../../../_services/drinks.service';
import { SharedDataService } from '../../../_services/shared-data.service';
import { Router } from '@angular/router';
var MyDrinksComponent = (function () {
    function MyDrinksComponent(drinksService, sharedData, router) {
        this.drinksService = drinksService;
        this.sharedData = sharedData;
        this.router = router;
        this.myDrinks = [];
    }
    MyDrinksComponent.prototype.contains = function (drink) {
        for (var _i = 0, _a = this.myDrinks; _i < _a.length; _i++) {
            var myDrink = _a[_i];
            if (myDrink.name === drink.name) {
                return true;
            }
        }
        return false;
    };
    MyDrinksComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.addMyDrinks();
        this.drinksService.drinkSelected
            .subscribe(function (drink) {
            var bool = _this.contains(drink);
            var result = [true, 'Save'];
            if (bool) {
                result = [false, 'Remove'];
            }
            _this.drinksService.saveButton.emit(result);
        });
        this.drinksService.drinkChanged
            .subscribe(function (data) { return _this.addMyDrinks(); });
    };
    MyDrinksComponent.prototype.loadDrink = function (i) {
        var slug = this.myDrinks[i].slug;
        this.router.navigate([slug]);
    };
    MyDrinksComponent.prototype.addMyDrinks = function () {
        var _this = this;
        this.drinksService.filterDrinks([], '', 'true')
            .subscribe(function (data) {
            _this.myDrinks = data.results.slice();
            _this.sharedData.ingredientOrDrinkChanged.emit('drink');
        });
    };
    MyDrinksComponent.prototype.removeItem = function (index) {
        var _this = this;
        var drink = this.myDrinks[index];
        this.drinksService.saveButton.emit([true, 'Save']);
        this.drinksService.saveCurrentDrink(drink.url)
            .subscribe(function (data) { return _this.drinksService.drinkChanged.emit(true); });
    };
    MyDrinksComponent = __decorate([
        Component({
            selector: 'app-my-drinks',
            templateUrl: './my-drinks.component.html',
            styleUrls: ['./my-drinks.component.css']
        }),
        __metadata("design:paramtypes", [DrinksService,
            SharedDataService,
            Router])
    ], MyDrinksComponent);
    return MyDrinksComponent;
}());
export { MyDrinksComponent };
//# sourceMappingURL=my-drinks.component.js.map