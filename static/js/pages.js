(function(){
	var pages = {
		init : function(){
			t.get('.section_one').on('click', function(){
			    t.get('.section_two').attr('class', 'section_two');
			    t.get('.section_one').attr('class', 'language_selected', true);
			    t.get('.two').css({ 'display' : 'none' });
				t.get('.one').css({ 'display' : 'inline' });
			});
			t.get('.section_two').on('click', function(){
			    t.get('.section_one').attr('class', 'section_one');
			    t.get('.section_two').attr('class', 'language_selected', true);
			    t.get('.one').css({ 'display' : 'none' });
				t.get('.two').css({ 'display' : 'inline' });
			});
		}
	}
	
	t.get(document).ready(function(){
		pages.init();
	})
		
})();
