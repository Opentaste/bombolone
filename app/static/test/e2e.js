'use strict';

var timpestamp = new Date().getTime();

describe('Scenario test', function() {
  
  if (app["path"] != "http://mydomanin.com") {
    describe('Settings Profile', function() {
      beforeEach(function() {
        browser().navigateTo( app["path"] + '/settings/profile/?sync=true' );
      });

      it('Chek', function() {
        element('[data-test=submit]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/Profile updated successfully/);

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

        element('[data-test=submit]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/Profile updated successfully/);
      });
    });

    describe('Settings Account', function() {
      beforeEach(function() {
        browser().navigateTo( app["path"] + '/settings/account/?sync=true' );
      });

      it('Chek tip target', function() {
        element('[data-test=submit]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/Account updated successfully/);

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
        expect(element('[ng-bind=message_message]').text()).toMatch(/Account updated successfully/);
      });
    });

    describe('Settings social', function() {
      beforeEach(function() {
        browser().navigateTo( app["path"] + '/settings/social/?sync=true' );
      });

      it('Chek tip target', function() {

      });
    });

    describe('Settings Password', function() {
      beforeEach(function() {
        browser().navigateTo( app["path"] + '/settings/password/?sync=true' );
      });

      it('Chek tip target', function() {
        element('[data-test=submit]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The old password is not matches with the one entered/);

        input("user.password").enter('admin123');
        element('[data-test=submit]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/You should enter a password/);

        input("user.password").enter('admin123');
        input("user.password_new").enter('123456');
        expect(element('[data-test="password_new"]').val()).toBe("123456");
        input("user.password_check").enter('password_check');
        expect(element('[data-test="password_check"]').val()).toBe("password_check");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The both new passwords are not the same/);

        input("user.password").enter('admin123');
        input("user.password_new").enter('123');
        input("user.password_check").enter('password_check');
        expect(element('[data-test="password_new"]').val()).toBe("123");
        element('[data-test="submit"]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/The password entered must be between 6 and 30 characters/);

        input("user.password").enter('admin123');
        input("user.password_new").enter('123456');
        input("user.password_check").enter('123456');

        element('[data-test=submit]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/Password updated successfully/);

        input("user.password").enter('123456');
        input("user.password_new").enter('admin123');
        input("user.password_check").enter('admin123');

        element('[data-test=submit]').click();
        expect(element('[ng-bind=message_message]').text()).toMatch(/Password updated successfully/);
      });
    });
  }

});