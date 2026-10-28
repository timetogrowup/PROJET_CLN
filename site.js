/* Shared language selection. No visitor text is automatically translated. */
(() => {
  'use strict';
  const langs = ['fr','en','pt-BR','es'];
  const valid = x => langs.includes(x) ? x : null;
  const normalise = x => x.replace(/\s+/g,' ').trim();
  const originalText = new WeakMap(), originalAttrs = new WeakMap();
  let catalog = {}, messages = {}, lang = 'fr';
  try {
    const item = JSON.parse(localStorage.getItem('clnLanguage') || 'null');
    if (item && item.expires > Date.now()) lang = valid(item.lang) || 'fr';
    else localStorage.removeItem('clnLanguage');
  } catch (_) {}
  lang = valid(new URLSearchParams(location.search).get('lang')) || lang;
  const CLN = window.CLN = {
    get lang() { return lang; },
    langs,
    translate(text) { return lang === 'fr' ? text : catalog[normalise(text)]?.[lang] || text; },
    t(key, values = {}) {
      const text = messages[key]?.[lang] || messages[key]?.fr || key;
      return text.replace(/\{(\w+)\}/g, (_, k) => String(values[k] ?? ''));
    },
    readSummary() {
      try {
        const data = JSON.parse(localStorage.getItem('clnRecommendation') || 'null');
        if (!data) return null;
        const date = Date.parse(data.generatedAt);
        if (!Number.isFinite(date) || date > Date.now() || Date.now()-date > 30*86400000) {localStorage.removeItem('clnRecommendation');return null;}
        return data;
      } catch (_) {try {localStorage.removeItem('clnRecommendation');} catch (_) {} return null;}
    },
    storeSummary(data) {try {localStorage.setItem('clnRecommendation',JSON.stringify(data));} catch (_) {}},
    setLanguage(next) {
      if (!valid(next)) return;
      lang = next;
      try {localStorage.setItem('clnLanguage',JSON.stringify({lang,expires:Date.now()+365*86400000}));} catch (_) {}
      const url = new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url);
      render();
      window.dispatchEvent(new CustomEvent('cln:language',{detail:{lang}}));
    }
  };
  function render() {
    document.documentElement.lang = lang;
    const walker = document.createTreeWalker(document,NodeFilter.SHOW_TEXT);
    let node;
    while ((node=walker.nextNode())) {
      if (!node.parentElement || node.parentElement.closest('script,style,[data-dynamic],.language-picker')) continue;
      if (!originalText.has(node)) originalText.set(node,node.nodeValue);
      const source=originalText.get(node), key=normalise(source);
      if (catalog[key]) node.nodeValue=source.replace(source.trim(),CLN.translate(key));
    }
    document.querySelectorAll('[alt],[placeholder],[aria-label],meta[name="description"]').forEach(el=>{
      if(el.closest('[data-dynamic],.language-picker')) return;
      let map=originalAttrs.get(el);if(!map){map={};originalAttrs.set(el,map);}
      for(const attr of ['alt','placeholder','aria-label',...(el.matches('meta')?['content']:[])]) {
        if(!el.hasAttribute(attr))continue;
        if(!(attr in map))map[attr]=el.getAttribute(attr);
        el.setAttribute(attr,CLN.translate(map[attr]));
      }
    });
    document.querySelectorAll('a[href]').forEach(a=>{
      const raw=a.getAttribute('href');if(!raw || raw.startsWith('#') || /^(mailto:|tel:)/.test(raw)) return;
      const url=new URL(raw,location.href);
      if(url.origin===location.origin && /\.html$/.test(url.pathname)){url.searchParams.set('lang',lang);a.setAttribute('href',url.pathname+url.search+url.hash);}
    });
    const canonical=document.querySelector('link[rel="canonical"]');
    if(canonical){const u=new URL(canonical.href);if(lang==='fr')u.searchParams.delete('lang');else u.searchParams.set('lang',lang);canonical.href=u.href;}
    const picker=document.querySelector('#site-language');if(picker)picker.value=lang;
    const label=document.querySelector('#language-label');if(label)label.textContent=CLN.t('language');
    document.querySelectorAll('[data-msg]').forEach(el=>{el.textContent=CLN.t(el.dataset.msg);});
    document.querySelectorAll('input[name="lang"]').forEach(el=>{el.value=lang;});
    document.querySelectorAll('input,textarea').forEach(el=>el.setCustomValidity(''));
  }
  CLN.ready = Promise.all(['i18n/static.json','i18n/messages.json'].map(path=>fetch(path,{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error('catalog');return r.json();}))).then(([s,m])=>{
    catalog=s;messages=m;
    const nav=document.querySelector('.navbar');
    if(nav){const box=document.createElement('label');box.className='language-picker';box.htmlFor='site-language';const label=document.createElement('span');label.id='language-label';box.append(label);const select=document.createElement('select');select.id='site-language';[['fr','Français'],['en','English'],['pt-BR','Português (Brasil)'],['es','Español']].forEach(([value,text])=>{const o=document.createElement('option');o.value=value;o.textContent=text;select.append(o);});box.append(select);nav.prepend(box);select.addEventListener('change',()=>CLN.setLanguage(select.value));}
    render();document.documentElement.dataset.i18nReady='true';
    document.addEventListener('invalid',event=>{const el=event.target;if(!el.validity)return;let key='required';if(el.type==='checkbox')key='check_required';else if(el.validity.typeMismatch)key='email_invalid';else if(el.validity.badInput||el.validity.stepMismatch)key='number_invalid';el.setCustomValidity(CLN.t(key));},true);
    document.addEventListener('input',event=>{if(event.target.setCustomValidity)event.target.setCustomValidity('');});
    if(new URLSearchParams(location.search).get('status')==='success'){try{sessionStorage.removeItem('clnContactDraft');}catch(_){}}
    return CLN;
  }).catch(()=>{document.documentElement.dataset.i18nReady='error';const send=document.querySelector('#contact-form button[type="submit"]');if(send)send.disabled=true;});
})();
