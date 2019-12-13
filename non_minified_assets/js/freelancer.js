(function($) {
  "use strict"; // Start of use strict
  
  $(document).click(function(event) {
    if ($(event.target).hasClass("my-menu")) {
      $(".my-content").hide();
      $(".my-menu").removeClass("active");

      // Show only the selected one and set the menu of the selected one as active
      $(event.target.hash).show();
      $(event.target).addClass("active");
    }
  });

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    console.log("tarace");
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      // Hide every other thing and un-highlight all non-related menu
      $(".my-content").hide();
      $(".my-menu").removeClass("active");

      // Show only the selected one and set the menu of the selected one as active
      $(this.hash).show();
      $(this).addClass("active");
      console.log($(this));
    }
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  // navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Floating label headings for the contact form
  $(function() {
    $("body").on("input propertychange", ".floating-label-form-group", function(e) {
      $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    }).on("focus", ".floating-label-form-group", function() {
      $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function() {
      $(this).removeClass("floating-label-form-group-with-focus");
    });
  });

  // Floating label headings for the contact form
  $(function() {
    $("body").on("focus", ".floating-label-form-group-primary", function() {
      $(this).addClass("floating-label-form-group-primary-with-focus");
    }).on("blur", ".floating-label-form-group-primary", function() {
      $(this).removeClass("floating-label-form-group-primary-with-focus");
    });
  });

})(jQuery); // End of use strict
