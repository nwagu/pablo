(function (window, App) {

  "use strict";

  App = {};
  App.settings = {};
  App.settings.locales = {};

  window.App = App;

}(window));

/* ============ */
/* APP SETTINGS */
/* ============ */

(function (settings) {

  "use strict";

  settings.debug = false;

  settings.locales.close = 'Fermer';
  settings.countryHaveState = [30, 37, 44, 54, 183];

  settings.tagging = {
    invitationForm: {
      invitationStatus: {
        key: 'invitationStatus',
        open: 'open',
        closed: 'closed'
      },
      newsletter: {
        key: 'newsletter',
        checked: true,
        unchecked: false
      }
    }
  };

  settings.currentCityId = '#city-1';

}(window.App.settings));
