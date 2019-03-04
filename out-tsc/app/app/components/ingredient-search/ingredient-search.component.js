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
import { Observable } from 'rxjs/Observable';
import { IngredientsService } from '../../_services/ingredients.service';
import { AuthService } from '../../_services/auth.service';
var IngredientSearchComponent = (function () {
    function IngredientSearchComponent(ingredientsService, auth) {
        var _this = this;
        this.ingredientsService = ingredientsService;
        this.auth = auth;
        this.ingredients = [];
        this.dataSource = Observable
            .create(function (observer) {
            observer.next(_this.asyncSelected);
        })
            .flatMap(function (token) { return _this.getIngredientsAsObservable(token); });
    }
    IngredientSearchComponent.prototype.ngOnInit = function () {
    };
    IngredientSearchComponent.prototype.getIngredientsAsObservable = function (query) {
        return this.ingredientsService.getSearchIngredients(query);
    };
    IngredientSearchComponent.prototype.changeTypeaheadLoading = function (e) {
        this.typeaheadLoading = e;
    };
    IngredientSearchComponent.prototype.changeTypeaheadNoResults = function (e) {
        this.typeaheadNoResults = e;
    };
    IngredientSearchComponent.prototype.typeaheadOnSelect = function (e) {
        var objUrl = e.item.url;
        this.addIngredient(objUrl);
    };
    IngredientSearchComponent.prototype.addIngredient = function (objUrl) {
        var _this = this;
        this.ingredientsService.addSearchedIngredient(objUrl)
            .subscribe(function () { return _this.ingredientsService.ingredientChanged.emit(true); });
    };
    IngredientSearchComponent = __decorate([
        Component({
            selector: 'app-ingredient-search',
            templateUrl: './ingredient-search.component.html',
            styleUrls: ['./ingredient-search.component.css']
        }),
        __metadata("design:paramtypes", [IngredientsService,
            AuthService])
    ], IngredientSearchComponent);
    return IngredientSearchComponent;
}());
export { IngredientSearchComponent };
//# sourceMappingURL=ingredient-search.component.js.map