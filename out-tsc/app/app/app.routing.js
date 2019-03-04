var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { DrinksComponent } from './components/drinks/drinks.component';
import { DetailComponent } from './components/detail/detail.component';
import { CallbackComponent } from './components/callback/callback.component';
import { AboutComponent } from './components/about/about.component';
import { ContactComponent } from './components/contact/contact.component';
var appRoutes = [
    {
        path: 'callback',
        component: CallbackComponent,
        canActivate: [],
    },
    {
        path: 'contact',
        component: ContactComponent,
        canActivate: [],
    },
    {
        path: 'about',
        component: AboutComponent,
        canActivate: [],
    },
    {
        path: '',
        component: HomeComponent,
        canActivate: [],
        children: [
            {
                path: '',
                component: DrinksComponent,
                canActivate: [],
            },
            {
                path: ':slug',
                component: DetailComponent,
                canActivate: [],
            },
        ]
    },
];
var AppRoutingModule = (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule = __decorate([
        NgModule({
            imports: [RouterModule.forRoot(appRoutes)],
            exports: [RouterModule]
        })
    ], AppRoutingModule);
    return AppRoutingModule;
}());
export { AppRoutingModule };
//# sourceMappingURL=app.routing.js.map