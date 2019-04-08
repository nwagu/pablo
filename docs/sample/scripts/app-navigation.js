(function($, App) {

  "use strict";

  /* ============== */
  /* MODULE TRIGGER */
  /* ============== */

  var sideNavTrigger = '[data-navigation]',
      body = $('body'),
      TweenMax = window.TweenMax;

  /* =============== */
  /* MODULE DEFAULTS */
  /* =============== */

  var defaults = {
    mobileMaxWidth: 768,
    animateDuration: 400,
    mobileRightSpace: 50,
    navTopPos: 74
  };

  /* ================= */
  /* MODULE DEFINITION */
  /* ================= */

  function SideNav(opts) {
    this.settings = $.extend({}, defaults, opts);
    return this.init();
  }

  /* ============== */
  /* MODULE METHODS */
  /* ============== */

  SideNav.prototype.init = function() {
    this.initSideNav($(sideNavTrigger));
    return this;
  };

  SideNav.prototype.initSideNav = function(navigation) {
    var that = this,
        vars = {};
    that.vars = vars;
    vars.app = $('#app');
    vars.header = $('> .header', vars.app);
    vars.mainHeader = $('.main-header .container-fluid', vars.header);

    if(navigation.length && vars.header.length) {
      vars.navigation = navigation;
      vars.sideNavDefaultPaddingLeft = parseInt(navigation.css('padding-left'), 10);
      vars.sideNavDefaultW = navigation.outerWidth() - vars.sideNavDefaultPaddingLeft;
      vars.allSubmenuWrap = $('.dropdown', vars.navigation);
      vars.overlay = $('.overlay');
      vars.winElm = $(window);
      vars.bodyElm = $('body');
      vars.iOSDevice = navigator.userAgent.match(/iPhone|iPad|iPod/i);
      vars.isMobile = App.viewportWidth() < that.settings.mobileMaxWidth;
      vars.toggleMenuBtn = $('.burger-btn');
      vars.iconBurger1 = $('.icon-burger-1', vars.toggleMenuBtn);
      vars.iconBurger2 = $('.icon-burger-2', vars.toggleMenuBtn);
      vars.iconBurger3 = $('.icon-burger-3', vars.toggleMenuBtn);
      vars.btnMenuPaddingLeft = parseInt(vars.toggleMenuBtn.parent().css('padding-left'), 10) * 2;
      vars.inputSearch = $('#input-search-nav', navigation);

      vars.toggleMenuBtn.off('click.toggleSideNav').on('click.toggleSideNav', function() {
        that.toggleSideNav();
      });

      vars.navigation.find('.btn-close').off('click.closeSideNav').on('click.closeSideNav', function() {
        that.closeSideNav();
      });

      vars.overlay.off('click.closeSideNav').on('click.closeSideNav', function() {
        that.closeSideNav();
      });

      that.initSubmenu();
      vars.winElm
        .on('resize.setSideNavPos', function() {
          that.setSideNavPos();
        }).trigger('resize.setSideNavPos');

      if(window.Modernizr.touch) {
        vars.navigation.on('touchstart', function() {
          if(vars.timeoutNavFocus) {
            clearTimeout(vars.timeoutNavFocus);
          }
          vars.isNavFocus = true;
        }).on('touchend', function() {
          vars.timeoutNavFocus = setTimeout(function() {
            vars.isNavFocus = false;
          }, 1000);
        });
        vars.bodyElm.on('touchstart', function() {
          if(vars.timeoutBodyTouch) {
            clearTimeout(vars.timeoutBodyTouch);
          }
          vars.isBodyTouch = true;
        }).on('touchend', function() {
          vars.timeoutBodyTouch = setTimeout(function() {
            vars.isBodyTouch = false;
          }, 1000);
        });
        if(vars.iOSDevice && vars.isMobile) {
          vars.navigation.css('position', 'absolute');
        }
        else {
          vars.inputSearch.on('focus.scrollToInput', function() {
            setTimeout(function() {
              vars.navigation.scrollTop(vars.inputSearch.offset().top);
            }, 500);
          });
        }
        vars.winElm.on('resize.setHeightBody', function() {
          if(window.Modernizr.touch && !vars.isBodyTouch && vars.navigation.hasClass('open')) {
            vars.app.css({
              'height': vars.winElm.height()
            });
          }
        });
      }
      else{
        vars.navigation.mCustomScrollbar();
        vars.navigation.on('mousewheel wheel', function(e){
          e.preventDefault();
        });
        vars.winElm.on('resize.setSideNavPaddingLeft', function() {
          if (App.viewportWidth() >= that.settings.mobileMaxWidth) {
            navigation.width(vars.sideNavDefaultW);
            navigation.css('padding-left', vars.mainHeader.offset().left + vars.sideNavDefaultPaddingLeft);
          }
          else {
            navigation.css('padding-left', vars.sideNavDefaultPaddingLeft);
          }
        }).trigger('resize.setSideNavPaddingLeft');
      }
      vars.winElm.on('scroll.closeSideNav touchmove', function() {
        if(vars.inputSearch.is(':focus') || vars.isNavFocus) {
          return;
        }
        if(window.Modernizr.touch && !vars.isBodyTouch && vars.navigation.hasClass('open')) {
          vars.app.css({
            'height': vars.winElm.height()
          });
          return;
        }
        if(vars.navigation.hasClass('open')) {
          that.closeSideNav();
        }
      });
    }
    return this;
  };

  SideNav.prototype.toggleSideNav = function() {
    if(this.vars.navigation.hasClass('open')) {
      this.closeSideNav();
    }
    else {
      this.openSideNav();
    }
  };

  SideNav.prototype.openSideNav = function() {
    var vars = this.vars;
    vars.overlay.removeClass('hide');
    vars.navigation.addClass('open');
    TweenMax.to(vars.iconBurger1, 0.3, {
      rotation: 45,
      top: 8
    });
    TweenMax.to(vars.iconBurger2, 0.3, {
      rotation: 30,
      top: 6,
      opacity: 0
    });
    TweenMax.to(vars.iconBurger3, 0.3, {
      rotation: -45,
      top: 8
    });
    if(window.Modernizr.touch && vars.isMobile) {
      vars.app.css({
        'height': vars.winElm.height(),
        'overflow': 'hidden'
      });
    }
    vars.navigation.stop().animate({
      'left': 0
    }, this.settings.animateDuration * 2, function() {
      vars.winElm.trigger('resize');
    });

    if (App.viewportWidth() < this.settings.mobileMaxWidth) {
      vars.header.stop().animate({
        'left': vars.navigationW
      }, this.settings.animateDuration * 2);
    }
  };

  SideNav.prototype.closeSideNav = function() {
    var vars = this.vars;
    TweenMax.to(vars.iconBurger1, 0.3, {
      rotation: 0,
      top: 0
    });
    TweenMax.to(vars.iconBurger2, 0.3, {
      rotation: 0,
      top: vars.iconBurger2.data('top-pos'),
      opacity: 1
    });
    TweenMax.to(vars.iconBurger3, 0.3, {
      rotation: 0,
      top: vars.iconBurger3.data('top-pos')
    });

    vars.navigation.stop().animate({
      'left': '-100%'
    }, this.settings.animateDuration * 2, function() {
      if(window.Modernizr.touch && vars.isMobile) {
        vars.app.css({
          'height': '',
          'overflow': ''
        });
      }
      vars.overlay.addClass('hide');
      vars.navigation.removeClass('open');
      vars.navigation.scrollTop(0);
      vars.winElm.trigger('scroll.setHeaderPosition');
    });

    if (App.viewportWidth() < this.settings.mobileMaxWidth) {
      vars.header.stop().animate({
        'left': 0
      }, this.settings.animateDuration * 2);
    }
    vars.inputSearch.removeClass('error').val('');
    this.closeSubMenu();
  };

  SideNav.prototype.setSideNavPos = function() {
    var that = this,
        vars = this.vars,
        headerLeft = 0,
        isMobileView = App.viewportWidth() < this.settings.mobileMaxWidth ? true : false;

    if(!window.Modernizr.touch){
      var jsp = vars.navigation.data('jsp');
      if(jsp){
        jsp.destroy();
      }
    }
    vars.navigation.css('height', '');
    vars.navigationW = '';
    if(isMobileView) {
      vars.navigationW = vars.bodyElm.width() - this.settings.mobileRightSpace;
      headerLeft = vars.navigationW;
      vars.navigation.css('top', '');
      vars.iconBurger2.data('top-pos', 6);
      vars.iconBurger3.data('top-pos', 12);
    }
    else {
      vars.iconBurger2.data('top-pos', 8);
      vars.iconBurger3.data('top-pos', 16);
      vars.navigation.css({
        'height': vars.navigation.height() - that.settings.navTopPos,
        'top': that.settings.navTopPos
      });
    }
    if(!vars.navigation.hasClass('open')) {
      vars.iconBurger2.css('top', vars.iconBurger2.data('top-pos'));
      vars.iconBurger3.css('top', vars.iconBurger3.data('top-pos'));
    }

    vars.navigation.css('width', vars.navigationW);
    if(vars.navigation.hasClass('open')) {
      vars.header.css('left', headerLeft);
    }
  };

  SideNav.prototype.initSubmenu = function() {
    var that = this,
        vars = this.vars;
    vars.allSubmenuWrap.each(function() {
      var subMenuWrap = $(this),
          subMenu = $('.dropdown-menu', subMenuWrap);
      subMenuWrap.on('click', function() {
        if(!vars.forceWait) {
          vars.forceWait = true;
          if(subMenuWrap.hasClass('isOpen')) {
            that.closeSubMenu();
          }
          else {
            that.closeSubMenu();
            subMenuWrap.addClass('isOpen');
            subMenu.slideDown(that.settings.animateDuration, function() {
              vars.activeSubmenuWrap = subMenuWrap;
              vars.activeSubmenu = subMenu;
              vars.forceWait = false;
            });
          }
        }
      });
    });
  };

  SideNav.prototype.closeSubMenu = function() {
    var vars = this.vars;
    if(vars.activeSubmenuWrap) {
      vars.activeSubmenuWrap.removeClass('isOpen');
      vars.activeSubmenu.slideUp(this.settings.animateDuration, function() {
        vars.activeSubmenuWrap = null;
        vars.activeSubmenu = null;
        vars.forceWait = false;
      });
    }
  };


  /* =============== */
  /* MODULE DATA-API */
  /* =============== */

  $(function() {
    var opts = {};
    App.sideNav = new SideNav(opts);
  });

}(window.jQuery, window.App));
