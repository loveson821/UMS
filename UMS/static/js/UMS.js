/* Project specific Javascript goes here. */
$(function() {
	$.get('/profile/2/ablum', function(data){
		console.log(data)
	});
});