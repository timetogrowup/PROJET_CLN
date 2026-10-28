CLN.ready.then(async () => {
  if(document.documentElement.dataset.i18nReady!=='true')return;
  const form=document.querySelector('#contact-form');if(!form)return;
  const button=form.querySelector('[type="submit"]'), question=document.querySelector('#captcha-question'), answer=form.elements.captcha_answer, token=form.elements.captcha_token,refresh=document.querySelector('#captcha-refresh'),captchaStatus=document.querySelector('#captcha-status'),alert=document.querySelector('#form-alert');
  const preview=document.querySelector('#recommendation-preview'),content=document.querySelector('#recommendation-content'),date=document.querySelector('#recommendation-date'),message=form.elements.message;
  for(const el of [question,captchaStatus,alert,content,date])el.dataset.dynamic='true';
  let challenge=null,loading=false,previousPrefill='',data=CLN.readSummary();
  const params=new URLSearchParams(location.search),status=params.get('status');
  const storageKey='clnContactDraft';
  try{const draft=JSON.parse(sessionStorage.getItem(storageKey)||'null');if(status==='success'){sessionStorage.removeItem(storageKey);}else if(draft&&draft.expires>Date.now()){for(const key of ['name','_replyto','company','message'])if(typeof draft.fields?.[key]==='string')form.elements[key].value=draft.fields[key];}else sessionStorage.removeItem(storageKey);}catch(_){}
  function renderSummary(){
    if(!data){preview.hidden=true;return;}preview.hidden=false;
    if(data.version!==2||!data.answers){content.textContent=CLN.t('old_summary');return;}
    const text=CLN.summaryText(data.answers);content.textContent=text;content.style.whiteSpace='pre-line';date.textContent=CLN.t('summary_date',{date:new Intl.DateTimeFormat(CLN.lang,{dateStyle:'long',timeStyle:'short'}).format(new Date(data.generatedAt))});
    const next=text+'\n\n'+CLN.t('meeting_request');if(!message.value||message.value===previousPrefill){message.value=next;previousPrefill=next;}
  }
  function showAlert(){if(!status)return;const known=['invalid','error','rate','captcha_required','captcha_invalid','captcha_used','forbidden','too_large'];if(!known.includes(status))return;const seconds=Math.min(3600,Math.max(1,Number(params.get('wait'))||60));alert.textContent=CLN.t(status,{minutes:new Intl.NumberFormat(CLN.lang).format(Math.ceil(seconds/60))});alert.className='form-alert form-alert--error';alert.hidden=false;}
  function renderChallenge(){question.textContent=challenge?CLN.t('captcha_question',challenge):CLN.t('loading');form.elements.lang.value=CLN.lang;showAlert();}
  async function loadChallenge(){loading=true;button.disabled=true;refresh.disabled=true;challenge=null;token.value='';answer.value='';captchaStatus.textContent=CLN.t('loading');renderChallenge();
    try{const url=new URL(form.action);url.searchParams.set('op','challenge');url.searchParams.set('lang',CLN.lang);const r=await fetch(url,{credentials:'omit',cache:'no-store'});if(!r.ok)throw Error('challenge');const item=await r.json();if(!Number.isInteger(item.a)||!Number.isInteger(item.b)||typeof item.token!=='string'||!Number.isInteger(item.expires))throw Error('challenge');challenge=item;token.value=item.token;captchaStatus.textContent='';button.disabled=false;}catch(_){captchaStatus.textContent=CLN.t('captcha_unavailable');}finally{loading=false;refresh.disabled=false;renderChallenge();}
  }
  refresh.addEventListener('click',()=>loadChallenge());
  document.querySelector('#recommendation-clear').addEventListener('click',()=>{try{localStorage.removeItem('clnRecommendation');}catch(_){}if(message.value===previousPrefill)message.value='';previousPrefill='';data=null;renderSummary();});
  window.addEventListener('cln:language',()=>{renderSummary();renderChallenge();if(!challenge&&!loading)captchaStatus.textContent=CLN.t('captcha_unavailable');});
  form.addEventListener('submit',event=>{
    if(!challenge||challenge.expires*1000<=Date.now()){event.preventDefault();loadChallenge();captchaStatus.textContent=CLN.t('captcha_invalid');return;}
    try{const fields={};for(const k of ['name','_replyto','company','message'])fields[k]=form.elements[k].value;sessionStorage.setItem(storageKey,JSON.stringify({fields,expires:Date.now()+30*60000}));}catch(_){}
    button.disabled=true;refresh.disabled=true;
  });
  window.addEventListener('pageshow',event=>{if(event.persisted)loadChallenge();});
  renderSummary();showAlert();await loadChallenge();
});
