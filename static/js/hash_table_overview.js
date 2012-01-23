(function(){
	var overview = {
		init : function(){
			
			t.get('.remove_item').on('click', function(e){
                var chosen = e.currentTarget.value;
                var chosen_id = e.currentTarget.className.split('_')[2];
                t.ajax({
		            'url' : '/admin/hash_table/remove/'+chosen_id+'/',
		            'success' : function(data){
		                    if (data == 'ok') {
		                        t.get('.item_'+chosen_id).destroy();
		                    }
		            }
		        });
	        });
			
		}
	}
	
	t.get(d).ready(function(){
	    
		overview.init();	
		
	})
		
})();
