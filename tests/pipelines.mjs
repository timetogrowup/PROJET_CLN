import {chromium,webkit} from 'playwright';
import assert from 'node:assert/strict';
const base=process.env.CLN_TEST_BASE||'http://127.0.0.1:8000';
const langs=['fr','en','pt-BR','es'];
let checks=0;
for(const engine of [chromium,webkit]){
 const browser=await engine.launch(),context=await browser.newContext({viewport:{width:1280,height:900}}),p=await context.newPage();
 const external=[],errors=[];
 p.on('request',r=>{if(new URL(r.url()).origin!==new URL(base).origin)external.push(r.url());});
 p.on('pageerror',e=>errors.push(e.message));
 for(const lang of langs){
  await p.goto(base+'/index.html?lang='+lang);await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');
  const sections=await p.locator('main > section').evaluateAll(items=>items.map(e=>({id:e.id,hero:e.classList.contains('hero')})));
  assert(sections[0].hero&&sections[1].id==='pipelines');checks++;
  assert.equal(await p.locator('#pipelines .pipeline-overview li').count(),5);checks++;
  await p.locator('#pipelines a').click();await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');
  assert.equal(await p.locator('html').getAttribute('lang'),lang);assert((await p.url()).includes('pipelines.html'));checks++;
  assert.equal(await p.locator('nav a.active').count(),1);assert((await p.locator('nav a.active').getAttribute('href')).includes('pipelines.html'));checks++;
  assert.equal(await p.locator('.pipeline-steps > li').count(),5);assert.equal(await p.locator('#capacites article').count(),4);checks++;
  assert.equal(await p.locator('.pipeline-case').count(),4);checks++;
  const summary=p.locator('.pipeline-case summary').last();await summary.focus();await p.keyboard.press('Enter');assert(await summary.evaluate(e=>e.parentElement.open));checks++;
  const text=await p.locator('main').innerText();assert(!text.includes('undefined'));assert(!text.includes('40 %'));assert(!text.includes('60 %'));checks++;
  await p.locator('#benefices a').click();await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');assert((await p.url()).includes('approche.html'));assert((await p.url()).includes('remuneration'));checks++;
  await p.goto(base+'/pipelines.html?lang='+lang);await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');
  await p.locator('main > section').last().locator('a').click();await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
  assert((await p.url()).includes('contact.html'));assert.equal(await p.locator('#message').inputValue(),'');checks++;
 }
 assert.equal(external.length,0,'pipeline journey must not call third-party APIs');assert.deepEqual(errors,[]);checks+=2;
 await context.close();await browser.close();
}
console.log('PASS',checks,'pipeline journey assertions: placement, stages, capabilities, keyboard exceptions, languages, active menu, method and contact; no third-party request or real email.');
