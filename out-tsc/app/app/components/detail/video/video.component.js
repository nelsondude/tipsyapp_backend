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
var VideoComponent = (function () {
    function VideoComponent(drinksService) {
        this.drinksService = drinksService;
        this.embedUrl = '';
        this.saveButton = [true, 'Save'];
        this.description = '';
        this.showDescription = false;
        this.max = 5;
        this.rate = 3;
        this.isReadonly = true;
    }
    VideoComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.drinksService.drinkSelected
            .subscribe(function (data) {
            _this.currentDrink = data;
            _this.embedUrl = data.embed_url;
            _this.rate = data.rating;
            _this.description = data.webpage_url.description;
        });
        this.drinksService.saveButton
            .subscribe(function (data) { return _this.saveButton = data; });
    };
    VideoComponent.prototype.saveDrink = function () {
        var _this = this;
        console.log(this.currentDrink.url);
        if (this.saveButton[0]) {
            this.saveButton = [false, 'Remove'];
        }
        else {
            this.saveButton = [true, 'Save'];
        }
        this.drinksService.saveCurrentDrink(this.currentDrink.url)
            .subscribe(function (data) { return _this.drinksService.drinkChanged.emit(true); });
    };
    VideoComponent = __decorate([
        Component({
            selector: 'app-video',
            templateUrl: './video.component.html',
            styleUrls: ['./video.component.css']
        }),
        __metadata("design:paramtypes", [DrinksService])
    ], VideoComponent);
    return VideoComponent;
}());
export { VideoComponent };
//# sourceMappingURL=video.component.js.map