/* V4: everyday needs, local orientation, explicit transfer. No server request. */
CLN.ready.then(() => {
  if (document.documentElement.dataset.i18nReady !== 'true') return;
  const choices = {
    problems:['ressaisies','repetitif','chiffres','suivi','personne','autre','inconnu'],
    frequency:['jour','semaine','parfois','inconnu'],people:['une','dix','cinquante','plus','inconnu'],
    impacts:['temps','erreurs','retards','decision','insatisfaction','autre','inconnu'],
    tools:['fichiers','emails','metier','plusieurs','inconnu'],goal:['temps','fiabilite','suivi','partage','inconnu'],
    horizon:['vite','mois','reflexion','inconnu']
  };
  const multi = ['problems','impacts','tools'];
  const clean = answers => Object.fromEntries(Object.entries(choices).map(([key,allowed])=>{
    const raw=answers?.[key];
    if(multi.includes(key)) {
      const selected=[...new Set((Array.isArray(raw)?raw:[]).filter(x=>typeof x==='string'&&allowed.includes(x)))];
      return [key,selected.length>1?selected.filter(x=>x!=='inconnu'):selected];
    }
    return [key,allowed.includes(raw)?raw:'inconnu'];
  }));
  CLN.orientation = answers => {
    const a=clean(answers), precise=a.problems.filter(k=>!['autre','inconnu'].includes(k));
    const explanation=CLN.t(precise.length===1&&a.problems.length===1?'v4.single':precise.length?'v4.multiple':'v4.unclear');
    const rows=Object.keys(choices).map(key=>({label:CLN.t('v4.field.'+key),value:multi.includes(key)?a[key].map(code=>CLN.t('v4.'+key+'.'+code)).join(' · ')||CLN.t('v4.none'):CLN.t('v4.'+key+'.'+a[key])}));
    const suggestions=precise.map(key=>CLN.t('v4.rec.'+key));
    return {rows,explanation,suggestions};
  };
  CLN.summaryText=answers=>{const s=CLN.orientation(answers);return [CLN.t('v4.title'),...s.rows.map(r=>r.label+' '+r.value),s.explanation,...s.suggestions].join('\n');};
  const form=document.querySelector('#diagnostic-form');if(!form)return;
  const result=document.querySelector('#diagnostic-resultat'),insights=document.querySelector('#resultat-insights'),transfer=document.querySelector('#summary-transfer'),error=document.querySelector('#summary-storage-error');
  let last=null,generatedAt=null;
  const selected=name=>[...form.querySelectorAll(`[name="${name}"]:checked`)].map(x=>x.value);
  function show(){
    if(!last)return;const s=CLN.orientation(last);insights.replaceChildren();
    const intro=document.createElement('p');intro.textContent=CLN.t('v4.intro');insights.append(intro);
    const list=document.createElement('dl');
    for(const row of s.rows){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=row.label;dd.textContent=row.value;list.append(dt,dd);}insights.append(list);
    const p=document.createElement('p');p.textContent=s.explanation;insights.append(p);
    if(s.suggestions.length){const h=document.createElement('h3');h.textContent=CLN.t('v4.next');insights.append(h);const ul=document.createElement('ul');for(const suggestion of s.suggestions){const li=document.createElement('li');li.textContent=suggestion;ul.append(li);}insights.append(ul);}
    result.hidden=false;
  }
  form.addEventListener('change',event=>{
    const input=event.target;
    if(multi.includes(input.name)&&input.checked){
      if(input.value==='inconnu')form.querySelectorAll(`[name="${input.name}"]:checked`).forEach(el=>{if(el!==input)el.checked=false;});
      else form.querySelector(`[name="${input.name}"][value="inconnu"]`).checked=false;
    }
    // An old result must never look like the synthesis of newly edited answers.
    last=null;result.hidden=true;error.hidden=true;
  });
  form.addEventListener('submit',event=>{
    event.preventDefault();if(!form.reportValidity())return;
    const raw={};for(const name of Object.keys(choices))raw[name]=multi.includes(name)?selected(name):form.elements[name].value;
    last=clean(raw);generatedAt=new Date().toISOString();show();result.focus();
  });
  transfer.addEventListener('click',event=>{
    if(!last){event.preventDefault();return;}
    if(!CLN.storeSummary({version:4,generatedAt,answers:last})){event.preventDefault();error.hidden=false;}
  });
  document.querySelector('#summary-edit').addEventListener('click',()=>{result.hidden=true;last=null;form.querySelector('input').focus();});
  window.addEventListener('cln:language',show);
});
