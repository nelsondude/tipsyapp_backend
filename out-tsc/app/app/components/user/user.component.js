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
import { SharedDataService } from '../../_services/shared-data.service';
import { AuthService } from '../../_services/auth.service';
var UserComponent = (function () {
    function UserComponent(sharedData, auth) {
        this.sharedData = sharedData;
        this.auth = auth;
        this.drinkActive = true;
        this.ingredientActive = false;
    }
    UserComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.sharedData.ingredientOrDrinkChanged.subscribe(function (data) {
            _this.drinkActive = data === 'drink';
            _this.ingredientActive = !_this.drinkActive;
        });
    };
    UserComponent = __decorate([
        Component({
            selector: 'app-user',
            templateUrl: './user.component.html',
            styleUrls: ['./user.component.css']
        }),
        __metadata("design:paramtypes", [SharedDataService,
            AuthService])
    ], UserComponent);
    return UserComponent;
}());
export { UserComponent };
//# sourceMappingURL=user.component.js.map