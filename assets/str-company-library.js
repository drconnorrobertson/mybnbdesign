'use strict';
const search = document.getElementById('comparison-search');
if (search) {
  const cards = [...document.querySelectorAll('#comparison-results [data-comparison]')];
  search.addEventListener('input', () => {
    const words = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      card.hidden = !words.every(word => card.textContent.toLowerCase().includes(word));
      if (!card.hidden) count++;
    });
    document.getElementById('search-count').textContent = `${count} comparison${count === 1 ? '' : 's'}`;
    document.getElementById('no-comparisons').hidden = count !== 0;
  });
}
const quoteInputs = [...document.querySelectorAll('[data-quote]')];
if (quoteInputs.length) {
  function updateCosts() {
    const result = document.getElementById('cost-result');
    const sums = {a: 0, b: 0};
    const missing = {a: 0, b: 0};
    let invalid = false;
    for (const input of quoteInputs) {
      const key = input.dataset.quote;
      if (input.value.trim() === '' && !input.validity.badInput) {
        missing[key]++;
        continue;
      }
      const cents = Math.round(Number(input.value) * 100);
      if (!input.validity.valid || !Number.isSafeInteger(cents) || cents < 0
          || !Number.isSafeInteger(sums[key] + cents)) {
        invalid = true;
        break;
      }
      sums[key] += cents;
    }
    if (invalid) {
      for (const key of ['a', 'b']) document.getElementById(`total-${key}`).textContent = 'Unavailable';
      result.textContent = 'Enter nonnegative costs with up to two decimal places and within the supported amount range. Totals are unavailable until all invalid entries are corrected.';
      return;
    }
    for (const key of ['a', 'b']) {
      document.getElementById(`total-${key}`).textContent = (sums[key] / 100).toFixed(2)
        + (missing[key] ? ` (partial; ${missing[key]} cost ${missing[key] === 1 ? 'field' : 'fields'} blank)` : '');
    }
    if (missing.a || missing.b) {
      result.textContent = 'Comparison incomplete: enter every cost field for both proposals. Use 0 only for a confirmed zero cost; leave unquoted costs blank. Partial totals do not establish which proposal costs less.';
      return;
    }
    const difference = Math.abs(sums.a - sums.b) / 100;
    result.textContent = sums.a === sums.b
      ? 'The entered totals are equal. Confirm the same currency, scope and exclusions before choosing.'
      : `Option ${sums.a < sums.b ? 'A' : 'B'} has an entered total ${difference.toFixed(2)} lower. Confirm the same currency, scope and exclusions before choosing.`;
  }
  updateCosts();
  quoteInputs.forEach(input => input.addEventListener('input', updateCosts));
}
const printButton = document.getElementById('print-comparison');
if (printButton) printButton.addEventListener('click', () => window.print());

const companySearch = document.getElementById('company-search');
if (companySearch) {
 const cards = [...document.querySelectorAll('#company-results [data-company]')];
 companySearch.addEventListener('input', () => {
  const words = companySearch.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
  let count = 0;
  cards.forEach(card => { card.hidden = !words.every(word => card.textContent.toLowerCase().includes(word)); if (!card.hidden) count++; });
  document.getElementById('company-count').textContent = `${count} provider${count === 1 ? '' : 's'}`;
  document.getElementById('no-companies').hidden = count !== 0;
 });
}
