import { NgModule } from '@angular/core';
import { RouterModule, Routes} from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { DrinksComponent } from './components/drinks/drinks.component';
import { AuthGuardService } from './_guards/auth-guard.service';
import { DetailComponent } from './components/detail/detail.component';
import { CallbackComponent } from './components/callback/callback.component';
import { AboutComponent } from './components/about/about.component';
import { ContactComponent } from './components/contact/contact.component';
import {PagenotfoundComponent} from './components/pagenotfound/pagenotfound.component';


const appRoutes: Routes = [
    {
        path: 'callback',
        component: CallbackComponent,
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

@NgModule({
    imports: [RouterModule.forRoot(appRoutes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}

