(function($){
  $(function(){
	 $(document).ready(function(){
		 $('.button-collapse').sideNav();
		 $('.parallax').parallax();
		 $('.carousel.carousel-slider').carousel({full_width: true});
		 $('.slider').slider({full_width: true});
		 $('.modal').modal();
		 new WOW().init();
		 $('.materialboxed').materialbox();
		 $('.carousel').carousel();
		 $(".dropdown-button").dropdown();
		 $('select').material_select();
	 });

	const SECTIONS_TW = "食品, 運動, 科技"
	new Vue({
	    el: '#app-init',
	    data: {
	        posts: [],
	        results: [],
			image:"",
	    },
	    methods: {

		  }
	    });


  }); // end of document ready
})(jQuery); // end of jQuery name space