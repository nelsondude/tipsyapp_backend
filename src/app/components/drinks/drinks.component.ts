import {Component, OnInit} from '@angular/core';
import {DrinksService} from '../../_services/drinks.service';
import {IngredientsService} from '../../_services/ingredients.service';
import {Router} from '@angular/router';
import {AuthService} from '../../_services/auth.service';

@Component({
  selector: 'app-drinks',
  templateUrl: './drinks.component.html',
  styleUrls: ['./drinks.component.css'],
})
export class DrinksComponent implements OnInit {
  drinksData = [];
  drinksDataGroups = [];

  playlistData = [];
  applied = true;
  isOpen = false;

  options = [
    {name: 'Most Recent', query: 'timestamp'},
    {name: 'Percent You Have', query: 'percent'},
    {name: 'Items Missing', query: 'count_need'},
    {name: 'Items You Have', query: 'count_have'}
  ];
  index = 0;

  extraLoading = false;
  lastResult = false;
  noResults = false;

  color = 'primary';
  mode = 'determinate';
  value = 0;
  bufferValue = 75;

  constructor(private router: Router,
              private drinksService: DrinksService,
              private ingredientsService: IngredientsService,
              public auth: AuthService) { }

  ngOnInit() {
    this.filterPossibleDrinks();
    this.addPlaylists();
    this.ingredientsService.ingredientChanged
      .subscribe(
        () => this.filterPossibleDrinks()
      );
  }

  loadVideo(drink: any) {
    this.router.navigate(['/', drink.slug])
  }

  groupDrinks(data: any) {
    const groups = [];
    for (let i = 0; i < data.length; i = i + 4) {
      const group = data.slice(i, i + 4);
      groups.push(group);
    }
    return groups
  }

  filterPossibleDrinks() {
    this.mode = 'indeterminate';
    const result = [];
    if (this.applied) {
      for (let i = 0; i < this.playlistData.length; i++) {
        if (this.playlistData[i].checkbox) {
          result.push(this.playlistData[i].name);
        }
      }
    }
    this.drinksService.filterDrinks(result, this.options[this.index].query, '')
      .subscribe(
        (data) => {
          this.drinksData = [data];
          this.noResults = data.count === 0
          this.drinksDataGroups = this.groupDrinks(data.results);
          this.mode = 'determinate';
        },
        err => {
          this.mode = 'determinate';
        }
      );
  }

  onClickApply() {
    this.isOpen = false;
    this.filterPossibleDrinks();
  }

  onClickCheckbox(event: any, i: number) {
    this.playlistData[i].checkbox = event.srcElement.checked;
    if (this.applied) {
      this.filterPossibleDrinks();
    }
  }

  menuOptionClicked(index: number) {
    if (index !== this.index) {
      this.index = index;
      this.filterPossibleDrinks();
    }
  }


  addPlaylists() {
    this.drinksService.getPlaylists()
      .subscribe(
        (data) => {
          for (const item of data.results) {
            const dict = {
              'name': item.name,
              'checkbox': false
            };
            this.playlistData.push(dict)
          }
        }
      );
  }

  loadMoreResults() {
    this.extraLoading = true;
    const url = this.drinksData[this.drinksData.length - 1].next;
    console.log(url)
    this.drinksService.getNextPage(url)
      .subscribe(
        (data) => {
          this.extraLoading = false;
          if (!data.next) {
            this.lastResult = true;
          }
          this.drinksData.push(data);
          this.drinksDataGroups.push.apply(this.drinksDataGroups, this.groupDrinks(data.results));
        },
        (error) => {
          this.extraLoading = false
        }
      );
  }
}
