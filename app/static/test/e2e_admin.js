'use strict';

var timpestamp = new Date().getTime();

describe('Scenario test admin', function() {
  describe('Write recipe', function() {

    it('Translations', function() {
      browser().navigateTo( app["path"] + '/admin/hash_table/overview/?sync=true' );
      expect(repeater('[ng-repeat="hash_map in items_list | orderBy:name"]').count()).toBeGreaterThan(5)

      browser().navigateTo( app["path"] + '/admin/hash_table/view/4ff6985cf33c84558c000231/?sync=true' );
      expect(repeater('[ng-repeat="(key, value) in hash_map.value | orderBy:value.key"]').count()).toBeGreaterThan(5)
      expect(element('[ng-bind="hash_map.name"]').text()).toMatch(/about/)

      element('[data-test=save]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/Hash map changed successfully/);
    });

    it('Crew', function() {
      browser().navigateTo( app["path"] + '/admin/crew/?sync=true' );
    });

    // Not runned on production
    if (app["path"] != "http://mydomanin.com") {

      it('New user', function() {
        browser().navigateTo( app["path"] + '/admin/users/new/?sync=true' );
        
        expect(element('[data-test=tab-2]').css("display")).toBe("none");
        expect(element('[data-test=tab-4]').css("display")).toBe("none");
        element('[data-test=tab-2]').click();
        expect(element('[data-test=tab-1]').css("display")).not().toBe("none");
        expect(element('[data-test=tab-2]').css("display")).toBe("none");

        
        // TEST ACCOUNT ERROR
        input("user.ot_name").enter('');
        expect(element('[data-test="ot_name"]').val()).toBe("");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/You should enter the username/);

        input("user.ot_name").enter('a');
        expect(element('[data-test="ot_name"]').val()).toBe("a");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The username entered must be at least two characters/);

        input("user.ot_name").enter('%%');
        expect(element('[data-test="ot_name"]').val()).toBe("%%");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The username must be alphanumeric with no spaces/);

        input("user.ot_name").enter('leonardo');
        expect(element('[data-test="ot_name"]').val()).toBe("leonardo");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The entered username is not available/);

        input("user.ot_name").enter('zizzamia');
        expect(element('[data-test="ot_name"]').val()).toBe("zizzamia");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The entered username is not available/);

        input("user.ot_name").enter('jack'+timpestamp);
        
        input("user.email").enter("");
        expect(element('[data-test="email"]').val()).toBe("");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/You should enter the email/);

        input("user.email").enter('mare');
        expect(element('[data-test="email"]').val()).toBe("mare");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The format of the email is incorrect/);

        input("user.email").enter('leonardo.zizzamia@gmail.com');
        expect(element('[data-test="email"]').val()).toBe("leonardo.zizzamia@gmail.com");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The email written is already used by another account/);

        input("user.email").enter('mare'+timpestamp+'@mydomanin.com');
        select("user.lan").option("en");
        select("user.time_zone").option("US/Hawaii");

        // TEST PROFILE ERROR
        input("user.name").enter('');
        expect(element('[data-test="name"]').val()).toBe("");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/You must enter the name/);

        input("user.name").enter('a');
        expect(element('[data-test="name"]').val()).toBe("a");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The name entered must be between 2 and 60 characters/);

        input("user.name").enter('%%');
        expect(element('[data-test="name"]').val()).toBe("%%");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The name must consist of only letters and spaces/);

        input("user.name").enter('un buon nome');

        input("user.web").enter('%%');
        expect(element('[data-test="web"]').val()).toBe("%%");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The url you entered is spelled incorrectly/);

        input("user.web").enter('http://www.mydomanin.com');

        // TEST PASSWORD ERROR
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/You should enter a password/);

        input("user.password_new").enter('123');
        expect(element('[data-test="password_new"]').val()).toBe("123");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The both new passwords are not the same/);

        input("user.password_new").enter('123');
        input("user.password_check").enter('123');
        expect(element('[data-test="password_new"]').val()).toBe("123");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The password entered must be between 6 and 30 characters/);

        input("user.password_new").enter('123456');
        input("user.password_check").enter('1234567');
        expect(element('[data-test="password_new"]').val()).toBe("123456");
        expect(element('[data-test="password_check"]').val()).toBe("1234567");
        input("user.password_check").enter('password_check');
        expect(element('[data-test="password_check"]').val()).toBe("password_check");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The both new passwords are not the same/);

        input("user.password_new").enter('123456');
        input("user.password_check").enter('123456');

        // SUCCESS NEW USER
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/success_new_user/);

        /*
        password stuff for settings -> The old password is not matches with the one entered

        error upload 1
        error upload 2
        */
      });

    };

    it('Update user', function() {
      browser().navigateTo( app["path"] + '/admin/users/4fe1d98ef33c8451a2000073/?sync=true' );
      
      expect(element('[data-test=tab-2]').css("display")).toBe("none");
      expect(element('[data-test=tab-3]').css("display")).toBe("none");
      expect(element('[data-test=tab-4]').css("display")).toBe("none");
      element('[data-test=tab-2]').click();
      expect(element('[data-test=tab-1]').css("display")).not().toBe("none");
      expect(element('[data-test=tab-2]').css("display")).toBe("none");

      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/User updated successfully/);

      // TEST ACCOUNT ERROR
      input("user.ot_name").enter('');
      expect(element('[data-test="ot_name"]').val()).toBe("");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/You should enter the username/);

      input("user.ot_name").enter('a');
      expect(element('[data-test="ot_name"]').val()).toBe("a");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The username entered must be at least two characters/);

      input("user.ot_name").enter('%%');
      expect(element('[data-test="ot_name"]').val()).toBe("%%");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The username must be alphanumeric with no spaces/);

      input("user.ot_name").enter('leonardo');
      expect(element('[data-test="ot_name"]').val()).toBe("leonardo");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The entered username is not available/);

      input("user.ot_name").enter('zizzamia');
      expect(element('[data-test="ot_name"]').val()).toBe("zizzamia");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The entered username is not available/);

      input("user.ot_name").enter('jack2'+timpestamp);
      
      input("user.email").enter("");
      expect(element('[data-test="email"]').val()).toBe("");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/You should enter the email/);

      input("user.email").enter('mare');
      expect(element('[data-test="email"]').val()).toBe("mare");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The format of the email is incorrect/);

      input("user.email").enter('leonardo.zizzamia@gmail.com');
      expect(element('[data-test="email"]').val()).toBe("leonardo.zizzamia@gmail.com");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The email written is already used by another account/);

      input("user.email").enter('mare2'+timpestamp+'@mydomanin.com');

      // TEST PROFILE ERROR
      input("user.name").enter('');
      expect(element('[data-test="name"]').val()).toBe("");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/You must enter the name/);

      input("user.name").enter('a');
      expect(element('[data-test="name"]').val()).toBe("a");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The name entered must be between 2 and 60 characters/);

      input("user.name").enter('%%');
      expect(element('[data-test="name"]').val()).toBe("%%");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The name must consist of only letters and spaces/);

      input("user.name").enter('un buon nome');

      input("user.web").enter('%%');
      expect(element('[data-test="web"]').val()).toBe("%%");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The url you entered is spelled incorrectly/);

      input("user.web").enter('http://www.mydomanin.com');

      // TEST PASSWORD ERROR
      input("user.password_new").enter('123');
      expect(element('[data-test="password_new"]').val()).toBe("123");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The password entered must be between 6 and 30 characters/);

      input("user.password_new").enter('123456');
      expect(element('[data-test="password_new"]').val()).toBe("123456");
      input("user.password_check").enter('password_check');
      expect(element('[data-test="password_check"]').val()).toBe("password_check");
      element('[data-test="submit"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The both new passwords are not the same/);

      input("user.password_new").enter('');
      input("user.password_check").enter('');

      /*
      password stuff for settings -> The old password is not matches with the one entered

      error upload 1
      error upload 2
      */
    });

    it('Update hash table', function() {
      browser().navigateTo( app["path"] + '/admin/hash_table/update/4febb657f33c847e560000ae/?sync=true' );
      expect(repeater('[ng-repeat="(key, value) in hash_map.value | orderBy:value.key"]').count()).toBeGreaterThan(2);
      expect(element('[data-test="key-0"]').val()).toBe("description")
      expect(element('[data-test="value-0"]').val()).toBe("For any suggestion or problem write below.")

      element('[data-test="add_label"]').click()
      expect(element('[data-test="key-0"]').val()).toBe("")
      expect(element('[data-test="value-0"]').val()).toBe("")

      element('[data-test="save"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The key name entered must be between two and 30 characters/);

      input("value.key").enter('mare key');
      element('[data-test="save"]').click();
      expect(element('[ng-bind=message_message]').text()).toMatch(/The key name must be alphanumeric with no spaces/);

      // NEED UNDERSTAND HOW CHANGE ONLY ONE INPUT INSIDE NG-REPEAT
      //input("value.key").enter('mare_key');
      //element('[data-test="save"]').click();
      //expect(element('[ng-bind=message_message]').text()).toMatch(/Hash map changed successfully/);
      //pause()
      //
      //element('[data-test="remove_label_0"]').click();
      //pause()
      //expect(element('[data-test="key-0"]').val()).toBe("add_field")
      //expect(element('[data-test="value-0"]').val()).toBe("+ Add field")
      //pause()
    });

    // Not runned on production
    if (app["path"] != "http://mydomanin.com") {

      it('New hash table', function() {
        browser().navigateTo( app["path"] + '/admin/hash_table/new/?sync=true' );
        element('[data-test="create"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The hash table name entered must be between two/);

        input("hash_map.name").enter('mare key');
        element('[data-test="create"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The hash table name must be alphanumeric with no spaces/);

        input("hash_map.name").enter('about');
        element('[data-test="create"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/error_5/);

        input("hash_map.name").enter('mare'+timpestamp);
        element('[data-test="create"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/hash_created/);
      });

    }

  });
});