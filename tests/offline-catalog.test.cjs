const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'courses.json'), 'utf8'));
const js = fs.readFileSync(path.join(root, 'courses-data.js'), 'utf8');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');

test('offline projection matches source and 28 local chapter files', () => {
  const window = {};
  vm.runInNewContext(js, { window });
  assert.deepEqual(JSON.parse(JSON.stringify(window.COURSE_CATALOG)), catalog);
  assert.equal(catalog.chapters.length, 28);
  for (const c of catalog.chapters) {
    assert.match(c.num, /^\d{2}$/);
    assert.equal(c.file, c.num + '.html');
    assert.ok(fs.existsSync(path.join(root, c.file)));
  }
});
test('index uses synchronous offline projection rather than fetch', () => {
  assert.match(html, /<script src="courses-data\.js"><\/script>/);
  assert.doesNotMatch(html, /\bfetch\s*\(/);
});
test('index validates local chapter links and uses safe error text', () => {
  assert.match(html, /course\.file !== course\.num \+ '\.html'/);
  assert.match(html, /error\.textContent = msg/);
  assert.doesNotMatch(html, /innerHTML\s*=\s*'<div class="state-msg error">/);
});
