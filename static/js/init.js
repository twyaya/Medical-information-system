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

	 new Vue({
		 el: '#app-init',
		 data: {
			 posts: [],
			 results: [],
			 image:"",
		 },
		 methods: {
			borrow(){
				Swal.mixin({
				  input: 'text',
				  confirmButtonText: 'Next &rarr;',
				  showCancelButton: true,
				  progressSteps: ['1', '2']
				}).queue([
				  {
				    title: '第一步:輸入電子郵件信箱',
				  },
				  {
				    title: '第二步:輸入密碼',
				  }
				]).then((result) => {
				  if (result.value) {
				    const answers = JSON.stringify(result.value)
					Swal.fire(
					  '登入成功',
					  ' ',
					  'success'
					)
				  }
				})
			}
		   }
		 });
 
 

  }); // end of document ready
})(jQuery); // end of jQuery name space