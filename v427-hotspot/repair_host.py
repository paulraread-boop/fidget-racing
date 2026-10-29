from pathlib import Path
import re
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text()
needle="for(const id of ['hostWifi','findWifi','joinWifi','hostBluetooth','joinBluetooth','pairPhones','wifiSettings'])$(id).onclick=()=>nativeRace(id);"
if needle not in s:
    raise SystemExit("STOP: Approved game does not contain expected multiplayer button wiring; refusing to alter unrelated gameplay")
replacement="""$('hostWifi').onclick=()=>{if(typeof FidgetMultiplayer==='undefined'){networkStatus('Android hotspot bridge unavailable');return;}FidgetMultiplayer.hostWifi(42714);networkStatus('Starting six-player Wi-Fi host on port 42714...');};
$('joinWifi').onclick=()=>{if(typeof FidgetMultiplayer==='undefined'){networkStatus('Android hotspot bridge unavailable');return;}const ip=prompt('Enter host hotspot IP address (example: 192.168.43.1)');if(ip){FidgetMultiplayer.joinWifi(ip.trim(),42714);networkStatus('Connecting to '+ip+'...');}};
$('findWifi').onclick=()=>networkStatus('Connect both devices to the same hotspot, then tap Join by address and enter the host IP.');
for(const id of ['hostBluetooth','joinBluetooth','pairPhones','wifiSettings'])$(id).onclick=()=>nativeRace(id);
window.addEventListener('fidget-local-multiplayer',e=>{const d=e.detail||{};if(d.type==='hosting')networkStatus('Hosting: '+d.message+' (maximum 6 human drivers)');else if(d.type==='connected'||d.type==='joined'||d.type==='disconnected'||d.type==='error')networkStatus(d.type+': '+d.message);});"""
s=s.replace(needle,replacement,1)
s=re.sub(r'(?i)up to (?:8|eight) (?:human )?drivers','up to 6 drivers',s)
s=re.sub(r'(?i)up to (?:8|eight) players','up to 6 players',s)
p.write_text(s)
print("Patched only Wi-Fi host/join controls; game assets and other controls unchanged")
