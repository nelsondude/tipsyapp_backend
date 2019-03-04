var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import 'rxjs/add/operator/filter';
import * as auth0 from 'auth0-js';
import { SharedDataService } from './shared-data.service';
import { CALLBACK, AUDIENCE, DOMAIN, CLIENT_ID, HOST } from '../globals/auth';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/timer';
var AuthService = (function () {
    function AuthService(router, sharedData) {
        this.router = router;
        this.sharedData = sharedData;
        this.auth0 = new auth0.WebAuth({
            clientID: CLIENT_ID,
            domain: DOMAIN,
            responseType: 'token id_token',
            audience: AUDIENCE,
            redirectUri: CALLBACK,
            scope: 'openid'
        });
        // setInterval(() => {
        //   console.log(this.expiresAt - Date.now());
        // }, 1000)
    }
    AuthService.prototype.login = function () {
        this.auth0.authorize();
    };
    AuthService.prototype.handleAuthentication = function () {
        var _this = this;
        this.auth0.parseHash(function (err, authResult) {
            if (authResult && authResult.accessToken && authResult.idToken) {
                window.location.hash = '';
                _this.setSession(authResult);
                _this.router.navigate(['/']);
            }
            else if (err) {
                _this.router.navigate(['/']);
                console.log(err);
            }
        });
    };
    AuthService.prototype.logout = function () {
        // Remove tokens and expiry time from localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('id_token');
        localStorage.removeItem('expires_at');
        this.sharedData.updateData();
        // Go back to the home route
        this.router.navigate(['/']);
    };
    AuthService.prototype.isAuthenticated = function () {
        // Check whether the current time is past the
        // access token's expiry time
        var expiresAt = JSON.parse(localStorage.getItem('expires_at'));
        return new Date().getTime() < expiresAt;
    };
    AuthService.prototype.renewToken = function () {
        var _this = this;
        this.auth0.renewAuth({
            audience: AUDIENCE,
            redirectUri: CALLBACK,
            usePostMessage: true,
            postMessageOrigin: HOST
        }, function (err, result) {
            if (err) {
                console.log(err);
            }
            else {
                _this.setSession(result);
            }
        });
    };
    AuthService.prototype.scheduleRenewal = function () {
        var _this = this;
        console.log('Scheduling renewal ...');
        if (!this.isAuthenticated())
            return;
        this.unscheduleRenewal();
        var expiresAt = JSON.parse(window.localStorage.getItem('expires_at'));
        console.log('expires at', expiresAt);
        console.log('date Now', Date.now());
        var source = Observable.of(expiresAt).flatMap(function (expiresAtTime) {
            return Observable.timer(Math.max(1000, expiresAtTime - Date.now()));
        });
        // Once the delay time from above is
        // reached, get a new JWT and schedule
        // additional refreshes
        console.log('subscriing to refresher');
        this.refreshSubscription = source.subscribe(function () {
            console.log('Supposed to Renew');
            _this.renewToken();
            _this.scheduleRenewal();
        });
    };
    AuthService.prototype.unscheduleRenewal = function () {
        if (!this.refreshSubscription)
            return;
        this.refreshSubscription.unsubscribe();
    };
    AuthService.prototype.setSession = function (authResult) {
        // Set the time that the access token will expire at
        var expiresAt = JSON.stringify((authResult.expiresIn * 1000) + Date.now());
        console.log(authResult);
        localStorage.setItem('access_token', authResult.accessToken);
        localStorage.setItem('id_token', authResult.idToken);
        localStorage.setItem('expires_at', expiresAt);
        this.scheduleRenewal();
        this.sharedData.updateData();
    };
    AuthService = __decorate([
        Injectable(),
        __metadata("design:paramtypes", [Router,
            SharedDataService])
    ], AuthService);
    return AuthService;
}());
export { AuthService };
//# sourceMappingURL=auth.service.js.map