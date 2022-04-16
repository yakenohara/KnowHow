// Module selenium-webdriver exports following
// 
//  - Builder
//  - By
//  - Capabilities
//  - Condition
//  - FileDetector
//  - Session
//  - WebDriver
//  - WebElement
//  - WebElementCondition
//  - WebElementPromise
//
const {Builder, By, Key, until} = require('selenium-webdriver');

(async () => {
    
    /**
     * Creates new {@link webdriver.WebDriver WebDriver} instances.
     */
    let driver = await new Builder()
    
        /**
         * Configures the target browser for clients created by this instance.
         * 
         * @return {!Builder} A self reference.
         */
        .forBrowser('chrome')    

        /**
         * Creates a new WebDriver client based on this builder's current
         * configuration.
         * 
         * @return {!ThenableWebDriver} A new WebDriver instance.
         * @throws {Error} If the current configuration is invalid.
         */
        .build() // <- executed asynchronously
    ;

    await driver
        
        /**
         * @return {!Options} The options interface for this instance.
         */
        .manage()

        /**
         * @return {!Window} The interface for managing the current window.
         */
        .window()

        /**
         * Maximizes the current window. The exact behavior of this command is
         * specific to individual window managers, but typically involves increasing
         * the window to the maximum available size without going full-screen.
         *
         * @return {!Promise<void>} A promise that will be resolved when the command
         *     has completed.
         */
        .maximize() // <- executed asynchronously
    ;

    /**
     * Navigates to the given URL.
     * 
     * @return {!Promise<void>} A promise that will be resolved when the document
     *     has finished loading.
     */
    await driver.get('https://github.com/');  // <- executed asynchronously

})();
