/* Maintained browser regression for CI; local interactive QA uses the supported browser. */
import {chromium,webkit} from 'playwright';import assert from 'node:assert/strict';
const base=process.env.CLN_TEST_BASE||'http://127.0.0.1:8000';let checks=0;
for(const engine of [chromium,webkit]){
 const browser=await engine.launch(),context=await browser.newContext({viewport:{width:1280,height:900}}),p=await context.newPage();let posts=0;
 await p.route('https://api.cln-performance.com/**',async route=>{if(route.request().method()==='POST')posts++;await route.abort();});
 for(const lang of ['fr','en','pt-BR','es']){
  await p.goto(base+'/diagnostic.html?lang='+lang);await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');
  assert.equal(await p.locator('nav a').count(),5);
  for(const name of ['applications','people','connections','difficulties','goals','approach','horizon'])await p.locator(`[name=${name}][value=inconnu]`).check();
  await p.locator('[name=goals][value=productivity]').check();assert.equal(await p.locator('[name=goals][value=inconnu]').isChecked(),false);
  await p.locator('[name=goals][value=modernise]').check();await p.locator('[name=goals][value=connect]').check();await p.locator('#diagnostic-form [type=submit]').click();assert((await p.url()).includes('diagnostic.html'));checks++;
  await p.locator('[name=goals][value=connect]').uncheck();await p.locator('#case-situation').fill('Fictional case <b>plain text</b>');await p.locator('#diagnostic-form [type=submit]').click();await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
  let message=await p.locator('#message').inputValue();assert(message.includes('Fictional case <b>plain text</b>'));assert.equal(await p.locator('#recommendation-add').count(),0);checks++;
  message+='\nVisitor edit';await p.locator('#message').fill(message);await p.reload();await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);assert.equal(await p.locator('#message').inputValue(),message);checks++;
  await p.locator('#site-language').selectOption(lang==='en'?'es':'en');assert.equal(await p.locator('#message').inputValue(),message);checks++;
  await p.goto(base+'/contact.html?status=error&lang='+lang);await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);assert.equal(await p.locator('#message').inputValue(),message);assert(await p.locator('#form-alert').isVisible());checks++;
 }
 assert.equal(posts,0);await browser.close();
}
console.log('PASS',checks,'V11 browser assertions: coherent form, goal limit, automatic transfer, editing/reload/error, languages and five-link navigation. No email sent.');
