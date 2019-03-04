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
import { IngredientsService } from '../../../_services/ingredients.service';
import { SharedDataService } from '../../../_services/shared-data.service';
var MyIngredientsComponent = (function () {
    function MyIngredientsComponent(ingredientsService, sharedData) {
        this.ingredientsService = ingredientsService;
        this.sharedData = sharedData;
        this.myIngredients = [];
    }
    MyIngredientsComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.ingredientsService.ingredientChanged
            .subscribe(function (value) {
            if (value) {
                _this.updateMyIngredients();
            }
        });
        this.updateMyIngredients();
    };
    MyIngredientsComponent.prototype.updateMyIngredients = function () {
        var _this = this;
        this.ingredientsService.getMyIngredients()
            .subscribe(function (data) {
            _this.myIngredients = data.results;
            _this.sharedData.ingredientOrDrinkChanged.emit('ingredient');
        });
    };
    MyIngredientsComponent.prototype.removeItem = function (index) {
        var _this = this;
        var item = this.myIngredients[index];
        this.myIngredients.splice(+index, 1);
        var objUrl = item.url;
        console.log(objUrl);
        this.ingredientsService.addSearchedIngredient(objUrl)
            .subscribe(function () {
            _this.ingredientsService.ingredientChanged.emit(true);
            _this.updateMyIngredients();
        });
    };
    MyIngredientsComponent = __decorate([
        Component({
            selector: 'app-my-ingredients',
            templateUrl: './my-ingredients.component.html',
            styleUrls: ['./my-ingredients.component.css'],
            animations: []
        }),
        __metadata("design:paramtypes", [IngredientsService,
            SharedDataService])
    ], MyIngredientsComponent);
    return MyIngredientsComponent;
}());
export { MyIngredientsComponent };
//# sourceMappingURL=my-ingredients.component.js.map