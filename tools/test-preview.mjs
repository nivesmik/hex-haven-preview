import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const elements=new Map(),handlers=new Map();
const keys=['hexhaven-save-v3','hexhaven-experiment-v07','hexhaven-view-v07'];
const storage=new Map(keys.map(key=>[key,'OFFICIAL-SAVE-DO-NOT-TOUCH']));
const prefix='hexhaven-preview:pr-3:';
storage.set(prefix+'hexhaven-experiment-v07','old-preview-save');
const ids=new Set([...readFileSync(new URL('../pr-3/index.html',import.meta.url),'utf8').matchAll(/id="([^"]+)"/g)].map(m=>m[1]));
const ctx=new Proxy({},{get:(t,k)=>t[k]??(()=>{})});
function element(id){
 if(elements.has(id))return elements.get(id);
 assert.ok(ids.has(id)||id.endsWith('-span'),`HTML element ${id}`);
 const el={style:{},clientWidth:390,clientHeight:844,handlers:new Map(),
  getContext:()=>ctx,getBoundingClientRect:()=>({left:0,top:0,width:390,height:844}),
  querySelector:()=>element(id+'-span'),addEventListener(name,fn){this.handlers.set(name,fn);},setPointerCapture(){}};
 elements.set(id,el);return el;
}
let rewritten;
globalThis.document={getElementById:element};
globalThis.localStorage={getItem:key=>storage.get(key),setItem:(key,value)=>storage.set(key,value)};
globalThis.window={devicePixelRatio:2,location:new URL('https://example.invalid/hex-haven-preview/pr-3/?fresh=1'),
 history:{replaceState:(state,title,url)=>{rewritten=url;}},setTimeout:()=>0,clearTimeout(){},addEventListener:(name,fn)=>handlers.set(name,fn)};
await import('../pr-3/preview-entry.js');
let state=JSON.parse(storage.get(prefix+'hexhaven-experiment-v07'));
assert.equal(state.experiment.difficulty,'standard');assert.equal(state.experiment.seed,202607);assert.equal(state.index,0);
assert.equal(rewritten,'/hex-haven-preview/pr-3/');
for(const key of keys)assert.equal(storage.get(key),'OFFICIAL-SAVE-DO-NOT-TOUCH');
const board=element('board'),event={clientX:259,clientY:422,pointerId:1,isPrimary:true,button:0,preventDefault(){}};
board.handlers.get('pointerdown')(event);board.handlers.get('pointerup')(event);
assert.equal(element('confirm').disabled,false);element('right').onclick();element('confirm').onclick();
state=JSON.parse(storage.get(prefix+'hexhaven-experiment-v07'));assert.equal(state.index,1);
element('switch-view').onclick();assert.ok(storage.has(prefix+'hexhaven-save-v3'));
for(const key of keys)assert.equal(storage.get(key),'OFFICIAL-SAVE-DO-NOT-TOUCH');
console.log('PASS: standard/202607 start, fresh URL cleanup, tap/rotate/place, isolated regular and experiment saves');
