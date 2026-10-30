from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text()
needle="$('pickTrack428').onclick="
assert needle in s
# Keep existing menu intact; supply missing host/client state from actual Android transport events.
needle="window.addEventListener('fidget-local-multiplayer',e=>"
assert needle in s
insert="""window.addEventListener('fidget-local-multiplayer',e=>{
 const d=e.detail||{};
 if(d.type==='hosting'){netRole='host';netTransport='Wi-Fi';updateRoom();}
 if(d.type==='connected'){netRole='client';netTransport='Wi-Fi';updateRoom();}
 if(d.type==='disconnected'&&netRole==='client'){networkStatus('Reconnecting to host...');}
 if(d.type==='message'){
   try{
     const msg=JSON.parse(d.message);
     if(msg.fidgetControl431==='start'&&netRole==='client'){
       const track=tracks[msg.track]?msg.track:activeTrack;
       prepareSession(msg.mode==='qualify',track,validGrid(msg.grid)?msg.grid:shuffledGrid());
       baseStart();hideNetwork();updateRoom();
     }
   }catch(err){}
 }
});
"""
s=s.replace(needle,insert+needle,1)
old="$('startShared').onclick=()=>{if(netRole!=='host'){networkStatus('Host a hotspot first, then connect the other drivers.');return;}requestShared(document.getElementById('qualifyEnabled428').checked?'qualify':'race');};"
assert old in s
new="""$('startShared').onclick=()=>{
 if(netRole!=='host'){networkStatus('Start hosting on this phone first.');return;}
 const track=$('sharedTrackChoice').value||activeTrack;
 const mode=$('qualifyEnabled428').checked?'qualify':'race';
 const grid=validGrid(gridOrder)?gridOrder:shuffledGrid();
 try{FidgetMultiplayer.send(JSON.stringify({fidgetControl431:'start',track,mode,grid}));}
 catch(err){networkStatus('Cannot send race start: '+err.message);return;}
 prepareSession(mode==='qualify',track,grid);baseStart();hideNetwork();updateRoom();
};"""
s=s.replace(old,new,1)
# label is deliberately small and local to multiplayer panel
needle='<button id="leaveShared">BACK TO MAIN MENU</button>'
assert needle in s
s=s.replace(needle,needle+'<span style="display:block;text-align:center;font-size:11px;opacity:.65;margin-top:8px">Build 431</span>',1)
p.write_text(s)
print("Build 431: wired host role, network race start, client start, and build label.")
