import {readFileSync} from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const code=readFileSync('pipeline-animation.js','utf8');
function setup(reduce=false){
 const events={},docEvents={},windowEvents={},classes=new Set();let loads=0;
 const toggle={dataset:{},hidden:true,addEventListener:(k,f)=>events['toggle:'+k]=f};
 const expand={focus:()=>events.focus='expand',addEventListener:(k,f)=>events['expand:'+k]=f};
 const poster={},zoom={},close={focus:()=>events.focus='close',addEventListener:(k,f)=>events['close:'+k]=f};
 const dialog={open:false,querySelector:s=>s==='img'?zoom:close,showModal(){this.open=true},close(){this.open=false;events['dialog:close']?.()},addEventListener:(k,f)=>events['dialog:'+k]=f};
 const figure={querySelector:s=>s==='.pipeline-poster'?poster:s==='.pipeline-toggle'?toggle:expand,classList:{add:k=>classes.add(k),remove:k=>classes.delete(k)}};
 const video={paused:true,currentTime:0,duration:15,children:[],closest:()=>figure,replaceChildren(){this.children=[]},append(s){this.children.push(s)},removeAttribute(){},load(){loads++;this.currentTime=0;events.loadedmetadata?.()},pause(){this.paused=true;events.pause?.()},async play(){this.paused=false;events.playing?.()},addEventListener:(k,f)=>events[k]=f};
 const motion={matches:reduce,addEventListener:(k,f)=>events.preference=f};
 const doc={hidden:false,querySelector:s=>s==='#pipeline-animation'?video:dialog,createElement:()=>({}),addEventListener:(k,f)=>docEvents[k]=f};
 const win={CLN:{lang:'fr',t:k=>k,ready:Promise.resolve()},addEventListener:(k,f)=>windowEvents[k]=f};
 class Observer{constructor(cb){this.cb=cb}observe(){this.cb([{isIntersecting:true}])}}
 vm.runInNewContext(code,{window:win,document:doc,matchMedia:()=>motion,IntersectionObserver:Observer});
 return {video,poster,zoom,expand,toggle,motion,events,windowEvents,docEvents,doc,win,get loads(){return loads}};
}
const a=setup();await Promise.resolve();await Promise.resolve();assert(!a.video.paused);assert(a.video.children[0].src.endsWith('-fr.webm'));
a.events['toggle:click']();assert(a.video.paused);a.video.currentTime=7;a.win.CLN.lang='en';a.windowEvents['cln:language']();assert(a.poster.src.endsWith('-en.webp'));assert(a.video.paused);assert.equal(a.video.children.length,0,'paused language change must not download video');
a.win.CLN.lang='es';a.windowEvents['cln:language']();a.win.CLN.lang='en';a.windowEvents['cln:language']();
a.events['toggle:click']();await Promise.resolve();assert(!a.video.paused);assert.equal(a.video.currentTime,7);assert(a.video.children[0].src.endsWith('-en.webm'));
a.events['expand:click']({preventDefault(){}});assert(a.video.paused);assert.equal(a.events.focus,'close');a.events['close:click']();await Promise.resolve();assert(!a.video.paused);assert.equal(a.events.focus,'expand');
a.doc.hidden=true;a.docEvents.visibilitychange();assert(a.video.paused);a.doc.hidden=false;a.docEvents.visibilitychange();await Promise.resolve();assert(!a.video.paused);
a.motion.matches=true;a.events.preference();assert(a.video.paused);assert(a.toggle.hidden);
const b=setup(true);await Promise.resolve();await Promise.resolve();assert.equal(b.loads,0);assert.equal(b.video.children.length,0);assert(b.poster.src.endsWith('-fr.webp'));
b.win.CLN.lang='pt-BR';b.windowEvents['cln:language']();assert(b.poster.src.endsWith('-pt-BR.webp'));assert.equal(b.video.children.length,0);
console.log('PASS pipeline: selected language, pause and position preserved, lazy loading, zoom/focus, visibility and reduced motion.');
