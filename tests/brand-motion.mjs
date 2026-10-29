import vm from 'node:vm';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const code=readFileSync('site.js','utf8').split('/* V7: progressive animated identity. Still image works without JS or playback. */')[1];
function setup(reduce=false,reject=false){
 const events={},docEvents={},windowEvents={},classes=new Set();let loads=0,plays=0;
 const sources=[{dataset:{src:'logo.webm'}},{dataset:{src:'logo.mp4'}}];
 const button={hidden:true,dataset:{},addEventListener:(k,v)=>events['button:'+k]=v};
 const figure={querySelector:()=>button,classList:{add:x=>classes.add(x),remove:x=>classes.delete(x)}};
 const video={paused:true,muted:false,closest:()=>figure,querySelectorAll:()=>sources,load:()=>loads++,play:async()=>{plays++;if(reject)throw Error('autoplay denied');video.paused=false;events.playing?.();},pause:()=>{video.paused=true;events.pause?.();},addEventListener:(k,v)=>events[k]=v};
 const media={matches:reduce,addEventListener:(k,v)=>events.preference=v};
 const doc={hidden:false,querySelector:()=>video,addEventListener:(k,v)=>docEvents[k]=v};
 const win={CLN:{t:k=>k,ready:Promise.resolve()},addEventListener:(k,v)=>windowEvents[k]=v};
 const context={document:doc,window:win,matchMedia:()=>media};
 vm.runInNewContext(code,context);
 return {video,button,events,media,doc,docEvents,classes,sources,get loads(){return loads},get plays(){return plays}};
}
const a=setup();await Promise.resolve();assert.equal(a.loads,1);assert.equal(a.video.paused,false);assert.equal(a.button.dataset.msg,'brand.pause');
a.events['button:click']();assert.equal(a.video.paused,true);assert.equal(a.button.dataset.msg,'brand.play');
a.doc.hidden=true;a.docEvents.visibilitychange();a.doc.hidden=false;a.docEvents.visibilitychange();assert.equal(a.video.paused,true,'user pause must survive visibility changes');
a.events['button:click']();await Promise.resolve();assert.equal(a.video.paused,false);assert.equal(a.loads,1);
a.media.matches=true;a.events.preference();assert.equal(a.video.paused,true);assert.equal(a.button.hidden,true);assert(!a.classes.has('is-playing'));
const b=setup(true);assert.equal(b.loads,0);assert.equal(b.plays,0);assert(b.sources.every(s=>!s.src));
const c=setup(false,true);await Promise.resolve();assert.equal(c.video.paused,true);assert(!c.classes.has('is-playing'));assert.equal(c.button.dataset.msg,'brand.play');
console.log('PASS animation: play/pause, manual preference, reduced motion without loading, preference change, autoplay rejection and poster fallback.');
