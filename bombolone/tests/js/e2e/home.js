describe('Home page', function() {
  var introContent, expectedText;

  beforeEach(function() {
    browser.get('/');
  });

  it('title should be "Bombolone - So Tasty!"', function() {
    expect(browser.getTitle()).toEqual("Bombolone - So Tasty!");
  });

  it('should containt a intro description in english', function() {
    introContent = element(by.css('[data-test="intro-content-part-two"]'));
    expectedText = "it's designed to be a simple, flexible toolset for projects of any size.";
    expect(introContent.getText()).toEqual(expectedText);
  });

  it('should change intro description in italiano after changed language', function() {
    introContent = element(by.css('[data-test="intro-content-part-two"]'));
    element(by.css('[data-test="language-it"]')).click();
    expectedText = "E' progettato per essere semplice, e flessibile per progetti di ogni taglia.";
    expect(introContent.getText()).toEqual(expectedText);
  });
});
