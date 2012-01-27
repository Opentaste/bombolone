(function(){
	var hash_Table = {
		init : function(){
		    
		    t.get('.list_language').css({ 'display' : 'none' });
		    
		    t.get('.list_language_button').on('click', function(){
		        var display = t.get('.list_language').css('display');
		        if (display == 'none') {
		            t.get('.list_language').css({ 'display' : 'block' });
		        } else {
		            t.get('.list_language').css({ 'display' : 'none' });
		        }
		    });
		    
		    t.get('ul.list_language li').on('click', function(e){
		        var li_press = e.currentTarget;
                var code = li_press.className.split('_')[0];
                
                for (var i = 12; i--;) {
		            var lan = hash_Table.list_languages[i];
		            t.get('.h3_'+lan).css({ 'display' : 'none' });
                    t.get('.section_'+lan).css({ 'display' : 'none' });
                    t.get('li.'+lan+'_lan').attr('class' , lan+'_lan' );
                }
                
                t.get('.h3_'+code).css({ 'display' : 'block' });
                t.get('.section_'+code).css({ 'display' : 'block' });
                t.get('.list_language').css({ 'display' : 'none' });
                t.get('li.'+code+'_lan').attr('class' , code+'_lan language_selected' );
                var val = t.get('li.'+code+'_lan').html();
                t.get('.list_language_button').html(val);
                
		    });
			
		},
		number_document : 0,
		list_languages : ['ar','cn','de','en','es','fr','gr','it','jp','pt','ru','tr'],
		init_add_label : function(){
		    
		    t.get('.hash_add_label').on('click', function(e){
		        hash_Table.number_document += 1; 
		        var num = hash_Table.number_document
		        for (var i = 12; i--;) {
		            var lan = hash_Table.list_languages[i];
		            var label = '<section class="section_num_'+num+'"><label class="width120">Key/Value :</label>';
		                label += '<input type="text" name="label_name_'+lan+'_'+num+'" value="" ';
    		            label += 'class="width180 name_label label_name_'+lan+'_'+num+'" /><input type="text" name="label_'+lan+'_'+num+'"';
    		            label += 'value="" tabindex="{{ j }}" class="width200 label_'+lan+'_'+num+'" />';
    		            label += '<span class="hash_remove_label button button_remove button-red num_'+num+'">- Remove label</span></section>';
		            
    		        t.get('.span_'+lan).before(label);
    		    }
		        hash_Table.init_remove_label();
		        hash_Table.init_change_name_label();	            
		    });
		    
		    
    	},
    	init_remove_label : function(){
    	    
    	    t.get('.hash_remove_label').on('click', function(e){
                var button_click = e.currentTarget.value;
                var num_label = t.get(this).attr('class').split('_')[4];
                t.get('.section_num_'+num_label).destroy() 
	        });

    	},
    	init_change_name_label : function(){
    	    
    	    t.get('.name_label').on('keyup', function(e){
                var label_press = e.currentTarget
                var label_value = label_press.value
                var label_num = label_press.className.split('_')[4]
                for (var i = 12; i--;) {
		            var lan = hash_Table.list_languages[i];
                    t.get('.label_name_'+lan+'_'+label_num).value(label_value);
                }
	        });
    	    
    	}
	}
	
	t.get(d).ready(function(){
	    
		hash_Table.init();
		hash_Table.init_add_label();
		
	})
		
})();
