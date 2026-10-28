CLN.ready.then(() => {
  if (!window.CLN || document.documentElement.dataset.i18nReady!=='true') return;
  const labels={chirurgical:'Ciblé · Interventions ciblées',liberer:'Libéré · Automatisation',normaliser:'Normé · Gouvernance des données',securiser:'Sécuriser · Conformité',valoriser:'Valoriser · Analytics',collaborer:'Collaborer · Partage',anticiper:'Anticiper · Innovation'};
  CLN.moduleLabel=(key,custom='')=>key==='autre'?custom:CLN.translate(labels[key]||key);
  CLN.summary = answers => {
    const modules=Array.isArray(answers.modules)?answers.modules.filter(k=>k in labels):[];
    const custom=typeof answers.custom==='string'?answers.custom:'';
    const order=Array.isArray(answers.order)?answers.order.filter(k=>modules.includes(k)||(k==='autre'&&custom)):[];
    const first=answers.priorityEnabled?order[0]:null;
    const parts=modules.map(k=>CLN.t('summary.'+k));if(custom)parts.push(CLN.t('custom_summary',{text:custom}));
    return {
      organisation:CLN.t('organisation',{size:CLN.t('size.'+answers.taille),horizon:CLN.t('horizon.'+answers.delai)}),
      modules:parts.join(' ')||CLN.t('summary.default'),
      priorities:answers.priorityEnabled?CLN.t('priorities_order',{order:order.map((k,i)=>`${i+1}. ${CLN.moduleLabel(k,custom)}`).join(' · ')}):CLN.t('priorities_off'),
      recommendation:first?CLN.t('top',{label:CLN.moduleLabel(first,custom)})+' '+CLN.t('rec.'+first,{label:custom}):CLN.t('rec.default'),
      next:CLN.t('meeting.'+answers.delai)+' '+CLN.t('mode.'+answers.mode)
    };
  };
  CLN.summaryText=answers=>{const s=CLN.summary(answers);return [s.organisation,s.modules,s.priorities,s.recommendation,s.next].join('\n');};
  const form=document.querySelector('#diagnostic-form');if(!form)return;
  const list=document.querySelector('.priority-list'), toggle=document.querySelector('#priorite-toggle'), count=document.querySelector('#modules-count'),custom=form.elements.autreEnjeu, other=form.querySelector('[value="autre"]');
  const result=document.querySelector('#diagnostic-resultat'), insights=document.querySelector('#resultat-insights');
  for(const el of [list,count,insights])el.dataset.dynamic='true';
  let order=[],last=null,generatedAt=null;
  function currentModules(){return [...form.querySelectorAll('[name="modules"]:checked')].map(x=>x.value);}
  function renderPriorities(){
    const selected=currentModules();order=order.filter(k=>selected.includes(k));selected.forEach(k=>{if(!order.includes(k))order.push(k);});
    toggle.disabled=!selected.length;if(!selected.length)toggle.checked=false;
    list.replaceChildren();list.hidden=!toggle.checked;list.classList.toggle('is-disabled',!toggle.checked);list.setAttribute('aria-disabled',String(!toggle.checked));
    order.forEach((key,i)=>{const item=document.createElement('div');item.className='priority-item';item.setAttribute('role','listitem');const rank=document.createElement('span');rank.className='priority-rank';rank.textContent=i+1;const label=document.createElement('span');label.className='priority-label';label.textContent=CLN.moduleLabel(key,custom.value);item.append(rank,label);const actions=document.createElement('div');actions.className='priority-actions';for(const[delta,label,arrow]of [[-1,'up','▲'],[1,'down','▼']]){const b=document.createElement('button');b.type='button';b.className='priority-move';b.textContent=arrow;b.setAttribute('aria-label',CLN.t(label));b.disabled=!toggle.checked||i+delta<0||i+delta>=order.length;b.addEventListener('click',()=>{[order[i],order[i+delta]]=[order[i+delta],order[i]];renderPriorities();});actions.append(b);}item.append(actions);list.append(item);});
    count.textContent=CLN.t('selected',{count:new Intl.NumberFormat(CLN.lang).format(selected.length)});
  }
  function show(){if(!last)return;const s=CLN.summary(last);insights.replaceChildren();for(const[key,text]of [['profile',s.organisation],['main_needs',s.modules],['roadmap',s.priorities+' '+s.recommendation],['next_step',s.next]]){const p=document.createElement('p'),strong=document.createElement('strong');strong.textContent=CLN.t(key)+'. ';p.append(strong,document.createTextNode(text));insights.append(p);}result.hidden=false;}
  form.querySelectorAll('[name="modules"]').forEach(el=>el.addEventListener('change',()=>{custom.closest('.pill--custom').classList.toggle('is-active',other.checked);custom.required=other.checked;if(!other.checked){custom.value='';custom.setCustomValidity('');}renderPriorities();}));
  custom.addEventListener('input',renderPriorities);toggle.addEventListener('change',renderPriorities);
  form.addEventListener('submit',event=>{event.preventDefault();if(other.checked&&!custom.value.trim()){custom.setCustomValidity(CLN.t('custom_required'));custom.reportValidity();return;}
    last={modules:currentModules().filter(k=>k!=='autre'),custom:other.checked?custom.value.trim():'',taille:form.elements.taille.value,delai:form.elements.delai.value,mode:form.elements.mode.value,priorityEnabled:toggle.checked,order:[...order]};generatedAt=new Date().toISOString();CLN.storeSummary({version:2,generatedAt,answers:last});show();result.scrollIntoView({behavior:'smooth',block:'start'});
  });
  window.addEventListener('cln:language',()=>{renderPriorities();show();});renderPriorities();
});
