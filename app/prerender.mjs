/* Пререндер стартового экрана в статический HTML.
   Страница должна быть видна даже там, где JS не выполняется:
   Быстрый просмотр macOS, предпросмотр вложений в почте и мессенджерах.

   Переиспользуем те же функции, что и в браузере: заглушаем DOM,
   даём app.js отрисоваться и забираем получившуюся разметку. */
import { readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const DIR = dirname(fileURLToPath(import.meta.url));

// Минимальная заглушка DOM: собирает innerHTML, который ему присваивают
const store = {};
const node = (id) => ({
  get innerHTML() { return store[id] || ''; },
  set innerHTML(v) { store[id] = v; },
  set onclick(_) {},
  style: { cssText: '', setProperty() {} },
  scrollIntoView() {}, animate() {},
  querySelectorAll: () => [],
});
globalThis.document = {
  querySelector: (sel) => node(sel.replace(/^#/, '')),
  querySelectorAll: () => [],
};

const app = await import(pathToFileURL(join(DIR, 'app.js')).href);

const html = readFileSync(join(DIR, 'index.html'), 'utf8');
const put = (h, id, content) =>
  h.replace(new RegExp(`(<[^>]*id="${id}"[^>]*>)`), `$1\n${content}\n`);

let out = html;
for (const id of ['chainPick', 'profPick', 'appbar', 'viewport', 'tabbar', 'console'])
  out = put(out, id, store[id] || '');

writeFileSync(join(DIR, '.prerendered.html'), out);
console.log('пререндер:', Object.entries(store).map(([k, v]) => `${k}=${v.length}`).join(' '));
