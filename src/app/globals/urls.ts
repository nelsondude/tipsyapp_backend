import { environment } from '../../environments/environment';

export namespace Urls {
  export let drinks: string = environment.apiUrl + 'api/drink/';
  export let playlists: string = environment.apiUrl + 'api/drink/playlists/';
  export let ingredients: string = environment.apiUrl + 'api/ingredients/';
}

