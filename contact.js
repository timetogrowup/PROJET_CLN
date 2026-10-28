CLN.ready.then(async () => {
  if(document.documentElement.dataset.i18nReady!=='true')return;
  const form=document.querySelector('#contact-form');if(!form)return;
  const button=form.querySelector('[type="submit"]'),dialog=document.querySelector('#human-dialog'),check=document.querySelector('#human-check'),confirm=document.querySelector('#human-confirm'),cancel=document.querySelector('#human-cancel'),retry=document.querySelector('#human-retry'),humanStatus=document.querySelector('#human-status'),alert=document.querySelector('#form-alert');
  const preview=document.querySelector('#recommendation-preview'),content=document.querySelector('#recommendation-content'),date=document.querySelector('#recommendation-date'),message=form.elements.message;
  for(const el of [humanStatus,alert,content,date])el.dataset.dynamic='true';
  let challenge=null,state='closed',generation=0,controller=null,statusKey='',previousPrefill='',data=CLN.readSummary();
  const params=new URLSearchParams(location.search),status=params.get('status');
  const storageKey='clnContactDraft';
  try{const draft=JSON.parse(sessionStorage.getItem(storageKey)||'null');if(status==='success'){sessionStorage.removeItem(storageKey);}else if(draft&&draft.expires>Date.now()){for(const key of ['name','_replyto','company','message'])if(typeof draft.fields?.[key]==='string')form.elements[key].value=draft.fields[key];}else sessionStorage.removeItem(storageKey);}catch(_){}
  function renderSummary(){
    if(!data){preview.hidden=true;return;}preview.hidden=false;
    if(data.version!==2||!data.answers){content.textContent=CLN.t('old_summary');return;}
    const text=CLN.summaryText(data.answers);content.textContent=text;content.style.whiteSpace='pre-line';date.textContent=CLN.t('summary_date',{date:new Intl.DateTimeFormat(CLN.lang,{dateStyle:'long',timeStyle:'short'}).format(new Date(data.generatedAt))});
    const next=text+'\n\n'+CLN.t('meeting_request');if(!message.value||message.value===previousPrefill){message.value=next;previousPrefill=next;}
  }
  function showAlert(){if(!status)return;const known=['invalid','error','rate','human_required','human_invalid','human_used','forbidden','too_large'];if(!known.includes(status))return;const seconds=Math.min(3600,Math.max(1,Number(params.get('wait'))||60));alert.textContent=CLN.t(status,{minutes:new Intl.NumberFormat(CLN.lang).format(Math.ceil(seconds/60))});alert.className='form-alert form-alert--error';alert.hidden=false;}
  function renderHuman(){
    form.elements.lang.value=CLN.lang;showAlert();
    humanStatus.textContent=statusKey?CLN.t(statusKey):'';
    confirm.disabled=state!=='ready'||!check.checked||!challenge;
    check.disabled=state!=='ready';cancel.disabled=state==='sending';
    retry.hidden=state!=='error';
    const active=document.activeElement;
    if(dialog.open&&dialog.contains(active)&&(active.disabled||active.hidden))(state==='ready'?check:cancel).focus();
  }
  function positionDialog(randomise=false){
    if(!dialog.open)return;
    const w=document.documentElement.clientWidth,h=window.innerHeight,box=dialog.getBoundingClientRect(),gap=16;
    const maxX=Math.max(gap,w-box.width-gap),maxY=Math.max(gap,h-box.height-gap);
    const small=w<768||h<520;
    let x=small?(w-box.width)/2:randomise?gap+Math.random()*(maxX-gap):Math.min(maxX,Math.max(gap,box.x));
    let y=small?(h-box.height)/2:randomise?gap+Math.random()*(maxY-gap):Math.min(maxY,Math.max(gap,box.y));
    dialog.style.left=Math.max(gap,x)+'px';dialog.style.top=Math.max(gap,y)+'px';
  }
  async function prepare(){
    const request=++generation;controller?.abort();controller=new AbortController();
    state='loading';statusKey='human_loading';challenge=null;check.checked=false;
    form.elements.human_token.value='';form.elements.human_confirmed.value='';renderHuman();
    const timeout=setTimeout(()=>{if(request===generation)controller?.abort();},20000);
    try{
      const url=new URL(form.action);url.searchParams.set('op','human');
      const r=await fetch(url,{credentials:'omit',cache:'no-store',signal:controller.signal});
      if(!r.ok)throw Error('human');const item=await r.json();
      if(typeof item.token!=='string'||!item.token||!Number.isInteger(item.expires)||item.expires*1000<=Date.now())throw Error('human');
      if(request!==generation||!dialog.open)return;
      challenge=item;state='ready';statusKey='';
    }catch(_){if(request!==generation||!dialog.open)return;state='error';statusKey='human_unavailable';}
    finally{clearTimeout(timeout);if(request===generation&&dialog.open){renderHuman();positionDialog();}}
  }
  function reset(){
    ++generation;controller?.abort();controller=null;challenge=null;check.checked=false;
    form.elements.human_token.value='';form.elements.human_confirmed.value='';
    if(state!=='sending'){state='closed';button.disabled=false;button.focus();}
  }
  cancel.addEventListener('click',()=>dialog.close());
  dialog.addEventListener('cancel',event=>{if(state==='sending')event.preventDefault();});
  dialog.addEventListener('close',reset);
  dialog.addEventListener('keydown',event=>{
    if(event.key!=='Tab')return;
    const items=[...dialog.querySelectorAll('button,input,[tabindex]')].filter(el=>!el.disabled&&!el.hidden&&el.getClientRects().length);
    if(!items.length){event.preventDefault();return;}
    const index=items.indexOf(document.activeElement);
    if(event.shiftKey&&index<=0){event.preventDefault();items.at(-1).focus();}
    else if(!event.shiftKey&&(index<0||index===items.length-1)){event.preventDefault();items[0].focus();}
  });
  check.addEventListener('change',renderHuman);
  retry.addEventListener('click',prepare);
  window.addEventListener('resize',()=>positionDialog());
  confirm.addEventListener('click',()=>{
    if(state!=='ready'||!check.checked||!challenge)return;
    if(challenge.expires*1000<=Date.now()){
      prepare().then(()=>{if(dialog.open&&state==='ready'){statusKey='human_invalid';renderHuman();}});return;
    }
    if(!form.reportValidity()){dialog.close();return;}
    state='sending';statusKey='human_sending';button.disabled=true;renderHuman();
    form.elements.human_token.value=challenge.token;form.elements.human_confirmed.value='1';
    try{const fields={};for(const k of ['name','_replyto','company','message'])fields[k]=form.elements[k].value;sessionStorage.setItem(storageKey,JSON.stringify({fields,expires:Date.now()+30*60000}));}catch(_){}
    HTMLFormElement.prototype.submit.call(form);
  });
  document.querySelector('#recommendation-clear').addEventListener('click',()=>{try{localStorage.removeItem('clnRecommendation');}catch(_){}if(message.value===previousPrefill)message.value='';previousPrefill='';data=null;renderSummary();});
  window.addEventListener('cln:language',()=>{renderSummary();renderHuman();positionDialog();});
  form.addEventListener('submit',event=>{
    event.preventDefault();if(state==='sending'||dialog.open)return;
    if(!form.reportValidity())return;
    dialog.showModal();positionDialog(true);prepare();
  });
  window.addEventListener('pageshow',event=>{if(event.persisted){state='closed';if(dialog.open)dialog.close();reset();}});
  renderSummary();showAlert();button.disabled=false;
});
