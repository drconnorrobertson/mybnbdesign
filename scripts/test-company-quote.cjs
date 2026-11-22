const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');
const inputs = ['a', 'b'].flatMap(key => Array.from({length: 4}, () => ({
  dataset: {quote: key}, value: '', validity: {valid: true, badInput: false},
  addEventListener(event, callback) { this.onInput = callback; }
})));
const nodes = Object.fromEntries(['cost-result', 'total-a', 'total-b'].map(id => [id, {textContent: ''}]));
vm.runInNewContext(readFileSync(require('node:path').join(__dirname, '../assets/str-company-library.js'), 'utf8'), {
  document: {getElementById: id => nodes[id] || null, querySelectorAll: () => inputs}
});
const status = () => nodes['cost-result'].textContent;
function set(index, value, valid = true, badInput = false) {
  Object.assign(inputs[index], {value, validity: {valid, badInput}}); inputs[index].onInput();
}
assert.match(status(), /Comparison incomplete/);
assert.match(nodes['total-a'].textContent, /4 cost fields blank/);
set(0, '1000');
assert.match(status(), /Comparison incomplete/);
assert.doesNotMatch(status(), /Option [AB]/);
set(0, '-1', false);
assert.equal(nodes['total-a'].textContent, 'Unavailable');
assert.equal(nodes['total-b'].textContent, 'Unavailable');
set(0, '1000');
assert.match(nodes['total-a'].textContent, /^1000.00 \(partial/);
for (let i = 1; i < 8; i++) set(i, '0');
assert.match(status(), /Option B.*1000.00 lower/);
set(4, '1000'); assert.match(status(), /totals are equal/);
set(0, ''); assert.match(status(), /Comparison incomplete/);
set(0, '', false, true); assert.equal(nodes['total-a'].textContent, 'Unavailable');
set(0, '0.001', false); assert.equal(nodes['total-b'].textContent, 'Unavailable');
set(0, '1e20'); assert.equal(nodes['total-a'].textContent, 'Unavailable');
set(0, '60000000000000'); set(1, '60000000000000');
assert.equal(nodes['total-a'].textContent, 'Unavailable');
for (let i = 0; i < 8; i++) set(i, '0');
set(0, '0.10'); set(1, '0.20'); set(4, '0.30');
assert.equal(nodes['total-a'].textContent, '0.30'); assert.match(status(), /totals are equal/);
set(4, '0.31'); assert.match(status(), /Option A.*0.01 lower/);
console.log('Quote regression checks passed: blank, partial, complete, confirmed zero, invalid, overflow, recovery and cents.');
