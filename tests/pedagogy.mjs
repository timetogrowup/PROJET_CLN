import {chromium,webkit} from 'playwright';
import assert from 'node:assert/strict';
const base=process.env.CLN_TEST_BASE||'http://127.0.0.1:8000';
let checks=0;
for(const engine of [chromium,webkit]){
 const browser=await engine.launch();
 const context=await browser.newContext({viewport:{width:1280,height:900}}),p=await context.newPage();
 let posts=0;
 await p.route('https://api.cln-performance.com/**',async route=>{if(route.request().method()==='POST')posts++;await route.abort();});
 await p.goto(base+'/diagnostic.html?lang=fr');await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');
 const fill=async()=>{for(const name of ['frequency','people','goal','horizon'])await p.locator(`[name=${name}][value=inconnu]`).check();};
 await fill();await p.locator('#diagnostic-form [type=submit]').click();
 assert((await p.locator('#resultat-insights').textContent()).includes('Un premier échange'));checks++;
 assert.equal(await p.evaluate(()=>localStorage.getItem('clnRecommendation')),null);checks++;
 await p.locator('#summary-edit').click();await p.locator('[name=problems][value=ressaisies]').check();await p.locator('#diagnostic-form [type=submit]').click();
 assert((await p.locator('#resultat-insights').textContent()).includes('objectif précis'));checks++;
 await p.locator('#summary-edit').click();await p.locator('[name=problems][value=repetitif]').check();await p.locator('#diagnostic-form [type=submit]').click();
 assert((await p.locator('#resultat-insights').textContent()).includes('Plusieurs possibilités'));checks++;
 await p.locator('#summary-edit').click();await p.locator('[name=problems][value=inconnu]').check();assert.equal(await p.locator('[name=problems]:checked').count(),1);checks++;
 await p.locator('[name=problems][value=chiffres]').check();assert.equal(await p.locator('[name=problems][value=inconnu]').isChecked(),false);checks++;
 await p.locator('#diagnostic-form [type=submit]').click();
 const before=await p.locator('#resultat-insights').textContent();await p.locator('#site-language').selectOption('en');
 assert.notEqual(await p.locator('#resultat-insights').textContent(),before);checks++;
 assert.equal(await p.evaluate(()=>localStorage.getItem('clnRecommendation')),null);checks++;
 await p.locator('#summary-transfer').click();await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');
 assert.equal(await p.locator('#message').inputValue(),'');checks++;
 await p.locator('#message').fill('My own words <b>not HTML</b>');await p.locator('#recommendation-add').click();
 assert((await p.locator('#message').inputValue()).startsWith('My own words <b>not HTML</b>'));checks++;
 assert((await p.locator('#message').inputValue()).includes('Your indicative summary'));checks++;
 await p.locator('#site-language').selectOption('pt-BR');
 assert((await p.locator('#message').inputValue()).includes('Your indicative summary'),'visitor message never translated');checks++;
 await p.locator('#recommendation-clear').click();assert.equal(await p.locator('#message').inputValue(),'My own words <b>not HTML</b>');checks++;
 assert.equal(await p.evaluate(()=>localStorage.getItem('clnRecommendation')),null);checks++;
 // Unrequested visit to contact never imports an earlier saved result.
 await p.evaluate(()=>localStorage.setItem('clnRecommendation',JSON.stringify({version:6,generatedAt:new Date().toISOString(),answers:{problems:['suivi']}})));
 await p.goto(base+'/contact.html?lang=fr&need=suivi');await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
 assert.equal(await p.locator('#recommendation-preview').isVisible(),false);assert.equal(await p.locator('#message').inputValue(),'');checks++;
 assert.equal(await p.locator('#need-context').inputValue(),'suivi');await p.locator('#need-context').selectOption('chiffres');await p.locator('#need-add').click();assert((await p.locator('#message').inputValue()).includes('information cohérente'));checks++;
 await p.goto(base+'/contact.html?need=%3Cscript%3E');await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);assert.equal(await p.locator('#need-context').inputValue(),'');checks++;
 // Legacy summary gets an actionable explanation, not a fabricated new summary.
 await p.evaluate(()=>localStorage.setItem('clnRecommendation',JSON.stringify({version:4,generatedAt:new Date().toISOString(),answers:{modules:['liberer']}})));
 await p.goto(base+'/contact.html?summary=1&lang=fr');await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
 assert((await p.locator('#recommendation-content').textContent()).includes('ancienne version'));assert.equal(await p.locator('#recommendation-add').isVisible(),false);checks++;
 await p.evaluate(()=>localStorage.setItem('clnRecommendation',JSON.stringify({version:6,generatedAt:new Date(Date.now()-31*86400000).toISOString(),answers:{}})));
 await p.reload();await p.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);assert.equal(await p.locator('#recommendation-preview').isVisible(),false);assert.equal(await p.evaluate(()=>localStorage.getItem('clnRecommendation')),null);checks++;
 // Structured codes are filtered, including potential script fragments.
 const safe=await p.evaluate(()=>CLN.summaryText({problems:['<img src=x onerror=alert(1)>','ressaisies','ressaisies'],tools:'bad'}));assert(!safe.includes('<img'));checks++;
 // Storage errors leave the result on screen and block misleading transfer.
 await p.goto(base+'/diagnostic.html?lang=fr');await p.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');await fill();await p.locator('#diagnostic-form [type=submit]').click();
 await p.evaluate(()=>{Storage.prototype.setItem=()=>{throw new Error('blocked in isolated test');};});await p.locator('#summary-transfer').click();assert(await p.locator('#summary-storage-error').isVisible());assert((await p.url()).includes('diagnostic.html'));checks++;
 assert.equal(posts,0);await context.close();await browser.close();
}
console.log('PASS',checks,'V4 orientation, explicit transfer, consent to insert, unknowns, languages, legacy/expiry, safe rendering, storage failure; no real email.');
