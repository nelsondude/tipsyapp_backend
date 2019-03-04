var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
import { EventEmitter, Injectable } from '@angular/core';
import { Http, RequestOptions, URLSearchParams } from '@angular/http';
import 'rxjs/add/operator/map';
import { SharedDataService } from './shared-data.service';
import { Urls } from '../globals/urls';
var IngredientsService = (function () {
    function IngredientsService(http, sharedData) {
        this.http = http;
        this.sharedData = sharedData;
        this.ingredientChanged = new EventEmitter();
    }
    IngredientsService.prototype.ngOnInit = function () { };
    IngredientsService.prototype.getSearchIngredients = function (query) {
        var params = new URLSearchParams();
        params.set('q', query);
        var options = new RequestOptions({ headers: this.sharedData.headers,
            search: params });
        return this.http.get(Urls.ingredients, options)
            .map(function (res) { return res.json().results; });
    };
    IngredientsService.prototype.addSearchedIngredient = function (objUrl) {
        return this.http.get(objUrl, { headers: this.sharedData.headers })
            .map(function (res) { return res.json(); });
    };
    IngredientsService.prototype.getMyIngredients = function () {
        return this.http.get(Urls.ingredients, { headers: this.sharedData.headers })
            .map(function (res) { return res.json(); });
    };
    IngredientsService.prototype.getSuggestedIngredients = function () {
        var params = new URLSearchParams();
        params.set('suggested', 'true');
        var options = new RequestOptions({ headers: this.sharedData.headers,
            search: params });
        return this.http.get(Urls.ingredients, options)
            .map(function (res) { return res.json(); });
    };
    IngredientsService = __decorate([
        Injectable(),
        __metadata("design:paramtypes", [Http,
            SharedDataService])
    ], IngredientsService);
    return IngredientsService;
}());
export { IngredientsService };
//# sourceMappingURL=ingredients.service.js.map