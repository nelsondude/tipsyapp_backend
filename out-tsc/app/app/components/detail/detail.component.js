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
import { ActivatedRoute } from '@angular/router';
import { DrinksService } from '../../_services/drinks.service';
import { Urls } from '../../globals/urls';
var DetailComponent = (function () {
    function DetailComponent(route, drinksService) {
        this.route = route;
        this.drinksService = drinksService;
        this.prefix = '';
    }
    DetailComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.route.params
            .subscribe(function (params) {
            var slug = params['slug'];
            _this.getDetailDrink(slug);
        });
    };
    DetailComponent.prototype.getDetailDrink = function (slug) {
        var _this = this;
        var url = Urls.drinks + slug + '/';
        console.log(url);
        this.drinksService.getDetailDrink(url)
            .subscribe(function (data) {
            _this.drinksService.drinkSelected.emit(data);
        });
    };
    DetailComponent = __decorate([
        Component({
            selector: 'app-detail',
            templateUrl: './detail.component.html',
            styleUrls: ['./detail.component.css']
        }),
        __metadata("design:paramtypes", [ActivatedRoute,
            DrinksService])
    ], DetailComponent);
    return DetailComponent;
}());
export { DetailComponent };
//# sourceMappingURL=detail.component.js.map