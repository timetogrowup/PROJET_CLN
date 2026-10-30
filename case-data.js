/* V11: shared, pure case schema. No network or browser persistence here. */
(() => {
 'use strict';
 const choices={applications:['a1_3','a4_10','a11_20','a20_plus','inconnu'],people:['p1_10','p11_50','p51_200','p200_plus','inconnu'],connections:['integrated','partial','files','separate','inconnu'],difficulties:['reentry','repetitive','quality','consolidation','handoffs','visibility','other','inconnu'],goals:['productivity','modernise','connect','quality','steer','teams','inconnu'],approach:['existing','replacement','ongoing','compare','inconnu'],horizon:['under3','m3_6','m6_12','over12','inconnu']};
 const multi=['difficulties','goals'],ttl=30*60000;
 function clean(raw={}){
  if(!raw||typeof raw!=='object'||Array.isArray(raw))raw={};
  const result={};
  for(const [name,allowed] of Object.entries(choices)){
   if(multi.includes(name)){
    let selected=[...new Set((Array.isArray(raw[name])?raw[name]:[]).filter(v=>typeof v==='string'&&allowed.includes(v)))];
    if(selected.includes('inconnu'))selected=['inconnu'];
    result[name]=selected.length?selected.slice(0,name==='goals'?2:allowed.length):['inconnu'];
   }else result[name]=allowed.includes(raw[name])?raw[name]:'inconnu';
  }
  result.situation=Array.from(typeof raw.situation==='string'?raw.situation:'').slice(0,2000).join('').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g,'').trim();
  return result;
 }
 function summary(raw){
  const a=clean(raw),t=k=>window.CLN.t(k),lines=[t('case.title')];
  for(const [section,names] of [['environment',['applications','people']],['functioning',['connections','difficulties']],['objectives',['goals','approach']],['calendar',['horizon']]]){
   lines.push('',t('case.'+section));
   for(const name of names){const values=multi.includes(name)?a[name]:[a[name]];lines.push(t('case.field.'+name)+' : '+values.map(v=>t('case.choice.'+name+'.'+v)).join(' · '));}
  }
  if(a.situation)lines.push('',t('case.free'),a.situation);
  return lines.join('\n');
 }
 function valid(item,now=Date.now()){
  if(!item||item.version!==11||typeof item.id!=='string'||item.id.length>100||!item.id||!item.answers||typeof item.answers!=='object'||Array.isArray(item.answers))return false;
  const a=item.answers;
  for(const [name,allowed] of Object.entries(choices)){const v=a[name];if(multi.includes(name)){if(!Array.isArray(v)||!v.length||v.some(x=>!allowed.includes(x))||(v.includes('inconnu')&&v.length!==1)||(name==='goals'&&v.length>2))return false;}else if(!allowed.includes(v))return false;}
  if(typeof a.situation!=='string'||Array.from(a.situation).length>2000)return false;
  const time=Date.parse(item.generatedAt);return Number.isFinite(time)&&time<=now&&now-time<ttl;
 }
 window.CLNCase={version:11,ttl,choices,multi,clean,summary,valid};
})();
