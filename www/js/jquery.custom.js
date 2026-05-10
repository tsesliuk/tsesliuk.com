//======================================================
//
//	Custom jQuery scripts for Typefolio
//	
//	Only simple scripts go here
//
//======================================================

// debulked onresize handler
// https://github.com/louisremi/jquery-smartresize
function on_resize(c,t){onresize=function(){clearTimeout(t);t=setTimeout(c,100)};return c};


$(document).ready(function(){	
	
	// Simple hover functions
	$('.hoverMe').fadeTo(0, 0.5);
	$('.hoverMe').hover(function () {
		$(this).stop().fadeTo(200, 1);
	}, function () {
		$(this).stop().fadeTo(200, 0.5);
	});
	
	// Table odd & even functions
	$('table').each(function() {
		$(this).children('tbody').find('tr:odd').addClass('odd'); 
		$(this).children('tbody').find('tr:even').addClass('even'); 
		
		$(this).find('tr').each(function() {
			$(this).children('td').last().addClass('last');
		});
	});

	// Table odd & even functions
	$('ul').each(function() {
		$(this).children('li:last-child').addClass('.last-child');
	});
	
	// Stackgrid show item information on hover
	$('.stackgrid.images-only .item').hover(function () {
		$(this).find('.box-desc').stop().fadeIn();
	}, function () {
		$(this).find('.box-desc').stop().fadeOut();
	});
	
	

	// initialize typeMenu
	// this plugin was specifically written for Typefolio
	$('.sticky').typeSticky();

	// initialize typeMenu
	// this plugin was specifically written for Typefolio
	$('#nav').typeMenu();

	// Select all links with hashes
	$('a[href*="#"]')
  // Remove links that don't actually link to anything

  $(function() {
    $("#top").on('click', function() {
        var bottom = $(document).height() - $(window).height();
        $("HTML, BODY").animate({
            scrollTop: bottom
        }, 1000);
    });
});

});


// Back to top button — vanilla JS, no jQuery dependency
(function () {
	var btn = document.createElement('button');
	btn.type = 'button';
	btn.className = 'back-to-top';
	btn.setAttribute('aria-label', 'Back to top');
	btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4l-8 8h5v8h6v-8h5z"/></svg>';
	document.body.appendChild(btn);

	var threshold = 400;
	var ticking = false;

	function update() {
		if (window.pageYOffset > threshold) {
			btn.classList.add('is-visible');
		} else {
			btn.classList.remove('is-visible');
		}
		ticking = false;
	}

	window.addEventListener('scroll', function () {
		if (!ticking) {
			window.requestAnimationFrame(update);
			ticking = true;
		}
	}, { passive: true });

	btn.addEventListener('click', function () {
		var prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		window.scrollTo({ top: 0, behavior: prefersReduced ? 'auto' : 'smooth' });
	});
})();


