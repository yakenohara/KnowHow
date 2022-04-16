const {Builder, By, Key, until} = require('selenium-webdriver');

(async () => {
  let driver = await new Builder().forBrowser('chrome').build(); // create a driver instance
  await driver.manage().window().maximize(); // maximize browser window
  await driver.get('https://github.com/'); // navigate to github.com
})();
