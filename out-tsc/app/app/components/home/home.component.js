var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
import { Component, ViewChild, HostListener } from '@angular/core';
import 'rxjs/add/observable/of';
import { DrinksService } from '../../_services/drinks.service';
var HomeComponent = (function () {
    function HomeComponent(drinkService) {
        var _this = this;
        this.drinkService = drinkService;
        this.resizeTimeout = setTimeout((function () {
            _this.correctSidenav();
        }).bind(this), 100);
    }
    HomeComponent.prototype.onWindowResize = function () {
        var _this = this;
        if (this.resizeTimeout) {
            clearTimeout(this.resizeTimeout);
        }
        this.resizeTimeout = setTimeout((function () {
            _this.correctSidenav();
        }).bind(this), 200);
    };
    HomeComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.drinkService.drinksToggle
            .subscribe(function (data) {
            if (_this.sidenav) {
                _this.sidenav.toggle();
            }
        });
    };
    HomeComponent.prototype.correctSidenav = function () {
        if (this.sidenav) {
            if (window.innerWidth < 580) {
                this.sidenav.close();
                this.sidenav.mode = 'push';
            }
            else {
                this.sidenav.open();
                this.sidenav.mode = 'side';
            }
        }
    };
    HomeComponent.prototype.onScroll = function () {
        console.log('Scrolling');
    };
    __decorate([
        ViewChild('mynav'),
        __metadata("design:type", Object)
    ], HomeComponent.prototype, "sidenav", void 0);
    __decorate([
        HostListener('window:resize'),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", []),
        __metadata("design:returntype", void 0)
    ], HomeComponent.prototype, "onWindowResize", null);
    HomeComponent = __decorate([
        Component({
            selector: 'app-home',
            templateUrl: './home.component.html',
            styleUrls: ['./home.component.css'],
        }),
        __metadata("design:paramtypes", [DrinksService])
    ], HomeComponent);
    return HomeComponent;
}());
export { HomeComponent };
//# sourceMappingURL=home.component.js.map