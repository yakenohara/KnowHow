// load module
var esprima = require('esprima');

// use loaded module
var code = "var answer = 6 * 7;";
var astObj = esprima.parseScript(code);

console.log(astObj);
