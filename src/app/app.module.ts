import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { TypeaheadModule } from 'ngx-bootstrap/typeahead';
import { TabsModule } from 'ngx-bootstrap/tabs';
import { RatingModule } from 'ngx-bootstrap/rating';

import { SidebarModule } from 'ng-sidebar';
import { MnFullpageModule } from 'ngx-fullpage';


import { RouteReuseStrategy } from '@angular/router';
import { CustomReuseStrategy } from './reuse-strategy';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { AppRoutingModule } from './app.routing';
import { DrinksComponent } from './components/drinks/drinks.component';
import { IngredientSearchComponent } from './components/ingredient-search/ingredient-search.component';
import { MyIngredientsComponent } from './components/user/my-ingredients/my-ingredients.component';
import { MyDrinksComponent } from './components/user/my-drinks/my-drinks.component';
import { VideoComponent } from './components/detail/video/video.component';
import { SuggestedComponent } from './components/suggested/suggested.component';
import { RecipeComponent } from './components/detail/recipe/recipe.component';
import { UserComponent } from './components/user/user.component';
import { DetailComponent } from './components/detail/detail.component';
import { ContactComponent } from './components/contact/contact.component';
import { AboutComponent } from './components/about/about.component';
import { PagenotfoundComponent } from './components/pagenotfound/pagenotfound.component';

import { AuthGuardService } from './_guards/auth-guard.service';
import { SharedDataService } from './_services/shared-data.service';
import { DrinksService } from './_services/drinks.service';
import { IngredientsService } from './_services/ingredients.service';
import { AuthService } from './_services/auth.service'

import { SafePipe } from './_pipes/safe.pipe';
import { TruncateModule } from 'ng2-truncate';
import { CallbackComponent } from './components/callback/callback.component';

// Material
import 'hammerjs';
import {
  MatAutocompleteModule,
  MatButtonModule,
  MatButtonToggleModule,
  MatCardModule,
  MatCheckboxModule,
  MatChipsModule,
  MatDatepickerModule,
  MatDialogModule,
  MatExpansionModule,
  MatGridListModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatMenuModule,
  MatNativeDateModule,
  MatPaginatorModule,
  MatProgressBarModule,
  MatProgressSpinnerModule,
  MatRadioModule,
  MatRippleModule,
  MatSelectModule,
  MatSidenavModule,
  MatSliderModule,
  MatSlideToggleModule,
  MatSnackBarModule,
  MatSortModule,
  MatTableModule,
  MatTabsModule,
  MatToolbarModule,
  MatTooltipModule,
} from '@angular/material';


@NgModule({
  exports: [
    MatAutocompleteModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatDatepickerModule,
    MatDialogModule,
    MatExpansionModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatMenuModule,
    MatNativeDateModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatRippleModule,
    MatSelectModule,
    MatSidenavModule,
    MatSliderModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatSortModule,
    MatTableModule,
    MatTabsModule,
    MatToolbarModule,
    MatTooltipModule,
  ]
})
export class GoogleMaterialModule {}

import {AdsenseModule} from 'ng2-adsense';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    DrinksComponent,
    IngredientSearchComponent,
    MyIngredientsComponent,
    MyDrinksComponent,
    VideoComponent,
    SuggestedComponent,
    RecipeComponent,
    SafePipe,
    UserComponent,
    DetailComponent,
    CallbackComponent,
    ContactComponent,
    AboutComponent,
    PagenotfoundComponent,
  ],
  imports: [
    // Material Modules
    GoogleMaterialModule,
    // Covalent Modules Core
    // CovalentLayoutModule,
    // CovalentStepsModule,
    // CovalentChipsModule,
    // CovalentNotificationsModule,
    // CovalentSearchModule,
    // Angular Modules
    ReactiveFormsModule,
    BrowserModule,
    AppRoutingModule,
    HttpModule,
    FormsModule,
    BrowserAnimationsModule,
    TruncateModule,
    // Full page Modules
    MnFullpageModule.forRoot(),
    // ng-sidebar Modules
    SidebarModule.forRoot(),
    // ngx-bootstrap Modules
    BsDropdownModule.forRoot(),
    TypeaheadModule.forRoot(),
    TabsModule.forRoot(),
    RatingModule.forRoot(),
    // Infinite Scroll
    AdsenseModule.forRoot({
      adClient: 'ca-pub-9206680173374432',
      adSlot: 7259870550,
    }),
  ],
  providers: [
    AuthGuardService,
    AuthService,
    IngredientsService,
    SharedDataService,
    DrinksService,
    {provide: RouteReuseStrategy, useClass: CustomReuseStrategy},
    ],
  bootstrap: [AppComponent],
  schemas: [ CUSTOM_ELEMENTS_SCHEMA ],
})
export class AppModule { }
