import vm from 'node:vm';import assert from 'node:assert/strict';import {readFileSync,writeFileSync} from 'node:fs';
const messages=JSON.parse(readFileSync('i18n/messages.json','utf8'));
const dataCode=readFileSync('case-data.js','utf8'),contactCode=readFileSync('contact.js','utf8'),questionCode=readFileSync('diagnostic.js','utf8');
function language(lang='fr'){return {lang,ready:Promise.resolve(),t(k,v={}){return (messages[k]?.[this.lang]||k).replace(/\{(\w+)\}/g,(_,x)=>v[x]??'')}};}
function storage(initial={},fail=false){const map=new Map(Object.entries(initial));return {map,getItem:k=>map.get(k)??null,setItem(k,v){if(fail)throw Error('blocked');map.set(k,v)},removeItem:k=>map.delete(k)};}
class E{constructor(value=''){this.value=value;this.hidden=true;this.disabled=false;this.checked=false;this.dataset={};this.events={};this.style={};this.open=false;this.validityMessage='';}addEventListener(k,fn){this.events[k]=fn}focus(){}setCustomValidity(s){this.validityMessage=s}getBoundingClientRect(){return {width:400,height:300,x:16,y:16}}contains(){return false}showModal(){this.open=true}close(){this.open=false;this.events.close?.()}querySelectorAll(){return []}}
const raw={applications:'a4_10',people:'p11_50',connections:'partial',difficulties:['reentry','quality'],goals:['productivity','modernise'],approach:'existing',horizon:'m3_6',situation:'Ressaisies entre trois outils. Équipe <b>terrain</b>.'};
const item=(id='new-case')=>({version:11,id,generatedAt:new Date().toISOString(),answers:structuredClone(raw)});
async function contact({lang='fr',store=storage(),search='?summary=1',failFetch=false}={}){
 const w={CLN:language(lang),events:{},innerHeight:900,addEventListener(k,f){this.events[k]=f}};const form=new E();form.elements={};for(const name of ['name','_replyto','company','message','lang','human_token','human_confirmed'])form.elements[name]=new E(name==='lang'?lang:'');form.reportValidity=()=>true;const submit=new E();form.querySelector=()=>submit;form.action='https://api.cln-performance.com/contact.php';
 const els=Object.fromEntries(['human-dialog','human-check','human-confirm','human-cancel','human-retry','human-status','form-alert','case-transfer-notice','case-restart','case-draft-warning'].map(k=>[k,new E()]));
 const doc={documentElement:{dataset:{i18nReady:'true'},clientWidth:1280},querySelector:s=>s==='#contact-form'?form:els[s.slice(1)],activeElement:null};
 let posts=[],gets=0;const ctx={window:w,CLN:w.CLN,document:doc,sessionStorage:store,location:{search},URLSearchParams,URL,Date,AbortController,setTimeout,clearTimeout,HTMLFormElement:{prototype:{submit(){posts.push(Object.fromEntries(Object.entries(this.elements).map(([k,e])=>[k,e.value])))}}},fetch:async()=>{gets++;if(failFetch)throw Error('test');return {ok:true,json:async()=>({token:'fixture-token',expires:Math.floor(Date.now()/1000)+600})}}};
 vm.runInNewContext(dataCode,ctx);vm.runInNewContext(contactCode,ctx);await new Promise(setImmediate);
 return {w,form,submit,els,store,ctx,posts,get gets(){return gets}};
}
const mailFixtures=[];
for(const lang of ['fr','en','pt-BR','es']){
 const st=storage({clnCaseTransfer:JSON.stringify(item())});const c=await contact({lang,store:st});const expected=c.w.CLNCase.summary(raw);
 assert.equal(c.form.elements.message.value,expected);assert.equal(st.getItem('clnCaseTransfer'),null);assert.equal(c.gets,0);assert.equal(c.posts.length,0);
 c.form.elements.name.value='Test';c.form.elements._replyto.value='test@example.invalid';c.form.elements.message.value=expected+'\nCorrection personnelle : éèà <script>texte seulement</script>.';c.form.events.input();
 const edited=c.form.elements.message.value;const reload=await contact({lang,store:st});assert.equal(reload.form.elements.message.value,edited);assert(reload.els['case-transfer-notice'].hidden);
 reload.w.CLN.lang=lang==='fr'?'en':'fr';reload.w.events['cln:language']();assert.equal(reload.form.elements.message.value,edited,'edited visitor text must survive language changes');
 const retry=await contact({lang,store:st,search:'?status=error&lang='+lang});assert.equal(retry.form.elements.message.value,edited);assert(!retry.els['form-alert'].hidden);
 c.form.events.submit({preventDefault(){}});await new Promise(setImmediate);assert.equal(c.gets,1);assert(c.els['human-dialog'].open);c.els['human-check'].checked=true;c.els['human-check'].events.change();c.els['human-confirm'].events.click();assert.equal(c.posts.length,1);assert.equal(c.posts[0].message,edited);assert.equal(c.posts[0].human_confirmed,'1');
 mailFixtures.push({lang,message:edited});
 st.setItem('clnCaseTransfer',JSON.stringify(item('second-case')));const replaced=await contact({lang,store:st});assert.equal(replaced.form.elements.message.value,expected);assert.equal(replaced.form.elements.name.value,'Test');
}
const old=item();old.version=6;const cOld=await contact({store:storage({clnCaseTransfer:JSON.stringify(old)})});assert(!cOld.els['case-transfer-notice'].hidden);assert.equal(cOld.form.elements.message.value,'');
const expired=item();expired.generatedAt=new Date(Date.now()-31*60000).toISOString();assert(!(await contact({store:storage({clnCaseTransfer:JSON.stringify(expired)})})).els['case-transfer-notice'].hidden);
const fresh=await contact({store:storage({clnCaseTransfer:JSON.stringify(item())})});fresh.w.CLN.lang='en';fresh.w.events['cln:language']();assert(fresh.form.elements.message.value.startsWith('Your situation'));
assert(!fresh.w.CLNCase.valid({...item(),answers:{}}));assert(!fresh.w.CLNCase.valid({...item(),generatedAt:new Date(Date.now()+60000).toISOString()}));assert.equal(fresh.w.CLNCase.clean(null).applications,'inconnu');assert.deepEqual(Array.from(fresh.w.CLNCase.clean({goals:['inconnu','quality']}).goals),['inconnu']);
const blocked=await contact({store:storage({clnCaseTransfer:JSON.stringify(item())},true)});assert(!blocked.els['case-draft-warning'].hidden);assert(blocked.store.getItem('clnCaseTransfer'));assert(blocked.form.elements.message.value);
const success=await contact({store:storage({clnCaseTransfer:JSON.stringify(item()),clnContactDraft:JSON.stringify({expires:Date.now()+1000,fields:{message:'old'}})}),search:'?status=success'});assert.equal(success.store.getItem('clnContactDraft'),null);assert.equal(success.store.getItem('clnCaseTransfer'),null);
async function questionnaire(fail=false){
 const w={CLN:language(),events:{},addEventListener(k,f){this.events[k]=f}};const st=storage({},fail),els={'case-transfer-error':new E(),'case-transfer-fallback':new E(),'case-copy':new E()},form=new E(),button=new E(),dest=[];
 const ctx={window:w,CLN:w.CLN,document:null,sessionStorage:st,location:{assign:u=>dest.push(u)},crypto:{randomUUID:()=> 'test-case'},Date,encodeURIComponent};vm.runInNewContext(dataCode,ctx);
 const inputs=[];form.elements={situation:new E(raw.situation)};
 for(const [name,codes] of Object.entries(w.CLNCase.choices)){
  for(const code of codes){const el=new E(code);el.name=name;el.checked=w.CLNCase.multi.includes(name)?raw[name].includes(code):raw[name]===code;inputs.push(el);}
  form.elements[name]={get value(){return inputs.find(e=>e.name===name&&e.checked)?.value||''}};
 }
 form.querySelectorAll=s=>{const name=s.match(/name="([^"]+)"/)[1];return inputs.filter(e=>e.name===name&&(!s.includes(':checked')||e.checked));};
 form.querySelector=s=>s==='[type=submit]'?button:inputs.find(e=>e.name===s.match(/name="([^"]+)"/)[1]&&(!s.includes('value=')||e.value==='inconnu'));
 form.reportValidity=()=>!inputs.some(e=>e.validityMessage);
 ctx.document={documentElement:{dataset:{i18nReady:'true'}},querySelector:s=>s==='#diagnostic-form'?form:els[s.slice(1)]};vm.runInNewContext(questionCode,ctx);await new Promise(setImmediate);
 return {w,st,form,inputs,els,dest};
}
const q=await questionnaire();const third=q.inputs.find(e=>e.name==='goals'&&e.value==='quality');third.checked=true;q.form.events.change({target:third});q.form.events.submit({preventDefault(){}});assert.equal(q.dest.length,0,'three goals must block transfer');
const unknown=q.inputs.find(e=>e.name==='goals'&&e.value==='inconnu');unknown.checked=true;q.form.events.change({target:unknown});assert.equal(q.inputs.filter(e=>e.name==='goals'&&e.checked).length,1);q.form.events.submit({preventDefault(){}});assert.equal(q.dest[0],'contact.html?summary=1&lang=fr');assert(!q.dest[0].includes('Ressaisies'));assert.equal(JSON.parse(q.st.getItem('clnCaseTransfer')).version,11);
const qb=await questionnaire(true);qb.form.events.submit({preventDefault(){}});assert.equal(qb.dest.length,0);assert(!qb.els['case-transfer-fallback'].hidden);assert(qb.els['case-copy'].value.includes('Applications concernées'));
if(process.argv[2])writeFileSync(process.argv[2],JSON.stringify(mailFixtures));
console.log('PASS V11: four-language handoff, automatic editable message, reload/error/new transfer, untouched/edited language changes, legacy/expiry, blocked storage, exclusive unknowns/two-goal limit and native form payload. No network or email.');
