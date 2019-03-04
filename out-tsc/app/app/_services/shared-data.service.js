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
import { Headers } from '@angular/http';
var SharedDataService = (function () {
    function SharedDataService() {
        this.headers = new Headers();
        this.ingredientOrDrinkChanged = new EventEmitter();
        this.updateData();
    }
    SharedDataService.prototype.updateData = function () {
        var token = localStorage.getItem('id_token');
        if (token) {
            this.headers.set('Authorization', 'JWT ' + token);
        }
    };
    SharedDataService = __decorate([
        Injectable(),
        __metadata("design:paramtypes", [])
    ], SharedDataService);
    return SharedDataService;
}());
export { SharedDataService };
//# sourceMappingURL=shared-data.service.js.map