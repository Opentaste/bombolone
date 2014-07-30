describe('Admin', function() {
  var params, admin, menuLeft, titleError;
  params = browser.params;

  browser.get('/login');
  element(by.name('username')).sendKeys(params.login.user);
  element(by.name('password')).sendKeys(params.login.password);
  element(by.id('submit')).click();

  beforeEach(function() {
    browser.get('/admin');
  });

  if (params.admin) {
    it('should load all the core module on the left menu', function() {
      menuLeft = element(by.css('[data-test="menu-left-1"]'));
      expect(menuLeft.getText()).toEqual('Dashboard');

      menuLeft = element(by.css('[data-test="menu-left-2"]'));
      expect(menuLeft.getText()).toEqual('Pages');

      menuLeft = element(by.css('[data-test="menu-left-3"]'));
      expect(menuLeft.getText()).toEqual('Users');

      menuLeft = element(by.css('[data-test="menu-left-4"]'));
      expect(menuLeft.getText()).toEqual('Rank');

      menuLeft = element(by.css('[data-test="menu-left-5"]'));
      expect(menuLeft.getText()).toEqual('Languages');
      
      menuLeft = element(by.css('[data-test="menu-left-6"]'));
      expect(menuLeft.getText()).toEqual('Hash Table');
    });

    it('should load the dashboard page after clicked on the menu', function() {
      element(by.css('[data-test="menu-left-1"]')).click();
      browser.getCurrentUrl().then(function(currentUrl) {
        expect(currentUrl.split('/')[3]).toEqual('admin');
      });
    });

    it('should load the Pages page after clicked on the menu', function() {
      element(by.css('[data-test="menu-left-2"]')).click();
      browser.getCurrentUrl().then(function(currentUrl) {
        expect(currentUrl.split('/')[4]).toEqual('pages');
      });
    });

    it('should load the Users page after clicked on the menu', function() {
      element(by.css('[data-test="menu-left-3"]')).click();
      browser.getCurrentUrl().then(function(currentUrl) {
        expect(currentUrl.split('/')[4]).toEqual('users');
      });
    });

    it('should load the Rank page after clicked on the menu', function() {
      element(by.css('[data-test="menu-left-4"]')).click();
      browser.getCurrentUrl().then(function(currentUrl) {
        expect(currentUrl.split('/')[4]).toEqual('rank');
      });
    });

    it('should load the Languages page after clicked on the menu', function() {
      element(by.css('[data-test="menu-left-5"]')).click();
      browser.getCurrentUrl().then(function(currentUrl) {
        expect(currentUrl.split('/')[4]).toEqual('languages');
      });
    });

    it('should load the Hash Table page after clicked on the menu', function() {
      element(by.css('[data-test="menu-left-6"]')).click();
      browser.getCurrentUrl().then(function(currentUrl) {
        expect(currentUrl.split('/')[4]).toEqual('hash-table');
      });
    });
  } else {
    it('should not allow the access if the user is not authorized', function() {
      titleError = element(by.css('[data-test="401-title"]'));
      expect(titleError.getText()).toEqual("User is not authorized.");
    });
  }
});