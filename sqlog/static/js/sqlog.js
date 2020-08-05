document.addEventListener("keyup", function (event) {
	if (event.key == '/') {
		s = document.getElementById("s");
		s.focus();
		s.select();
		//s.scrollIntoView();
		document.body.scrollTop = 0; // For Safari
		document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
	}
	if (event.key == 'Escape') {
		s = document.getElementById("s");
		s.blur();
	}
});
