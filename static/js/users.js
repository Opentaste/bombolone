(function(){
	var users = {
		init : function(){
		    
			t.get('.li_account').on('click', function(){
			    t.get('.li_account').attr('class', 'language_selected', true);
			    t.get('.li_profile').attr('class', 'li_profile');
			    t.get('.li_password').attr('class', 'li_password');
			    t.get('.sec_account').css({ 'display' : 'inline' });
			    t.get('.sec_profile').css({ 'display' : 'none' });
			    t.get('.sec_password').css({ 'display' : 'none' });
			});
			
			t.get('.li_profile').on('click', function(){
			    t.get('.li_account').attr('class', 'li_account');
			    t.get('.li_profile').attr('class', 'language_selected', true);
			    t.get('.li_password').attr('class', 'li_password');
			    t.get('.sec_account').css({ 'display' : 'none' });
			    t.get('.sec_profile').css({ 'display' : 'inline' });
			    t.get('.sec_password').css({ 'display' : 'none' });
			});
			
			t.get('.li_password').on('click', function(){
			    t.get('.li_account').attr('class', 'li_account');
			    t.get('.li_profile').attr('class', 'li_profile');
			    t.get('.li_password').attr('class', 'language_selected', true);
			    t.get('.sec_account').css({ 'display' : 'none' });
			    t.get('.sec_profile').css({ 'display' : 'none' });
			    t.get('.sec_password').css({ 'display' : 'inline' });
			});
		}
	}
	
	t.get(d).ready(function(){
	    
		users.init();
		
	})
		
})();
