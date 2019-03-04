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
var RecipeComponent = (function () {
    function RecipeComponent(drinksService) {
        this.drinksService = drinksService;
    }
    RecipeComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.drinksService.drinkSelected
            .subscribe(function (data) { return _this.drinkData = data; });
    };
    RecipeComponent = __decorate([
        Component({
            selector: 'app-recipe',
            templateUrl: './recipe.component.html',
            styleUrls: ['./recipe.component.css']
        }),
        __metadata("design:paramtypes", [DrinksService])
    ], RecipeComponent);
    return RecipeComponent;
}());
export { RecipeComponent };
//# sourceMappingURL=recipe.component.js.map