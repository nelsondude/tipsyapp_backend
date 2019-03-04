import {Injectable} from '@angular/core';
import { Router } from '@angular/router';
import 'rxjs/add/operator/filter';
import * as auth0 from 'auth0-js';
import {SharedDataService} from './shared-data.service';
import {CALLBACK, AUDIENCE, DOMAIN, CLIENT_ID, HOST} from '../globals/auth';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/observable/timer';


@Injectable()
export class AuthService {

  userProfile: any;
  refreshSubscription: any;


  auth0 = new auth0.WebAuth({
    clientID: CLIENT_ID,
    domain: DOMAIN,
    responseType: 'token id_token',
    audience: AUDIENCE,
    redirectUri: CALLBACK,
    scope: 'openid'
  });

  constructor(public router: Router,
              public sharedData: SharedDataService) {
    // setInterval(() => {
    //   console.log(this.expiresAt - Date.now());
    // }, 1000)
  }

  public login(): void {
    this.auth0.authorize();
  }

  public handleAuthentication(): void {
    this.auth0.parseHash((err, authResult) => {
      if (authResult && authResult.accessToken && authResult.idToken) {
        window.location.hash = '';
        this.setSession(authResult);
        this.router.navigate(['/']);
      } else if (err) {
        this.router.navigate(['/']);
        console.log(err);
      }
    });
  }

  public logout(): void {
    // Remove tokens and expiry time from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('id_token');
    localStorage.removeItem('expires_at');
    this.sharedData.updateData();
    // Go back to the home route
    this.router.navigate(['/']);
  }

  public isAuthenticated(): boolean {
    // Check whether the current time is past the
    // access token's expiry time
    const expiresAt = JSON.parse(localStorage.getItem('expires_at'));
    return new Date().getTime() < expiresAt;
  }

  public renewToken() {
    this.auth0.renewAuth({
      audience: AUDIENCE,
      redirectUri: CALLBACK,
      usePostMessage: true,
      postMessageOrigin: HOST
    }, (err, result) => {
      if (err) {
        console.log(err);
      } else {
        this.setSession(result);
      }
    });
  }

  public scheduleRenewal() {
    console.log('Scheduling renewal ...')
    if(!this.isAuthenticated()) return;
    this.unscheduleRenewal();

    const expiresAt = JSON.parse(window.localStorage.getItem('expires_at'));

    console.log('expires at', expiresAt);
    console.log('date Now', Date.now())
    const source = Observable.of(expiresAt).flatMap(
      expiresAtTime => {
        return Observable.timer(Math.max(1000, expiresAtTime - Date.now()));
      });

    // Once the delay time from above is
    // reached, get a new JWT and schedule
    // additional refreshes
    console.log('subscriing to refresher');
    this.refreshSubscription = source.subscribe(() => {
      console.log('Supposed to Renew');
      this.renewToken();
      this.scheduleRenewal();
    });
  }

  public unscheduleRenewal() {
    if(!this.refreshSubscription) return;
    this.refreshSubscription.unsubscribe();
  }

  private setSession(authResult): void {
    // Set the time that the access token will expire at
    const expiresAt = JSON.stringify((authResult.expiresIn * 1000) + Date.now());

    console.log(authResult);

    localStorage.setItem('access_token', authResult.accessToken);
    localStorage.setItem('id_token', authResult.idToken);
    localStorage.setItem('expires_at', expiresAt);
    this.scheduleRenewal();
    this.sharedData.updateData();
  }

}
