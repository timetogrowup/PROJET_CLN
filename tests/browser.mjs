import {chromium,webkit} from 'playwright';import assert from 'node:assert/strict';
const langs=['fr','en','pt-BR','es'],pages=['index','solutions','approche','realisations','diagnostic','contact','merci','mentions-legales','confidentialite'];
let checks=0;
for(const [engineName,engine] of Object.entries({chromium,webkit})){
 const browser=await engine.launch();
 for(const width of [320,390,768,1024,1280]){
  const context=await browser.newContext({viewport:{width,height:844},locale:'fr-FR'});context.setDefaultTimeout(15000);context.setDefaultNavigationTimeout(15000);const page=await context.newPage();
  await page.route('https://api.cln-performance.com/**',async route=>{const url=new URL(route.request().url());if(url.searchParams.get('op')==='challenge'){await route.fulfill({status:200,headers:{'Access-Control-Allow-Origin':'http://127.0.0.1:8000'},contentType:'application/json',body:JSON.stringify({a:3,b:4,expires:Math.floor(Date.now()/1000)+600,token:'test-token'})});}else await route.abort();});
  for(const lang of langs)for(const name of pages){
   await page.goto(`http://127.0.0.1:8000/${name}.html?lang=${lang}`);await page.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');assert.equal(await page.locator('html').getAttribute('lang'),lang);assert.equal(await page.locator('#site-language').inputValue(),lang);
   const overflow=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:document.documentElement.clientWidth}));assert(overflow.scroll<=overflow.width+1,`${engineName} ${width} ${lang} ${name} overflow ${JSON.stringify(overflow)}`);
   assert.equal(await page.locator('nav a').count(),6);assert(!(await page.title()).includes('undefined'));
   if(lang!=='fr'){const home=await page.locator('nav a').first().textContent();assert(!home.includes('Accueil'));}
   if(name==='contact'){await page.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);assert.equal(await page.locator('input[name=website]').isVisible(),false);await page.locator('#name').fill('Texte libre <test>');await page.locator('#message').fill('Do not translate <b>visitor text</b>');const next=lang==='es'?'en':'es';await page.locator('#site-language').selectOption(next);assert.equal(await page.locator('#message').inputValue(),'Do not translate <b>visitor text</b>');assert.equal(await page.locator('#name').inputValue(),'Texte libre <test>');assert.equal(await page.locator('#captcha-question').textContent(),next==='en'?'What is 3 + 4?':'¿Cuánto es 3 + 4?');}
   checks++;
  }
  await page.goto('http://127.0.0.1:8000/diagnostic.html?lang=en');await page.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');await page.locator('[name=modules][value=liberer]').check();await page.locator('[name=modules][value=autre]').check();await page.locator('#autre-enjeu').fill('<img src=x onerror=alert(1)>');await page.locator('[name=taille][value=moyenne]').check();await page.locator('[name=delai][value=moyen]').check();await page.locator('[name=mode][value=flash]').check();await page.locator('#priorite-toggle').check();await page.locator('#diagnostic-form [type=submit]').click();assert(await page.locator('#diagnostic-resultat').isVisible());const summary=await page.locator('#resultat-insights').textContent();await page.locator('#site-language').selectOption('pt-BR');assert(await page.locator('[name=modules][value=liberer]').isChecked());assert.equal(await page.locator('#autre-enjeu').inputValue(),'<img src=x onerror=alert(1)>');assert(!(await page.locator('#resultat-insights').textContent()).includes('Main priorities'));assert.equal(await page.locator('#resultat-insights img').count(),0);await page.locator('#diagnostic-resultat a').click();await page.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');assert((await page.locator('#message').inputValue()).includes('Prioridade'));await page.locator('#recommendation-clear').click();assert.equal(await page.locator('#message').inputValue(),'');assert.equal(await page.evaluate(()=>localStorage.getItem('clnRecommendation')),null);
  await context.close();
 }
 await browser.close();
}
console.log('PASS',checks,'multilingual page layouts plus language changes, diagnostic, user text preservation and safe rendering. No email sent.');
