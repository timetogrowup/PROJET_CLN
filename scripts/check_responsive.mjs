import { chromium, webkit } from 'playwright';
import assert from 'node:assert/strict';

const pages = ['index.html','solutions.html','approche.html','realisations.html','diagnostic.html','contact.html','merci.html','mentions-legales.html','confidentialite.html'];
let failures = 0;
for (const [engineName, engine] of Object.entries({chromium, webkit})) {
  const browser = await engine.launch();
  for (const width of [320,375,390,768,820,1024,1100,1280]) {
    const context = await browser.newContext({viewport:{width,height:844},isMobile:true,hasTouch:true,locale:'fr-FR',timezoneId:'Europe/Paris'});
    const page = await context.newPage();
    for (const name of pages) {
      const response = await page.goto('http://127.0.0.1:8000/' + name);
      assert.equal(response.status(),200);
      await page.locator('body').waitFor();
      const check = await page.evaluate(() => {
        const width = document.documentElement.clientWidth;
        const offenders = [...document.querySelectorAll('main *,header *')].filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 0 && (r.right > width + 1 || r.left < -1);
        }).slice(0,8).map(el => ({tag:el.tagName,id:el.id,class:el.className}));
        return {viewport:width,scroll:document.documentElement.scrollWidth,offenders};
      });
      const overflow = check.scroll > check.viewport + 1;
      if (overflow) {failures++;console.log('OVERFLOW',engineName,width,name,JSON.stringify(check));}
      const links = page.locator('nav a');
      assert.equal(await links.count(),5);
      for (const link of await links.all()) assert(await link.isVisible());
      if (name === 'contact.html') {
        assert(await page.locator('#contact-form').isVisible());
        assert.equal(await page.locator('#recommendation-preview').count(),0);
        assert.equal(await page.locator('input[name="website"]').isVisible(),false);
      }
      console.log('LAYOUT',engineName,width,name,overflow?'FAIL':'PASS');
    }
    await page.goto('http://127.0.0.1:8000/contact.html');
    await page.getByRole('button',{name:'Envoyer la demande'}).click();
    assert.equal(await page.locator('#contact-form').evaluate(el=>el.checkValidity()),false);
    assert((await page.url()).endsWith('/contact.html'));
    await context.close();
  }
  await browser.close();
}
assert.equal(failures,0,failures+' responsive layouts overflow');
console.log('Responsive layout checks and required-field validation passed. No email sent.');
