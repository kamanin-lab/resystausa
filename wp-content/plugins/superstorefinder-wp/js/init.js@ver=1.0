var FE = {};
jQuery(function() {
"use strict";
    homebrew.Carousel.prototype.options.transitions.enable = Modernizr.csstransitions;
    homebrew.Tooltip.prototype.options.appendTo = '#mainContent';
    homebrew.Tooltip.prototype.options.transitions.enable = Modernizr.csstransitions;


    jQuery.extend(FE, {
        $els : {
            backToTop : jQuery('#globalBackToTop'),
            body : jQuery('body'),
            mainSite : jQuery('#mainSite'),
            pageOverlay : jQuery('#pageOverlay'),
            root : jQuery('html')
        },

        events: {
            transitionEnd : homebrew.events.transitionEnd || 'transitionend oTransitionEnd otransitionend webkitTransitionEnd msTransitionEnd',
            animationEnd: homebrew.events.animationEnd || 'animationend webkitAnimationEnd MSAnimationEnd oAnimationEnd'
        },

        browser : homebrew.browser,

        baseURL : (typeof fileUrl === 'string')
                    ? fileUrl
                    : (window.location.href.indexOf('') > -1)
                        ? ''
                        : ''
    });

    if(!FE.$els.pageOverlay.length) {
        FE.$els.pageOverlay = jQuery('<div class="page-overlay" id="pageOverlay" />').appendTo(FE.$els.mainSite);
    }

    if(!FE.$els.backToTop.length) {
        FE.$els.backToTop = jQuery('<a href="#top" title="Back To Top" class="main-back-to-top" id="mainBackToTop" />').appendTo('#mainContent');

        FE.$els.backToTop.on('click', function(e) {
            e.preventDefault();

            jQuery('html, body').animate({
                scrollTop : 0
            }, 400);
        });

        jQuery(window).on('scroll.toggleBackToTop', homebrew.utils.throttle(function() {
            FE.$els.backToTop.toggleClass('is-shown', jQuery(window).scrollTop() > jQuery(window).height()*0.5);
        }, 50));
    }

    if(typeof FE.browser === 'undefined') {
        FE.browser = {
            ie      : FE.$els.root.hasClass('ie'),
            ie9     : FE.$els.root.hasClass('ie9'),
            lt9     : FE.$els.root.hasClass('lt9'),
            ie8     : FE.$els.root.hasClass('ie8'),
            lt8     : FE.$els.root.hasClass('lt8'),
            ie7     : FE.$els.root.hasClass('ie7'),
            firefox : (window.mozIndexedDB !== undefined)
        }
    }


    jQuery.extend(true, FE, {
        alert : function(args) {
            this.showAlertPopup(args, 'alert');
        },

        confirm : function(args) {
            this.showAlertPopup(args, 'confirm');
        },

        showAlertPopup : function(args, method) {
            args = args || {};

            var $popup = jQuery('#FE__alertPopup');

            if(!$popup.length) {
                $popup = jQuery([
                        '<div class="ssf-popup text-center" id="FE__alertPopup">',
                            '<h2 class="title space-bottom-2x" />',
                            '<div class="popup-message" />',
                            '<div class="space-top-2x">',
                                '<a href="#/" class="button padded xlarge okay-button">Okay</a>',
                                '<a href="#/" class="button padded xlarge space-left cancel-button" style="display: none;">Cancel</a>',
                            '</div>',
                        '</div>'
                    ].join('')).appendTo('body');

                $popup.popupify({
                    addCloseBtns : false,
                    closeOnOverlay : false
                });
            }

            /* Alerts/Confirm dialog boxes should only happen one at a time,
             * so if it is already shown, then do not proceed. */
            if(jQuery('body').hasClass('popup-is-shown')
            && $popup.hasClass('is-shown')) {
                return;
            }

            var $title = $popup.find('.title'),
                $message = $popup.find('.popup-message'),
                $prevPopup = jQuery('.popup-is-shown').find('.ssf-popup.is-shown');

            if(args.title) $title.html(args.title);
            if(args.message) $message.html(args.message);

            $popup.find('.cancel-button').toggle(method === 'confirm');

            $popup.find('.okay-button, .cancel-button')
                .off('.alert')
                .on('click.alert', function() {
                    if($prevPopup.length
                    && typeof $prevPopup.eq(0).data('popupify') !== 'undefined') {
                        $prevPopup.data('popupify').reveal();
                    } else {
                        $popup.data('popupify').conceal();
                    }

                    if(typeof args.onConfirm === 'function') {
                        if(method === 'confirm') {
                            args.onConfirm(jQuery(this).is('.okay-button'));
                        } else {
                            args.onConfirm();
                        }
                    }
                });

            $popup.data('popupify').reveal();
        },


        FootnoteAnchor : function() {
            this.init.apply(this, arguments);
        },

        Hasher : function(options) {
            this.options = options;
        },

        HeightSlider : function(heightSlider) {
            if(typeof heightSlider === 'string') heightSlider = jQuery(heightSlider);

            var self = this;

            jQuery.extend(self, {
                reveal : function() {
                    if(Modernizr.csstransitions) {
                        if(heightSlider.height() !== 0) return;

                        var targetHeight = 0;
                        heightSlider.css('height', 'auto');
                        targetHeight = heightSlider.height();
                        heightSlider.css('height', '');

                        setTimeout(function() {
                            heightSlider
                                .off(FE.events.transitionEnd)
                                .on(FE.events.transitionEnd, function() {
                                    heightSlider
                                        .off(FE.events.transitionEnd)
                                        .removeClass('is-transitionable')
                                        .css('height', '')
                                        .addClass('is-toggled');
                                })
                                .addClass('is-transitionable')
                                .css('height', targetHeight + 'px');
                        }, 1);
                    } else {
                        if(heightSlider.css('display') !== 'none') return;

                        heightSlider.slideDown(400, function() {
                            jQuery(this).addClass('is-toggled');
                        });
                    }
                },

                conceal : function() {
                    if(Modernizr.csstransitions) {
                        if(heightSlider.height() === 0) return;

                        heightSlider
                            .css('height', heightSlider.height() + 'px')
                            .removeClass('is-toggled');

                        setTimeout(function() {
                            heightSlider
                                .off(FE.events.transitionEnd)
                                .on(FE.events.transitionEnd, function() {
                                    heightSlider.off(FE.events.transitionEnd);
                                        heightSlider.removeClass('is-transitionable');
                                        heightSlider.css('height', '');
                                })
                                .addClass('is-transitionable')
                                .css('height', '0px');
                        }, 1);
                    } else {
                        if(heightSlider.css('display') === 'none') return;

                        heightSlider
                            .removeClass('is-toggled')
                            .slideUp(400);
                    }
                },

                toggle : function() {
                    if(Modernizr.csstransitions) {
                        heightSlider.trigger((heightSlider.height() === 0) ? 'reveal' : 'conceal');
                    } else {
                        heightSlider.trigger((heightSlider.css('display') === 'none') ? 'reveal' : 'conceal');
                    }
                }
            });

            heightSlider.data('height-slider', self);
        },
        /* End HeightSlider */

        StickyColumn : function() {
            this.load.apply(this, arguments);
        },

        getHash : function() {
            var hash = window.location.hash;

            /*
             * Need to check if second character is a period; sometimes
             * AddThis adds its own hash to the URL, and its second
             * character is always a period, which is problematic.
             */
            if(hash === '' || hash.substr(1,1) === '.') {
                return '';
            } else {
                return hash;
            }
        },
        /* End getHash */

        getQueryStr: function(str) {
            var search = window.location.search;
            if(!search) return false;

            if(search.substr(0,1) === '?') {
                search = search.substr(1);
            }

            var splitSearch = search.split('&');
                keyValuePairs = {};

            splitSearch.map(function(searchStr) {
                var splitSearchStr = searchStr.split('=');

                splitSearchStr = splitSearchStr.map(function(str) {
                    return jQuery.trim(str);
                });

                keyValuePairs[splitSearchStr[0]] = splitSearchStr[1];
            });

            if(typeof str === 'string') {
                return (typeof keyValuePairs[str] === 'undefined') ? false : keyValuePairs[str];
            } else {
                return keyValuePairs;
            }
        },
        /* End getQueryStr */

        initContentTabbers : function() {
            /* For tabs that toggle contents instead of going to new pages */

            jQuery('.js-togglerify-tabs').each(function() {
                var $this = jQuery(this),
                    $nestedTabs = $this.find('.js-togglerify-tabs').find('.tab'),
                    $tabs = $this.find('.tab').not($nestedTabs),
                    $nestedContents = $this.find('.js-togglerify-tabs').find('.tab-content'),
                    $contents = $this.find('.tab-content').not($nestedContents);

                $tabs
                    .togglerify('destroy')
                    .togglerify({
                        toggledClass: 'current',
                        selfToggleable: false,
                        singleActive: true,
                        content: function(index) {
                            return $contents.eq(index);
                        }
                    })
                    .on('afterToggleOn', function() {
                        jQuery(window).trigger('resize');
                    })
                    .on('toggleOff', function(e, $thisTab, $thisContent) {
                        /* Pause videos if available */
                        $thisContent.find('.video-holder').find('iframe').each(function() {
                            this.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
                        });
                    });
            });
        },
        /* End initContentTabbers */

        initContentShowers : function() {
            var types = {
                    TAB: 'tab',
                    TOGGLER: 'toggler',
                    NOTES: 'notes'
                },
                $notesToggler = jQuery('#notesToggler'),
                $notesContent = jQuery('#notesContent');

            jQuery('.js-show-content').each(function() {
                var $this = jQuery(this),
                    thisHref = $this.attr('href');

                if(typeof thisHref !== 'string') {
                    console.log($this);
                    console.error("No target specified. Set the target's ID as the `href` attribute on the element.");
                    return
                }
                
                var $target = jQuery($this.attr('href'));

                if(!$target.length) {
                    console.log($this);
                    console.error("Target `" + $this.attr('href') + "` does not exist.");
                    return;
                }

                var data = $this.data('show-content-options');

                if(!data) {
                    console.log($this);
                    console.error('Options undeclared. Declare the options using the `data-show-content-options` attribute on the element.');
                    return;
                }

                var options = (typeof data === 'string')
                        ? homebrew.getKeyValuePairsFromString(data)
                        : {};

                if(!options.type) {
                    console.log($this);
                    console.error('Options declared, but no type specified.');
                    return;
                }

                var scrollArgs = [$target];

                if(options.smoothScroll !== true) {
                    scrollArgs.push('snap');
                }

                switch(options.type) {
                    case types.TAB:
                        $this.on('click', function(e) {
                            e.preventDefault();

                            var $tabContent = $target.closest('.tab-content'),
                                $heightSyncers = $tabContent.find('.js-sync-height-wrapper');

                            if($tabContent.hasClass('current')) {
                                FE.scrollTo.apply(null, scrollArgs);
                            } else {
                                if($heightSyncers.length) {
                                    $heightSyncers.last().one('afterSync', function() {
                                        FE.scrollTo.apply(null, scrollArgs);
                                    });
                                    $tabContent.data('togglerify').toggleOn();
                                } else {
                                    $tabContent.data('togglerify').toggleOn();
                                    FE.scrollTo.apply(null, scrollArgs);
                                }
                            }
                        });
                    break;

                    case types.NOTES:
                        if(!$notesToggler.length || !$notesContent.length) {
                            return;
                        }

                        $this.on('click', function(e) {
                            e.preventDefault();

                            if(!$notesToggler.hasClass('is-toggled')) {
                                $notesToggler.togglerify('toggleOn', { noSlide : true });
                            }

                            FE.scrollTo($target);
                        });
                    break;

                    default:
                        console.log($this);

                        var errorMsg = [
                                'The type `', options.type, '` is not supported. Our currently supported types are: '
                            ];

                        jQuery.each(types, function(key, value) {
                            errorMsg.push('\n' + value);
                        });

                        errorMsg.push('\n\nCheck the type again.');

                        console.error(errorMsg.join(''));
                    break;
                }
            });
        },
        /* End initContentShowers */

        initDropdownSwitchers : function($scope) {
            var $holders = ($scope && $scope.length)
                               ? $scope.find('.dropdown-switcher-holder')
                               : jQuery('.dropdown-switcher-holder');

            if(!$holders.length) return;

            $holders.each(function() {
                var $dropdown = jQuery(this).find('.dropdown-switcher'),
                    $contents = jQuery(this).find('.dropdown-content');

                $dropdown
                    .on('change', function() {
                        $contents
                            .hide()
                            .eq(this.selectedIndex)
                                .show();
                    })
                    .trigger('change');
            });
        },
      

        initNumberTabbers : function() {
            jQuery('.number-tabber').each(function() {
                var $tabs = jQuery(this).find('.number-tabber__tabs').children('li'),
                    $contents = jQuery(this).find('.number-tabber__contents').children('li');

                $tabs
                    .togglerify('destroy')
                    .togglerify({
                        toggledClass: 'current',
                        singleActive: true,
                        selfToggleable: false,
                        content: function(index) {
                            return $contents.eq(index);
                        }
                    });
            });
        },
        /* End initNumberTabbers */

        initPage : function() {
            jQuery('.js-dropdownify').dropdownify();
            jQuery('.js-inputify').inputify();

            jQuery.each(FE, function(key, value) {
                if(key.indexOf('init') === 0 && key !== 'initPage') value();
            });

            FE.loadXMLForm(jQuery('.js-xml-form-holder'));
            FE.loadXMLTable(jQuery('.js-xml-tbl-holder'));
            FE.loadXMLLocations(jQuery('.js-xml-locations-holder'));

            if(FE.browser.ie) jQuery('[placeholder]').placeholderify();
        },
        /* End initPage */

        initSectionSnap : function() {
            /* Only needed for touchscreens, where the header does not
             * automatically hide itself. */
            if(!Modernizr.touch) return;

            var hash = FE.getHash();
            if(!hash || hash.indexOf('#/') > -1) return;

            var $hash = jQuery(hash);
            if(!$hash.length || !$hash.is('.section')) return;

            setTimeout(function() {
                FE.scrollTo($hash);
            }, 25);
        },
        /* End initSectionSnap */

        initSelfTogglers : function() {
            /* Self Togglers - for things like FAQ questions */

            jQuery('.self-toggler__toggler').togglerify({
                singleActive: false,
                slide: true,
                content: function() {
                    return jQuery(this).next();
                }
            });
        },
        /* End initSelfTogglers */

        initSectionContentToggler : function() {
            /* Section Content togglers - for pages like Popular FAQs */

            var $sectionContentTogglers = jQuery('.section-content-toggler');
            if(!$sectionContentTogglers.length) return;

            var $sectionToggleableContents = jQuery('.section-toggleable-content'),
                $sectionDropdown = jQuery('<select>'),
                optionsStrArray = [];

            $sectionContentTogglers
                .togglerify({
                    selfToggleable: false,
                    singleActive : true,
                    content : function(index) {
                        return $sectionToggleableContents.eq(index);
                    }
                })
                .each(function(index) {
                    var $dropdownOption = jQuery(['<option>', jQuery.trim(jQuery(this).find('.toggler__title').text()), '</option>'].join(''));
                    $dropdownOption.data('section-content-toggler', jQuery(this));
                    $dropdownOption.appendTo($sectionDropdown);
                });

            jQuery('<div class="column show-for-small-down" />')
                .prepend($sectionDropdown)
                .prependTo($sectionContentTogglers.eq(0).closest('.row'));

            $sectionDropdown
                .dropdownify({
                    markups : {
                        holder : '<div class="expand space-bottom" />'
                    }
                })
                .on('change', function() {
                    var $thisToggler = jQuery(this).find('option:checked').data('section-content-toggler');
                    $thisToggler.togglerify('toggleOn');
                });

            FE.watchSize('small', function(isSmallScreen) {
                var method = (isSmallScreen) ? 'deactivate' : 'activate';
                $sectionContentTogglers.togglerify(method);
            });
        },
        /* End initSectionContentToggler */

        initSmallNav : function() {
            if(Modernizr.touch || jQuery('#mainSmallNav').data('initSmallNav') === true) return;

            jQuery('#mainSmallNav').data('initSmallNav', true);

            var prevScrollTop = jQuery(window).scrollTop(),
                navHeight = jQuery('#mainSmallNav').height() + jQuery('#mainNav').height();

            jQuery(window)
                .on('resize.navHider', function() {
                    navHeight = jQuery('#mainSmallNav').height() + jQuery('#mainNav').height();
                })
                .trigger('resize.navHider')
                .on('scroll.navHider', function() {
                    var currentScrollTop = jQuery(window).scrollTop(),
                        partialHiddenBool = currentScrollTop > 47,
                        hiddenBool = currentScrollTop >= prevScrollTop && currentScrollTop > navHeight && !FE.$els.body.hasClass('mobile-nav-is-shown');

                    jQuery('body').toggleClass('main-header-is-partially-hidden', partialHiddenBool);
                    jQuery('body').toggleClass('main-header-is-hidden', hiddenBool);
                    prevScrollTop = currentScrollTop;
                })
                .trigger('scroll.navHider');
        },
        /* End initSmallNav */

        initSyncHeightWrappers : function($scope) {
            var $syncHeightWrappers = jQuery('.js-sync-height-wrapper');
            if(!$syncHeightWrappers.length) return;

            $syncHeightWrappers.each(function() {
                var selectors = jQuery(this).data('sync-height-selector');
                if(!selectors) return;

                var selectorsSplitArray = selectors.split(',');

                for(var i = selectorsSplitArray.length-1; i > -1; i--) {
                    selectorsSplitArray[i] = jQuery.trim(selectorsSplitArray[i]);
                }
                
                jQuery(this).heightSyncify({
                    items : selectorsSplitArray
                });
            });
        },
        /* End initSyncHeightWrappers */

        initTooltips : function() {
            var $els = jQuery('.icon--question[title], .js-tooltipify');

            $els.tooltipify();
        },
        /* End initTooltips */

        initQuickLinks : function() {
            var $quicklinksToggler = jQuery('#mainNav__quicklinksToggler'),
                $quicklinks = jQuery('#mainNav__quicklinks');

            if(!$quicklinksToggler.length || !$quicklinks.length) return;
            if($quicklinksToggler.data('initQuickLinks') === true) return;

            $quicklinksToggler.data('initQuickLinks', true);

            var mouseupEv = 'mouseup.mainNavQuicklinksFauxBlur',
                resizeEv = 'resize.limitQuicklinksHeight';

            $quicklinksToggler
                .togglerify({
                    slide: true,
                    content: function() {
                        return $quicklinks;
                    }
                })
                .togglerify('deactivate')
                .on({
                    click : function(e) {
                        e.preventDefault();
                        
                        var $thisToggler = jQuery(this);

                        if($thisToggler.hasClass('is-toggled')) {
                            $thisToggler.togglerify('toggleOff');
                        } else {
                            var heightLimit = jQuery(window).height() - jQuery('#mainNav').height(),
                                contentHeight;

                            $quicklinks.css('height', 'auto');
                            contentHeight = $quicklinks.height();
                            $quicklinks.css('height', '');

                            if(contentHeight >= heightLimit) {
                                $thisToggler.togglerify('toggleOn', { contentHeight : heightLimit });
                            } else {
                                $thisToggler.togglerify('toggleOn');
                            }
                        }
                    },

                    toggleOn : function(e, $thisToggler, $target) {
                        jQuery(document).on(mouseupEv, function(e) {
                            var container = $thisToggler.add($target);
                        
                            if(!container.is(e.target) && container.has(e.target).length === 0) {
                                jQuery(document).off(mouseupEv);
                                $target.data('togglerify').toggleOff();
                            }
                        });

                        jQuery(window).on(resizeEv, function() {
                            if(!$thisToggler.hasClass('is-toggled')) return;

                            var heightLimit = jQuery(window).height() - jQuery('#mainNav').height();

                            $quicklinks.css('height', '');
                            
                            if($quicklinks.height() >= heightLimit) {
                                $quicklinks.height(heightLimit);
                            }
                        });
                    },

                    toggleOff : function() {
                        jQuery(document).off(mouseupEv);
                        jQuery(window).off(resizeEv);
                    }
                });
        },
        /* End initQuickLinks */

        loadXMLForm : function($holders) {
            $holders = jQuery($holders);
            if(!$holders.length) return;

            $holders.each(function() {
                var $thisHolder = jQuery(this);
                if(jQuery.data(this, 'loaded-xml-form') === true) return;

                var xmlURL = $thisHolder.data('xml-form-url');
                if(typeof xmlURL !== 'string') return;

                jQuery.ajax({
                    type: 'GET',
                    url: xmlURL,
                    dataType: 'xml',
                    success: function(data) {
                        makeXMLForm(data, $thisHolder);
                        FE.initFancyPlaceholders($thisHolder);
                        FE.initInputFocus($thisHolder);
                        $thisHolder.find('.js-inputify').inputify();
                        $thisHolder.find('.js-dropdownify').dropdownify();
                        $thisHolder.data('loaded-xml-form', true);
                    },
                    error: function(d) {
                        console.log(d);
                    }
                });
            });

            function makeXMLForm(data, $holder) {
                var $data = jQuery(data),
                    $inputs = $data.find('formInput'),
                    uniqueID = new Date().getTime() + '_' + Math.round(Math.random()*10000),
                    $xmlForm = jQuery([
                        '<form action="https://docs.google.com/forms/d/', getText($data.find('formID')), '/formResponse"',
                        'target="hiddenIframe_', uniqueID, '"',
                        'method="post" class="xml-form-asset xml-form-contents" />'
                    ].join('')).prependTo($holder),
                    xmlFormStrArray = [];

                xmlFormStrArray.push([
                    '<div class="row collapse   space-bottom medium-space-bottom-2x">',
                        makeTitle($data.find('formTitle')),
                    '</div>'
                ].join(''));

                $inputs.each(function(index) {
                    var $thisInput = jQuery(this),
                        uniqueInputID = new Date().getTime() + '_' + index,
                        name = getText($thisInput.find('name')),
                        label = getText($thisInput.find('label')),
                        type = getText($thisInput.find('type')).toLowerCase(),
                        required = getText($thisInput.find('required')).toLowerCase(),
                        pattern = getText($thisInput.find('pattern')),
                        tooltip = getText($thisInput.find('tooltip'));

                    switch(type) {
                        case 'text':
                        case 'number':
                        case 'email':
                        case 'textarea':
                            var validifyStrArray = ['response: #response_' + uniqueInputID],
                                floaterStrArray = [];

                            if(!pattern) {
                                if(type === 'number') {
                                    validifyStrArray.unshift('pattern: numbers');
                                } else if(type === 'email') {
                                    validifyStrArray.unshift('pattern: email');
                                }
                            }

                            if(required === 'yes') {
                                validifyStrArray.unshift('required: true');
                            }

                            validifyStrArray.push('floater: #floater_roi_' + uniqueInputID);

                            floaterStrArray.push('<div class="validify-floater" id="floater_roi_', uniqueInputID, '">');
                                if(required === 'yes') {
                                    floaterStrArray.push([
                                        '<span class="validify-floater__message validify-floater__message--failed-required">',
                                            'This input is required.',
                                        '</span>'
                                    ].join(''));
                                }

                                var errorMessage = getText($thisInput.find('errorMessage'));

                                /*if(!errorMessage) {*/
                                    if(type === 'number') {
                                        errorMessage = 'This input should consist of numbers only.'
                                    } else if(type === 'email') {
                                        errorMessage = 'The address should be in this format: username@youremail.com'
                                    } else if(!errorMessage) {
                                        errorMessage = 'Invalid input.'
                                    }
                                /*}*/

                                floaterStrArray.push([
                                    '<span class="validify-floater__message validify-floater__message--failed-pattern">',
                                        errorMessage,
                                    '</span>'
                                ].join(''));

                            floaterStrArray.push('</div>');
                            
                            var elementStr;

                            if(type === 'textarea') {
                                elementStr = [
                                    '<textarea'
                                ];
                            } else {
                                elementStr = [
                                    '<input',
                                        ' type="', (type === 'email') ? 'email' : 'text', '"'
                                ];
                            }

                                elementStr.push(
                                        ' data-validify="', validifyStrArray.join(', '), '"',
                                        (pattern)
                                            ? ' data-validify-pattern="' + pattern + '"'
                                            : '',
                                        ' name="', name, '"',
                                        ' class="field expand"',
                                        ' id="roi_', uniqueInputID ,'"',
                                    (type === 'textarea')
                                    ? '></textarea>'
                                    : ' />'
                                );

                            xmlFormStrArray.push([
                                '<div class="form-obj', (tooltip) ? ' form-obj--with-tooltip' : '', '">',
                                    '<div class="field-holder expand">',
                                        elementStr.join(''),
                                        '<label for="roi_', uniqueInputID, '" class="field-holder__label">',
                                            label, (required === 'yes') ? '<span class="text-red">*</span>' : '',
                                        '</label>',
                                    '</div>',

                                    '<span class="validify-responses  form-obj__icon" id="response_', uniqueInputID, '">',
                                        '<span class="validify-response validify-response--success">',
                                            '<i class="icon icon--success-tick"></i>',
                                        '</span>',
                                    '</span>',

                                    (tooltip)
                                    ? '<i title="' + tooltip + '" class="icon icon--question round-circle   form-obj__icon"></i>'
                                    : '',

                                    floaterStrArray.join(''),
                                '</div>'
                            ].join(''));
                        break;

                        case 'dropdown':
                            var validifyStrArray = ['response: #response_' + uniqueInputID],
                                floaterStr = '';

                            if(required === 'yes') {
                                validifyStrArray.unshift('required: true');
                                validifyStrArray.push('floater: #floater_roi_' + uniqueInputID);

                                floaterStr = [
                                    '<div class="validify-floater" id="floater_roi_', uniqueInputID, '">',
                                        '<span class="validify-floater__message validify-floater__message--failed-required">',
                                            'This input is required.',
                                        '</span>',
                                    '</div>'
                                ].join('');
                            }

                            var optionsArray = getText($thisInput.find('options')).split('\n'),
                                options = [];

                            while(optionsArray.length) {
                                options.push([
                                    '<option value="', optionsArray[0], '">',
                                        optionsArray[0],
                                    '</option>'
                                ].join(''));

                                optionsArray.shift();
                            }

                            xmlFormStrArray.push([
                                '<div class="form-obj', (tooltip) ? ' form-obj--with-tooltip' : '', '">',
                                    '<span class="expand js-dropdownify">',
                                        '<select data-validify="', validifyStrArray.join(', '), '" name="', name, '">',
                                            '<option value="">', label, (required === 'yes') ? '*' : '', '</option>',
                                            options.join(''),
                                        '</select>',
                                    '</span>',

                                    '<span class="validify-responses  form-obj__icon" id="response_', uniqueInputID, '">',
                                        '<span class="validify-response validify-response--success">',
                                            '<i class="icon icon--success-tick"></i>',
                                        '</span>',
                                    '</span>',

                                    (tooltip)
                                    ? '<i title="' + tooltip + '" class="icon icon--question round-circle   form-obj__icon"></i>'
                                    : '',

                                    floaterStr,
                                '</div>'
                            ].join(''));
                        break;

                        case 'radio':
                        case 'checkbox':
                            var validifyStrArray = ['groupResponse: #response_' + uniqueInputID],
                                validifyRequiredStr = '';

                            if(required === 'yes') {
                                validifyStrArray.unshift('required: true');

                                validifyRequiredStr = [
                                    '<span class="validify-response validify-response--failed-required">',
                                        '<br />This input is required.',
                                    '</span>'
                                ].join('');
                            }

                            var optionsArray = getText($thisInput.find('options')).split('\n'),
                                optionsLabelsArray = getText($thisInput.find('optionsLabels')).split('\n'),
                                options = [],
                                currentOption;

                            for(var i = 0, ii = optionsArray.length; i < ii; i++) {
                                if(optionsArray[i] === '__other_option__') {

                                } else {
                                    options.push([
                                        '<label>',
                                            '<input type="', type, '" name="', name, '" data-validify value="', optionsArray[i], '" class="js-inputify" /> ',
                                            (typeof optionsLabelsArray[i] === 'string'
                                            && optionsLabelsArray[i])
                                            ? optionsLabelsArray[i]
                                            : optionsArray[i],
                                        '</label>'
                                    ].join(''));
                                }
                            }

                            xmlFormStrArray.push([
                                '<div class="form-obj" data-validify-group="', validifyStrArray.join(', '), '">',
                                    '<p class="form-obj__label">',
                                        label, (required === 'yes') ? '<span class="text-red">*</span>' : '',

                                        (tooltip)
                                        ? ' <i title="' + tooltip + '" class="icon icon--question round-circle"></i>'
                                        : '',

                                        ' <span class="validify-responses" id="response_', uniqueInputID, '">',
                                            '<span class="validify-response validify-response--success">',
                                                '<i class="icon icon--success-tick"></i>',
                                            '</span>',

                                            validifyRequiredStr,
                                        '</span>',
                                    '</p>',

                                    options.join(''),
                                '</div>'
                            ].join(''));
                        break;
                    }
                });

                xmlFormStrArray.push([
                    '<div class="text-center space-top medium-space-top-2x">',
                        '<input type="submit" value="Submit" class="button padded xlarge" />',
                    '</div>'
                ].join(''));

                $xmlForm.append(xmlFormStrArray.join(''));
                $xmlForm.find('.icon--question[title]').tooltipify();

                var $hiddenIframe = jQuery('<iframe data-submitted="false" name="hiddenIframe_' + uniqueID + '" style="display: none;" />').appendTo($xmlForm);

                $hiddenIframe.on('load', function() {
                    if(jQuery(this).data('submitted') !== true) return;
                    
                    $xmlForm.addClass('is-hidden');
                    $holder.find('.xml-form-thanks').addClass('is-shown');
                    FE.scrollTo($holder.find('.xml-form-thanks'));
                });

                $xmlForm.validify().on('submit', function(e) {
                    var validifyData = jQuery.data(this, 'validify');

                    validifyData.set('strict', true).validate();

                    if(validifyData.valid !== true) {
                        //alert('Please check the form!');

                        var $errorInput = jQuery(this).find('.is-failed').eq(0);
                        
                        FE.scrollTo($errorInput, function() {
                            $errorInput.focus().select();
                        });

                        e.preventDefault();
                    } else {
                        $hiddenIframe.data('submitted', true);
                        $xmlForm.find('input[type="submit"]').addClass('is-loading').prop('disabled', true);
                    }
                });
            }

            function getText($node) {
                return ($node.length) ? jQuery.trim($node.text()) : '';
            }

            function makeTitle($title) {
                var title = getText($title);

                if(title) {
                    return [
                        '<div class="large-6 column">',
                            '<h3>', title, '</h3>',
                        '</div>',

                        '<div class="large-6 column   medium-down-pad-vertical large-text-right align-to-h3 text-dark-grey">',
                            '<span class="text-red">*</span> Please fill in the mandatory fields.',
                        '</div>'
                    ].join('');
                } else {
                    return [
                        '<div class="column   medium-down-pad-vertical large-text-right text-dark-grey">',
                            '<span class="text-red">*</span> Please fill in the mandatory fields.',
                        '</div>'
                    ].join('');
                }
            }
        },
        /* End loadXMLForm */

        loadXMLTable : function($holders) {
            $holders = jQuery($holders);
            if(!$holders.length) return;

            var worksheets = {},
                xmlSerializer = new XMLSerializer(); // Needed for makeCellInlineFormats

            $holders.each(function() {
                var $thisHolder = jQuery(this);
                if($thisHolder.data('loaded-xml-table') === true) return;

                var xmlURL = $thisHolder.data('xml-table-url');
                if(typeof xmlURL !== 'string') return;

                jQuery.ajax({
                    type: 'GET',
                    url: xmlURL,
                    dataType: 'xml',
                    success: function(data) {
                        var xmlStyles = getXMLStyles(data);
                        makeXMLTable(data, xmlStyles, $thisHolder);
                        attachRowHoverers();
                        $thisHolder.data('loaded-xml-table', true);
                    },
                    error: function(d) {
                        console.log(d);
                    }
                });
            });

            function makeXMLTable(data, xmlStyles, $holder) {
                var $data = jQuery(data),
                    $worksheets = $data.find('Worksheet'),
                    dropdown = {},
                    finalTableStrArr = [];

                worksheets = {};

                $worksheets.each(function() {
                    var $thisWorksheet = jQuery(this),
                        thisWorksheetName = $thisWorksheet.attr('ss:Name').toLowerCase();

                    if(thisWorksheetName.indexOf('dropdown') === 0) {
                        $thisWorksheet.find('Data').each(function() {
                            var $Data = jQuery(this),
                                DataIndex = $Data.index(),
                                DataText = jQuery(this).text().toLowerCase();

                            switch(DataText) {
                                case 'dropdown label':
                                    dropdown.__label = jQuery(this).closest('Row').next('Row').find('Data').text();
                                break;

                                case 'option label':
                                    jQuery(this).closest('Row').nextUntil().each(function() {
                                        var optionLabelText = jQuery(this).find('Data').eq(DataIndex).text();
                                        if(optionLabelText === '') return;
                                        dropdown[jQuery(this).find('Data').eq(DataIndex).text()] = jQuery(this).find('Data').eq(DataIndex+1).text().toLowerCase();
                                    });
                                break;
                            }
                        });
                    } else {
                        worksheets[thisWorksheetName] = $thisWorksheet;
                    }
                });

                if(jQuery.isEmptyObject(dropdown)) {
                    var worksheetNames = [];

                    jQuery.each(worksheets, function(key, value) {
                        worksheetNames.push(key);
                    });

                    finalTableStrArr.push(iterateWorksheetsArray(worksheetNames, xmlStyles));
                } else {
                    var dropdownOptionsArray = [],
                        dropdownContentsArray = [];

                    jQuery.each(dropdown, function(key, value) {
                        if(key === '__label') return;

                        dropdownOptionsArray.push(key);

                        var dropdownWorksheets = {},
                            valueSplitArray = value.split('\n');

                        if(valueSplitArray.length === 1) {
                            valueSplitArray = valueSplitArray[0].split(',');
                        }

                        for(var i = valueSplitArray.length-1; i > -1; i--) {
                            valueSplitArray[i] = jQuery.trim(valueSplitArray[i]);
                        }

                        dropdownContentsArray.push(iterateWorksheetsArray(valueSplitArray, xmlStyles));
                    });

                    var dropdownOptionsStrArray = [],
                        dropdownContentsStrArray = [];

                    while(dropdownOptionsArray.length) {
                        dropdownOptionsStrArray.push([
                            '<option>', dropdownOptionsArray.shift(), '</option>'
                        ].join(''));
                    }

                    while(dropdownContentsArray.length) {
                        dropdownContentsStrArray.push([
                            '<div class="dropdown-content">',
                                dropdownContentsArray.shift(),
                            '</div>'
                        ].join(''));
                    }

                    finalTableStrArr.push([
                        '<div class="dropdown-switcher-holder">',
                            '<div class="text-center text-large">',
                                dropdown.__label,
                                '<span class="js-dropdownify tbl-dropdown">',
                                    '<select class="dropdown-switcher">',
                                        dropdownOptionsStrArray.join(''),
                                    '</select>',
                                '</span>',
                            '</div>',

                            '<div class="dropdown-contents-holder">',
                                dropdownContentsStrArray.join(''),
                            '</div>',
                        '</div>'
                    ].join(''));
                }

                $holder.append(finalTableStrArr.join(''));

                FE.initFootnotes($holder);

                if(!$holder.find('.js-dropdownify').length) return;

                $holder.find('.js-dropdownify').dropdownify();
                FE.initDropdownSwitchers($holder);
            }

            function iterateWorksheetsArray(worksheetNames, xmlStyles) {
                var worksheetStrArr = [],
                    currentWorksheetName,
                    mediaClass;

                while(worksheetNames.length) {
                    currentWorksheetName = worksheetNames.shift();

                    if(typeof worksheets[currentWorksheetName] === 'undefined') {
                        console.error("FE.loadXMLTable(): Can't find the worksheet '" + currentWorksheetName + "'");
                        continue;
                    }
                    
                    if(currentWorksheetName.indexOf('desktop') === 0) {
                        mediaClass = 'show-for-large-up';
                    } else if(currentWorksheetName.indexOf('tabletup') === 0) {
                        mediaClass = 'show-for-medium-up';
                    } else if(currentWorksheetName.indexOf('tabletonly') === 0) {
                        mediaClass = 'show-for-medium-only';
                    } else if(currentWorksheetName.indexOf('tabletdown') === 0) {
                        mediaClass = 'show-for-medium-down';
                    } else if(currentWorksheetName.indexOf('mobile') === 0) {
                        mediaClass = 'show-for-small-down';
                    }

                    worksheetStrArr.push([
                        '<div class="tbl-holder', (typeof mediaClass === 'string') ? ' ' + mediaClass : '', '">'
                    ].join(''));
                        worksheetStrArr.push(makeTableString(worksheets[currentWorksheetName], xmlStyles));
                    worksheetStrArr.push('</div>');
                }

                return (worksheetStrArr.length) ? worksheetStrArr.join('') : false;
            }

            function getColumnCount($worksheet) {
                var $worksheetRows = $worksheet.find('Row'),
                    _columnCount = [];

                $worksheetRows.each(function() {
                    var $cells = jQuery(this).find('Cell');

                    /* Filter out empty cells */
                    $cells.each(function() {
                        if(!jQuery(this).text()) {
                            $cells = $cells.not(jQuery(this));
                        }
                    });

                    _columnCount.push($cells.length);
                });

                return Math.max.apply(null, _columnCount);
            }

            function getXMLStyles(data) {
                var $styles = jQuery(data).find('Style'),
                    styleObj = {};
                
                $styles.each(function() {
                    var $thisStyle = jQuery(this),
                        $alignment = $thisStyle.find('Alignment'),
                        $interior = $thisStyle.find('Interior'),
                        $numberFormat = $thisStyle.find('NumberFormat'),
                        $font = $thisStyle.find('Font'),
                        thisStyleObj = {};

                    /* Allow adjustment of alignment in the Excel spreadsheet */
                    if($alignment.length && hasAttributes($alignment, ['ss:Horizontal', 'ss:Vertical'])) {
                        var verticalAlignment, horizontalAlignment;

                        switch($alignment.attr('ss:Vertical')) {
                            case 'Top' : verticalAlignment = 'top'; break;
                            case 'Center' : verticalAlignment = 'middle'; break;
                            case 'Bottom' : verticalAlignment = 'bottom'; break;
                        }

                        switch($alignment.attr('ss:Horizontal')) {
                            case 'Top' : horizontalAlignment = 'top'; break;
                            case 'Center' : horizontalAlignment = 'center'; break;
                            case 'Bottom' : horizontalAlignment = 'bottom'; break;
                        }

                        thisStyleObj.alignment = {
                            'vertical' : verticalAlignment,
                            'horizontal' : horizontalAlignment
                        };
                    }

                    /* Interior is where the cell's background color data is stored */
                    if($interior.length && hasAttributes($interior, ['ss:Color'])) {
                        thisStyleObj.bgColor = $interior.attr('ss:Color');
                    }

                    if($font.length && hasAttributes($font, ['ss:Italic', 'ss:Bold', 'ss:Underline', 'ss:Color', 'ss:Size'])) {
                        thisStyleObj.font = {
                            'italic' : $font.attr('ss:Italic'),
                            'bold' : $font.attr('ss:Bold'),
                            'underline' : $font.attr('ss:Underline'),
                            'color' : $font.attr('ss:Color'),
                            'size' : $font.attr('ss:Size')
                        };
                    }

                    if($numberFormat.length && hasAttributes($numberFormat, ['ss:Format'])) {
                        thisStyleObj.numberFormat = $numberFormat.attr('ss:Format');
                    }

                    styleObj[$thisStyle.attr('ss:ID')] = thisStyleObj;
                });

                return styleObj;
            }

            function makeTableString($worksheet, xmlStyles) {
                var $rows = filterOutEmptyRows($worksheet.find('Row'));                    
                if(!$rows.length) return '';

                var totalColumns = parseInt(getColumnCount($worksheet), 10),
                    totalRows = $rows.length,
                    i, ii, j, jj,
             
                    tableLayout = [];

                for(i = $rows.length-1; i >-1; i--) {
                    tableLayout.push(new Array(totalColumns));
                }

                $rows.each(function(rowIndex) {
                   
                    var cellCount = 0;

                    jQuery(this).find('Cell').each(function(cellIndex) {
                        if(cellCount >= totalColumns) return;

                        var $thisCell = jQuery(this),
                            cellMergeDown = parseInt($thisCell.attr('ss:MergeDown'), 10) || 0,
                            cellMergeAcross = parseInt($thisCell.attr('ss:MergeAcross'), 10) || 0;

                       
                        while(typeof tableLayout[rowIndex][cellCount] === 'number') {
                            cellCount++;
                        }

                        tableLayout[rowIndex][cellCount] = $thisCell;

                        /* If there's colspan, then denote the overlapping cells
                         * as 0 so that it won't be rendered later. */
                        if(cellMergeAcross) {
                            for(i = cellCount, ii = cellCount+cellMergeAcross; i < ii; i++) {
                                tableLayout[rowIndex][i+1] = 0;
                            }

                            cellCount += cellMergeAcross;
                        }

                        /* Same thing, if there's rowspan, then denote the
                         * overlapping cells as 0 so that it won't be
                         * rendered later. */
                        if(cellMergeDown) {
                            for(i = rowIndex+1, ii = rowIndex+cellMergeDown; i <= ii; i++) {
                                tableLayout[i][cellCount] = 0;

                                /* Same thing; this is to account for both rowspan
                                 * and colspan from the same cell. */
                                if(cellMergeAcross) {
                                    for(j = cellCount+1, jj = cellCount+cellMergeAcross; j <= jj; j++) {
                                        tableLayout[i][j] = 0;
                                    }
                                }
                            }
                        }

                        cellCount++;
                    });
                });

                var tableStrArr = [],
                    tableStyleID = $worksheet.find('Table').attr('ss:StyleID'),
                    defaultStyle = (xmlStyles[tableStyleID]) ? xmlStyles[tableStyleID] : {};

                tableStrArr.push('<table class="default-tbl">');

                var cellStrArr, cellArray, cell, k, kk;
                while(tableLayout.length) {
                    cellStrArr = [];

                    cellArray = tableLayout.shift();

                    for(k = 0, kk = cellArray.length; k < kk; k++) {
                        if(typeof cellArray[k] === 'undefined') {
                            cellStrArr.push('<td></td>');
                        } else if(typeof cellArray[k] === 'object') {
                            cellStrArr.push(makeCellString(cellArray[k], k));
                        }
                    }

                    if(cellStrArr.length) {
                        cellStrArr.unshift('<tr>');
                        cellStrArr.push('</tr>');
                        tableStrArr.push(cellStrArr.join(''));
                    }
                }

                tableStrArr.push('</table>');

                return tableStrArr.join('');

                function makeCellString($cell, cellIndex, log) {
                    var $thisCell = $cell,
                        cellContent = $thisCell.text();

                    if(cellContent === '') {
                        if(cellIndex % 2 === 1) {
                            return '<td class="alt"></td>';
                        } else {
                            return '<td></td>';
                        }
                    }

                    var cellStyle = jQuery.extend({}, defaultStyle),
                        cellData = $thisCell.find('Data'),
                        cellDataType = cellData.attr('ss:Type');

                    if(cellDataType === 'Number') {
                        var decimalSplit = cellContent.split('.');

                        if(decimalSplit.length > 1 && decimalSplit[1].length > 2) {
                            cellContent = parseFloat(cellContent, 10).toFixed(2);
                        }
                    }

                    if(xmlStyles[$thisCell.attr('ss:StyleID')]) {
                        jQuery.extend(cellStyle, xmlStyles[$thisCell.attr('ss:StyleID')]);
                    }

                    var cellNumberFormat = cellStyle.numberFormat,
                        cellMergeDown = parseInt($thisCell.attr('ss:MergeDown'), 10) || 0,
                        cellMergeAcross = parseInt($thisCell.attr('ss:MergeAcross'), 10) || 0,
                        cellSSData = $thisCell.children('ss\\:Data'),
                        cellInlineTags = {
                            'italic' : 0,
                            'bold' : 0,
                            'underline' : 0
                        },

                        cellTagName = (cellStyle.bgColor && cellStyle.bgColor !== '#FFFFFF') ? 'th' : 'td',
                        cellClassNames = [],
                        cellClassName = '',
                        cellRowspan = '',
                        cellColspan = '',
                        cellInlineStyles = [];

                    if(cellIndex % 2 === 1) {
                        cellClassNames.push('alt');
                    }

                    if(cellSSData.length) {
                        cellInlineTags = {
                            'bold' : cellSSData.find('B').length,
                            'italic' : cellSSData.find('I').length,
                            'underline' : cellSSData.find('U').length
                        };

                        cellContent = makeCellInlineFormats(cellSSData);
                    }

                    if(typeof cellStyle.bgColor === 'string') {
                        cellInlineStyles.push('background-color: ' + cellStyle.bgColor);
                    }

                    if(typeof cellStyle.alignment === 'object') {
                        if(typeof cellStyle.alignment.horizontal === 'string') {
                            cellInlineStyles.push('text-align: ' + cellStyle.alignment.horizontal);
                        }
                        if(typeof cellStyle.alignment.vertical === 'string') {
                            cellInlineStyles.push('vertical-align: ' + cellStyle.alignment.vertical);
                        }
                    }

                    if(typeof cellStyle.font === 'object') {
                        if(typeof cellStyle.font.italic !== 'undefined') {
                            cellInlineStyles.push('font-style: italic');
                        }
                        if(typeof cellStyle.font.bold !== 'undefined') {
                            cellInlineStyles.push('font-weight: bold');
                        }
                        if(typeof cellStyle.font.underline !== 'undefined') {
                            cellInlineStyles.push('text-decoration: underline');
                        }
                        if(typeof cellStyle.font.color !== 'undefined') {
                            cellInlineStyles.push('color: ' + cellStyle.font.color);
                        }
                    }


                    /* Compile all the attributes */

                    if(cellClassNames.length) {
                        cellClassName = [' class="', cellClassNames.join(' '), '"'].join('');
                    }

                    if(cellMergeDown) {
                        cellRowspan = [' rowspan="', cellMergeDown+1, '"'].join('');
                    }

                    if(cellMergeAcross) {
                        cellColspan = [' colspan="', cellMergeAcross+1, '"'].join('');
                    }

                    if(typeof cellNumberFormat !== 'undefined') {
                        cellContent = makeCellCurrency(cellNumberFormat, cellContent);
                    }

                    if(cellInlineStyles.length) {
                        cellInlineStyles = [' style="', cellInlineStyles.join('; '), '"'].join('');
                    } else {
                        cellInlineStyles = '';
                    }

                    cellContent = cellContent.replace(/\n/g, '<br />');

                    if(typeof cellStyle.font === 'object'
                    && typeof cellStyle.font.size !== 'undefined'
                    && cellStyle.font.size !== '11') {
                        cellContent = [
                            '<span style="font-size: ', Math.round(parseFloat(cellStyle.font.size, 10) / 11 * 100, 10), '%;">',
                                cellContent,
                            '</span>'
                        ].join('');
                    }

                    return [
                        '<', cellTagName, cellClassName, cellRowspan, cellColspan, cellInlineStyles, '>',
                            cellContent,
                        '</', cellTagName, '>'
                    ].join('');
                }
            }

            function makeCellInlineFormats($ssData) {
                /*
                 * $ssData.html() was initially used to get the string of the
                 * contents. However, that produced an error in all versions
                 * of IE as well as Safari. This was with jQuery 1.11.0.
                 *
                 * To work around this, an XMLSerializer is used instead. 
                 * https://developer.mozilla.org/en-US/docs/XMLSerializer
                 */
                var ssDataChildNodes = jQuery.makeArray($ssData[0].childNodes),
                    contentsStr = [];

                while(ssDataChildNodes.length) {
                    contentsStr.push(xmlSerializer.serializeToString(ssDataChildNodes.shift()));
                }

                contentsStr = contentsStr.join('');

                var cellContentStr = contentsStr,
                    fontMatchArray = cellContentStr.match(/<Font+(.*?)>/g);

                var inlineStyles;
                for(var i = 0, ii = fontMatchArray.length; i < ii; i++) {
                    inlineStyles = getInlineStyles(fontMatchArray[i]);

                    if(inlineStyles === '') {
                        cellContentStr = cellContentStr
                                            .replace(fontMatchArray[i], '')
                                            .replace('</Font>', '');
                    } else {
                        cellContentStr = cellContentStr
                                            .replace(fontMatchArray[i], '<span style="' + inlineStyles + '">')
                                            .replace('</Font>', '</span>');
                    }
                }

                var inlineTags = ['b', 'i', 'u', 'sup'],
                    tagName;

                while(inlineTags.length) {
                    tagName = inlineTags.shift();

                    cellContentStr = cellContentStr
                                        .replace(new RegExp('<' + tagName + '+(.*?)>', 'gi'), '<' + tagName + '>')
                                        .replace(new RegExp('<\/' + tagName + '+(.*?)>', 'gi'), '</' + tagName + '>');
                }

                return cellContentStr;

                function getInlineStyles(fontHTMLStr) {
                    /*
                     * The subtstring is to remove the opening and closing
                     * angled brackets (`<` and `>`) at the start and end
                     * of the string.
                     */
                    var splitArray = fontHTMLStr.substring(1, fontHTMLStr.length-1).split(' '),
                        attrStr,
                        splitAttrArray,
                        inlineStylesArray = [];

                    while(splitArray.length) {
                        attrStr = splitArray.shift();
                        if(attrStr.indexOf('html:') === -1) continue;

                        splitAttrArray = attrStr.replace(/(html\:)|"/g, '').toLowerCase().split('=');


                        switch(splitAttrArray[0]) {
                            case 'color':
                                if(splitAttrArray[1] === '#000000') continue;
                                inlineStylesArray.push(['color: ', splitAttrArray[1]].join(''));
                            break;

                            case 'size':
                                inlineStylesArray.push(['font-size: ', Math.round((parseFloat(splitAttrArray[1], 10) / 11 * 100), 10), '%'].join(''));
                            break;
                        }
                    }

                    return inlineStylesArray.join('; ');
                }
            }

            function makeCellCurrency(cellNumberFormat, cellContent) {
                if(cellNumberFormat === '@'
                || cellNumberFormat === '0') return cellContent;

                var splitCellContentArray;

                if(cellNumberFormat === 'Currency') {
                    splitCellContentArray = parseFloat(cellContent, 10).toFixed(2).split('.');

                    cellContent = 'RM' + contentWithcommas();

                    if(splitCellContentArray.length > 1) {
                        cellContent += '.' + splitCellContentArray[1];
                    }
                } else if(cellNumberFormat === 'Fixed') {
                    splitCellContentArray = parseFloat(cellContent, 10).toFixed(2).split('.');

                    cellContent = contentWithcommas();

                    if(splitCellContentArray.length > 1) {
                        cellContent += '.' + splitCellContentArray[1];
                    }
                } else {
 
                    var currencyFormatArray = cellNumberFormat.split(';')[0].split(','),

                        currency = currencyFormatArray[0].replace(/\[|\]| |#|\\|"/g, '').replace(/\$/, '').split('-'),
                        decimals = currencyFormatArray[1].split('.');

                    if(currency.length > 1) currency = currency[0];

                    if(decimals.length === 1) {
                        decimals = 0;
                    } else {
                        decimals = decimals[1].replace(/_\)/g, '').length;
                    }

                    splitCellContentArray = parseFloat(cellContent, 10).toFixed(decimals).split('.');
                    cellContent = currency + contentWithcommas();
                    if(splitCellContentArray.length > 1) {
                        cellContent += '.' + splitCellContentArray[1];
                    }
                }

                return cellContent;

                function contentWithcommas() {
                    return splitCellContentArray[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                }
            }

            function attachRowHoverers() {
                $holders.find('[rowspan]').each(function() {
                    var $thisCell = jQuery(this),
                        rowspan = $thisCell.attr('rowspan');

                    if(typeof rowspan !== 'string') return;

                    rowspan = parseInt(rowspan, 10);

                    var $thisRow = $thisCell.closest('tr'),
                        $nextRows = $thisRow.nextAll('tr').slice(0, rowspan-1);

                    $nextRows.each(function() {
                        jQuery(this).on({
                            mouseenter : function() {
                                $thisCell.addClass('is-hovered');
                            },

                            mouseleave : function() {
                                $thisCell.removeClass('is-hovered');
                            }
                        });
                    });
                });
            }

            function filterOutEmptyRows($rows) {
                /* Filter out rows that only have empty cells */
                $rows.each(function() {
                    var empty = true;

                    jQuery(this).find('Cell').each(function() {
                        if(jQuery(this).text() !== '') empty = false;
                        return false;
                    });

                    if(empty) $rows = $rows.not(jQuery(this));
                });

                return $rows;
            }

            function hasAttributes($obj, attrArr) {
                while(attrArr.length) {
                    if(typeof $obj.attr(attrArr.shift()) !== 'undefined') {
                        return true;
                    }
                }

                return false;
            }
        },
        /* End loadXMLTable */

        loadXMLLocations : function($holders) {
            $holders = jQuery($holders);
            if(!$holders.length) return;

            $holders.each(function() {
                var $thisHolder = jQuery(this);
                if($thisHolder.data('loaded-xml-locations') === true) return;

                var xmlURL = $thisHolder.data('xml-locations-url');
                if(typeof xmlURL !== 'string') return;

                jQuery.ajax({
                    type: 'GET',
                    url: xmlURL,
                    dataType: 'xml',
                    success: function(data) {
                        makeLocationsList(data, $thisHolder);
                        $thisHolder.data('loaded-xml-locations', true);
                    },
                    error: function(d) {
                        console.log(d);
                    }
                });
            });

            function makeLocationsList(data, $holder) {
                var $locations = jQuery(data).find('obj'),
                    regions = [];

                $locations.each(function() {
                    var $region = jQuery(this).find('region'),
                        regionStr = jQuery.trim($region.text());

                    regionStr = (regionStr) ? regionStr : 'Default';

                    if(regions.length) {
                        for(var i = regions.length-1; i > -1; i--) {
                            if(regions[i].name === regionStr) {
                                regions[i].$els.push(jQuery(this));
                                return;
                            }
                        }
                    }

                    regions.push({
                        'name' : regionStr,
                        '$els' : [jQuery(this)]
                    });
                });

                regions.sort(function(a,b) {
                    var strA = a.name.toLowerCase(),
                        strB = b.name.toLowerCase();

                    if(strA < strB) return -1; // sort ascending
                    if(strA > strB) return 1;
                    return 0; // do nothing
                });

                var output = [],
                    switcherStrArr = ['<span class="location-dropdown"><select>', '', '</select></span>'],
                    rowMarkup = ['<div class="row location-list', 1, '"><div class="row__flexi-width ', 3, '">'],
                    i, ii, totalLocationsInRegion;
                
                for(i = 0, ii = regions.length; i < ii; i++) {
                    rowMarkup[1] = (i === 0) ? ' current' : '';

                    totalLocationsInRegion = regions[i].$els.length;

                    if(totalLocationsInRegion < 2) {
                        rowMarkup[3] = 'has-1-item';
                    } else if(totalLocationsInRegion === 2) {
                        rowMarkup[3] = 'has-2-items';
                    } else if(totalLocationsInRegion === 3) {
                        rowMarkup[3] = 'has-3-items';
                    } else {
                        rowMarkup[3] = 'more-than-3-items';
                    }

                    output.push(rowMarkup.join(''));
                        while(regions[i].$els.length) {
                            output.push([
                                '<div class="column">',
                                    '<div class="location">',
                                        '<div class="location__name">',
                                            jQuery.trim(regions[i].$els[0].find('storeName').text()),
                                        '</div>',

                                        '<div class="location__address">',
                                            jQuery.trim(regions[i].$els[0].find('storeAddress').text()),
                                        '</div>',

                                        '<div class="location__footer">',
                                            '<a href="https://maps.google.com/maps?daddr=',
                                                jQuery.trim(regions[i].$els[0].find('storeLat').text()), ',',
                                                jQuery.trim(regions[i].$els[0].find('storeLng').text()), '" target="_blank">',
                                                'Get Directions',
                                            '</a>',
                                        '</div>',
                                    '</div>',
                                '</div>'
                            ].join(''));

                            regions[i].$els.shift();
                        }
                    output.push('</div></div>');
                }

                $holder.html(output.join(''));

                if(regions.length > 1) {
                    for(i = 0, ii = regions.length; i < ii; i++) {
                        switcherStrArr[1] += [
                            '<option value="', i, '">', regions[i].name, '</option>'
                        ].join('');
                    }

                    var $switcher = jQuery(switcherStrArr.join(''));

                    jQuery('<div class="text-center" />')
                        .prependTo($holder)
                        .append($switcher);

                    $switcher.dropdownify();

                    var $locationLists = $holder.find('.location-list');

                    $holder.find('select').on('change', function() {
                        var targetIndex = parseInt(jQuery(this).val(), 10);

                        $locationLists.each(function(index) {
                            if(index === targetIndex) {
                                jQuery(this)
                                    .addClass('current')
                                    .heightSyncify('enable')
                                    .heightSyncify('sync');
                            } else {
                                jQuery(this)
                                    .removeClass('current')
                                    .heightSyncify('disable');
                            }
                        });
                    });
                }

                var syncHeightSelectors = ['.location__name', '.location__address'];

                $holder.find('.location-list').heightSyncify({
                    items : syncHeightSelectors
                });
            }
        },
        /* End loadXMLLocations */

        scrollTo : function($obj, callback) {
            if(typeof $obj !== 'object'
            || !$obj instanceof jQuery
            || !$obj.length) {
                return;
            }

            var targetScrollPos = $obj.offset().top - 50;

            if(targetScrollPos < jQuery(window).scrollTop()) {
                targetScrollPos -= jQuery('#mainNav').outerHeight();

                if(jQuery('#mainSmallNav').css('display') !== 'none'
                && !jQuery('#mainHeader').hasClass('is-partially-hidden')) {
                    targetScrollPos -= jQuery('#mainSmallNav').outerHeight();
                }
            }

            if(callback === 'snap') {
                jQuery(window).scrollTop(targetScrollPos);
            } else {
                jQuery('html, body').animate({
                    scrollTop : targetScrollPos
                }, 400, callback);
            }
        },
        /* End scrollTo */

        watchSize : function() {
            homebrew.watchSize.apply(homebrew, arguments);
        }
        /* End watchSize */
    });


    jQuery.extend(FE.FootnoteAnchor.prototype, {
        init : function($el, $footnote) {
            if(!$el.length || !$footnote.length) return;

            var instance = this;

            instance.$el = $el;
            instance.$footnote = $footnote;

            $el.tooltipify({
                contents : $footnote.html()
            });

            instance.$el.data('footnote-anchor', this);

            instance.enable();
        },

        enable : function() {
            if(Modernizr.touch) return this;

            var instance = this;

            instance.$el.on({
                'click.footnotesTooltip' : function(e) {
                    e.preventDefault();
                    e.stopPropagation();

                    var $thisFootnote = instance.$footnote;

                    if(!jQuery('#notesToggler').hasClass('is-toggled')) {
                        jQuery('#notesToggler').togglerify('toggleOn', { noSlide : true });
                    }

                    FE.scrollTo($thisFootnote);
                    $thisFootnote.addClass('is-active');

                    jQuery(document)
                        .off('mouseup.notesFauxBlur')
                        .on('mouseup.notesFauxBlur', function(e) {
                            if(!$thisFootnote.is(e.target) && $thisFootnote.has(e.target).length === 0) {
                                jQuery(document).off('mouseup.notesFauxBlur');
                                $thisFootnote.removeClass('is-active');
                            }
                        });
                }
            });

            return this;
        },

        disable : function() {
            var instance = this;

            instance.$el.off('click.footnotesTooltip');
            instance.$el.tooltipify('disable');

            return instance;
        }
    });


    jQuery.extend(FE.Hasher.prototype, {
        get : function(args) {
            var instance = this,
                hash = window.location.hash;

            if(hash === ''
            || hash === '#/'
            || hash.substr(0,2) !== '#/') {
                instance.data = {};
                return instance;
            }

            var splitHash = hash.substring(2).split('&'),
                keyValuePairs,
                dataObj = {};

            while(splitHash.length) {
                keyValuePairs = splitHash.shift().split('=');
                dataObj[jQuery.trim(keyValuePairs[0])] = decodeURIComponent(jQuery.trim(keyValuePairs[1]));
            }

            instance.data = dataObj;

            return instance;
        },

        setData : function(data) {
            if(!data || !jQuery.isPlainObject(data)) return this;
            this.data = jQuery.extend({}, data);
            return this;
        },

        extendData : function(data) {
            if(!data || !jQuery.isPlainObject(data)) return this;

            if(this.data) {
                jQuery.extend(this.data, data);
            } else {
                this.data = data;
            }
            

            return this;
        },

        set : function(args) {
            args = args || {};

            var instance = this,
                options = jQuery.extend(instance.options, args);

            if(options.ignoreDefault && !instance.data) return instance;

            instance.data = instance.data || {};

            var hashKeys = [],
                hash = [],
                sequence = options.sequence;

            if(sequence === 'alphabetical'
            || typeof sequence === 'function') {
                jQuery.each(instance.data, function(key, value) {
                    if(key === '' || value === '') return;
                    hashKeys.push(key);
                });

                var sorter;

                if(sequence === 'alphabetical') {
                    sorter = function(a, b) {
                        var _a = a.toLowerCase(),
                            _b = b.toLowerCase();

                        if(_a < _b) return -1;
                        if(_a > _b) return 1;
                        return 0;
                    };
                } else if(typeof sequence === 'function') {
                    sorter = sequence;
                }

                hashKeys.sort(sorter);

                var currentHashKey;

                while(hashKeys.length) {
                    currentHashKey = hashKeys.shift();
                    hash.push([currentHashKey, encodeURIComponent(instance.data[currentHashKey])].join('='));
                }
            } else if(typeof sequence === 'string') {
                var splitSequence = sequence.split(','),
                    i, ii, currentSequenceKey;

                for(i = 0, ii = splitSequence.length; i < ii; i++) {
                    currentSequenceKey = splitSequence[i];

                    if(instance.data[currentSequenceKey]) {
                        hash.push([currentSequenceKey, encodeURIComponent(instance.data[currentSequenceKey])].join('='));
                    }
                }

                jQuery.each(instance.data, function(key, value) {
                    if(key === '' || value === '') return;

                    for(i = splitSequence.length-1; i > -1; i--) {
                        if(key === splitSequence[i]) return;
                    }

                    hash.push([key, encodeURIComponent(value)].join('='));
                });
            } else {
                jQuery.each(instance.data, function(key, value) {
                    if(key === '' || value === '') return;
                    hash.push([key, encodeURIComponent(value)].join('='));
                });
            }

            window.location.hash = '#/' + hash.join('&');
        },

        isSameWith : function(data) {
            if(!data) return false;

            var same = true,
                count = 0,
                instance = this;

            jQuery.each(data, function(key, value) {
                if(typeof instance.data[key] === 'undefined'
                || instance.data[key] !== value) {
                    same = false;
                    return false;
                } else {
                    count++;
                }
            });

            if(same) {
                var refCount = 0;

                jQuery.each(instance.data, function() {
                    refCount++;
                });

                same = (count === refCount);
            }

            return same;
        }
    });


    jQuery.extend(FE.StickyColumn.prototype, {
        callbacks : jQuery({}),

        hasMousewheel : Boolean(jQuery.fn.mousewheel),

        classes : {
            stickyColumn : 'sticky-column',
            sticky : 'is-sticky',
            stickBottom : 'is-stick-to-bottom'
        },

        load : function(args) {
            var instance = this,
                proto = FE.StickyColumn.prototype;

            /* If Mousewheel isn't available, load it now. */
            if(!proto.hasMousewheel) {
                if(!proto.loadingMousewheel) {
                    proto.loadingMousewheel = true;

                    jQuery.getScript(FE.baseURL + 'js/plugins/jquery.mousewheel.min.js', function() {
                        FE.StickyColumn.prototype.hasMousewheel = true;
                        proto.callbacks.dequeue('mousewheelLoaded');
                    });
                }

                proto.callbacks.queue('mousewheelLoaded', function(next) {
                    instance.init(args);
                    if(typeof next === 'function') next();
                });
            }
        },

        init : function(args) {
            var $el = args.$el,
                $comparee = args.$comparee;

            if(!$el || !$comparee
            || !$el instanceof jQuery || !$comparee instanceof jQuery
            || !$el.length || !$comparee.length) {
                return;
            }

            var instance = this,
                proto = FE.StickyColumn.prototype;

            instance.$el = $el;
            instance.$comparee = $comparee;
            instance.uniqueID = homebrew.generateUniqueID();

            $el.addClass(instance.classes.stickyColumn);
            
            FE.watchSize('large', function(isLargeScreen) {
                if(isLargeScreen) {
                    instance.watch();
                } else {
                    instance.rest();
                    instance.unstick();
                    instance.updatePosition();
                }
            });

            return instance;
        },

        determineState : function() {
            if(!homebrew.screenSize.large) return 'should-be-unstuck';

            var instance = this,
                $stickyCol = instance.$el,
                $comparee = instance.$comparee,
                windowTop = jQuery(window).scrollTop(),
                stickyColMarginTop = parseInt($stickyCol.css('margin-top'), 10);

            instance.offsetTop = (jQuery('#mainHeader').css('position') === 'fixed') ? /*instance.$els.mainNav.height()*/ 0 : 0;
            instance.offsetBottom = parseInt($comparee.find('.column').css('margin-bottom'), 10)*2;

            if(!$comparee.is(':visible') || $stickyCol.height() >= $comparee.height()) {
                return 'should-be-unstuck';
            } else if($stickyCol.hasClass(instance.classes.stickBottom) && $stickyCol.offset().top >= windowTop + instance.offsetTop) {
                return 'should-be-stuck';
            } else if((windowTop + $stickyCol.height() + stickyColMarginTop + instance.offsetTop) > ($comparee.offset().top + $comparee.height() - instance.offsetBottom)) {
                return 'should-be-stuck-to-bottom';
            } else if($comparee.offset().top <= windowTop + instance.offsetTop) {
                return 'should-be-stuck';
            } else {
                return 'should-be-unstuck';
            }
        },

        updatePosition : function() {
            var instance = this,
                $el = instance.$el;

            if($el.hasClass(instance.classes.stickBottom) || !$el.hasClass(instance.classes.sticky)) {
                $el.css('top', '');
            } else {
                $el.css('top', jQuery(window).scrollTop() - instance.$comparee.offset().top + instance.offsetTop + 'px');
            }

            return instance;
        },

        stick : function() {
            var instance = this;
            
            instance.$el
                .addClass(instance.classes.sticky)
                .removeClass(instance.classes.stickBottom);
            
            return instance;
        },

        stickToBottom : function() {
            var instance = this;

            instance.$el
                .addClass([
                    instance.classes.sticky,
                    instance.classes.stickBottom
                ].join(' '))
                .css('margin-top', '');
            
            return instance;
        },

        unstick : function() {
            var instance = this;
            
            instance.$el
                .removeClass([
                    instance.classes.sticky,
                    instance.classes.stickBottom
                ].join(' '))
                .css('margin-top', '');
            
            return instance;
        },

        watch : function() {
            var instance = this;
            
            jQuery(window).on([
                'scroll.', instance.uniqueID,
                ' resize.', instance.uniqueID
            ].join(''), function() {
                var state = instance.determineState();
                
                switch(state) {
                    case 'should-be-stuck' :           instance.stick();         break;
                    case 'should-be-stuck-to-bottom' : instance.stickToBottom(); break;
                    case 'should-be-unstuck' :         instance.unstick();       break;
                }
                
                instance.updatePosition();
            }).trigger('scroll');
            
            instance.$el.on('mousewheel', function(e) {
                if(instance.determineState() !== 'should-be-stuck') return;

                var vector;

                if(e.deltaY < 0) {
                    var bottomDiff = jQuery(window).scrollTop() + jQuery(window).height() - jQuery(this).offset().top - jQuery(this).height();

                    if(bottomDiff >= 0) {
                        return;
                    } else if(Math.abs(bottomDiff) < 100) {
                        vector = bottomDiff;
                    } else {
                        vector = -100;
                    }
                } else if(e.deltaY > 0) {
                    var topDiff = jQuery(window).scrollTop() + instance.offsetTop - jQuery(this).offset().top;

                    if(topDiff === 0) {
                        return;
                    } else if(topDiff < 100) {
                        vector = topDiff;
                    } else {
                        vector = 100;
                    }
                }

                e.preventDefault();
                instance.$el.css('margin-top', [parseInt(instance.$el.css('margin-top'), 10) + vector, 'px'].join(''));
            });

            return instance;
        },

        rest : function() {
            jQuery(window).off('.' + this.uniqueID);
            return this;
        }
    });


    /*---- Init page ----*/

    FE.initPage();

    /* Run through any queued callbacks if available. */
    if(typeof FE__callbacks === 'object'
    && FE__callbacks instanceof Array
    && FE__callbacks.length) {
        while(FE__callbacks.length) {
            FE__callbacks.shift()();
        }
    }
});