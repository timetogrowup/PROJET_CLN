import fs from 'node:fs';
import assert from 'node:assert/strict';
const catalog=JSON.parse(fs.readFileSync('i18n/static.json')),messages=JSON.parse(fs.readFileSync('i18n/messages.json'));
for(const [key,row]of Object.entries(catalog))for(const lang of ['en','pt-BR','es'])assert.equal(typeof row[lang],'string',key+' '+lang);
for(const [key,row]of Object.entries(messages))for(const lang of ['fr','en','pt-BR','es']){assert.equal(typeof row[lang],'string',key+' '+lang);assert(row[lang].length);const placeholders=s=>[...s.matchAll(/\{(\w+)\}/g)].map(x=>x[1]).sort();assert.deepEqual(placeholders(row[lang]),placeholders(row.fr),key);}
console.log('PASS catalogues:',Object.keys(catalog).length,'static and',Object.keys(messages).length,'dynamic entries; all languages and placeholders complete.');
