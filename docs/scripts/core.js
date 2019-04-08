/*!
 * Hennessy 250 Redesign v1.0.0
 * Generated on Fri Mar 06 2015 16:44:23
 * DIGITAS France
 */

/* =========
 * get-window-width.js
 * ========= */

(function ($, App) {

    "use strict";

    /* =============== */
    /* MODULE DATA-API */
    /* =============== */

    $(function () {
        App.viewportWidth = (function () {
            if (window.Modernizr && window.Modernizr.touch) {
                return function () {
                    return $(window).width();
                };
            } else {
                if (navigator.userAgent.match(/safari/i) && !navigator.userAgent.match(/chrome/i)) {
                    return function () {
                        return document.documentElement.clientWidth;
                    };
                } else {
                    return function () {
                        return window.innerWidth || document.documentElement.clientWidth;
                    };
                }
            }
        })();
    });

}(window.jQuery, window.App));

/* =========
 * image-loader.js
 * ========= */

(function ($, App) {

    "use strict";

    /* =============== */
    /* IMAGE LOADER DEFAULTS */
    /* =============== */

    var defaults = {};

    /* ================= */
    /* IMAGE LOADER DEFINITION */
    /* ================= */

    function ImageLoader(opts) {
        this.settings = $.extend({}, defaults, opts);
        return this.init();
    }

    /* ============== */
    /* IMAGE LOADER METHODS */
    /* ============== */

    ImageLoader.prototype.init = function () {
        var that = this;
        return this;
    };

    ImageLoader.prototype.check = function (container, callback) {
        var that = this;
        var images = container.find('img'),
                imagesLen = images.length,
                imagesLoaded = 0,
                imgsUrl = [];

        if (!imagesLen) {
            callback();
            return this;
        }

        var checkFinish = function () {
            imagesLoaded += 1;
            if (imagesLoaded === imagesLen) {
                callback();
            }
        };

        images.each(function () {
            var src = $(this).attr('src');
            if (imgsUrl.indexOf(src) === -1) {
                var img = new Image();
                img.onerror = img.onload = checkFinish;
                img.src = src + '?rand=' + Math.random();
                imgsUrl.push(src);
            }
            else {
                checkFinish();
            }
        });

        return this;
    };

    /* =============== */
    /* IMAGE LOADER DATA-API */
    /* =============== */

    $(function () {
        App.imageLoader = new ImageLoader();
    });

}(window.jQuery, window.App));
/* =========
 * check-browser.js
 * ========= */

(function ($, App) {

    "use strict";

    /* =============== */
    /* MODULE DATA-API */
    /* =============== */

    $(function() {
    var ua = navigator.userAgent.toLowerCase();

    if(window.Modernizr && !window.Modernizr.touch) {
      if(ua.match(/ie 10/ig)) {
        $('html').addClass('ie10');
      }
    }

    if(ua.indexOf('windows') !== -1 && ua.indexOf('safari') !== -1 && ua.indexOf('chrome') === -1) {
      $('html').addClass('windows-safari');
    }
  });

}(window.jQuery, window.App));

/* =========
 * lazyload.js
 * ========= */

(function ($, App) {

    "use strict";

    /* ============== */
    /* MODULE TRIGGER */
    /* ============== */

    var lazyloadTrigger = '.lazyload-item',
            winElm = $(window),
            body = $('body'),
            isIE9 = $('html').hasClass('ie9');

    /* =============== */
    /* LAZY LOAD DEFAULTS */
    /* =============== */

    var defaults = {
        animDuration: 800,
        timeoutShow: 100,
        offsetDiff: 50,
        initTopPos: 100
    };

    $.easing.jswing = $.easing.swing;

    $.extend($.easing, {
        easeOutCubic: function (x, t, b, c, d) {
            return c * ((t = t / d - 1) * t * t + 1) + b;
        }
    });

    /* ================= */
    /* LAZY LOAD DEFINITION */
    /* ================= */

    function Lazyload(opts) {
        this.settings = $.extend({}, defaults, opts);
        return this.init();
    }

    /* ============== */
    /* LAZY LOAD METHODS */
    /* ============== */

    Lazyload.prototype.init = function () {
        var that = this;
        $('html, body').scrollTop(0);
        that.initLazyload();
        return this;
    };

    Lazyload.prototype.initLazyload = function () {
        var that = this,
                namespace = 'lazyLoad' + Math.random();

        winElm.on('scroll.' + namespace, function () {
            var listItem = $(lazyloadTrigger).not('.inited').filter(':visible'),
                    topPos = (window.innerHeight ? window.innerHeight : winElm.height()) + winElm.scrollTop(),
                    timeout = that.settings.timeoutShow;

            if (body.data('scrolling')) {
                return;
            }

            listItem.each(function () {
                var item = $(this);
                if (!item.hasClass('inited')) {
                    if (item.offset().top + that.settings.offsetDiff < topPos) {
                        item.addClass('inited');
                        if (isIE9) {
                            setTimeout(function () {
                                item.css({
                                    opacity: 0,
                                    top: that.settings.initTopPos
                                }).animate({
                                    opacity: 1,
                                    top: 0
                                }, that.settings.animDuration, 'easeOutCubic');
                            }, timeout);
                        }
                        else {
                            item.css("transition-delay", timeout + "ms");
                        }
                        timeout += that.settings.timeoutShow;
                    }
                }
            });
        }).trigger('scroll.' + namespace);

        winElm.on('resize.lazyload.' + namespace, function () {
            winElm.trigger('scroll.' + namespace);
        });
        return this;
    };

    /* =============== */
    /* LAZY LOAD DATA-API */
    /* =============== */

    $(function () {
        if (!isIE9) {
            $('html').addClass('not-ie9');
        }
        setTimeout(function () {
            App.lazyload = new Lazyload();
        }, 1000);
    });

}(window.jQuery, window.App));
/* =========
 * custom-select.js
 * ========= */
(function ($, App) {

    "use strict";
    /* ============== */
    /* MODULE TRIGGER */
    /* ============== */

    var customSelectTrigger = '[data-custom-select]',
        win = $(window),
            main = $('#main');

    /* =============== */
    /* MODULE DEFAULTS */
    /* =============== */

    var defaults = {
        duration: 200,
        closeCustomSelectTimeout: 700,
        classOpened: 'select-open',
        customClass: 'item-list list-unstyled'
    };

    /* ================= */
    /* MODULE DEFINITION */
    /* ================= */

    function CustomSelect(opts) {
        this.settings = $.extend({}, defaults, opts);
        this.init();
    }

    /* ============== */
    /* MODULE METHODS */
    /* ============== */

    CustomSelect.prototype.init = function () {
        var that = this;
        $(customSelectTrigger).each(function () {
            that.initCustomSelect($(this));
        });
        return this;
    };

    CustomSelect.prototype.generateCustomSelect = function (select, wrapper) {
        var that = this,
                liTemplate = '<li value="{value}">{text}</li>',
                customSelectItems = '';
        $('option', select).each(function () {
            var option = $(this);
            customSelectItems += liTemplate.replace(/{value}/ig, option.val()).replace(/{text}/ig, option.text());
        });
        return $('<ul class="' + that.settings.customClass + '">' + customSelectItems + '</ul>').appendTo(wrapper);
    };

    CustomSelect.prototype.updateOptions = function (select, newOpts) {
        $('option', select).remove();
        for (var i = 0, l = newOpts.length; i < l; i++) {
            select.append('<option value="' + newOpts[i].value + '">' + newOpts[i].text + '</option>');
        }
    };

    CustomSelect.prototype.initCustomSelect = function (wrapper) {
        var that = this,
                label = $('[data-label]', wrapper),
                handler = $('[data-handler]', wrapper),
                select = $('select', wrapper),
                customSelect = this.generateCustomSelect(select, wrapper),
                listItem = $('li:gt(0)', customSelect),
                countItem = listItem.length,
                namespace = Math.random(),
                timeout, isDragger, isHover,
                clearTimeoutCloseCustomSelect = function () {
                    if (timeout) {
                        clearTimeout(timeout);
                    }
                },
                setTimeoutCloseCustomSelect = function () {
                    timeout = setTimeout(function () {
                        that.closeCustomSelect(customSelect);
                    }, that.settings.closeCustomSelectTimeout);
                };

        customSelect
                .data('showed', false)
                .data('selected-index', 0);

        if (window.Modernizr && !window.Modernizr.touch) {
            customSelect.mCustomScrollbar();
            customSelect.on('mousewheel wheel', function (e) {
                e.preventDefault();
            });
            customSelect.maxHeight = parseInt(customSelect.css('max-height'), 10);
            customSelect.scrollBar = $('.mCSB_draggerContainer', customSelect);
            customSelect.scrollBtn = $('.mCSB_dragger', customSelect.scrollBar);
            customSelect.scrollContent = $('.mCSB_container', customSelect);
            customSelect.scrollBtn.on('mousedown.' + Math.random(), function (evt) {
                evt.stopPropagation();
                evt.preventDefault();
                isDragger = true;
            });

            $(document).on('mouseup.' + Math.random(), function () {
                isDragger = false;
                if (!isHover) {
                    setTimeoutCloseCustomSelect();
                }
            });
        }

        handler.off('click.toggleCustomSelect').on('click.toggleCustomSelect', function () {
            handler.removeClass('error');
            that.toggleCustomSelect(customSelect, handler);
        }).off('mouseenter.clearTimeoutCloseCustomSelect').on('mouseenter.clearTimeoutCloseCustomSelect', function () {
            isHover = true;
            clearTimeoutCloseCustomSelect();
        }).off('mouseleave.setTimeoutCloseCustomSelect').on('mouseleave.setTimeoutCloseCustomSelect', function () {
            isHover = false;
            if (!isDragger) {
                setTimeoutCloseCustomSelect();
            }
        });

        customSelect.off('mouseenter.clearTimeoutCloseCustomSelect').on('mouseenter.clearTimeoutCloseCustomSelect', function () {
            isHover = true;
            clearTimeoutCloseCustomSelect();
        }).off('mouseleave.setTimeoutCloseCustomSelect').on('mouseleave.setTimeoutCloseCustomSelect', function () {
            isHover = false;
            if (!isDragger) {
                setTimeoutCloseCustomSelect();
            }
        });

        $('li', customSelect).off('click.selectItem').on('click.selectItem', function () {
            that.selectItem(customSelect, select, label, $(this).index());
        });

        select.off('change.changeLabel').on('change.changeLabel', function () {
            that.selectItem(customSelect, select, label, $('option:selected', select).index());
        });

        if (select.data('auto-scroll') && window.Modernizr && !window.Modernizr.touch) {
            $(window).on('keypress.scrollToItem' + namespace, function (e) {
                if (customSelect.data('showed')) {
                    var keyCode = e.keyCode || e.which,
                            character = String.fromCharCode(keyCode).toUpperCase();
                    for (var i = 0; i < countItem; i++) {
                        var item = listItem.eq(i);
                        if (item.text().charAt(0) === character) {
                            customSelect.mCustomScrollbar('scrollTo', item.offset().top - customSelect.scrollContent.offset().top, {scrollInertia: that.settings.duration});
                            return;
                        }
                    }
                }
            });
        }

        that.selectItem(customSelect, select, label, select.find('option:selected').index(), true);
        return this;
    };

    CustomSelect.prototype.toggleCustomSelect = function (customSelect, handler) {
        var that = this;
        if (!customSelect.data('showed')) {
            that.openCustomSelect(customSelect, handler);
        }
        else {
            that.closeCustomSelect(customSelect);
        }
    };

    CustomSelect.prototype.openCustomSelect = function (customSelect, handler) {
        var that = this;
        customSelect.addClass(that.settings.classOpened);
        if (window.Modernizr && !window.Modernizr.touch && customSelect.scrollBar) {
            customSelect.scrollBar.css('opacity', 0);
        }
        if (!customSelect.closest('.modal').length) {
            main.css('zIndex', 10);
        }
        customSelect.slideDown(that.settings.duration, function(){
        var activeItem = customSelect.find('li:eq(' + customSelect.data('selected-index') + ')');
            customSelect.data('showed', true);
            if (window.Modernizr && !window.Modernizr.touch) {
                customSelect.mCustomScrollbar('scrollTo', activeItem.offset().top - customSelect.scrollContent.offset().top, {scrollInertia: that.settings.duration});
                if (customSelect.scrollContent.height() > customSelect.maxHeight) {
                    customSelect.scrollBar.css('opacity', 1);
                }
            }
            else {
                var curScollTop = customSelect.scrollTop(),
                    scrollTopPos;
                customSelect.scrollTop(0);
                scrollTopPos = activeItem.offset().top - customSelect.offset().top;
                customSelect.scrollTop(curScollTop);
                customSelect.animate({
                    scrollTop: scrollTopPos
                }, that.settings.duration);
            }
          //Check if custom select overflow
           if(customSelect.closest('[data-check-slideup]').length) {
            var handlerH = handler.outerHeight(),
              customSelectH = customSelect.outerHeight();
            if (handler.offset().top + handlerH + customSelectH > win.height()) {
              customSelect.css('margin-top', -(customSelectH + handlerH));
            } else {
              customSelect.css('margin-top', 'auto');
            }
          }
          else {
            customSelect.css('margin-top', 'auto');
          }

        });
    };

    CustomSelect.prototype.closeCustomSelect = function (customSelect) {
        var that = this;
        customSelect.removeClass(that.settings.classOpened);
        if (window.Modernizr && !window.Modernizr.touch && customSelect.scrollBar) {
            customSelect.scrollBar.css('opacity', 0);
        }
        customSelect.slideUp(that.settings.duration, function () {
            customSelect.data('showed', false);
            if (0 === main.find('.' + that.settings.classOpened).length) {
                main.css('zIndex', '');
            }
        });
    };

    CustomSelect.prototype.selectItem = function (customSelect, select, label, index, forceChange) {
        var that = this,
                selectedItem = $('option:eq(' + index + ')', select),
                oldSelectedIndex = select.find('option:selected').index();
        if (oldSelectedIndex !== index || forceChange) {
            selectedItem.prop('selected', true);
            customSelect.data('selected-index', index);
            if (select.data('show-value')) {
                var value = selectedItem.val();
                if (value) {
                    label.text(value);
                }
                else {
                    label.text(selectedItem.text());
                }
            }
            else {
                label.text(selectedItem.text());
            }
            select.trigger('change');
        }
        that.closeCustomSelect(customSelect);
    };

    CustomSelect.prototype.refreshCustomSelect = function (wrapper, newOpts) {
        $('ul', wrapper).remove();
        this.updateOptions($('select', wrapper), newOpts);
        this.initCustomSelect(wrapper);
    };

    /* =============== */
    /* MODULE DATA-API */
    /* =============== */

    $(function () {
        var opts = {};
        App.customSelect = new CustomSelect(opts);
    });

}(window.jQuery, window.App));
/* =========
 * video.js
 * ========= */
(function($, App) {

  "use strict";
  /* ============== */
  /* MODULE TRIGGER */
  /* ============== */

  var btnPlayTrigger = '[data-play-video]',
      videoWrapTrigger = '[data-video-wrap]';

  /* =============== */
  /* MODULE DEFAULTS */
  /* =============== */

  var defaults = {};

  /* ================= */
  /* MODULE DEFINITION */
  /* ================= */

  function VideoManager(opts) {
    this.settings = $.extend({}, defaults, opts);
    this.init();
  }

  /* ============== */
  /* MODULE METHODS */
  /* ============== */

  VideoManager.prototype.init = function() {
    var that = this;
    that.isWindowSafari = $('html').hasClass('windows-safari') ? true : false;

    var tag = document.createElement('script');
    tag.src = 'http://www.youtube.com/player_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    window.onYouTubePlayerAPIReady = function() {
      $('iframe.youtube-video').each(function() {
        that.addYoutubeEvent(this);
      });
    };

    $('body')
      .off('click.playVideo', btnPlayTrigger)
      .on('click.playVideo', btnPlayTrigger, function() {
        var elm = $(this),
            videoType = elm.data('type'),
            videoSrc = elm.data('src'),
            wrapper = elm.closest(videoWrapTrigger),
            sliderViewport = elm.closest('.flex-viewport'),
            content = wrapper.children(),
            slider = wrapper.closest('[data-slider]'),
            iframeContent, videoContent;

        wrapper.data('content', content.clone());
        if (!that.isWindowSafari || !sliderViewport.length) {
          content.remove();
        }

        if(slider.length) {
          var sliderDirection = $('.flex-direction-nav', slider);
          if(sliderDirection.length) {
            sliderDirection.hide();
          }
        }

        switch(videoType) {
          case 'vimeo':
            iframeContent = '<iframe class="embed-responsive-item" src="//player.vimeo.com/video/' + videoSrc + '?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=1&amp;api=1&amp;frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>';
            break;
          case 'dailymotion':
            iframeContent = '<iframe class="embed-responsive-item" src="//www.dailymotion.com/embed/video/' + videoSrc + '?api=true&autoplay=1" frameborder="0"></iframe>';
            break;
          case 'youku':
            iframeContent = '<iframe class="embed-responsive-item" src="//player.youku.com/embed/' + videoSrc + '" allowFullScreen="true"></iframe>';
            break;
          default:
            videoType = 'youtube';
            iframeContent = '<iframe class="embed-responsive-item youtube-video" frameborder="0" allowfullscreen="1" title="YouTube video player" src="//www.youtube.com/embed/' + videoSrc + '?wmode=opaque&autoplay=1&rel=0&showinfo=0&modestbranding=1&controls=1&showinfo=0&enablejsapi=1"></iframe>';
            break;
        }
        if(wrapper.closest('.home-slider').length) {
          videoContent = $('<div class="container-fluid" style="padding: 0;"><div class="embed-responsive embed-responsive-4by3">' + iframeContent + '</div></div>');
        }
        else {
          videoContent = $('<div class="embed-responsive embed-responsive-4by3">' + iframeContent + '</div>');
        }
        if (that.isWindowSafari && sliderViewport.length) {
          videoContent.addClass('tempt-video').prependTo(sliderViewport);
          sliderViewport.children('.slides').hide();
        }
        else {
          wrapper.data('video-showing', true).append(videoContent);
        }

        if(videoType === 'youtube' && window.YT) {
          that.addYoutubeEvent($('iframe', videoContent)[0]);
        }

      });
    return this;
  };

  VideoManager.prototype.addYoutubeEvent = function(dom) {
    var el = $(dom),
        wrapper = el.closest(videoWrapTrigger),
        viewport = el.closest('.flex-viewport');

    var handle = function() {
      wrapper
          .html(wrapper.data('content'))
          .data('video-showing', false);
    };
    if (this.isWindowSafari && viewport.length) {
      handle = function() {
        viewport.children('.tempt-video').remove();
        viewport.children('.slides').show();
      };
    }

    var player = new window.YT.Player(dom, {
      events: {
        onStateChange: function(e) {
          if(e.data === window.YT.PlayerState.ENDED) {
            handle();
          }
        }
      }
    });
  };

  /* =============== */
  /* MODULE DATA-API */
  /* =============== */

  $(function() {
    var opts = {};
    App.video = new VideoManager(opts);
  });

}(window.jQuery, window.App));
/* =========
 * load-more.js
 * ========= */
(function ($, App) {

    "use strict";
    /* ============== */
    /* MODULE TRIGGER */
    /* ============== */

    var loadMoreTrigger = '[data-btn-load-more]',
            mediumSliderTrigger = '[data-medium-slider]',
            winElm = $(window);

    /* =============== */
    /* MODULE DEFAULTS */
    /* =============== */

    var defaults = {};

    /* ================= */
    /* MODULE DEFINITION */
    /* ================= */

    function LoadMore(opts) {
        this.settings = $.extend({}, defaults, opts);
        this.init();
    }

    /* ============== */
    /* MODULE METHODS */
    /* ============== */

    LoadMore.prototype.init = function () {
        $(loadMoreTrigger).on('click.loadMore', function () {
            var btnLoadMore = $(this);
            if (btnLoadMore.data('force-wait')) {
                return;
            }
            btnLoadMore.data('force-wait', true);
            $.ajax({
                type: 'get',
                url: btnLoadMore.data('url'),
                success: function (res) {
                    var wrapContent = $(btnLoadMore.data('target')),
                            inputLoadMore, loadMoreURL, slider;
                    if (typeof res !== 'object') {
                        res = $.parseJSON(res);
                    }
                    if (res.results) {
                        wrapContent.append(res.results);
                    }
                    winElm.trigger('scroll');
                    if (res.ajax_url) {
                        btnLoadMore.data('url', res.ajax_url).parent().show();
                    }
                    else {
                        btnLoadMore.parent().hide();
                    }
                    slider = $(mediumSliderTrigger, wrapContent);
                    if (slider.length && App.mediumSlider) {
                        App.mediumSlider.initMediumSlider(slider);
                    }
                    btnLoadMore.data('force-wait', false);
                },
                error: function () {
                    btnLoadMore.data('force-wait', false);
                }
            });
        });
        return this;
    };

    /* =============== */
    /* MODULE DATA-API */
    /* =============== */

    $(function () {
        var opts = {};
        App.loadMore = new LoadMore(opts);
    });

}(window.jQuery, window.App));

/* ========
 * alert-form.js
 * ========= */

(function ($, App) {

    "use strict";

    var winElm = $(window);

    /* =============== */
    /* MODULE DATA-API */
    /* =============== */
    App.AlertForm = {
        vars: {
            mobileMaxWidth: 768,
            layerClass: 'alert-layer',
            timeHide: 5000,
            timeWait: null,
            reEmail: /^[a-z0-9._%-]+@[a-z0-9.-]+\.[a-z]{2,4}$/i,
            reString: /(([a-zA-Z]_*)+)/,
            rePass: /^[a-z0-9._%-].{7,100}$/i,
            reCode: /^[a-z0-9._%-].{5,5}$/,
            reNum: /\d/i,
            rePhone: /^(\+?|d+)?(\(\+?\d+\))?(-|\s)?\d+(-|\s)?\d+(-|\s)?\d+(-|\s)?\d+$/,
            reUrl: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/i,
            notAllowChar: /[‘’“”„‚†‡‰‹›♠♣♥♦←↑→↓™!"#$%&'()*+,.\/0123456789:;<=>?@\[\\\]^`{|}~…—¡¢£¤¥¦§¨©ª«¬®¯°±²³´¶·¸¹º»¼½¾¿÷●•]/
        },
        initialize: function (options) {
            $.extend(this.vars, options);

            this.layer = $('<div id="alert-form" class="' + this.vars.layerClass + '">' + '<p class="message"></p>' + '</div>');

            $(document).unbind('mousedown.zhlayer').bind('mousedown.zhlayer', function () {
                App.AlertForm.hide();
            });
        },
        show: function (element, message, offset) {
            var elm = $(element),
                    offs = {
                        x: 0,
                        y: 0,
                        w: 11,
                        h: 0
                    },
            elmoffs = elm.offset();

            $.extend(offs, offset);
            this.layer.css('width', 'auto').find('p.message').html(message);
            this.layer.css({
                'top': elmoffs.top + elm.outerHeight() + offs.y,
                'left': elmoffs.left + offs.x,
                'width': Math.max(0, Math.min(winElm.width() - elmoffs.left + offs.x, Math.max(elm.outerWidth() - 6, this.layer.width()))) + offs.w - 15 //10 = padding left + right of layer
            });

            var tag = elm[0].tagName;
            if (tag === 'INPUT' || tag === 'TEXTAREA') {
                elm[0].select();
                elm[0].focus();
            }

            this.layer.stop(true).fadeTo(300, 1);
            this.layer.data('show', 1);

            var scrollTop = winElm.scrollTop(),
                    wndHeight = winElm.height(),
                    layerTop = this.layer.offset().top;

            if (layerTop < scrollTop) {
                $('html, body').stop().animate({
                    scrollTop: Math.max(0, layerTop - 50)
                });
            } else if (layerTop > scrollTop + wndHeight) {
                $('html, body').stop().animate({
                    scrollTop: Math.max(0, layerTop - wndHeight + 50)
                });
            }

            var that = this;
            clearInterval(this.vars.timeWait);
            this.vars.timeWait = setInterval(function () {
                App.AlertForm.hide();
            }, this.vars.timeHide);
        },
        showInner: function (element, message, hCheck) {
            var elm = $(element),
                    elmParent;
            if (elm.length) {
                elmParent = elm.parent();
                if (elm.attr('type') === 'checkbox') {
                    elmParent.addClass('error');
                    elmParent.unbind('click.alter').bind('click.alter', function () {
                        elmParent.removeClass('error');
                    });
                } else if (elmParent[0].tagName === 'SPAN') {
                    if (elm[0].tagName === 'TEXTAREA') {
                        elmParent.addClass('error');
                        elm.val(message);
                        elm.unbind('blur.alter').unbind('focus.alter').bind('blur.alter', function () {
                            if (elm.val() === '') {
                                elm.val(message);
                                elmParent.addClass('error');
                            }
                        }).bind('focus.alter', function () {
                            if (elm.val() === message) {
                                elm.val('');
                                elmParent.removeClass('error');
                            }
                        });
                    } else {
                        elmParent.addClass('error');
                        elmParent.unbind('click.alter').bind('click.alter', function () {
                            elmParent.removeClass('error');
                        });
                    }
                } else if (elm.attr('type') === 'password') {
                    elm.addClass('error');
                    elm.unbind('blur.alter').unbind('focus.alter').bind('blur.alter', function () {
                        if (elm.val() === '') {
                            elm.addClass('error');
                        } else {
                            elm.removeClass('error');
                        }
                    }).bind('focus.alter', function () {
                        if (elm.val() === '') {
                            elm.val('');
                            elm.removeClass('error');
                        }
                    });
                } else {
                    if (navigator.platform === 'iPad' || window.screen.height === 768) {
                        elm.addClass('error').val(message);
                        elm.css('font-size', '85%');
                    } else {
                        elm.addClass('error').val(message);
                        elm.unbind('keydown.valid').bind('keydown.valid', function () {
                            if (elm.val() === message) {
                                elm.val('');
                                elm.removeClass('error');
                            }
                        });
                    }
                    if (elm.data('handler') === undefined) {
                        elm.unbind('blur.alter').unbind('focus.alter').bind('blur.alter', function () {
                            if (elm.val() === '') {
                                if (navigator.platform === 'iPad') {
                                    elm.addClass('error').val(message);
                                    elm.css('font-size', '85%');
                                } else {
                                    if (!hCheck) {
                                        elm.addClass('error').val(message);
                                    }
                                }
                            }
                        }).bind('focus.alter', function () {
                            if (elm.val() === message || !elm.val()) {
                                elm.val('');
                                elm.removeClass('error');
                            }
                        });
                    }
                }
            }
        },
        autoHideMessage: function (element, delay, duration) {
            delay = delay || 3000;
            duration = duration || 400;
            return setTimeout(function () {
                element.animate({
                    opacity: 0
                }, duration, function () {
                    $(this).css({
                        opacity: 1,
                        display: "none"
                    });
                });
            }, delay);
        },
        hide: function () {
            if (this.layer.data('show')) {
                clearInterval(this.vars.timeWait);
                this.layer.stop(true).fadeTo(200, 0, function () {
                    App.AlertForm.layer.css('top', -50000);
                });
                this.layer.data('show', 0);
            }
        },
        initTextRemain: function (element, counter, limit, zalert) {
            var counterElm = $(counter),
                    elmParent = element.parent();
            element.unbind('keypress.zcremain').bind('keypress.zcremain', function (e) {
                if (elmParent.hasClass('error')) {
                    element.val('');
                    elmParent.removeClass('error');
                    counterElm.text('0/1500 ');
                }
                var code = typeof (e.charCode) !== 'undefined' ? e.charCode : e.keyCode,
                        key = (code === 0) ? '' : String.fromCharCode(code);
                if (key !== '' && this.value.length >= limit) {
                    App.AlertForm.showInner(element, zalert);
                    element.focus(function () {
                        counterElm.text('0/1500 ');
                    });
                    return false;
                }
            })
                    .unbind('keyup.zcremain').bind('keyup.zcremain', function (e) {
                var code = typeof (e.charCode) !== 'undefined' ? e.charCode : e.keyCode,
                        key = (code === 0) ? '' : String.fromCharCode(code);

                if (key !== '' && this.value.length >= limit) {
                    App.AlertForm.showInner(element, zalert);
                    element.focus(function () {
                        counterElm.text('0/1500 ');
                    });
                    return false;
                } else {
                    if (this.value.replace(/^\s+|\s+$/g, '').replace(/\s+/g, ' ') !== "") {
                        counterElm.text(this.value.length + '/1500 ');
                    } else {
                        counterElm.text('0/1500 ');
                    }
                }
            })
                    .unbind('change.zcremain').bind('change.zcremain', function (e) {
                counterElm.text(this.value.length + '/1500 ');
            });
        },
        requireField: function (element, init, temptext) {
            if (element && ($.trim(element.val()).length === 0 || $.trim(element.val()) === init || $.trim(element.val()) === temptext)) {
                return false;
            }
            return true;
        },
        isValidDate: function (day, month, year) {
            var valid = true;
            day = parseInt(day);
            month = parseInt(month);
            year = parseInt(year);
            var newDate = new Date(year, month - 1, day);
            if (newDate.getDate() !== day || newDate.getMonth() + 1 !== month || newDate.getFullYear() !== year) {
                valid = false;
            }
            return valid;
        },
        checkConfirmPass: function (element, curpass) {
            if (element && ($.trim(element.val()) !== curpass.val())) {
                return false;
            }
            return true;
        },
        checkSelect: function (select) {
            var selectedOpt = $('option:selected', select);
            if (!selectedOpt.val() || selectedOpt.index() === 0) {
                return false;
            }
            return true;
        },
        checkCharacters: function (element, limit) {
            if (element.val().length > limit) {
                return false;
            }
            return true;
        },
        validEmail: function (element) {
            return this.vars.reEmail.test(element.val());
        },
        validPass: function (element) {
            return this.vars.rePass.test(element.val());
        },
        validUrl: function (element) {
            return this.vars.reUrl.test(element.val());
        },
        resetText: function (element, init, color) {
            if (element.attr('type') === 'checkbox') {
                element.removeClass('error');
                element.parent().removeClass('checked');
            } else if (element.tagName === "SPAN") {
                element.text(init);
            } else {
                if (color) {
                    element.val(init);
                    element.css('color', color);
                } else {
                    element.val(init);
                }
            }
            element.removeClass('error');
        },
        checkFirstLastName: function (el, holder) {
            if (this.requireField(el, holder)) {
                return $.trim(el.val()).length > 0 && $.trim(el.val()).length < 36 && !this.vars.notAllowChar.test(el.val());
            }
            return false;
        },
        checkCity: function (el, holder) {
            if (this.requireField(el, holder)) {
                return $.trim(el.val()).length > 1 && $.trim(el.val()).length < 51 && !this.vars.notAllowChar.test(el.val());
            }
            return false;
        },
        checkPhoneNumber: function (el, holder) {
            return !$.trim(el.val()).length || $.trim(el.val()) === holder || /^[0-9]{5,11}$/.test(el.val());
        },
        checkCountryhasState: function (value) {
            for (var i = 0, l = App.settings.countryHaveState.length; i < l; i++) {
                if (value === App.settings.countryHaveState[i]) {
                    return true;
                }
            }
            return false;
        },
        isMobile: function () {
            return window.Modernizr && window.Modernizr.touch && (App.viewportWidth() <= this.vars.mobileMaxWidth) ? true : false;
        },
        validatePhoneNumber: function (selectCountryCode, handlerPhoneCountryCode, txtPhone) {
            var trimPhoneNumber = function (value) {
                value = $.trim(value);
                var firstChar = value[0];
                while (firstChar === '0') {
                    value = value.replace(/^0/g, '');
                    firstChar = value[0];
                }
                return value;
            },
                    phoneValue = trimPhoneNumber(txtPhone.val()),
                    isNullPhone = !phoneValue || phoneValue === window.L10N.valid.phone || phoneValue === window.L10N.required.phone,
                    selectedValue = selectCountryCode.find('option:selected').val(),
                    hasError = false;
            txtPhone.val(phoneValue);
            handlerPhoneCountryCode.removeClass('error');
            if (isNullPhone && (!selectedValue || selectedValue === '0')) {
                txtPhone.removeClass('error').val('');
            }
            else {
                if (isNullPhone) {
                    App.AlertForm.showInner(txtPhone, window.L10N.required.phone);
                    hasError = true;
                }
                else {
                    if (!App.AlertForm.checkPhoneNumber(txtPhone, window.L10N.valid.phone)) {
                        App.AlertForm.showInner(txtPhone, window.L10N.valid.phone);
                        hasError = true;
                    }
                    else {
                        if (!App.AlertForm.checkSelect(selectCountryCode)) {
                            App.AlertForm.showInner(handlerPhoneCountryCode);
                            hasError = true;
                        }
                    }
                }
            }
            return hasError;
        },
        initPlaceHolder: function (input) {
            var val, placeHolderVal = $.trim(input.data('placeholder') || input.attr('placeholder')),
                    timeoutBlur;
            if ($('html').hasClass('ie9') || input.data('placeholder')) {
                input.on('focus.checkPlaceHolder', function () {
                    if (timeoutBlur) {
                        clearTimeout(timeoutBlur);
                    }
                    val = $.trim(input.val());
                    if (val === placeHolderVal) {
                        input.val('');
                    }
                }).on('blur.checkPlaceHolder', function () {
                    timeoutBlur = setTimeout(function () {
                        val = $.trim(input.val());
                        if (!val) {
                            input.val(placeHolderVal);
                        }
                    }, 200);
                });
            }
        },
        initDatepicker: function (input, inputHidden, timeSlotReq) {
            var listDisableDate = input.data('disable-date'),
                    ajaxURL = input.data('url'),
                    timeSlotRadioGroup = $('.radio-group', timeSlotReq),
                    listRadio = timeSlotRadioGroup.children(),
                    morning = listRadio.eq(0),
                    afternoon = listRadio.eq(1),
                    allday = listRadio.eq(2),
                    inputMorning = $('input', morning),
                    inputAfternoon = $('input', afternoon),
                    inputAllday = $('input', allday),
                    msgErr = $('.text-danger', timeSlotReq),
                    opts = {
                        showOn: 'both',
                        buttonImage: input.data('img-src'),
                        buttonImageOnly: true,
                        dateFormat: 'dd/mm/yy',
                        minDate: new Date(),
                        onSelect: function (date) {
                            var arrayDate = date.split('/'),
                                    string = $.datepicker.formatDate('mm/dd/yy', new Date(arrayDate[2], (parseInt(arrayDate[1]) - 1), arrayDate[0])),
                                    stringDate = $.datepicker.formatDate('yy-mm-dd', new Date(arrayDate[2], (parseInt(arrayDate[1]) - 1), arrayDate[0]));
                            input.removeClass('error');
                            inputHidden.val(string);
                            $.ajax({
                                type: 'post',
                                url: ajaxURL,
                                data: {
                                    currentDate: stringDate
                                },
                                success: function (res) {
                                    if (typeof res !== 'object') {
                                        res = $.parseJSON(res);
                                    }
                                    timeSlotRadioGroup.show();
                                    listRadio.show();
                                    msgErr.addClass('hidden');
                                    if (res.un) {
                                        switch (res.un) {
                                            case "1":
                                                morning.hide();
                                                afternoon.show();
                                                allday.hide();
                                                inputAfternoon.prop('checked', true);
                                                break;
                                            case "2":
                                                morning.show();
                                                afternoon.hide();
                                                allday.hide();
                                                inputMorning.prop('checked', true);
                                                break;
                                            case "3":
                                                timeSlotRadioGroup.hide();
                                                msgErr.removeClass('hidden').text(res.message);
                                                break;
                                        }
                                    }
                                }
                            });
                        }
                    };
            if (listDisableDate) {
                opts.beforeShowDay = function (date) {
                    var string = $.datepicker.formatDate('dd/mm/yy', date);
                    return [listDisableDate.indexOf(string) === -1];
                };
            }
            input.datepicker(opts);
        }
    };

}(window.jQuery, window.App));

/* =========
 * modal.js
 * ========= */
(function ($, App) {

    "use strict";
    /* ============== */
    /* MODULE TRIGGER */
    /* ============== */

    var modalTrigger = '.modal',
            win = $(window),
            body = $('body'),
            iOSDevice = navigator.userAgent.match(/iPhone|iPad|iPod/i);

    /* =============== */
    /* MODULE DEFAULTS */
    /* =============== */

    var defaults = {};

    /* ================= */
    /* MODULE DEFINITION */
    /* ================= */

    function Modal(opts) {
        this.settings = $.extend({}, defaults, opts);
        this.init();
    }

    /* ============== */
    /* MODULE METHODS */
    /* ============== */

    Modal.prototype.init = function () {
        var main = $('#main'),
                header = $('header'),
                resetForm = function (form) {
                    if (form.hasClass('product-filter-popin')) {
                        return;
                    }
                    form[0].reset();
                    form.find('.error').removeClass('error');
                    form.show();
                    if (form.hasClass('block-sendmail')) {
                        form.next().hide();
                    }
                    if (form.hasClass('captcha-form')) {
                        form.hide();
                    }
                },
                checkBodyScroll = function (popupContent) {
                    if (popupContent.outerHeight() < win.height()) {
                        body.removeClass('reset');
                    }
                    else {
                        body.addClass('reset');
                    }
                },
                setPopupPos = function (popup, popupDialog, popupContent, duration) {
                    var contentH = popupDialog.height(),
                            popupH = popup.height(),
                            contentMarginTop = contentH < popupH ? (popupH - contentH) / 2 : 0;
                    checkBodyScroll(popupContent);
                    popupDialog.css('margin-bottom', Math.max(0, contentMarginTop - 30)).animate({
                        marginTop: contentMarginTop
                    }, duration, function () {
                        checkBodyScroll(popupContent);
                    });
                };

        $(modalTrigger).each(function () {
            var popup = $(this),
                    popupDialog = $('.modal-dialog', popup),
                    popupContent = $('.modal-content', popupDialog),
                    form = $('form', popup);

            if (!popupContent.length) {
                popupContent = $('.modal-body', popupDialog);
            }
            popup.on('show.bs.modal', function (e) {
                if (iOSDevice) {
                    popup.css({
                        position: 'absolute',
                        marginTop: win.scrollTop() + 'px',
                        bottom: 'auto'
                    });

                    setTimeout(function () {
                        $('.modal-backdrop').css({
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '100%',
                            height: Math.max(
                                    document.body.scrollHeight, document.documentElement.scrollHeight,
                                    document.body.offsetHeight, document.documentElement.offsetHeight,
                                    document.body.clientHeight, document.documentElement.clientHeight
                                    ) + 'px'
                        });
                    }, 0);
                }
                else {
                    checkBodyScroll(popupContent);
                    setTimeout(function () {
                        setPopupPos(popup, popupDialog, popupContent, 200);
                    }, 300);
                }
            }).on('shown.bs.modal', function () {
                /*var backdrop = $('.modal-backdrop');
                if (backdrop.length && backdrop.is(':visible') && window.Modernizr.touch) {
                    header.addClass('openedForm hidden');
                    if (!navigator.userAgent.match(/os 6/ig)) {
                        main.addClass('hidden');
                    }
                }*/
                if (!iOSDevice) {
                    setPopupPos(popup, popupDialog, popupContent, 0);
                }
            }).on('hide.bs.modal', function () {
                main.removeClass('hidden');
                header.removeClass('openedForm hidden');
                win.trigger('scroll.setHeaderPosition');
            }).on('hidden.bs.modal', function () {
                form.each(function () {
                    resetForm($(this));
                });
                body.removeClass('reset');
            });

            win.on('resize.setPopupPos' + Math.random(), function () {
                if (popup.is(':visible') && !iOSDevice) {
                    setPopupPos(popup, popupDialog, popupContent, 0);
                }
            });
        });
        return this;
    };

    /* =============== */
    /* MODULE DATA-API */
    /* =============== */

    $(function () {
        var opts = {};
        App.modal = new Modal(opts);
    });

}(window.jQuery, window.App));

/* ============
 * full-height.js
 * ============ */

(function ($, App) {

    "use strict";

    /* ============== */
    /* MODULE TRIGGER */
    /* ============== */

    var fullheightTrigger = '[data-fullheight]',
            setHeightTrigger = '[data-setheight]',
            win = $(window);

    /* =============== */
    /* MODULE DEFAULTS */
    /* =============== */

    var defaults = {};

    /* ================= */
    /* MODULE DEFINITION */
    /* ================= */

    function SetHeight(opts) {
        this.settings = $.extend({}, defaults, opts);
        return this.init();
    }

    /* ============== */
    /* MODULE METHODS */
    /* ============== */

    SetHeight.prototype.init = function () {
        var that = this,
                heightBlock = $(fullheightTrigger),
                setHeight = $(setHeightTrigger);

        win.bind('resize.setHeight', function () {
            if (win.width() > 992) {
                setTimeout(function () {
                    setHeight.css({height: heightBlock.outerHeight()});
                }, 100);
            } else {
                setHeight.css({height: 'auto'});
            }
        }).trigger('resize.setHeight');

        return this;
    };


    /* =============== */
    /* MODULE DATA-API */
    /* =============== */

    $(function () {
        var opts = {};
        App.setHeight = new SetHeight(opts);
    });

}(window.jQuery, window.App));

/* =========
 * back-to-top.js
 * ========= */

(function ($, App) {

    "use strict";

    /* ============== */
    /* MODULE TRIGGER */
    /* ============== */

    var scrollTopTrigger = '[data-scroll-top]';

    /* =============== */
    /* MODULE DEFAULTS */
    /* =============== */

    var defaults = {
        scrollDuration: 1000
    };

    /* ================= */
    /* MODULE DEFINITION */
    /* ================= */

    function BackToTop(opts) {
        this.settings = $.extend({}, defaults, opts);
        return this.init();
    }

    /* ============== */
    /* MODULE METHODS */
    /* ============== */

    BackToTop.prototype.init = function () {
        var that = this,
                scrollElm = $('html, body');

        $(scrollTopTrigger).on('click.backToTop', function (e) {
            e.preventDefault();
            scrollElm.animate({
                scrollTop: 0
            }, that.settings.scrollDuration);
        });
        return this;
    };

    /* =============== */
    /* MODULE DATA-API */
    /* =============== */

    $(function () {
        var opts = {};
        App.backToTop = new BackToTop(opts);
    });

}(window.jQuery, window.App));

/* =================
 * tagging/app.js
 * ================= */
(function ($, App) {

    "use strict";

    var taggingTrigger = '[data-tagging]';
    var taggingDelayTime = 2000;

    /* TAGGING CLASS DEFINITION
     * ======================== */

    function Tagging() {
    }

    Tagging.prototype = {
        constructor: Tagging,
        tag: function (e) {
            var that = $(this);

            Tagging.prototype.pushData(that.attr('data-tagging'));

            if (that.attr('data-tagging-leave') !== undefined) {
                e.preventDefault();
                setTimeout(function () {
                    window.top.location.href = that.attr('href');
                }, taggingDelayTime);
            }
        },
        pushData: function (strData) {
            if (window.dataLayer) {
                if (typeof strData === 'string') {
                    window.dataLayer.push($.parseJSON(strData.replace(/'/g, '"')));
                } else {
                    window.dataLayer.push(strData);
                }
            }
        }
    };

    /* TAGGING PLUGIN DEFINITION
     * ========================= */

    var old = $.fn.tagging;
    $.fn.tagging = function (option) {
        return this.each(function () {
            var $this = $(this),
                    data = $this.data('tagging');
            if (!data) {
                data = new Tagging(this);
                $this.data('tagging', data);
            }
            if (typeof option === 'string') {
                data[option].call($this);
            }
        });
    };

    $.fn.tagging.Constructor = Tagging;

    /* TAGGING NO CONFLICT
     * =================== */

    $.fn.tagging.noConflict = function () {
        $.fn.tagging = old;
        return this;
    };

    /* TAGGING DATA-API
     * ================ */

    $(function () {
        window.tagging = new Tagging();
        $(document).on('click.tagging', taggingTrigger, window.tagging.tag);
    });

}(window.jQuery, window.App));
