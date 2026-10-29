import {chromium,webkit} from 'playwright';import assert from 'node:assert/strict';
const langs=['fr','en','pt-BR','es'],pages=['index','solutions','pipelines','approche','realisations','diagnostic','contact','merci','mentions-legales','confidentialite'];
let checks=0;
for(const [engineName,engine] of Object.entries({chromium,webkit})){
 const browser=await engine.launch();
 for(const width of [320,390,768,1024,1280]){
  const context=await browser.newContext({viewport:{width,height:844},locale:'fr-FR'});context.setDefaultTimeout(15000);context.setDefaultNavigationTimeout(15000);const page=await context.newPage();
  await page.route('https://api.cln-performance.com/**',async route=>{const url=new URL(route.request().url());if(url.searchParams.get('op')==='human'){await route.fulfill({status:200,headers:{'Access-Control-Allow-Origin':'http://127.0.0.1:8000'},contentType:'application/json',body:JSON.stringify({expires:Math.floor(Date.now()/1000)+600,token:'test-token'})});}else await route.abort();});
  for(const lang of langs)for(const name of pages){
   await page.goto(`http://127.0.0.1:8000/${name}.html?lang=${lang}`);await page.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');assert.equal(await page.locator('html').getAttribute('lang'),lang);assert.equal(await page.locator('#site-language').inputValue(),lang);
   const overflow=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:document.documentElement.clientWidth,offenders:[...document.querySelectorAll('main *,header *,footer *')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1).slice(0,5).map(e=>({tag:e.tagName,id:e.id,cls:e.className,right:e.getBoundingClientRect().right}))}));assert(overflow.scroll<=overflow.width+1,`${engineName} ${width} ${lang} ${name} overflow ${JSON.stringify(overflow)}`);
   assert.equal(await page.locator('nav a').count(),7);assert(!(await page.title()).includes('undefined'));
   if(lang!=='fr'){const home=await page.locator('nav a').first().textContent();assert(!home.includes('Accueil'));}
   if(name==='contact'){
    await page.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
    assert.equal(await page.locator('#human-dialog').isVisible(),false);
    assert.equal(await page.locator('#captcha-answer').count(),0);
    assert.equal(await page.locator('input[name=website]').isVisible(),false);
    await page.locator('#contact-form [type=submit]').click();assert.equal(await page.locator('#human-dialog').isVisible(),false);
    await page.locator('#name').fill('Texte libre <test>');await page.locator('#email').fill('contact@example.invalid');await page.locator('#message').fill('Do not translate <b>visitor text</b>');await page.locator('[name=consent]').check();
    const next=lang==='es'?'en':'es';await page.locator('#site-language').selectOption(next);
    assert.equal(await page.locator('#message').inputValue(),'Do not translate <b>visitor text</b>');
    await page.locator('#contact-form [type=submit]').click();await page.waitForFunction(()=>!document.querySelector('#human-check').disabled);
    assert(await page.locator('#human-dialog').isVisible());assert.equal(await page.locator('#human-check').isChecked(),false);assert.equal(await page.locator('#human-confirm').isEnabled(),false);
    assert.equal(await page.locator('#human-title').textContent(),next==='en'?'Human verification':'Verificación humana');
    const box=await page.locator('#human-dialog').boundingBox();assert(box.x>=0&&box.y>=0&&box.x+box.width<=width+1&&box.y+box.height<=844+1);
    await page.locator('#human-check').check();assert(await page.locator('#human-confirm').isEnabled());await page.locator('#human-check').uncheck();assert.equal(await page.locator('#human-confirm').isEnabled(),false);
    await page.locator('#human-cancel').click();assert.equal(await page.locator('#human-dialog').isVisible(),false);assert.equal(await page.locator('#message').inputValue(),'Do not translate <b>visitor text</b>');
    assert.equal(await page.evaluate(()=>document.activeElement===document.querySelector('#contact-form [type=submit]')),true);
    await page.locator('#contact-form [type=submit]').click();await page.keyboard.press('Escape');assert.equal(await page.locator('#human-dialog').isVisible(),false);
   }
   checks++;
  }
  await page.goto('http://127.0.0.1:8000/diagnostic.html?lang=en');await page.waitForFunction(()=>document.documentElement.dataset.i18nReady==='true');
  await page.locator('[name=problems][value=repetitif]').check();
  for(const name of ['frequency','people','goal','horizon'])await page.locator(`[name=${name}][value=inconnu]`).check();
  await page.locator('#diagnostic-form [type=submit]').click();assert(await page.locator('#diagnostic-resultat').isVisible());
  await page.locator('#site-language').selectOption('pt-BR');assert(await page.locator('[name=problems][value=repetitif]').isChecked());
  await page.locator('#summary-transfer').click();await page.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
  assert.equal(await page.locator('#message').inputValue(),'');await page.locator('#recommendation-add').click();
  assert((await page.locator('#message').inputValue()).includes('Sua síntese indicativa'));await page.locator('#recommendation-clear').click();
  assert.equal(await page.locator('#message').inputValue(),'');assert.equal(await page.evaluate(()=>localStorage.getItem('clnRecommendation')),null);
  await context.close();
 }
 await browser.close();
}
console.log('PASS',checks,'multilingual page layouts plus language changes, diagnostic, user text preservation and safe rendering. No email sent.');
