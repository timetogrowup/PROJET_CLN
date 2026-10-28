import {chromium,webkit} from 'playwright';
import assert from 'node:assert/strict';
for(const engine of [chromium,webkit]){
 const browser=await engine.launch(),context=await browser.newContext({viewport:{width:1280,height:844}}),page=await context.newPage();
 let gets=0,posts=0,mode='ok',issuedExpiry=0,posted;
 await page.route('https://api.cln-performance.com/**',async route=>{
  const request=route.request();
  if(request.method()==='POST'){posts++;posted=new URLSearchParams(request.postData());await route.fulfill({status:200,contentType:'text/html',body:'<p>Mock accepted</p>'});return;}
  gets++;
  if(mode==='fail'){await route.fulfill({status:503,headers:{'Access-Control-Allow-Origin':'http://127.0.0.1:8000'}});return;}
  if(mode==='slow')await new Promise(r=>setTimeout(r,150));
  issuedExpiry=Math.floor(Date.now()/1000)+600+(mode==='renewed'?601:0);
  await route.fulfill({status:200,headers:{'Access-Control-Allow-Origin':'http://127.0.0.1:8000'},contentType:'application/json',body:JSON.stringify({token:'test-human-token',expires:issuedExpiry})}).catch(()=>{});
 });
 await page.goto('http://127.0.0.1:8000/contact.html?lang=fr');await page.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
 assert.equal(gets,0,'no verification request before submit');
 await page.locator('#contact-form [type=submit]').click();assert.equal(gets,0,'invalid form does not request verification');
 await page.locator('#name').fill('Test');await page.locator('#email').fill('contact@example.invalid');await page.locator('#message').fill('Do not send real mail');await page.locator('[name=consent]').check();
 mode='fail';await page.locator('#contact-form [type=submit]').click();await page.locator('#human-retry').waitFor({state:'visible'});assert.equal(await page.locator('#human-confirm').isEnabled(),false);assert.equal(posts,0);
 mode='ok';await page.locator('#human-retry').click();await page.waitForFunction(()=>!document.querySelector('#human-check').disabled);
 await page.keyboard.press('Tab');assert(await page.evaluate(()=>document.querySelector('#human-dialog').contains(document.activeElement)),'focus contained');
 await page.locator('#human-cancel').click();
 mode='slow';await page.locator('#contact-form [type=submit]').click();await page.locator('#human-cancel').click();await page.waitForTimeout(200);assert.equal(await page.locator('#human-dialog').isVisible(),false,'late response does not reopen');
 mode='ok';await page.locator('#contact-form [type=submit]').click();await page.waitForFunction(()=>!document.querySelector('#human-check').disabled);
 const first=await page.locator('#human-dialog').boundingBox();await page.locator('#human-cancel').click();await page.locator('#contact-form [type=submit]').click();await page.waitForFunction(()=>!document.querySelector('#human-check').disabled);const second=await page.locator('#human-dialog').boundingBox();assert(first.x!==second.x||first.y!==second.y,'desktop position changes');
 // Simulated clock expiry in isolated browser fixture only.
 await page.evaluate(expiry=>{const real=Date.now;Date.now=()=>Math.max(real(),expiry*1000+1);},issuedExpiry);
 mode='renewed';await page.locator('#human-check').check();await page.locator('#human-confirm').click();await page.waitForFunction(()=>!document.querySelector('#human-check').disabled);assert.equal(await page.locator('#human-check').isChecked(),false);assert.equal(posts,0,'expired verification never sends');
 // Reset clock by reloading, then simulate two same-task clicks; only one POST may leave.
 await page.reload();await page.waitForFunction(()=>!document.querySelector('#contact-form [type=submit]').disabled);
 await page.locator('#name').fill('Test');await page.locator('#email').fill('contact@example.invalid');await page.locator('#message').fill('Do not send real mail');await page.locator('[name=consent]').check();
 await page.locator('#contact-form [type=submit]').click();await page.waitForFunction(()=>!document.querySelector('#human-check').disabled);await page.locator('#human-check').check();
 await page.evaluate(()=>{document.querySelector('#human-confirm').click();document.querySelector('#human-confirm').click();});
 await page.waitForURL('https://api.cln-performance.com/contact.php');assert.equal(posts,1);assert.equal(posted.get('human_confirmed'),'1');assert.equal(posted.get('human_token'),'test-human-token');assert.equal(posted.has('captcha_answer'),false);
 await browser.close();
}
console.log('PASS human dialog: delayed verification, invalid fields, network error/retry, cancellation race, focus, random position, expiry/reconfirmation and exactly one mocked POST in Chromium and WebKit. No email sent.');
