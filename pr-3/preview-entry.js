import {createExperiment,serialize} from './src/engine.js';
const prefix="hexhaven-preview:pr-3:";
const params=new URLSearchParams(window.location.search);
// Only an explicit fresh link resets this PR's own save; reload then resumes it.
if(params.get('fresh')==='1'){
  try{
    localStorage.setItem(prefix+'hexhaven-experiment-v07',JSON.stringify(serialize(createExperiment('standard',202607))));
    localStorage.setItem(prefix+'hexhaven-view-v07','experiment');
  }catch{}
  params.delete('fresh');
  window.history.replaceState(null,'',window.location.pathname+(params.size?'?'+params.toString():'')+window.location.hash);
}
await import('./src/main.js');
