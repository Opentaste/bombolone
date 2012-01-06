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
			
		},
		init_change_label : function(){
		    
		    var len = t.get('.label_form').length / 2;
		    
		    for (var i = len; i--;){
		        t.get('.label_'+i+'_0').on('change', function(e){
                    var chosen = e.currentTarget.value;
                    var chosen_num = e.currentTarget.name.split('_')[2];
                    t.get('.label_'+chosen_num+'_1').css({ 'display' : 'none' })
                    t.get('.label_'+chosen_num+'_2').css({ 'display' : 'none' })
                    t.get('.label_'+chosen_num+'_3').css({ 'display' : 'none' })
                    t.get('.label_'+chosen_num+'_'+chosen).css({ 'display' : 'inline' })
		        })
		    }
		    
		}
	}
	
	t.get(document).ready(function(){
		pages.init();
		pages.init_change_label();
	})
		
})();
