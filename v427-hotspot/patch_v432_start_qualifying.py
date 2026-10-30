from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text()
# Existing later script overwrites the earlier V431 click handler; attach ours after all scripts load.
anchor='</body>'
assert anchor in s
addon="""<script>
(function(){
 function install432(){
  const button=document.getElementById('startShared');
  const box=document.getElementById('qualifyEnabled428');
  if(!button||!box)return;
  box.checked=false;
  const label=box.closest('label');
  if(label){label.style.display='flex';label.style.visibility='visible';label.style.opacity='1';label.style.background='#263e61';label.style.padding='10px';label.style.borderRadius='8px';}
  const panel=document.getElementById('networkPanel');
  if(panel){
    let tag=document.getElementById('fidgetBuild432');
    if(!tag){tag=document.createElement('div');tag.id='fidgetBuild432';tag.textContent='Build 432';tag.style.cssText='font-size:12px;text-align:center;opacity:.8;padding:6px';panel.appendChild(tag);}
  }
  // Capture phase prevents the legacy click handler from replacing this action.
  button.addEventListener('click',function(ev){
   ev.preventDefault();ev.stopImmediatePropagation();
   if(netRole!=='host'){networkStatus('Only the host can start the race.');return;}
   const chosen=document.getElementById('sharedTrackChoice').value||activeTrack;
   const mode=box.checked?'qualify':'race';
   const grid=mode==='race'?shuffledGrid():[];
   if(typeof FidgetMultiplayer==='undefined'){networkStatus('Android Wi-Fi bridge unavailable');return;}
   try{
    FidgetMultiplayer.send(JSON.stringify({fidgetControl431:'start',track:chosen,mode,grid}));
    prepareSession(mode==='qualify',chosen,grid);
    hideNetwork();baseStart();updateRoom();
   }catch(e){networkStatus('Start failed: '+e.message);}
  },true);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install432);
 else install432();
})();
</script>"""
s=s.replace(anchor,addon+anchor,1)
# Existing qualifying completion waits for a second manual press; auto-advance host.
needle="if($('useGrid'))$('useGrid').onclick=()=>{if(netRole==='host')requestShared('race');else{prepareSession(false,activeTrack,gridOrder);baseStart();}};"
assert needle in s
s=s.replace(needle,"""if($('useGrid'))$('useGrid').onclick=()=>{
 if(netRole==='host'&&typeof FidgetMultiplayer!=='undefined'){
  const grid=validGrid(gridOrder)?gridOrder:shuffledGrid();
  FidgetMultiplayer.send(JSON.stringify({fidgetControl431:'start',track:activeTrack,mode:'race',grid}));
  prepareSession(false,activeTrack,grid);$('overlay').classList.add('hidden');baseStart();
 }else if(netRole==='host')requestShared('race');
 else{prepareSession(false,activeTrack,gridOrder);baseStart();}
};
if(netRole==='host')setTimeout(()=>{const b=$('useGrid');if(b&&qualifying&&qualifyShown)b.click();},1500);""",1)
p.write_text(s)
print('Build 432: visible qualifying off by default, host start capture, random grid, qualifying transition, build label')
