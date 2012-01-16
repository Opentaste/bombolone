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
		number_of_label : 0,
		init_change_label : function(){
		    
		    var len = t.get('.label_form').length / 2;
		    
		    for (var i = len; i--;){
		        this.add_on_change(i);
		    }
		    
		    this.number_of_label = len - 1;
		    
		},
    	init_add_label : function(){
    	    
		    t.get('.page_add_label').on('click', function(e){
		        pages.number_of_label += 1; 
		        console.log(pages.number_of_label)
		        t.ajax({
		            'url' : '/admin/pages/add_label/'+pages.number_of_label+'/',
		            'success' : function(data){
		                    t.get('.submit_one').before(data.split('__Bombolone__')[0]);
		                    t.get('.submit_two').before(data.split('__Bombolone__')[1]);
		                    pages.add_on_change(pages.number_of_label);
		                    pages.init_remove_label();
		                    pages.init_change_name_label();
		            }
		        });		            
		    });
		    
    	},
    	init_remove_label : function(){
    	    
    	    t.get('.page_remove_label').on('click', function(e){
                var button_click = e.currentTarget.value;
                var num_label = t.get(this).attr('class').split('_')[3];
                t.get('.section_num_'+num_label).destroy() 
	        });
    	    
    	},
    	init_change_name_label : function(){
    	    
    	    t.get('.name_label').on('keyup', function(e){
                var label_press = e.currentTarget
                var label_value = label_press.value
                var label_num = label_press.className.split('_')[4]
                t.get('.label_en_name_'+label_num).value(label_value);
                t.get('.label_it_name_'+label_num).value(label_value);
	        });
    	    
    	},
    	add_on_change : function(i) {
    	    
    	    t.get('.label_'+i+'_0').on('change', function(e){
                var chosen = e.currentTarget.value;
                var chosen_num = e.currentTarget.name.split('_')[2];
                t.get('.label_'+chosen_num+'_1').css({ 'display' : 'none' })
                t.get('.label_'+chosen_num+'_2').css({ 'display' : 'none' })
                t.get('.label_'+chosen_num+'_3').css({ 'display' : 'none' })
                t.get('.label_'+chosen_num+'_'+chosen).css({ 'display' : 'inline' })
	        });
	        
    	}
	}
	
	t.get(d).ready(function(){
	    
		pages.init();
		pages.init_change_label();
		pages.init_add_label();
		pages.init_remove_label();
		pages.init_change_name_label();
		
	})
		
})();
