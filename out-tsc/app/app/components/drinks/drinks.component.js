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
import { DrinksService } from '../../_services/drinks.service';
import { IngredientsService } from '../../_services/ingredients.service';
import { Router } from '@angular/router';
import { AuthService } from '../../_services/auth.service';
var DrinksComponent = (function () {
    function DrinksComponent(router, drinksService, ingredientsService, auth) {
        this.router = router;
        this.drinksService = drinksService;
        this.ingredientsService = ingredientsService;
        this.auth = auth;
        this.drinksData = [];
        this.drinksDataGroups = [];
        this.playlistData = [];
        this.applied = true;
        this.isOpen = false;
        this.options = [
            { name: 'Most Recent', query: 'timestamp' },
            { name: 'Percent You Have', query: 'percent' },
            { name: 'Items Missing', query: 'count_need' },
            { name: 'Items You Have', query: 'count_have' }
        ];
        this.index = 0;
        this.extraLoading = false;
        this.lastResult = false;
        this.noResults = false;
        this.color = 'primary';
        this.mode = 'determinate';
        this.value = 0;
        this.bufferValue = 75;
    }
    DrinksComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.filterPossibleDrinks();
        this.addPlaylists();
        this.ingredientsService.ingredientChanged
            .subscribe(function () { return _this.filterPossibleDrinks(); });
    };
    DrinksComponent.prototype.loadVideo = function (drink) {
        this.router.navigate(['/', drink.slug]);
    };
    DrinksComponent.prototype.groupDrinks = function (data) {
        var groups = [];
        for (var i = 0; i < data.length; i = i + 4) {
            var group = data.slice(i, i + 4);
            groups.push(group);
        }
        return groups;
    };
    DrinksComponent.prototype.filterPossibleDrinks = function () {
        var _this = this;
        this.mode = 'indeterminate';
        var result = [];
        if (this.applied) {
            for (var i = 0; i < this.playlistData.length; i++) {
                if (this.playlistData[i].checkbox) {
                    result.push(this.playlistData[i].name);
                }
            }
        }
        this.drinksService.filterDrinks(result, this.options[this.index].query, '')
            .subscribe(function (data) {
            _this.drinksData = [data];
            _this.noResults = data.count === 0;
            _this.drinksDataGroups = _this.groupDrinks(data.results);
            _this.mode = 'determinate';
        }, function (err) {
            _this.mode = 'determinate';
        });
    };
    DrinksComponent.prototype.onClickApply = function () {
        this.isOpen = false;
        this.filterPossibleDrinks();
    };
    DrinksComponent.prototype.onClickCheckbox = function (event, i) {
        this.playlistData[i].checkbox = event.srcElement.checked;
        if (this.applied) {
            this.filterPossibleDrinks();
        }
    };
    DrinksComponent.prototype.menuOptionClicked = function (index) {
        if (index !== this.index) {
            this.index = index;
            this.filterPossibleDrinks();
        }
    };
    DrinksComponent.prototype.addPlaylists = function () {
        var _this = this;
        this.drinksService.getPlaylists()
            .subscribe(function (data) {
            for (var _i = 0, _a = data.results; _i < _a.length; _i++) {
                var item = _a[_i];
                var dict = {
                    'name': item.name,
                    'checkbox': false
                };
                _this.playlistData.push(dict);
            }
        });
    };
    DrinksComponent.prototype.loadMoreResults = function () {
        var _this = this;
        this.extraLoading = true;
        var url = this.drinksData[this.drinksData.length - 1].next;
        console.log(url);
        this.drinksService.getNextPage(url)
            .subscribe(function (data) {
            _this.extraLoading = false;
            if (!data.next) {
                _this.lastResult = true;
            }
            _this.drinksData.push(data);
            _this.drinksDataGroups.push.apply(_this.drinksDataGroups, _this.groupDrinks(data.results));
        }, function (error) {
            _this.extraLoading = false;
        });
    };
    DrinksComponent = __decorate([
        Component({
            selector: 'app-drinks',
            templateUrl: './drinks.component.html',
            styleUrls: ['./drinks.component.css'],
        }),
        __metadata("design:paramtypes", [Router,
            DrinksService,
            IngredientsService,
            AuthService])
    ], DrinksComponent);
    return DrinksComponent;
}());
export { DrinksComponent };
//# sourceMappingURL=drinks.component.js.map