/* V11: explicit questionnaire validation hands a factual summary to Contact. No submission request. */
CLN.ready.then(()=>{
 if(document.documentElement.dataset.i18nReady!=='true')return;
 const form=document.querySelector('#diagnostic-form');if(!form)return;
 const data=window.CLNCase,button=form.querySelector('[type=submit]'),error=document.querySelector('#case-transfer-error'),fallback=document.querySelector('#case-transfer-fallback'),copy=document.querySelector('#case-copy');
 const selected=name=>[...form.querySelectorAll(`[name="${name}"]:checked`)].map(el=>el.value);
 function validate(){
  for(const name of data.multi){const values=selected(name),first=form.querySelector(`[name="${name}"]`);first.setCustomValidity(values.length===0?CLN.t('case.select'):name==='goals'&&values.length>2?CLN.t('case.max'):'');}
 }
 form.addEventListener('change',event=>{
  const input=event.target;
  if(data.multi.includes(input.name)&&input.checked){
   if(input.value==='inconnu')form.querySelectorAll(`[name="${input.name}"]:checked`).forEach(el=>{if(el!==input)el.checked=false;});
   else form.querySelector(`[name="${input.name}"][value="inconnu"]`).checked=false;
  }
  validate();error.hidden=true;fallback.hidden=true;
 });
 form.addEventListener('input',validate);
 form.addEventListener('submit',event=>{
  event.preventDefault();validate();if(!form.reportValidity())return;
  const raw={};for(const name of Object.keys(data.choices))raw[name]=data.multi.includes(name)?selected(name):form.elements[name].value;
  raw.situation=form.elements.situation.value;
  const id=typeof crypto.randomUUID==='function'?crypto.randomUUID():Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
  const item={version:11,id,generatedAt:new Date().toISOString(),answers:data.clean(raw)};
  try{sessionStorage.setItem('clnCaseTransfer',JSON.stringify(item));}
  catch(_){error.textContent=CLN.t('case.storage');error.hidden=false;copy.value=data.summary(item.answers);fallback.hidden=false;copy.focus();return;}
  location.assign('contact.html?summary=1&lang='+encodeURIComponent(CLN.lang));
 });
 window.addEventListener('cln:language',()=>{validate();if(!error.hidden)error.textContent=CLN.t('case.storage');});
 validate();button.disabled=false;
});
