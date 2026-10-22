/* MegaNavbar BS4 v1.0.2 (http://www.Navbar4.com/) Copyright 2018 www.Navbar4.com. All Rights Reserved.
** Licensed under Regular License (http://codecanyon.net/licenses/regular) or Extended License (http://codecanyon.net/licenses/extended)
** We will take legal action against those who copy our HTML content, CSS style sheets and JavaScript functions without a license.*/

$( document ).ready(function() {

  //Correct display of active and open arrows.
  $('.navbar .dropdown-menu').on('show.bs.collapse  hidden.bs.collapse', function (event) {
    event.stopPropagation();
    (event.type=='show')?$(this).parent().addClass('show'):$(this).parent().removeClass('show');
  });

  //Close a menu by clicking anywhere on the document.
  $(document).on('click', function (e) {
    if (!$(e.target).closest('.dropdown-menu').length)  {
      $('.navbar .dropdown-menu.collapse.show, .navbar .dropdown-menu.collapsing').collapse('hide');
    }
  });

  //Close all submenus if the parent menu is closed.
  $('.navbar .dropdown-menu').on('hidden.bs.collapse', function (event) {
    event.stopPropagation();
    $(this).find('.collapse.show').each(function () {$(this).collapse('hide');});
  });

  //Close a menu by clicking on other menu item.
  $('.navbar .dropdown-menu').on('show.bs.collapse shown.bs.collapse', function (event) {
    event.stopPropagation();
    $(this).parent().siblings('.show').children('.dropdown-menu').collapse('hide');
  });

  //How to fix MegaNavbar menu when scrolling page
  var target=$('.navbar'), offset = target.offset().top;
  $(window).scroll(function() {
    if (!$('.navbar').is('.fixed-onscroll')) return false;
    if ($(window).scrollTop() >= offset) {target.addClass('fixed-top'); $('body').css({'margin-top': target.height()+'px'});}
    else {target.removeClass('fixed-top'); $('body').css({'margin-top': ''});}
  });


  //Open menu on hover.
  //Check if not collapsed
  var CheckHover = function(e) {
    if (!$('.navbar').is('.navbar-hover')) return false;
    var w = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    return (e.is('.navbar-expand')) ||
      (e.is('.navbar-expand-xl') && w >= 1200) || (e.is('.navbar-expand-lg') && w >= 992) ||
      (e.is('.navbar-expand-md') && w >= 768) ||  (e.is('.navbar-expand-sm') && w >= 576);
  }

  //Prevent click if hover
  $('.navbar [data-toggle="collapse"]').on( "click", function(e) {if (CheckHover($(this.closest('.navbar')))) {e.preventDefault(); e.stopPropagation();}});

  $('.navbar [class*="drop"]').hover(
    function() {
      if (!CheckHover($(this.closest('.navbar')))) return;
      $(this).children('.dropdown-menu').collapse('show').on('shown.bs.collapse.hover', function (e) {
        if (!$(this).parent(':hover').length) {$(this).collapse('hide').parent().removeClass('show');}
        $(this).off('shown.bs.collapse.hover');
      }).parent().addClass('show');
    },
    function() {
      if (!CheckHover($(this.closest('.navbar')))) return;
      $(this).children('.dropdown-menu').collapse('hide').on('hidden.bs.collapse.hover', function (e) {
        if ($(this).parent(':hover').length) {$(this).collapse('show').parent().addClass('show');}
        $(this).off('hidden.bs.collapse.hover');
      }).parent().removeClass('show');
    }
  );

});
