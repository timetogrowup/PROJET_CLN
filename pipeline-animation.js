/* V8: one selected-language video; static fallback and accessible zoom. */
(() => {
 'use strict';
 const video=document.querySelector('#pipeline-animation');
 if(!video)return;
 const figure=video.closest('.pipeline-demo'),poster=figure.querySelector('.pipeline-poster');
 const toggle=figure.querySelector('.pipeline-toggle'),expand=figure.querySelector('.pipeline-expand');
 const dialog=document.querySelector('#pipeline-dialog'),zoom=dialog.querySelector('img');
 const mediaBase=figure.dataset?.mediaBase||'assets/pipeline/pipeline';
 function openLinkedExample(){
  if(location.hash==='#exemple'){const detail=document.querySelector('#exemple .pipeline-other-example');if(detail)detail.open=true;}
 }
 openLinkedExample();window.addEventListener('hashchange',openLinkedExample);
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 let lang='fr',loaded='',epoch=0,visible=false,userPaused=false,position=0;
 const t=k=>window.CLN?.t(k)||k;
 function label(){const key=video.paused?'pipeline.play':'pipeline.pause';toggle.dataset.msg=key;toggle.textContent=t(key);}
 function allowed(){return !motion.matches&&!userPaused&&visible&&!document.hidden&&!dialog.open;}
 function pause(){video.pause();label();}
 function configure(){
  if(loaded===lang)return;
  epoch++;loaded=lang;
  video.replaceChildren();
  for(const [ext,type] of [['webm','video/webm'],['mp4','video/mp4']]){
   const source=document.createElement('source');source.src=`${mediaBase}-${lang}.${ext}`;source.type=type;video.append(source);
  }
  video.muted=true;video.load();
 }
 async function play(){
  if(!allowed())return;
  configure();const version=epoch;
  try{await video.play();if(version===epoch&&!allowed())pause();}
  catch(_){if(version===epoch){figure.classList.remove('pipeline-playing');label();}}
 }
 function language(){
  const next=window.CLN?.lang||'fr';
  if(next!==lang){if(loaded&&Number.isFinite(video.currentTime))position=video.currentTime;pause();epoch++;loaded='';lang=next;figure.classList.remove('pipeline-playing');video.removeAttribute('src');video.replaceChildren();video.load();}
  const path=`${mediaBase}-${lang}.webp`;
  poster.src=path;video.poster=path;zoom.src=path;expand.href=path;label();play();
 }
 video.addEventListener('loadedmetadata',()=>{if(Number.isFinite(video.duration)){try{video.currentTime=position%video.duration;}catch(_){}}});
 video.addEventListener('playing',()=>{if(allowed()){figure.classList.add('pipeline-playing');label();}else pause();});
 video.addEventListener('pause',label);
 video.addEventListener('error',()=>{figure.classList.remove('pipeline-playing');label();});
 toggle.addEventListener('click',()=>{userPaused=!video.paused;if(userPaused)pause();else play();});
 expand.addEventListener('click',event=>{
  if(typeof dialog.showModal!=='function')return;
  event.preventDefault();dialog.showModal();pause();dialog.querySelector('button').focus();
 });
 dialog.querySelector('button').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',()=>{expand.focus();play();});
 function preference(){toggle.hidden=motion.matches;if(motion.matches){pause();figure.classList.remove('pipeline-playing');}else play();}
 motion.addEventListener('change',preference);
 document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();else play();});
 window.addEventListener('cln:language',language);
 window.CLN.ready.then(()=>{
  language();toggle.hidden=motion.matches;
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)play();else pause();},{threshold:.12}).observe(figure);
  else{visible=true;play();}
 });
})();
