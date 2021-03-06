/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.l = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };

/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};

/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};

/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 10);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _rapidMainCtrl = __webpack_require__(4);

var _rapidMainCtrl2 = _interopRequireDefault(_rapidMainCtrl);

var _rapidAdminUsersCtrl = __webpack_require__(3);

var _rapidAdminUsersCtrl2 = _interopRequireDefault(_rapidAdminUsersCtrl);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var mod = angular.module('ds.rapid.controllers', []);

mod.controller('RapidMainCtrl', _rapidMainCtrl2.default);
mod.controller('RapidAdminUsersCtrl', _rapidAdminUsersCtrl2.default);

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _eventListing = __webpack_require__(6);

var _eventListing2 = _interopRequireDefault(_eventListing);

var _eventListingDetailed = __webpack_require__(5);

var _eventListingDetailed2 = _interopRequireDefault(_eventListingDetailed);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var mod = angular.module('ds.rapid.directives', []);

mod.directive('eventListing', _eventListing2.default);
mod.directive('eventListingDetailed', _eventListingDetailed2.default);

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _rapidDataService = __webpack_require__(8);

var _rapidDataService2 = _interopRequireDefault(_rapidDataService);

var _rapidAdminService = __webpack_require__(7);

var _rapidAdminService2 = _interopRequireDefault(_rapidAdminService);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var mod = angular.module('ds.rapid.services', []);

mod.service('RapidDataService', _rapidDataService2.default);
mod.service('RapidAdminService', _rapidAdminService2.default);

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var RapidAdminUsersCtrl = function () {
  RapidAdminUsersCtrl.$inject = ["UserService", "RapidAdminService"];
  function RapidAdminUsersCtrl(UserService, RapidAdminService) {
    'ngInject';

    _classCallCheck(this, RapidAdminUsersCtrl);

    this.UserService = UserService;
    this.RapidAdminService = RapidAdminService;
    this.list_admin_users();
  }

  _createClass(RapidAdminUsersCtrl, [{
    key: 'list_admin_users',
    value: function list_admin_users() {
      var _this = this;

      this.UserService.search({ q: '', role: 'Rapid Admin' }).then(function (resp) {
        _this.admin_users = resp;
      });
    }
  }, {
    key: 'search_users',
    value: function search_users(q) {
      var _this2 = this;

      if (q.length > 1) {
        this.UserService.search({ q: q }).then(function (resp) {
          console.log(resp);
          _this2.found_users = resp;
        });
      } else {
        this.found_users = [];
      }
    }
  }, {
    key: 'make_admin',
    value: function make_admin(user) {
      var _this3 = this;

      this.RapidAdminService.update_permissions(user, 'grant').then(function (resp) {
        _this3.list_admin_users();
      });
    }
  }, {
    key: 'revoke_admin',
    value: function revoke_admin(user) {
      var _this4 = this;

      this.RapidAdminService.update_permissions(user, 'revoke').then(function (resp) {
        _this4.list_admin_users();
      });
    }
  }]);

  return RapidAdminUsersCtrl;
}();

exports.default = RapidAdminUsersCtrl;

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _L = __webpack_require__(9);

var _L2 = _interopRequireDefault(_L);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var RapidMainCtrl = function () {
  RapidMainCtrl.$inject = ["$scope", "$compile", "RapidDataService"];
  function RapidMainCtrl($scope, $compile, RapidDataService) {
    'ngInject';

    var _this = this;

    _classCallCheck(this, RapidMainCtrl);

    console.log("RapidMainCtrl");
    this.$scope = $scope;
    this.$compile = $compile;
    this.RapidDataService = RapidDataService;
    this.show_sidebar = true;
    this.filter_options = {};
    this.active_rapid_event = null;

    var streets = _L2.default.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });

    var satellite = _L2.default.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy;',
      maxZoom: 18
    });

    var basemaps = {
      'Street': streets,
      'Satellite': satellite
    };
    this.map = _L2.default.map('map', {
      layers: [streets, satellite],
      scrollWheelZoom: true
    }).setView([30.2672, -97.7431], 2);
    this.map.zoomControl.setPosition('topright');

    this.RapidDataService.get_event_types().then(function (resp) {
      _this.event_types = resp;
    });

    this.RapidDataService.get_events().then(function (resp) {
      _this.events = resp;
      _this.events.forEach(function (d) {
        // let template = "<div class=''>" +
        //   "<h3> {{event.title}} </h3>" +
        //   "<div ng-repeat='dataset in event.datasets'>" +
        //   "<a href='{{dataset.href}}'> {{dataset.doi}} </a>"+
        //   "</div>";
        // let linker = this.$compile(angular.element(template));
        var marker = _L2.default.marker([d.location.lat, d.location.lon]);
        // let newScope = this.$scope.$new();
        // newScope.event = d;
        // marker.bindPopup(linker(newScope)[0], {className : 'rapid-popup'});
        _this.map.addLayer(marker);
        marker.rapid_event = d;
        marker.on('click', function (ev) {
          if (marker.rapid_event == _this.active_rapid_event) {
            _this.active_rapid_event = null;
          } else {
            _this.active_rapid_event = marker.rapid_event;
            _this.show_sidebar = true;
          }
          _this.$scope.$apply();
        });
      });
    });
  }

  _createClass(RapidMainCtrl, [{
    key: 'select_event',
    value: function select_event(ev) {
      this.map.setView([ev.location.lat, ev.location.lon], 8, { animate: true });
      this.active_rapid_event = ev;
    }
  }, {
    key: 'search',
    value: function search() {
      console.log(this.filter_options);
      this.filtered_events = this.RapidDataService.search(this.events, this.filter_options);
    }
  }, {
    key: 'clear_filters',
    value: function clear_filters() {
      this.filter_options = {};
      this.search();
    }
  }]);

  return RapidMainCtrl;
}();

exports.default = RapidMainCtrl;

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = eventListingDetailed;
function eventListingDetailed() {
  return {
    templateUrl: "/static/designsafe/apps/rapid/html/event-listing-detailed.html",
    scope: {
      event: '=event'
    }
  };
}

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = eventListing;
function eventListing() {
  return {
    templateUrl: "/static/designsafe/apps/rapid/html/event-listing.html",
    scope: {
      event: '=event'
    }
  };
}

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var RapidAdminService = function () {
  RapidAdminService.$inject = ["$http", "$q"];
  function RapidAdminService($http, $q) {
    'ngInject';

    _classCallCheck(this, RapidAdminService);

    this.$http = $http;
    this.$q = $q;
  }

  _createClass(RapidAdminService, [{
    key: 'update_permissions',
    value: function update_permissions(user, action) {
      var payload = {
        username: user.username,
        action: action
      };

      return this.$http.post('/rapid/admin/users/permissions', payload).then(function (resp) {
        return resp.data;
      });
    }
  }]);

  return RapidAdminService;
}();

exports.default = RapidAdminService;

/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var RapidDataService = function () {
  RapidDataService.$inject = ["$http", "$q"];
  function RapidDataService($http, $q) {
    'ngInject';

    _classCallCheck(this, RapidDataService);

    this.$http = $http;
    this.$q = $q;
  }

  _createClass(RapidDataService, [{
    key: 'get_events',
    value: function get_events(opts) {
      console.log(opts);
      return this.$http.get('/recon-portal/events', opts).then(function (resp) {
        resp.data.forEach(function (d) {
          d.created_date = new Date(d.created_date);
          d.event_date = new Date(d.event_date);
        });
        return resp.data;
      });
    }
  }, {
    key: 'get_event_types',
    value: function get_event_types() {
      return this.$http.get('/recon-portal/event-types').then(function (resp) {
        return resp.data;
      });
    }
  }, {
    key: 'search',
    value: function search(events, filter_options) {
      var tmp = _.filter(events, function (item) {
        var f1 = true;
        if (filter_options.event_type) {
          f1 = item.event_type == filter_options.event_type.name;
        }
        var f2 = true;
        if (filter_options.search_text) {
          f2 = item.title.toLowerCase().indexOf(filter_options.search_text.toLowerCase()) !== -1;
        }
        var f3 = true;
        if (filter_options.start_date) {
          f3 = item.event_date > filter_options.start_date;
        }
        var f4 = true;
        if (filter_options.end_date) {
          f4 = item.event_date < filter_options.end_date;
        }
        return f1 && f2 && f3 && f4;
      });
      return tmp;
    }
  }]);

  return RapidDataService;
}();

exports.default = RapidDataService;

/***/ }),
/* 9 */
/***/ (function(module, exports) {

module.exports = L;

/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


config.$inject = ["$stateProvider", "$uibTooltipProvider", "$urlRouterProvider", "$locationProvider"];
Object.defineProperty(exports, "__esModule", {
  value: true
});

var _controllers = __webpack_require__(0);

var _services = __webpack_require__(2);

var _directives = __webpack_require__(1);

var mod = angular.module('designsafe');
mod.requires.push('ui.router', 'ds.rapid.controllers', 'ds.rapid.services', 'ds.rapid.directives', 'ngAnimate');

function config($stateProvider, $uibTooltipProvider, $urlRouterProvider, $locationProvider) {
  'ngInject';

  $locationProvider.html5Mode({
    enabled: true,
    rewriteLinks: false
  });

  $stateProvider.state('rapid', {
    url: '/',
    templateUrl: '/static/designsafe/apps/rapid/html/index.html',
    controller: 'RapidMainCtrl as vm',
    resolve: {
      auth: function auth() {
        return true;
      }
    }
  }).state('rapid_admin', {
    url: '/admin/users',
    templateUrl: '/static/designsafe/apps/rapid/html/rapid-admin-users.html',
    controller: 'RapidAdminUsersCtrl as vm',
    resolve: {
      auth: function auth() {
        return true;
      }
    }
  });

  //config popups etc
  $uibTooltipProvider.options({ popupDelay: 1000 });
}

mod.config(config);

exports.default = mod;

/***/ })
/******/ ]);
//# sourceMappingURL=bundle.9658dc11a576a697925d.js.map