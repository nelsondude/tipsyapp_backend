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
import { IngredientsService } from '../../_services/ingredients.service';
import { AuthService } from '../../_services/auth.service';
var SuggestedComponent = (function () {
    function SuggestedComponent(ingredientsService, auth) {
        this.ingredientsService = ingredientsService;
        this.auth = auth;
        this.suggestedIngredients = [];
        this.loading = -1;
        this.checked = false;
        this.indeterminate = false;
        this.align = 'start';
    }
    SuggestedComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.addSuggestedIngredients();
        this.ingredientsService.ingredientChanged
            .subscribe(function (data) { return _this.addSuggestedIngredients(); });
    };
    SuggestedComponent.prototype.addSuggestedIngredients = function () {
        var _this = this;
        this.ingredientsService.getSuggestedIngredients()
            .subscribe(function (data) { return _this.suggestedIngredients = data.results; });
    };
    SuggestedComponent.prototype.addIngredient = function (index) {
        var _this = this;
        this.loading = index;
        var url = this.suggestedIngredients[index].url;
        this.ingredientsService.addSearchedIngredient(url)
            .subscribe(function () {
            _this.ingredientsService.ingredientChanged.emit(true);
            _this.loading = -1;
        });
    };
    SuggestedComponent = __decorate([
        Component({
            selector: 'app-suggested',
            templateUrl: './suggested.component.html',
            styleUrls: ['./suggested.component.css']
        }),
        __metadata("design:paramtypes", [IngredientsService,
            AuthService])
    ], SuggestedComponent);
    return SuggestedComponent;
}());
export { SuggestedComponent };
//# sourceMappingURL=suggested.component.js.map