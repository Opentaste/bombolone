var admin = {
  'username': 'admin',
  'password': 'admin123'
};

// An example configuration file.
exports.config = {
  // The address of a running selenium server.
  seleniumAddress: 'http://localhost:4444/wd/hub',

  // Capabilities to be passed to the webdriver instance.
  capabilities: {
    'browserName': 'chrome'
  },

  // Spec patterns are relative to the current working directly when
  // protractor is called.
  specs: ['tests/js/e2e/specs/*.js'],

  baseUrl: 'http://0.0.0.0:5000',

  // Options to be passed to Jasmine-node.
  jasmineNodeOpts: {
    showColors: true,
    defaultTimeoutInterval: 30000
  },

  onPrepare: function() {
    browser.driver.get('http://0.0.0.0:5000/login/');

    browser.driver.findElement(by.name('username')).sendKeys(admin.username);
    browser.driver.findElement(by.name('password')).sendKeys(admin.password);
    browser.driver.findElement(by.id('submit')).click();
  }
};
