var G5Plus = G5Plus || {};
(function ($) {
	"use strict";
	var $window = $(window),
		$body = $('body'),
		isRTL = $body.hasClass('rtl'),
		deviceAgent = navigator.userAgent.toLowerCase(),
		isMobile = deviceAgent.match(/(iphone|ipod|android|iemobile)/),
		isMobileAlt = deviceAgent.match(/(iphone|ipod|ipad|android|iemobile)/),
		isAppleDevice = deviceAgent.match(/(iphone|ipod|ipad)/),
		isIEMobile = deviceAgent.match(/(iemobile)/);

	G5Plus.common = {
		init: function () {
			this.retinaLogo();
			this.owlCarousel();
			this.counterUp();
			this.count_down();
			this.lightGallery();
			this.canvasSidebar();
			this.adminBarProcess();
			this.registerCarouselTrigger($(document));
			this.registerEqualHeight_All($(document));
			this.registerEqualHeight($(document));
			setTimeout(G5Plus.common.owlCarouselRefresh, 1000);
			setTimeout(G5Plus.common.owlCarouselCenter, 1000);
			this.login_link_event();
			this.portfolioLike();
			this.toggleIconClick();
			this.gridAfterAjax();
			this.moveCateToHeader();
            this.initStickySidebar();
		},
        moveCateToHeader: function () {
			$('.move-cate-to-header').each(function () {
				var grid_category = $('.grid-category', $(this)),
					header_inner = $('.header-above-inner', '.main-header');
				if(grid_category.length > 0) {
					grid_category.clone(true).insertAfter('.logo-header', header_inner);
					$('.grid-dropdown-toggle', header_inner).text('Filter');
                    header_inner.closest('.main-header').addClass('header-have-filter');
				}
            });
        },
        initStickySidebar: function ($wrapper){
            // disabled on mobile screens
            if ( !$.fn.hcSticky) {
                return;
            }

            if (typeof $wrapper === 'undefined') {
                $wrapper = $body;
            }

            var _top = G5Plus.common.getScrollOffset();
            var defaults = {
                top : _top
            };

            $('.gf-sticky',$wrapper).each(function(){
                var $this = $(this);
                if (G5Plus.common.isDesktop()) {
                    if ($this.data('hcSticky')) {
                        $this.hcSticky('reinit');
                    } else {
                        var _top = G5Plus.common.getScrollOffset();
                        var defaults = {
                            top : _top
                        };
                        var config = $.extend({}, defaults, $this.data("sticky-options"));
                        $this.hcSticky(config);
                    }
                }
            });
        },
        getScrollOffset: function () {
            var scroll_offset = 0;
            scroll_offset += this.getAdminBarOffset();
            scroll_offset += this.getHeaderStickyOffset();
            return scroll_offset;
        },
        getAdminBarOffset: function () {
            var adminBarOffset = 0,
                $adminBar = $('#wpadminbar');
            if ($adminBar.length > 0 && ($adminBar.css('position') == 'fixed')) {
                adminBarOffset = $adminBar.outerHeight();
            }
            return adminBarOffset;
        },
        getHeaderStickyOffset: function(){
            var headerStickyOffset = 0,
                $header = $('.sticky-region');
            if ($header.length > 0) {
                headerStickyOffset = 80;
            }
            return headerStickyOffset;
        },
		gridAfterAjax: function () {
			$('.grid-plus-inner').off('grid-plus-affter-ajax').on('grid-plus-affter-ajax', function () {
				G5Plus.blog.processQuote();
				G5Plus.common.portfolioLike();
                //G5Plus.woocommerce.init();
                // woocommerce
                G5Plus.woocommerce.quickView();
                $(document).on('yith-wcan-ajax-filtered', G5Plus.common.tooltip);
                G5Plus.woocommerce.tooltip();
                G5Plus.woocommerce.addToCart();
                G5Plus.woocommerce.addToWishlist();
                G5Plus.woocommerce.compare();
			});
		},
		portfolioLike: function () {
			var on_handle = false;
			$('.portfolio-like').off('click').on('click', function (event) {
				event.preventDefault();
				if (on_handle == true) return;
				on_handle = true;
				var $this = $(this),
					ico_class = $this.children('i').attr('class'),
					options = $this.data('options'),
					ajax_url = $this.data('ajax-url');
				$this.children('i').attr('class', 'fa fa-spinner fa-spin');
				$.ajax({
					type: 'POST',
					url: ajax_url,
					data: options,
					dataType: 'json',
					success: function (response) {
						$this.children('i').attr('class', ico_class);
						if (response.success) {
							$this.find('.like-count').text(response.data);
							if (options.status === true) {
								$this.find('i').attr('class', 'fa fa-heart-o');
							} else {
								$this.find('i').attr('class', 'fa fa-heart');
							}
							options.status = !options.status;
							$this.data('options', options);
						}
						on_handle = false;
					},
					error: function (XMLHttpRequest, textStatus, errorThrown) {
						$this.children('i').attr('class', ico_class);
						on_handle = false;
					}
				});
			});
		},
		windowResized: function () {
            $body.on('resized.hcSticky',function(event,target){
                if (!G5Plus.common.isDesktop()) {
                    var $this = $(target);
                    if ($this.data('hcSticky')) {
                        $this.hcSticky('destroy');
                    }
                    $this.removeAttr('style');
                }
            });
			this.canvasSidebar();
			this.adminBarProcess();
			setTimeout(G5Plus.common.owlCarouselRefresh, 1000);
			setTimeout(G5Plus.common.owlCarouselCenter, 1000);
		},
		lightGallery: function () {
			$("[data-rel='lightGallery']").each(function () {
				var $this = $(this),
					galleryId = $this.data('gallery-id');
				$this.on('click', function (event) {
					event.preventDefault();
					var _data = [];
					var $index = 0;
					var $current_src = $(this).attr('href');
					var $current_thumb_src = $(this).data('thumb-src');

					if (typeof galleryId != 'undefined') {
						$('[data-gallery-id="' + galleryId + '"]').each(function (index) {
							var src = $(this).attr('href'),
								thumb = $(this).data('thumb-src'),
								subHtml = $(this).attr('title');
							if (src == $current_src && thumb == $current_thumb_src) {
								$index = index;
							}
							if (typeof(subHtml) == 'undefined')
								subHtml = '';
							_data.push({
								'src': src,
								'downloadUrl': src,
								'thumb': thumb,
								'subHtml': subHtml
							});
						});
						$this.lightGallery({
							hash: false,
							galleryId: galleryId,
							dynamic: true,
							dynamicEl: _data,
							thumbWidth: 80,
							index: $index
						})
					}
				});
			});
			$('a.view-video').on('click', function (event) {
				event.preventDefault();
				var $src = $(this).attr('data-src');
				$(this).lightGallery({
					dynamic: true,
					dynamicEl: [{
						'src': $src,
						'thumb': '',
						'subHtml': ''
					}]
				});
			});
		},
		owlCarousel: function () {
			$('.owl-carousel:not(.manual):not(.owl-loaded)').each(function () {
				var slider = $(this);
				var defaults = {
					items: 4,
					nav: false,
					navText: ['<i class="pe-7s-left-arrow"></i>', '<i class="pe-7s-right-arrow"></i>'],
					dots: false,
					loop: false,
					center: false,
					mouseDrag: true,
					touchDrag: true,
					pullDrag: true,
					freeDrag: false,
					margin: 0,
					stagePadding: 0,
					merge: false,
					mergeFit: true,
					autoWidth: false,
					startPosition: 0,
					rtl: isRTL,
					smartSpeed: 250,
					fluidSpeed: false,
					dragEndSpeed: false,
					autoplayHoverPause: true,
					onResized: G5Plus.common.resizeCarousel,
					onInitialized: G5Plus.common.initializedCarousel,
					onChanged: G5Plus.common.onChangeCarousel
				};
				var config = $.extend({}, defaults, slider.data("plugin-options"));
				// Initialize Slider

				slider.imagesLoaded(function () {
					slider.owlCarousel(config);
				});
				slider.on('changed.owl.carousel', function (e) {
					G5Plus.blog.masonryLayoutRefresh();
				});

			});
		},
		counterUp: function () {
			$('.counter').each(function () {
				var $counter = $(this);
				var defaults = {
					delay: 10,
					time: 800
				};
				var config = $.extend({}, defaults, $counter.data("counter-config"));
				$counter.counterUp(config);
			});
		},
		count_down: function () {
			$('.g5plus-countdown').each(function () {
				var date_end = $(this).data('date-end');
				var show_month = $(this).data('show-month');
				var $this = $(this);
				$this.countdown(date_end, function (event) {
					count_down_callback(event, $this);
				}).on('update.countdown', function (event) {
					count_down_callback(event, $this);
				}).on('finish.countdown', function (event) {
					$('.countdown-seconds', $this).html('00');
					var $url_redirect = $this.attr('data-url-redirect');
					if (typeof $url_redirect != 'undefined' && $url_redirect != '') {
						window.location.href = $url_redirect;
					}
				});
			});

			function count_down_callback(event, $this) {
				var seconds = parseInt(event.offset.seconds);
				var minutes = parseInt(event.offset.minutes);
				var hours = parseInt(event.offset.hours);
				var days = parseInt(event.offset.totalDays);
				var show_month = $this.data('show-month');
				var months = 0;

				if (show_month == 'show') {
					if (days >= 30) {
						months = parseFloat(parseInt(days / 30));
						var days_tem = days % 30;
						days = days_tem;
					}
				}

				if (months == 0) {
					$('.countdown-section.months', $this).remove();
				}

				if ((seconds == 0) && (minutes == 0) && (hours == 0) && (days == 0) && (months == 0)) {
					var $url_redirect = $this.attr('data-url-redirect');
					if (typeof $url_redirect != 'undefined' && $url_redirect != '') {
						window.location.href = $url_redirect;
					}
					return;
				}
				if (months < 10) months = '0' + months;
				if (days < 10) days = '0' + days;
				if (hours < 10) hours = '0' + hours;
				if (minutes < 10) minutes = '0' + minutes;
				if (seconds < 10) seconds = '0' + seconds;

				$('.countdown-month', $this).text(months);
				$('.countdown-day', $this).text(days);
				$('.countdown-hours', $this).text(hours);
				$('.countdown-minutes', $this).text(minutes);
				$('.countdown-seconds', $this).text(seconds);
			}
		},
		owlCarouselRefresh: function () {
			$('.owl-carousel.owl-loaded').each(function () {
				var $this = $(this),
					$slider = $this.data('owl.carousel');
				if (typeof ($slider) != 'undefined') {
					if ($slider.options.autoHeight) {
						var maxHeight = 0;
						$('.owl-item.active', $this).each(function () {
							if ($(this).outerHeight() > maxHeight) {
								maxHeight = $(this).outerHeight();
							}
						});

						$('.owl-height', $this).css('height', maxHeight + 'px');
					}
				}
			});
		},
		owlCarouselCenter: function () {
			$('.product-listing > .owl-nav-center').each(function () {
				var $this = $(this);
				$this.imagesLoaded({background: true}, function () {
					var top = $('img', $this).height() / 2;
					if (window.matchMedia('(min-width: 1350px)').matches) {
						$('.owl-nav > div', $this).css('top', top + 'px');
					} else {
						$('.owl-nav > div', $this).css('top', '');
					}
				});
			});
		},
		initializedCarousel: function (event) {
			$(event.target).trigger("initCarouselCompleted");
			$(event.target).trigger('owl.carousel.initialized');
			G5Plus.common.registerEqualHeight_All('.g5plus-products-slider-single');
		},
		resizeCarousel: function (event) {
			$(event.target).trigger("onResizedCompleted");
		},
		onChangeCarousel: function (event) {
			$(event.target).trigger("onChangedCarousel");
		},
		canvasSidebar: function () {
			var canvas_sidebar_mobile = $('.sidebar-mobile-canvas');
			var changed_class = 'changed';
			if (canvas_sidebar_mobile.length > 0) {
				if (!$('body').find('#wrapper').next().hasClass('overlay-canvas-sidebar')) {
					$('#wrapper').after('<div class="overlay-canvas-sidebar"></div>');
				}
				if (!G5Plus.common.isDesktop()) {
					canvas_sidebar_mobile.css('height', $(window).height() + 'px');
					canvas_sidebar_mobile.css('overflow-y', 'auto');
					if ($.isFunction($.fn.perfectScrollbar)) {
						canvas_sidebar_mobile.perfectScrollbar({
							wheelSpeed: 0.5,
							suppressScrollX: true
						});
					}
				} else {
					canvas_sidebar_mobile.css('overflow-y', 'hidden');
					canvas_sidebar_mobile.css('height', 'auto');
					canvas_sidebar_mobile.scrollTop(0);
					if ($.isFunction($.fn.perfectScrollbar) && canvas_sidebar_mobile.hasClass('ps-active-y')) {
						canvas_sidebar_mobile.perfectScrollbar('destroy');
					}
					canvas_sidebar_mobile.removeAttr('style');
					$('.overlay-canvas-sidebar').removeClass(changed_class);
					$('.sidebar-mobile-canvas', '#wrapper').removeClass(changed_class);
					$('.sidebar-mobile-canvas-icon', '#wrapper').removeClass(changed_class);

				}
				$('.sidebar-mobile-canvas-icon').on('click', function () {
					var $canvas_sidebar = $(this).parent().children('.sidebar-mobile-canvas');
					$(this).addClass(changed_class);
					$canvas_sidebar.addClass(changed_class);
					$('.overlay-canvas-sidebar').addClass(changed_class);

				});
				$('.overlay-canvas-sidebar').on('click', function () {
					if ($('.sidebar-mobile-canvas-icon').hasClass(changed_class)) {
						$(this).removeClass(changed_class);
						$('.sidebar-mobile-canvas', '#wrapper').removeClass(changed_class);
						$('.sidebar-mobile-canvas-icon', '#wrapper').removeClass(changed_class);
					}
				});
			}
		},
		isDesktop: function () {
			var responsive_breakpoint = 991;
			var $menu = $('.x-nav-menu');
			if (($menu.length > 0) && (typeof ($menu.attr('responsive-breakpoint')) != "undefined" ) && !isNaN(parseInt($menu.attr('responsive-breakpoint'), 10))) {
				responsive_breakpoint = parseInt($menu.attr('responsive-breakpoint'), 10);
			}
			return window.matchMedia('(min-width: ' + (responsive_breakpoint + 1) + 'px)').matches;
		},
		adminBarProcess: function () {
			if (window.matchMedia('(max-width: 600px)').matches) {
				$('#wpadminbar').css('top', '-46px');
			}
			else {
				$('#wpadminbar').css('top', '');
			}
		},
		retinaLogo: function () {
			if (window.matchMedia('only screen and (min--moz-device-pixel-ratio: 1.5)').matches
				|| window.matchMedia('only screen and (-o-min-device-pixel-ratio: 3/2)').matches
				|| window.matchMedia('only screen and (-webkit-min-device-pixel-ratio: 1.5)').matches
				|| window.matchMedia('only screen and (min-device-pixel-ratio: 1.5)').matches) {
				$('img[data-retina]').each(function () {
					$(this).attr('src', $(this).attr('data-retina'));
				});
			}
		},
		registerEqualHeight_All: function ($container) {
			$('.column-equal-height', $container).each(function () {
				$('> div', this).responsiveEqualHeightGrid();
			});
		},
		registerEqualHeight: function ($container) {
			$('.column-equal-height', $container).each(function () {
				$('> div:not(.owl-carousel)', this).responsiveEqualHeightGrid();
			});
		},
		registerCarouselTrigger: function ($container) {
			$('.column-equal-height > div.owl-carousel', $container).each(function () {
				$(this).on('initCarouselCompleted', function () {
					$('> div', $(this).parent()).responsiveEqualHeightGrid();
				});
				$(this).on('onResizedCompleted', function () {
					$('> div', $(this).parent()).responsiveEqualHeightGrid();
				})
			});
		},
		login_link_event: function () {
			$('.startup-login-link-sign-in, .startup-login-link-sign-up').off('click').click(function (event) {
				event.preventDefault();
				var action_name = 'startup_login';
				if ($(this).hasClass('startup-login-link-sign-up')) {
					action_name = 'startup_sign_up'
				}
				var popupWrapper = '#startup-popup-login-wrapper';
				$('body').addClass('overflow-hidden');
				$("body").append('<div class="processing-title"><i class="fa fa-spinner fa-spin fa-fw"></i></div>');
				$.ajax({
					type: 'POST',
					data: 'action=' + action_name,
					url: g5plus_app_variable.ajax_url,
					success: function (html) {
						$('.processing-title').fadeOut(function () {
							$('.processing-title').remove();
							$('body').removeClass('overflow-hidden');
						});
						if ($(popupWrapper).length) {
							$(popupWrapper).remove();
						}
						$('body').append(html);

						$(popupWrapper).modal();

						$('#startup-popup-login-form').submit(function (event) {
							var input_data = $('#startup-popup-login-form').serialize();
							$('body').addClass('overflow-hidden');
							$("body").append('<div class="processing-title"><i class="fa fa-spinner fa-spin fa-fw"></i></div>');
							jQuery.ajax({
								type: 'POST',
								data: input_data,
								url: g5plus_app_variable.ajax_url,
								success: function (html) {
									$('.processing-title').fadeOut(function () {
										$('.processing-title').remove();
										$('body').removeClass('overflow-hidden');
									});
									var response_data = jQuery.parseJSON(html);
									if (response_data.code < 0) {
										jQuery('.login-message', '#startup-popup-login-form').html(response_data.message);
									}
									else {
										window.location.reload();
									}
								},
								error: function (html) {
									$('.processing-title').fadeOut(function () {
										$('.processing-title').remove();
										$('body').removeClass('overflow-hidden');
									});
								}
							});
							event.preventDefault();
							return false;
						});
					},
					error: function (html) {
						$('.loading-wrapper').fadeOut(function () {
							$('.loading-wrapper').remove();
							$('body').removeClass('overflow-hidden');
						});
					}
				});
			});
		},

		toggleIconClick: function () {
			$('.toggle-icon-wrapper').on('click', function () {
				$(this).toggleClass('in');
				$(this).trigger('toggle-icon-clicked');
			});
		}
	};

	G5Plus.page = {
		init: function () {
			this.parallax();
			this.parallaxDisable();
			this.pageTitle();
			this.footerParallax();
			this.footerWidgetCollapse();
			this.pageTransition();
			this.backToTop();
			this.events();
		},
		events: function () {
			$(document).on('vc-full-width-row', function (event, $elements) {
				G5Plus.page.fixFullWidthRow();
			});
		},
		windowLoad: function () {
			this.fadePageIn();
		},
		windowResized: function () {
			this.parallaxDisable();
			this.pageTitle();
			this.footerParallax();
			this.footerWidgetCollapse();
			this.wpb_image_grid();
		},
		parallax: function () {
			$.stellar({
				horizontalScrolling: false,
				scrollProperty: 'scroll',
				positionProperty: 'position',
				responsive: false
			});
		},
		parallaxDisable: function () {
			if (G5Plus.common.isDesktop()) {
				$('.parallax').removeClass('parallax-disabled');
			} else {
				$('.parallax').addClass('parallax-disabled');
			}
		},
		pageTitle: function () {
			var $this = $('.page-title-layout-normal'),
				$container = $('.container', $this),
				$pageTitle = $('h1', $this),
				$breadcrumbs = $('.breadcrumbs', $this);
			$this.removeClass('left');
			if (($pageTitle.width() + $breadcrumbs.width()) > $container.width()) {
				$this.addClass('left');
			}
		},
		footerParallax: function () {
			if (window.matchMedia('(max-width: 767px)').matches) {
				$body.css('margin-bottom', '');
			}
			else {
				setTimeout(function () {
					var $footer = $('footer.main-footer-wrapper');
					if ($footer.hasClass('enable-parallax')) {
						var headerSticky = $('header.main-header .sticky-wrapper').length > 0 ? 55 : 0,
							$adminBar = $('#wpadminbar'),
							$adminBarHeight = $adminBar.length > 0 ? $adminBar.outerHeight() : 0;
						if (($window.height() >= ($footer.outerHeight() + headerSticky + $adminBarHeight))) {
							$body.css('margin-bottom', ($footer.outerHeight()) + 'px');
							$footer.removeClass('static');
						} else {
							$body.css('margin-bottom', '');
							$footer.addClass('static');
						}
					}
				}, 100);
			}

		},
		footerWidgetCollapse: function () {
			if (window.matchMedia('(max-width: 767px)').matches) {
				$('footer.footer-collapse-able aside.widget').each(function () {
					var $title = $('h4.widget-title', this);
					if ($title.length === 0) {
						$title = $('.widget_block .wp-block-group__inner-container > h2');
					}

					if ($title.length === 0) {
						$title = $('.widgettitle');
					}

					var $content = $title.next();
					$title.addClass('title-collapse');
					if ($content.length > 0) {
						$content.hide();
					}
					$title.off();
					$title.on('click', function () {
						var $content = $(this).next();

						if ($(this).hasClass('title-expanded')) {
							$(this).removeClass('title-expanded');
							$title.addClass('title-collapse');
							$content.slideUp();
						}
						else {
							$(this).addClass('title-expanded');
							$title.removeClass('title-collapse');
							$content.slideDown();
						}

					});

				});
			} else {
				$('footer aside.widget').each(function () {
					var $title = $('h4.widget-title', this);
					if ($title.length === 0) {
						$title = $('.widget_block .wp-block-group__inner-container > h2');
					}
					if ($title.length === 0) {
						$title = $('.widgettitle');
					}
					$title.off();
					var $content = $title.next();
					$title.removeClass('collapse');
					$title.removeClass('expanded');
					$content.show();
				});
			}
		},
		fullWidthRow: function () {
			$('[data-vc-full-width="true"]').each(function () {
				var $this = $(this),
					$wrapper = $('#wrapper');
				$this.addClass("vc_hidden");
				$this.attr('style', '');
				if (!$body.hasClass('has-sidebar')) {
					var $el_full = $this.next(".vc_row-full-width");
					$el_full.length || ($el_full = $this.parent().next(".vc_row-full-width"));
					var el_margin_left = parseInt($this.css("margin-left"), 10),
						el_margin_right = parseInt($this.css("margin-right"), 10),
						offset = $wrapper.offset().left - $el_full.offset().left - el_margin_left,
						width = $wrapper.width();
					$this.css({
						position: "relative",
						left: offset,
						"box-sizing": "border-box",
						width: $wrapper.width()
					});

					if (!$this.data("vcStretchContent")) {
						var padding = -1 * offset;
						if (padding < 0) {
							padding = 0;
						}
						var paddingRight = width - padding - $el_full.width() + el_margin_left + el_margin_right;
						if (paddingRight < 0) {
							paddingRight = 0;
						}
						$this.css({
							"padding-left": padding + "px",
							"padding-right": paddingRight + "px"
						});
					}
				}
				$this.removeClass("vc_hidden");
			});
		},
		fullWidthRowRTL: function () {
            $('[data-vc-full-width="true"]').each(function () {
                var offset = $(this).css('left');
                $(this).css({
                    left: '',
                    right: offset
                });
            });
		},
		wpb_image_grid: function () {
			$(".wpb_gallery_slides.wpb_image_grid .wpb_image_grid_ul").each(function (index) {
				var $imagesGrid = $(this);
				setTimeout(function () {
					$imagesGrid.isotope('layout');
				}, 1000);
			});
		},
		pageTransition: function () {
			if ($body.hasClass('page-transitions')) {
				var linkElement = '.animsition-link, a[href]:not([target="_blank"]):not([href^="#"]):not([href*="javascript"]):not([href*=".jpg"]):not([href*=".jpeg"]):not([href*=".gif"]):not([href*=".png"]):not([href*=".mov"]):not([href*=".swf"]):not([href*=".mp4"]):not([href*=".flv"]):not([href*=".avi"]):not([href*=".mp3"]):not([href^="mailto:"]):not([class*="no-animation"]):not([class*="prettyPhoto"]):not([class*="add_to_wishlist"]):not([class*="add_to_cart_button"]):not([class*="compare"])';
				$(linkElement).on('click', function (event) {
					if ($(event.target).closest($('b.x-caret', this)).length > 0) {
						event.preventDefault();
						return;
					}
					event.preventDefault();
					var $self = $(this);
					var url = $self.attr('href');

					// middle mouse button issue #24
					// if(middle mouse button || command key || shift key || win control key)
					if (event.which === 2 || event.metaKey || event.shiftKey || navigator.platform.toUpperCase().indexOf('WIN') !== -1 && event.ctrlKey) {
						window.open(url, '_blank');
					} else {
						G5Plus.page.fadePageOut(url);
					}

				});
			}
		},
		fadePageIn: function () {
			if ($body.hasClass('page-loading')) {
				var preloadTime = 1000,
					$loading = $('.site-loading');
				$loading.css('opacity', '0');
				setTimeout(function () {
					$loading.css('display', 'none');
				}, preloadTime);
			}
		},
		fadePageOut: function (link) {

			$('.site-loading').css('display', 'block').animate({
				opacity: 1,
				delay: 200
			}, 600, "linear");

			$('html,body').animate({scrollTop: '0px'}, 800);

			setTimeout(function () {
				window.location = link;
			}, 600);
		},
		backToTop: function () {
			var $backToTop = $('.back-to-top');
			if ($backToTop.length > 0) {
				$backToTop.on('click', function (event) {
					event.preventDefault();
					$('html,body').animate({scrollTop: '0px'}, 800);
				});
				$window.on('scroll', function (event) {
					var scrollPosition = $window.scrollTop();
					var windowHeight = $window.height() / 2;
					if (scrollPosition > windowHeight) {
						$backToTop.addClass('in');
					}
					else {
						$backToTop.removeClass('in');
					}
				});
			}
		},
		fixFullWidthRow: function () {
			if ($body.hasClass('boxed') || $body.hasClass('header-is-left')||$body.hasClass('one-page')) {
				G5Plus.page.fullWidthRow();
			}
			if (isRTL) {
				G5Plus.page.fullWidthRowRTL();
			}
			$('.owl-carousel.owl-loaded', $('[data-vc-full-width="true"]')).each(function () {
				$(this).data('owl.carousel').onResize();
			});
		}
	};

	G5Plus.blog = {
		init: function () {
			this.masonryLayout();
			setTimeout(this.masonryLayout, 300);
			this.loadMore();
			this.processQuote();
			this.infiniteScroll();
			this.commentReplyTitle();
			this.singleMetaTags();

		},
		windowResized: function () {
			G5Plus.blog.masonryLayoutRefresh();
			this.singleMetaTags();
			this.processQuote();
		},
		loadMore: function () {
			$('.paging-navigation').on('click', '.blog-load-more', function (event) {
				event.preventDefault();
				var $this = $(this).button('loading'),
					link = $(this).attr('data-href'),
					contentWrapper = '.blog-wrap',
					element = '.blog-wrap article';

				$.get(link, function (data) {
					var next_href = $('.blog-load-more', data).attr('data-href'),
						$newElems = $(element, data).css({
							opacity: 0
						});
					$(contentWrapper).append($newElems);
					$newElems.imagesLoaded({background: true}, function () {
						G5Plus.common.registerCarouselTrigger();
						G5Plus.common.owlCarousel();
						G5Plus.common.lightGallery();
						G5Plus.blog.processQuote();
						$newElems.animate({
							opacity: 1
						});
						G5Plus.common.registerEqualHeight_All();
						if ($('.archive-wrap').hasClass('archive-masonry')) {
							$(contentWrapper).isotope('appended', $newElems);
							setTimeout(function () {
								$(contentWrapper).isotope('layout');
							}, 400);
						}
					});

					if (typeof(next_href) == 'undefined') {
						$this.parent().remove();
					} else {
						$this.button('reset');
						$this.attr('data-href', next_href);
					}
				});
			});

		},
		infiniteScroll: function () {
			var $container = $('.blog-wrap');
			$container.infinitescroll({
				navSelector: '#infinite_scroll_button',    // selector for the paged navigation
				nextSelector: '#infinite_scroll_button a',  // selector for the NEXT link (to page 2)
				itemSelector: '.blog-wrap article',     // selector for all items you'll retrieve
				animate: true,
				loading: {
					finishedMsg: 'No more pages to load.',
					selector: '#infinite_scroll_loading',
					img: g5plus_app_variable.theme_url + 'assets/images/ajax-loader.gif',
					msgText: 'Loading...'
				}
			}, function (newElements) {
				var $newElems = $(newElements).css({
					opacity: 0
				});

				$newElems.imagesLoaded({background: true}, function () {
					G5Plus.common.registerCarouselTrigger();
					G5Plus.common.owlCarousel();
					G5Plus.common.lightGallery();
					G5Plus.blog.processQuote();
					$newElems.animate({
						opacity: 1
					});
					G5Plus.common.registerEqualHeight_All();
					if ($('.archive-wrap').hasClass('archive-masonry')) {
						$container.isotope('appended', $newElems);
						setTimeout(function () {
							$container.isotope('layout');
						}, 400);
					}
				});
			});

		},
		masonryLayout: function () {
			var $container = $('.archive-masonry .blog-wrap');
			$container.imagesLoaded({background: true}, function () {
				$container.isotope({
					itemSelector: 'article',
					layoutMode: "masonry",
					isOriginLeft: !isRTL
				});
				setTimeout(function () {
					$container.isotope('layout');
				}, 500);
			});

		},
		commentReplyTitle: function () {
			var $replyTitle = $('h3#reply-title');
			$replyTitle.addClass('block-title mg-top-100');
			var $smallTag = $('small', $replyTitle);
			$smallTag.remove();
			$replyTitle.html($replyTitle.text());
			$replyTitle.append($smallTag);
		},
		masonryLayoutRefresh: function () {
			var $container = $('.archive-masonry .blog-wrap');
			setTimeout(function () {
				$container.isotope('layout');
			}, 500);
		},
		singleMetaTags: function () {
			var $container = $('.entry-meta-tag-wrap'),
				$tags = $('.entry-meta-tag', $container),
				$social = $('.social-share', $container);
			$container.removeClass('left');
			if (($tags.outerWidth() + $social.outerWidth()) > $container.outerWidth()) {
				$container.addClass('left');
			}
		},
		processQuote: function () {
			$('.format-quote,.format-link').each(function () {
				var $wrap = $('.entry-thumb-wrap', $(this)),
					$container = $('.entry-quote-content', $(this)),
					$content = $('.block-center-inner', $(this));
				$wrap.removeClass('quote');
				if ($content.height() > $container.height()) {
					$wrap.addClass('quote');
				}
			});
		}

	};

	G5Plus.header = {
		timeOutSearch: null,
		xhrSearchAjax: null,
		init: function () {
			this.anchoPreventDefault();
			this.topDrawerToggle();
			this.switchMenu();
			this.sticky();
			this.menuCategories();
			this.searchProduct();
			this.searchButton();
			this.closeButton();
			this.searchAjaxButtonClick();
			this.closestElement();
			this.menuMobileToggle();
			$('[data-search="ajax"]').each(function () {
				G5Plus.header.searchAjax($(this));
			});

			this.escKeyPress();
			this.mobileNavOverlay();
			this.menuOnePage();
			this.canvasMenu();
			this.headerLeftScrollBar();
			this.headerLeftHeight();
			this.canvasMenuScrollBar();
			this.canvasMenuHeight();
		},
		windowsScroll: function () {
			this.sticky();
			this.menuDropFlyPosition();
		},
		windowResized: function () {
			this.sticky();
			this.menuDropFlyPosition();
			this.headerLeftHeight();
			this.canvasMenuHeight();
			this.page404();
		},
		windowLoad: function () {
			this.page404();
		},
		topDrawerToggle: function () {
			$('.top-drawer-toggle').on('click', function () {
				$('.top-drawer-inner').slideToggle();
				$('.top-drawer-wrapper').toggleClass('in');
			});
		},
		switchMenu: function () {
			$('header .menu-switch').on('click', function () {
				$('.header-nav-inner').toggleClass('in');
			});
		},
		menuCategories: function () {
			$('.menu-categories-select > i').on('click', function () {
				$('.menu-categories').toggleClass('in');
			});
		},
		sticky: function () {
			$('.sticky-wrapper').each(function () {
				var $this = $(this);
				var stickyHeight = 60;
				if (G5Plus.common.isDesktop()) {
					stickyHeight = 55;
				}
				if ($(document).outerHeight() - $this.outerHeight() - $this.offset().top <= $window.outerHeight() - stickyHeight) {
					$this.removeClass('is-sticky');
					$('.sticky-region', $this).css('top', '');
					return;
				}
				var adminBarHeight = 0;
				if ($('#wpadminbar').length && ($('#wpadminbar').css('position') == 'fixed')) {
					adminBarHeight = $('#wpadminbar').outerHeight();
				}
				if ($(window).scrollTop() > $this.offset().top - adminBarHeight) {
					$this.addClass('is-sticky');
					$('.sticky-region', $this).css('top', adminBarHeight + 'px');
				}
				else {
					$this.removeClass('is-sticky');
					$('.sticky-region', $this).css('top', '');
				}
			});
		},

		searchProduct: function () {
			$('.search-product-wrapper .categories').each(function () {
				var $this = $(this);
				$('> span', $this).on('click', function () {
					$('.search-product-wrapper .search-category-dropdown').slideToggle();
					$(this).toggleClass('in');
					$('.search-product-wrapper .search-ajax-result').html('');
					$('.search-product-wrapper input[type="text"]').val('');
				});
				$('.search-category-dropdown span', $this).on('click', function () {
					$('> span', $this).html($(this).html());
					$('> span', $this).attr('data-id', $(this).attr('data-id'));
					$('.search-product-wrapper .search-category-dropdown').slideToggle();
					$('> span', $this).toggleClass('in');
				});
			});
		},

		searchButton: function () {
			var $itemSearch = $('.header-customize-item.item-search > a, .mobile-search-button > a');
			if (!$itemSearch.length) {
				return;
			}
			var $searchPopup = $('#search_popup_wrapper');
			if (!$searchPopup.length) {
				return;
			}
			if ($itemSearch.hasClass('search-ajax')) {
				$itemSearch.on('click', function () {
					$window.scrollTop(0);
					$searchPopup.addClass('in');
					$('body').addClass('overflow-hidden');
					var $input = $('input[type="text"]', $searchPopup);
					$input.focus();
					$input.val('');

					var $result = $('.search-ajax-result', $searchPopup);
					$result.html('');
				});
			}
			else {
				var dlgSearch = new DialogFx($searchPopup[0]);
				$itemSearch.on('click', dlgSearch.toggle.bind(dlgSearch));
				$itemSearch.on('click', function () {
					var $input = $('input[type="text"]', $searchPopup);

					$input.focus();
					$input.val('');
				});
			}
		},
		searchAjax: function ($wrapper) {
			$('input[type="text"]', $wrapper).on('keyup', function (event) {
				if (event.altKey || event.ctrlKey || event.shiftKey || event.metaKey) {
					return;
				}
				var keys = ["Control", "Alt", "Shift"];
				if (keys.indexOf(event.key) != -1) return;
				switch (event.which) {
					case 27:	// ESC
						$('.search-ajax-result', $wrapper).html('');
						$wrapper.removeClass('in');
						$(this).val('');
						break;
					case 38:	// UP
						G5Plus.header.searchAjaxKeyUp($wrapper);
						event.preventDefault();
						break;
					case 40:	// DOWN
						G5Plus.header.searchAjaxKeyDown($wrapper);
						event.preventDefault();
						break;
					case 13:
						G5Plus.header.searchAjaxKeyEnter($wrapper);
						break;
					default:
						clearTimeout(G5Plus.header.timeOutSearch);
						G5Plus.header.timeOutSearch = setTimeout(G5Plus.header.searchAjaxSearchProcess, 500, $wrapper, false);
						break;
				}
			});
		},
		searchAjaxKeyUp: function ($wrapper) {
			var $item = $('.search-ajax-result li.selected', $wrapper);
			if ($('.search-ajax-result li', $wrapper).length < 2) return;
			var $prev = $item.prev();
			$item.removeClass('selected');
			if ($prev.length) {
				$prev.addClass('selected');
			}
			else {
				$('.search-ajax-result li:last', $wrapper).addClass('selected');
				$prev = $('.search-ajax-result li:last', $wrapper);
			}
			if ($prev.position().top < $('.ajax-search-result', $wrapper).scrollTop()) {
				$('.ajax-search-result', $wrapper).scrollTop($prev.position().top);
			}
			else if ($prev.position().top + $prev.outerHeight() > $('.ajax-search-result', $wrapper).scrollTop() + $('.ajax-search-result', $wrapper).height()) {
				$('.ajax-search-result', $wrapper).scrollTop($prev.position().top - $('.ajax-search-result', $wrapper).height() + $prev.outerHeight());
			}
		},
		searchAjaxKeyDown: function ($wrapper) {
			var $item = $('.search-ajax-result li.selected', $wrapper);
			if ($('.search-ajax-result li', $wrapper).length < 2) return;
			var $next = $item.next();
			$item.removeClass('selected');
			if ($next.length) {
				$next.addClass('selected');
			}
			else {
				$('.search-ajax-result li:first', $wrapper).addClass('selected');
				$next = $('.search-ajax-result li:first', $wrapper);
			}
			if ($next.position().top < $('.search-ajax-result', $wrapper).scrollTop()) {
				$('.search-ajax-result', $wrapper).scrollTop($next.position().top);
			}
			else if ($next.position().top + $next.outerHeight() > $('.search-ajax-result', $wrapper).scrollTop() + $('.search-ajax-result', $wrapper).height()) {
				$('.search-ajax-result', $wrapper).scrollTop($next.position().top - $('.search-ajax-result', $wrapper).height() + $next.outerHeight());
			}
		},
		searchAjaxKeyEnter: function ($wrapper) {
			var $item = $('.search-ajax-result li.selected a', $wrapper);
			if ($item.length > 0) {
				window.location = $item.attr('href');
			}
		},
		searchAjaxSearchProcess: function ($wrapper, isButtonClick) {
			var keyword = $('input[type="text"]', $wrapper).val();
			if (!isButtonClick && keyword.length < 3) {
				$('.search-ajax-result', $wrapper).html('');
				return;
			}
			$('.search-button i', $wrapper).addClass('fa-spinner fa-spin');
			$('.search-button i', $wrapper).removeClass('fa-search');
			if (G5Plus.header.xhrSearchAjax) {
				G5Plus.header.xhrSearchAjax.abort();
			}
			var action = $wrapper.attr('data-ajax-action');
			var data = 'action=' + action + '&keyword=' + keyword;
			if ($('.categories > span[data-id]', $wrapper)) {
				data += '&cate_id=' + $('.categories > span[data-id]', $wrapper).attr('data-id');
			}

			G5Plus.header.xhrSearchAjax = $.ajax({
				type: 'POST',
				data: data,
				url: g5plus_app_variable.ajax_url,
				success: function (data) {
					$('.search-button i', $wrapper).removeClass('fa-spinner fa-spin');
					$('.search-button i', $wrapper).addClass('fa-search');
					$wrapper.addClass('in');
					$('.search-ajax-result', $wrapper).html(data);
				},
				error: function (data) {
					if (data && (data.statusText == 'abort')) {
						return;
					}
					$('.search-button i', $wrapper).removeClass('fa-spinner fa-spin');
					$('.search-button i', $wrapper).addClass('fa-search');
				}
			});
		},
		searchAjaxButtonClick: function () {
			$('.search-button').on('click', function () {
				var $wrapper = $($(this).attr('data-search-wrapper'));
				G5Plus.header.searchAjaxSearchProcess($wrapper, true);
			});
		},
		menuMobileToggle: function () {
			$('.toggle-mobile-menu').on('toggle-icon-clicked', function (event) {
				var $this = $(event.target);
				var dropType = $this.attr('data-drop-type');
				if (dropType == 'menu-drop-fly') {
					$('body').toggleClass('mobile-nav-in');
				}
				else {
					$('.header-mobile-nav').slideToggle();
				}
			});
		},
		escKeyPress: function () {
			$(document).on('keyup', function (event) {
				if (event.altKey || event.ctrlKey || event.shiftKey || event.metaKey) {
					return;
				}
				var keys = ["Control", "Alt", "Shift"];
				if (keys.indexOf(event.key) != -1) return;
				if (event.which == 27) {
					if ($('#search_popup_wrapper').hasClass('in')) {
						$('#search_popup_wrapper').removeClass('in');
						setTimeout(function () {
							$('body').removeClass('overflow-hidden');
						}, 500);

					}

				}
			});
		},
		anchoPreventDefault: function () {
			$('.prevent-default').on('click', function (event) {
				event.preventDefault();
			});
		},
		closeButton: function () {
			$('.close-button').on('click', function () {
				var $closeButton = $(this);
				var ref = $closeButton.attr('data-ref');
				if ($('#search_popup_wrapper').hasClass('in')) {
					setTimeout(function () {
						$('body').removeClass('overflow-hidden');
					}, 500);
				}
				$(ref).removeClass('in');
			});

		},
		closestElement: function () {
			$($window).on('click', function (event) {
				if ($(event.target).closest('.search-product-wrapper .categories').length == 0) {
					$('.search-product-wrapper .search-category-dropdown').slideUp();
					$('.search-product-wrapper .categories > span').removeClass('in');
				}

				if ($(event.target).closest('.search-product-wrapper').length == 0) {
					$('.search-ajax-result').html('');
					$('.search-product-wrapper').removeClass('in');
					$('input[type="text"]', '.search-product-wrapper').val('');
				}
			});
		},
		mobileNavOverlay: function () {
			$('.mobile-nav-overlay').on('click', function () {
				$('body').removeClass('mobile-nav-in');
				$('.toggle-mobile-menu').removeClass('in');
			})
		},
		menuDropFlyPosition: function () {
			var adminBarHeight = 0;
			if ($('#wpadminbar').length && ($('#wpadminbar').css('position') == 'fixed')) {
				adminBarHeight = $('#wpadminbar').outerHeight();
			}
			$('.header-mobile-nav.menu-drop-fly').css('top', adminBarHeight + 'px');
		},
		menuOnePage: function () {
			$('.menu-one-page').onePageNav({
				currentClass: 'menu-current',
				changeHash: false,
				scrollSpeed: 750,
				scrollThreshold: 0,
				filter: '',
				easing: 'swing'
			});
		},
		canvasMenu: function () {
			//Menu
			$(document).on('click', function (event) {
				if (($(event.target).closest('nav.canvas-menu-wrapper').length == 0)
					&& ($(event.target).closest('.menu-switch')).length == 0) {
					$('nav.canvas-menu-wrapper').removeClass('in');
				}
			});

			$('.menu-switch').on('click', function (event) {
				event.preventDefault();
				$('nav.canvas-menu-wrapper').toggleClass('in');
			});
			$('.canvas-menu-close').on('click', function (event) {
				event.preventDefault();
				$('nav.canvas-menu-wrapper').removeClass('in');
			});

			// Sidebar
			$('nav.canvas-sidebar-wrapper').perfectScrollbar({
				wheelSpeed: 0.5,
				suppressScrollX: true
			});

			$(document).on('click', function (event) {
				if (($(event.target).closest('nav.canvas-sidebar-wrapper').length == 0)
					&& ($(event.target).closest('.canvas-sidebar-toggle')).length == 0) {
					$('nav.canvas-sidebar-wrapper').removeClass('in');
				}
			});

			$('.canvas-sidebar-toggle').on('click', function (event) {
				event.preventDefault();
				$('nav.canvas-sidebar-wrapper').toggleClass('in');
			});
			$('.canvas-sidebar-close').on('click', function (event) {
				event.preventDefault();
				$('nav.canvas-sidebar-wrapper').removeClass('in');
			});
		},
		headerLeftScrollBar: function () {
			$('header.header-left .primary-menu').perfectScrollbar({
				wheelSpeed: 0.5,
				suppressScrollX: true
			});
		},
		headerLeftHeight: function () {
			var $headerLeft = $('header.header-left');
			if ($headerLeft.length > 0) {
				var _navWrapHeight = $headerLeft.height() - $headerLeft.find('.header-above-wrapper').height();
				$headerLeft.find('.header-nav-wrapper').css('height', _navWrapHeight);

				var _height = $headerLeft.find('.header-nav-wrapper').height() - $headerLeft.find('.header-customize-nav').outerHeight();
				$headerLeft.find('.primary-menu').css('height', _height);
			}
		},
		canvasMenuScrollBar: function () {
			$('.canvas-menu-wrapper .primary-menu').perfectScrollbar({
				wheelSpeed: 0.5,
				suppressScrollX: true
			});
		},
		canvasMenuHeight: function () {
			var $canvasMenu = $('nav.canvas-menu-wrapper');
			if ($canvasMenu.length > 0) {
				var _navWrapHeight = $canvasMenu.height() - $canvasMenu.find('.header-above-wrapper').height();
				$canvasMenu.find('.header-nav-wrapper').css('height', _navWrapHeight);

				var _height = $canvasMenu.find('.header-nav-wrapper').height() - $canvasMenu.find('.header-customize-nav').outerHeight();
				$canvasMenu.find('.primary-menu').css('height', _height);
			}
		},
		page404: function () {
			if (!$body.hasClass('error404')) return;
			var windowHeight = $window.outerHeight();
			var page404Height = 0;
			var $header = null;
			if (G5Plus.common.isDesktop()) {
				$header = $('header.main-header');
			}
			else {
				$header = $('header.header-mobile');
			}
			if ($header.length == 0) return;
			page404Height = windowHeight - $header.offset().top - $header.outerHeight() - $('body.error404 .page404-inner').outerHeight();
			if (page404Height < 200) {
				page404Height = 200;
			}
			page404Height /= 2;
			$('body.error404 .page404').css('padding', page404Height + 'px 0');
		}
	};

	G5Plus.menu = {
		init: function () {
			this.processMobileMenu();
			this.mobileMenuItemClick();
		},
		processMobileMenu: function () {
			$('.nav-menu-mobile:not(.x-nav-menu) li > a').each(function () {
				var $this = $(this);
				var html = '<span>' + $this.html() + '</span>';
				if ($('> ul', $this.parent()).length) {
					html += '<b class="menu-caret"></b>';
				}
				$this.html(html);
			});
		},
		mobileMenuItemClick: function () {
			$('.nav-menu-mobile:not(.x-nav-menu) li').on('click', function () {
				if ($('> ul', this).length == 0) {
					return;
				}
				if ($(event.target).closest($('> ul', this)).length > 0) {
					return;
				}

				if ($(event.target).closest($('> a > span', this)).length > 0) {
					var baseUri = '';
					if ((typeof (event.target) != "undefined") && (event.target != null) && (typeof (event.target.baseURI) != "undefined") && (event.target.baseURI != null)) {
						var arrBaseUri = event.target.baseURI.split('#');
						if (arrBaseUri.length > 0) {
							baseUri = arrBaseUri[0];
						}

						var $aClicked = $('> a', this);
						if ($aClicked.length > 0) {
							var clickUrl = $aClicked.attr('href');
							if (clickUrl != '#') {
								if ((typeof (clickUrl) != "undefined") && (clickUrl != null)) {
									clickUrl = clickUrl.split('#')[0];
								}
								if (baseUri != clickUrl) {
									return;
								}
							}

						}
					}
				}

				event.preventDefault();
				$(this).toggleClass('menu-open');
				$('> ul', this).slideToggle();
			});
		}
	};

	G5Plus.widget = {
		init: function () {
			//this.categoryCaret();
		},
		categoryCaret: function () {
			$('li', '.widget_categories, .widget_pages, .widget_nav_menu, .widget_product_categories, .product-categories').each(function () {
				if ($(' > ul', this).length > 0) {
					$(this).append('<span class="li-caret fa fa-plus"></span>');
				}
			});
			$('.li-caret').on('click', function () {
				$(this).toggleClass('in');
				$(' > ul', $(this).parent()).slideToggle();
			});
		}
	};

	G5Plus.woocommerce = {
		init: function () {
			this.setCartScrollBar();
			this.sale_countdown();
			this.addCartQuantity();
			this.updateShippingMethod();
			this.quickView();
			$(document).on('yith-wcan-ajax-filtered', G5Plus.common.tooltip);
			this.processTitle();
			var $productImageWrap = $('#single-product-image');
			this.singleProductImage($productImageWrap);
			this.tooltip();
			this.addToCart();
			this.addToWishlist();
			this.compare();
			this.ajaxFilter();
		},
		ajaxFilter: function () {
			$(document).on("yith-wcan-ajax-filtered", function () {
				G5Plus.woocommerce.sale_countdown();
			});
		},
		windowResized: function () {
			setTimeout(function () {
				G5Plus.woocommerce.sale_countdown_width();
			}, 500);
			this.setCartScrollBar();
		},
		windowLoad: function () {
			this.setCartScrollBar();
		},
		tooltip: function () {
			if ($().tooltip && !isMobileAlt) {
				if (!$body.hasClass('woocommerce-compare-page')) {
					$('[data-toggle="tooltip"]').tooltip({
							placement: "top"
						}
					);
				}

				$('.yith-wcwl-wishlistexistsbrowse,.yith-wcwl-add-button,.yith-wcwl-wishlistaddedbrowse', '.product-actions').each(function () {
					var title = $('a', $(this)).text().trim();
					$(this).tooltip({
						title: title,
						placement: "top"
					});
				});
				$('.yith-wcwl-wishlistexistsbrowse,.yith-wcwl-add-button,.yith-wcwl-wishlistaddedbrowse', '.g5plus-products-slider-single').each(function () {
					var title = $('a', $(this)).text().trim();
					$(this).tooltip({
						title: title
					});
				});
				$('.yith-wcwl-wishlistexistsbrowse,.yith-wcwl-add-button,.yith-wcwl-wishlistaddedbrowse', '.shop-loop-listing').each(function () {
					var title = $('a', $(this)).text().trim();
					$(this).tooltip({
						title: title,
						placement: "top"
					});
				});

				$('.compare, .product-quick-view', '.product-actions').each(function () {
					var title = $(this).text().trim();
					$(this).tooltip({
						title: title,
						placement: "top"
					});
				});
				$('.compare', '.g5plus-products-slider-single').each(function () {
					var title = $(this).text().trim();
					$(this).tooltip({
						title: title,
						placement: "top"
					});
				});
				$('.compare', '.shop-loop-listing').each(function () {
					var title = $(this).text().trim();
					$(this).tooltip({
						title: title,
						placement: "top"
					});
				});
			}
		},
		sale_countdown: function () {
			$('.product-deal-countdown').each(function () {
				var date_end = $(this).data('date-end');
				var $this = $(this);
				$this.countdown(date_end, function (event) {
					count_down_callback(event, $this);
				}).on('update.countdown', function (event) {
					count_down_callback(event, $this);
				});
			});

			function count_down_callback(event, $this) {
				var seconds = parseInt(event.offset.seconds);
				var minutes = parseInt(event.offset.minutes);
				var hours = parseInt(event.offset.hours);
				var days = parseInt(event.offset.totalDays);

				//if ((seconds == 0)&& (minutes == 0) && (hours == 0) && (days == 0)) {
				//	$this.remove();
				//	return;
				//}

				if (days < 10) days = '0' + days;
				if (hours < 10) hours = '0' + hours;
				if (minutes < 10) minutes = '0' + minutes;
				if (seconds < 10) seconds = '0' + seconds;


				$('.countdown-day', $this).text(days);
				$('.countdown-hours', $this).text(hours);
				$('.countdown-minutes', $this).text(minutes);
				$('.countdown-seconds', $this).text(seconds);
			}

			G5Plus.woocommerce.sale_countdown_width();

		},
		sale_countdown_width: function () {
			$('.product-deal-countdown').each(function () {
				var innerWidth = 0;
				$(this).removeClass('small');
				$('.countdown-section', $(this)).each(function () {
					innerWidth += $(this).outerWidth() + parseInt($(this).css('margin-right').replace("px", ''), 10);
				});
				if (innerWidth > $(this).outerWidth()) {
					$(this).addClass('small');
				}
			});
		},
		addCartQuantity: function () {
			$(document).off('click', '.quantity .btn-number').on('click', '.quantity .btn-number', function (event) {
				event.preventDefault();
				var type = $(this).data('type'),
					input = $('input', $(this).parent()),
					current_value = parseFloat(input.val()),
					max = parseFloat(input.attr('max')),
					min = parseFloat(input.attr('min')),
					step = parseFloat(input.attr('step')),
					stepLength = 0;
				if (input.attr('step').indexOf('.') > 0) {
					stepLength = input.attr('step').split('.')[1].length;
				}

				if (isNaN(max)) {
					max = -1;
				}
				if (isNaN(min)) {
					min = 0;
				}
				if (isNaN(step)) {
					step = 1;
					stepLength = 0;
				}

				if (!isNaN(current_value)) {
					if (type == 'minus') {
						if (current_value > min) {
							current_value = (current_value - step).toFixed(stepLength);
							input.val(current_value).change();
						}

						if (parseFloat(input.val()) <= min) {
							input.val(min).change();
							$(this).attr('disabled', true);
						}
					}

					if (type == 'plus') {
						if ((max === -1) || (current_value < max)) {
							current_value = (current_value + step).toFixed(stepLength);
							input.val(current_value).change();
						}
						if ((max !== -1) && (parseFloat(input.val()) >= max)) {
							input.val(max).change();
							$(this).attr('disabled', true);
						}
					}
				} else {
					input.val(min);
				}
			});


			$('input', '.quantity').on('focusin', function () {
				$(this).data('oldValue', $(this).val());
			});

			$('input', '.quantity').on('change', function () {
				var input = $(this),
					max = parseFloat(input.attr('max')),
					min = parseFloat(input.attr('min')),
					current_value = parseFloat(input.val()),
					step = parseFloat(input.attr('step'));

				if (isNaN(max)) {
					max = -1;
				}
				if (isNaN(min)) {
					min = 0;
				}

				if (isNaN(step)) {
					step = 1;
				}


				var btn_add_to_cart = $('.add_to_cart_button', $(this).parent().parent().parent());
				if (current_value >= min) {
					$(".btn-number[data-type='minus']", $(this).parent()).removeAttr('disabled');
					if (typeof(btn_add_to_cart) != 'undefined') {
						btn_add_to_cart.attr('data-quantity', current_value);
					}

				} else {
					alert(g5plus_framework_constant.add_cart_quantity.add_cart_quantity.min);
					$(this).val($(this).data('oldValue'));

					if (typeof(btn_add_to_cart) != 'undefined') {
						btn_add_to_cart.attr('data-quantity', $(this).data('oldValue'));
					}
				}

				if ((max === -1) || (current_value <= max)) {
					$(".btn-number[data-type='plus']", $(this).parent()).removeAttr('disabled');
					if (typeof(btn_add_to_cart) != 'undefined') {
						btn_add_to_cart.attr('data-quantity', current_value);
					}
				} else {
					alert(g5plus_framework_constant.add_cart_quantity.add_cart_quantity.max);
					$(this).val($(this).data('oldValue'));
					if (typeof(btn_add_to_cart) != 'undefined') {
						btn_add_to_cart.attr('data-quantity', $(this).data('oldValue'));
					}
				}

			});
		},
		singleProductImage: function ($productImageWrap) {
			var $sliderMain = $productImageWrap.find('.single-product-image-main.owl-carousel'),
				$sliderThumb = $productImageWrap.find('.single-product-image-thumb.owl-carousel');

			$sliderMain.owlCarousel({
				items: 1,
				nav: false,
				dots: false,
				loop: false,
				smartSpeed: 250,
				rtl: isRTL
			}).on('changed.owl.carousel', syncPosition);

			$sliderThumb.on('initialized.owl.carousel', function () {
				$sliderThumb.find(".owl-item").eq(0).addClass("current");
			}).owlCarousel({
				items: 4,
				nav: false,
				dots: false,
				rtl: isRTL,
				margin: 10,
				responsive: {}
			}).on('changed.owl.carousel', syncPosition2);

			function syncPosition(el) {
				//if you set loop to false, you have to restore this next line
				var current = el.item.index;

				$sliderThumb
					.find(".owl-item")
					.removeClass("current")
					.eq(current)
					.addClass("current");
				var onscreen = $sliderThumb.find('.owl-item.active').length - 1;
				var start = $sliderThumb.find('.owl-item.active').first().index();
				var end = $sliderThumb.find('.owl-item.active').last().index();

				if (current > end) {
					$sliderThumb.data('owl.carousel').to(current, 100, true);
				}
				if (current < start) {
					$sliderThumb.data('owl.carousel').to(current - onscreen, 100, true);
				}
			}

			function syncPosition2(el) {
				var number = el.item.index;
				$sliderMain.data('owl.carousel').to(number, 100, true);
			}

			$sliderThumb.on("click", ".owl-item", function (e) {
				e.preventDefault();
				if ($(this).hasClass('current')) return;
				var number = $(this).index();
				$sliderMain.data('owl.carousel').to(number, 300, true);
			});

			$(document).on('found_variation',function(event,variation){
				var $product = $(event.target).closest('.product');
				if ((typeof variation !== 'undefined') && (typeof variation.variation_id !== 'undefined')) {

					var variation_id = variation.variation_id;
					var index = parseInt($('a[data-variation_id*="|'+variation_id+'|"]',$sliderMain).data('index'),10) ;
					if (!isNaN(index) ) {
						$sliderMain.data('owl.carousel').to(index, 300, true);
					}
				}
			});

			$(document).on('reset_data',function(event){
				$sliderMain.data('owl.carousel').to(0, 300, true);
			});
		},
		addToCart: function () {
			$(document).on('click', '.add_to_cart_button', function () {
				var button = $(this);
				if (!button.hasClass('single_add_to_cart_button') && button.is('.product_type_simple')) {
					var productWrap = button.parent().parent().parent().parent().parent();
					if (typeof(productWrap) == 'undefined') {
						return;
					}
					productWrap.addClass('active');
				}
			});

			$body.on('wc_cart_button_updated',function (event,$button) {
                G5Plus.woocommerce.setCartScrollBar();
                var is_single_product = $button.hasClass('single_add_to_cart_button');

                if (is_single_product) return;

                var buttonWrap = $button.parent(),
                    buttonViewCart = buttonWrap.find('.added_to_cart'),
                    addedTitle = buttonViewCart.text(),
                    productWrap = buttonWrap.parent().parent().parent().parent();

                $button.remove();

                setTimeout(function () {
                    buttonWrap.tooltip('hide').attr('title', addedTitle).tooltip('fixTitle');
                }, 500);
                setTimeout(function () {
                    productWrap.removeClass('active');
                }, 700);
            });
		},
		setCartScrollBar: function () {
			var $cart = $('ul.cart_list.product_list_widget');
			var $CartHeight = $cart.outerHeight();
			var $maxCartHeight = 315;
			if ($CartHeight > 315) {
				$cart.css('max-height', $maxCartHeight);
				$cart.perfectScrollbar({
					wheelSpeed: 0.5,
					suppressScrollX: true
				});
			}

			$(document.body).on('wc_fragments_refreshed', function () {
				if ($CartHeight > 315) {
					$cart.css('max-height', $maxCartHeight);
					$cart.perfectScrollbar({
						wheelSpeed: 0.5,
						suppressScrollX: true
					});
				}
			});
		},
		addToWishlist: function () {
			$(document).on('click', '.add_to_wishlist', function (event) {
				var button = $(this),
					buttonWrap = button.parent().parent();
				if (!buttonWrap.parent().hasClass('single-product-function')) {
					button.addClass("added-spinner");
					var productWrap = buttonWrap.parent().parent().parent().parent();
					if (typeof(productWrap) == 'undefined') {
						return;
					}
					productWrap.addClass('active');
				}
			});

			$body.on("added_to_wishlist", function (event, fragments, cart_hash, $thisbutton) {
				event.preventDefault();
				var button = $('.added-spinner.add_to_wishlist'),
					buttonWrap = button.parent().parent();
				if (!buttonWrap.parent().hasClass('single-product-function')) {
					var productWrap = buttonWrap.parent().parent().parent().parent();
					if (typeof(productWrap) == 'undefined') {
						return;
					}
					setTimeout(function () {
						productWrap.removeClass('active');
						button.removeClass('added-spinner');
					}, 700);
				}

			});
		},
		compare: function () {
			$(document).on('click', 'a.compare:not(.added)', function (e) {
				var button = $(this),
					buttonWrap = button.parent();
				if (!buttonWrap.hasClass('single-product-function')) {
					var productWrap = buttonWrap.parent().parent().parent().parent();
					if (typeof(productWrap) == 'undefined') {
						return;
					}
					productWrap.addClass('active');
				}
			});

			$body.on("yith_woocompare_open_popup", function (event, obj) {
				var button = obj.button,
					buttonWrap = button.parent();
				if (!buttonWrap.hasClass('single-product-function')) {
					var productWrap = buttonWrap.parent().parent().parent().parent();
					if (typeof(productWrap) == 'undefined') {
						return;
					}
					setTimeout(function () {
						productWrap.removeClass('active');
					}, 700);
				}

			});
		},
		updateShippingMethod: function () {
			$body.on('updated_shipping_method', function () {
				$('select.country_to_state, input.country_to_state').change();
			});
		},
		quickView: function () {
			var is_click_quick_view = false;
			$(document).off('click', '.product-quick-view').on('click', '.product-quick-view', function (event) {
				var productWrap = $(this).parent().parent().parent().parent().addClass('active');
				event.preventDefault();
				productWrap.addClass('active');
				if (is_click_quick_view) return;
				is_click_quick_view = true;
				var product_id = $(this).data('product_id'),
					popupWrapper = '#popup-product-quick-view-wrapper',
					$icon = $(this).find('i'),
					iconClass = $icon.attr('class'),
					button = $(this);
				$icon.attr('class', 'fa fa-refresh fa-spin');
				$.ajax({
					url: g5plus_app_variable.ajax_url,
					data: {
						action: 'product_quick_view',
						id: product_id
					},
					success: function (html) {
						$icon.attr('class', iconClass);
						if ($(popupWrapper).length) {
							$(popupWrapper).remove();
						}
						$('body').append(html);
						productWrap.removeClass('active');
						G5Plus.woocommerce.addCartQuantity();
						G5Plus.woocommerce.tooltip();
						G5Plus.woocommerce.sale_countdown();
						var $productImageWrap = $('#quick-view-product-image');
						G5Plus.woocommerce.singleProductImage($productImageWrap);

						if (typeof $.fn.wc_variation_form !== 'undefined') {
							var form_variation = $(popupWrapper).find('.variations_form');
							var form_variation_select = $(popupWrapper).find('.variations_form .variations select');
							form_variation.wc_variation_form();
							form_variation.trigger('check_variations');
							form_variation_select.change();
						}

						$(popupWrapper).modal();
						is_click_quick_view = false;
						G5Plus.common.lightGallery();
					},
					error: function (html) {
						is_click_quick_view = false;
					}
				});
			});
		},
		processTitle: function () {
			$('.woocommerce-account .woocommerce h3,.woocommerce-account .woocommerce h2,.woocommerce-checkout .woocommerce h3,.woocommerce-checkout .woocommerce h2,.wishlist-title h2').each(function () {
				$(this).addClass('block-title');
			});
		}
	};

	G5Plus.onReady = {
		init: function () {
			G5Plus.common.init();
			G5Plus.menu.init();
			G5Plus.page.init();
			G5Plus.header.init();
			G5Plus.blog.init();
			G5Plus.widget.init();
			G5Plus.woocommerce.init();
		}
	};

	G5Plus.onLoad = {
		init: function () {
			G5Plus.header.windowLoad();
			G5Plus.page.windowLoad();
			G5Plus.woocommerce.windowLoad();
		}
	};

	G5Plus.onResize = {
		init: function () {
			G5Plus.header.windowResized();
			G5Plus.common.windowResized();
			G5Plus.page.windowResized();
			G5Plus.blog.windowResized();
			G5Plus.woocommerce.windowResized();
		}
	};

	G5Plus.onScroll = {
		init: function () {
			G5Plus.header.windowsScroll();
		}
	};

	$(window).resize(G5Plus.onResize.init);
	$(window).scroll(G5Plus.onScroll.init);
	$(document).ready(G5Plus.onReady.init);
	$(window).load(G5Plus.onLoad.init);
})(jQuery);