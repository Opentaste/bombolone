describe('Hash Table', function() {
  var params, rows, row, expectedMessage, timpestamp;
  params = browser.params;
  timpestamp = new Date().getTime();

  browser.get('/login');
  element(by.name('username')).sendKeys(params.login.user);
  element(by.name('password')).sendKeys(params.login.password);
  element(by.id('submit')).click();

  if (params.admin) {

    describe('index', function() {

      beforeEach(function() {
        browser.get('/admin/hash-table/');
      });

      it('should list all the hashmap', function() {
        rows = element.all(by.repeater('item in itemsList | orderBy:sortTable'));
        expect(rows.count()).toBeGreaterThan(5);
      });
    });

    describe('update', function() {

      beforeEach(function() {
        browser.get('/admin/hash-table/update/4f2b3e3918429f1b86000016/');
      });

      it('should have more than 2 rows', function() {
        rows = element.all(by.repeater('(key, value) in hash_map.value | orderBy:value.key'));
        expect(rows.count()).toBeGreaterThan(2);
      });

      it('should show an error when the key is empty', function() {
        element(by.css('[data-test="add_label"]')).click();
        element(by.css('[data-test="save"]')).click();
        expectedMessage = 'The key name entered must be between two and 30 characters';
        expect(element(by.binding('message_message')).getText()).toEqual(expectedMessage);
      });

      //it('should show an error when the key name is not correct', function() {
      //  element(by.css('[data-test="add_label"]')).click()
      //  row = element(by.repeater('(key, value) in hash_map.value | orderBy:value.key'));
      //  element(row.element(by.model('value.key'))).sendKeys('mare key');
      //  element(by.css('[data-test="save"]')).click();
      //  expectedMessage = 'The key name must be alphanumeric with no spaces';
      //  expect(element(by.binding('message_message')).getText()).toEqual(expectedMessage);
      //});
      //
      //it('should save the hash map if the key is correct', function() {
      //  element(by.css('[data-test="add_label"]')).click()
      //  row = element(by.repeater('(key, value) in hash_map.value | orderBy:value.key').row(0));
      //  element(row.element(by.model('value.key'))).sendKeys('mare_key');
      //  element(by.css('[data-test="save"]')).click();
      //  expect(element(by.binding('message_message')).getText()).toMatch(/Hash map changed successfully/);
      //  
      //  element(by.css('[data-test="remove_label_0"]')).click();
      //  expect(element(by.css('[data-test="key-0"]')).getText()).toBe("add_field")
      //  expect(element(by.css('[data-test="value-0"]')).getText()).toBe("+ Add field")
      //});
    });

    describe('new', function() {

      beforeEach(function() {
        browser.get('/admin/hash-table/new/');
      });

      it('should show an error if the right number of characters', function() {
        element(by.css('[data-test="create"]')).click();
        expectedMessage = "The hash table name entered must be between two and twenty characters";
        expect(element(by.binding('message_message')).getText()).toEqual(expectedMessage);
      });

      it('should show an error if the name is not correct', function() {
        element(by.model("hash_map.name")).sendKeys('mare key');
        element(by.css('[data-test="create"]')).click();
        expectedMessage = 'The hash table name must be alphanumeric with no spaces';
        expect(element(by.binding('message_message')).getText()).toEqual(expectedMessage);
      });

      it('should show an error if the name is not correct', function() {
        element(by.model("hash_map.name")).sendKeys('languages');
        element(by.css('[data-test="create"]')).click();
        expectedMessage = 'The name entered is not available';
        expect(element(by.binding('message_message')).getText()).toEqual(expectedMessage);
      });

      it('should show an error if the name is not correct', function() {
        element(by.model("hash_map.name")).sendKeys('mare' + timpestamp);
        element(by.css('[data-test="create"]')).click();
        expect(element(by.binding('message_message')).getText()).toEqual('Hash map created');
      });
    });
  } else {

    describe('index', function() {
      it('should not allow the access if the user is not authorized', function() {
        browser.get('/admin/hash-table/');
        titleError = element(by.css('[data-test="401-title"]'));
        expect(titleError.getText()).toEqual("User is not authorized.");
      });
    });

    describe('update', function() {
      it('should not allow the access if the user is not authorized', function() {
        browser.get('/admin/hash-table/update/4febb657f33c847e560000ae/');
        titleError = element(by.css('[data-test="401-title"]'));
        expect(titleError.getText()).toEqual("User is not authorized.");
      });
    });

    describe('new', function() {
      it('should not allow the access if the user is not authorized', function() {
        browser.get('/admin/hash-table/new/');
        titleError = element(by.css('[data-test="401-title"]'));
        expect(titleError.getText()).toEqual("User is not authorized.");
      });
    });
  }
});