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
    if (quoteInputs.some(input => !input.validity.valid)) {
      document.getElementById('cost-result').textContent = 'Enter nonnegative costs with up to two decimal places.';
      return;
    }
    const sums = {a: 0, b: 0};
    quoteInputs.forEach(input => { sums[input.dataset.quote] += Math.round((Number(input.value) || 0) * 100); });
    for (const key of ['a', 'b']) document.getElementById(`total-${key}`).textContent = (sums[key] / 100).toFixed(2);
    const difference = Math.abs(sums.a - sums.b) / 100;
    document.getElementById('cost-result').textContent = sums.a === sums.b
      ? 'The entered totals are equal. Compare fit and responsibilities before choosing.'
      : `Option ${sums.a < sums.b ? 'A' : 'B'} has an entered total ${difference.toFixed(2)} lower. Confirm exclusions and property fit before choosing.`;
  }
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
