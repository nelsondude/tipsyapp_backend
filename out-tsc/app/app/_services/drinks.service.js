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
import { SharedDataService } from './shared-data.service';
import { Urls } from '../globals/urls';
var DrinksService = (function () {
    function DrinksService(http, sharedData) {
        this.http = http;
        this.sharedData = sharedData;
        this.drinkSelected = new EventEmitter();
        this.drinkChanged = new EventEmitter();
        this.drinksToggle = new EventEmitter();
        this.saveButton = new EventEmitter();
        this.query = '';
    }
    DrinksService.prototype.getDetailDrink = function (url) {
        return this.http.get(url, { headers: this.sharedData.headers })
            .map(function (res) { return res.json(); });
    };
    DrinksService.prototype.saveCurrentDrink = function (url) {
        var params = new URLSearchParams();
        params.set('changeUser', 'true');
        var options = new RequestOptions({ headers: this.sharedData.headers,
            search: params });
        return this.http.get(url, options)
            .map(function (res) { return res.json(); });
    };
    DrinksService.prototype.setQuery = function (q) {
        this.query = q;
    };
    DrinksService.prototype.filterDrinks = function (filters, ordering, user) {
        var params = new URLSearchParams();
        for (var _i = 0, filters_1 = filters; _i < filters_1.length; _i++) {
            var filter = filters_1[_i];
            params.append('filter', filter);
        }
        if (ordering !== '') {
            params.append('ordering', ordering);
        }
        ;
        if (user !== '') {
            params.append('user', user);
        }
        ;
        params.set('q', this.query);
        var options = new RequestOptions({ headers: this.sharedData.headers,
            search: params });
        return this.http.get(Urls.drinks, options)
            .map(function (res) { return res.json(); });
    };
    DrinksService.prototype.getNextPage = function (url) {
        return this.http.get(url, { headers: this.sharedData.headers })
            .map(function (res) { return res.json(); });
    };
    DrinksService.prototype.getPlaylists = function () {
        return this.http.get(Urls.playlists, { headers: this.sharedData.headers })
            .map(function (res) { return res.json(); });
    };
    DrinksService = __decorate([
        Injectable(),
        __metadata("design:paramtypes", [Http,
            SharedDataService])
    ], DrinksService);
    return DrinksService;
}());
export { DrinksService };
//# sourceMappingURL=drinks.service.js.map