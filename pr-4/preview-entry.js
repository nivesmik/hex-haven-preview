import {createExperiment,serialize} from './src/engine.js';
const prefix='hexhaven-preview:pr-4:';
const params=new URLSearchParams(window.location.search);
if(params.get('fresh')==='1'){
 try{
  localStorage.setItem(prefix+'hexhaven-v08-experiment',JSON.stringify(serialize(createExperiment('standard',202607))));
  localStorage.setItem(prefix+'hexhaven-v08-view','experiment');
 }catch{}
 params.delete('fresh');window.history.replaceState(null,'',window.location.pathname+(params.size?'?'+params.toString():'')+window.location.hash);
}
await import('./src/boot3d.js');
