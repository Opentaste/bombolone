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

  suites: {
    admin: 'tests/js/e2e/admin.js',
    adminHashTable: 'tests/js/e2e/admin-hash-table.js',
    adminLanguages: 'tests/js/e2e/admin-languages.js',
    home: 'tests/js/e2e/home.js',
  },

  baseUrl: 'http://0.0.0.0:5000',

  // Options to be passed to Jasmine-node.
  jasmineNodeOpts: {
    showColors: true,
    defaultTimeoutInterval: 30000,
    isVerbose: true
  },

  // This can be changed via the command line as:
  // --params.login.user 'ngrocks'
  params: {
    admin: false,
    login: {
      user: 'username',
      password: 'password' 
    }
  }
};
