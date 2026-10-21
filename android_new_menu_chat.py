from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text(encoding="utf-8")
if 'id="fidget-new-home"' in s: raise SystemExit("New menu already installed")
addon=r"""
<style id="fidget-new-home-style">
#fidget-new-home{position:fixed;inset:0;z-index:3000;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at top,#183f62,#071021 75%);color:white;font-family:Arial,sans-serif;overflow:auto;padding:12px}
#fidget-new-home.hidden,#fidget-chat-screen.hidden,#fidget-settings-screen.hidden{display:none!important}
.fidget-home-card{width:min(96%,850px);max-height:96dvh;overflow:auto;border:2px solid #4bd9ff;border-radius:18px;padding:16px;background:linear-gradient(130deg,#0b1b31,#1a193b);text-align:center}
.fidget-home-card h1{font-size:clamp(28px,6vw,54px);color:#ffce39;text-shadow:2px 3px #a82c34;margin:4px 0 8px}
.fidget-home-card p{color:#b5e9ff;margin:4px 0 12px}
.fidget-home-buttons{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.fidget-home-buttons button,.fidget-chat-button{background:linear-gradient(110deg,#38e1ee,#9e78f9);color:#081b2b;border:0;border-radius:12px;padding:14px 8px;min-height:46px;font-weight:900;font-size:clamp(13px,2.4vw,19px);touch-action:manipulation}
.fidget-home-buttons button:last-child{grid-column:1/-1}
#fidget-chat-screen,#fidget-settings-screen{position:fixed;inset:0;z-index:3100;display:flex;justify-content:center;align-items:center;background:#081223ed;padding:14px;color:white;font-family:Arial,sans-serif}
.fidget-chat-panel{width:min(95%,720px);max-height:94dvh;overflow:auto;background:#151b2b;border:2px solid #e6ae27;border-radius:16px;padding:16px}
.fidget-chat-panel h2{text-align:center;color:#ffce39;margin:4px 0}
.fidget-chat-panel p{text-align:center;color:#9fd8e9}
.fidget-chat-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.fidget-chat-tabs button{flex:1;min-width:85px}
#fidget-chat-messages{height:min(27dvh,150px);overflow:auto;background:#090f1d;padding:10px;border-radius:9px}
.fidget-chat-compose{display:flex;gap:8px;margin:10px 0}
.fidget-chat-compose input{flex:1;min-width:0;border-radius:8px;padding:10px;color:#111;background:white}
.fidget-chat-panel button{touch-action:manipulation}
@media(max-height:420px){.fidget-home-card{padding:8px}.fidget-home-buttons button{min-height:38px;padding:7px}#fidget-chat-messages{height:75px}}
</style>
<div id="fidget-new-home"><section class="fidget-home-card"><h1>FIDGET RACING</h1><p>20 CARS • 12 TRACKS</p><div class="fidget-home-buttons"><button data-home="race">🏁 RACE</button><button data-home="garage">🔧 GARAGE</button><button data-home="championship">🏆 CHAMPIONSHIP</button><button data-home="chat">💬 CHAT ROOM</button><button data-home="settings">⚙ SETTINGS</button></div></section></div>
<div id="fidget-chat-screen" class="hidden"><section class="fidget-chat-panel"><h2>🏁 Racing Chat</h2><p>Preview only · 0 / 20 players connected</p><div class="fidget-chat-tabs"><button class="fidget-chat-button" data-chat-mode="Wi-Fi">Wi-Fi</button><button class="fidget-chat-button" data-chat-mode="Bluetooth">Bluetooth</button><button class="fidget-chat-button" data-chat-mode="Online">Online</button></div><p id="fidget-chat-status">Select a connection mode (preview only)</p><div id="fidget-chat-messages"><div>System: Welcome to Fidget Racing chat.</div><div>System: Real connections are not enabled yet.</div></div><form id="fidget-chat-form" class="fidget-chat-compose"><input id="fidget-chat-input" maxlength="200" placeholder="Type a message" aria-label="Message"><button class="fidget-chat-button">Send</button></form><button class="fidget-chat-button" data-home="back">← Back to Main Menu</button></section></div>
<div id="fidget-settings-screen" class="hidden"><section class="fidget-chat-panel"><h2>⚙ Settings</h2><p>Game controls and display</p><div class="fidget-chat-tabs"><button class="fidget-chat-button" data-setting="side">Steering Side</button><button class="fidget-chat-button" data-setting="sound">Sound</button><button class="fidget-chat-button" data-setting="view">Camera View</button></div><button class="fidget-chat-button" data-home="back">← Back to Main Menu</button></section></div>
<script id="fidget-new-home-script">
(function(){
const $=id=>document.getElementById(id);
function home(){for(const id of ['fidget-chat-screen','fidget-settings-screen'])$(id).classList.add('hidden');$('fidget-new-home').classList.remove('hidden');}
function launch(id){$('fidget-new-home').classList.add('hidden');$('overlay')?.classList.add('hidden');const btn=$(id);if(btn)btn.click();}
document.addEventListener('click',function(e){
const b=e.target.closest('[data-home],[data-chat-mode],[data-setting]');if(!b)return;
if(b.dataset.chatMode){$('fidget-chat-status').textContent=b.dataset.chatMode+' · Preview only — not connected';return;}
if(b.dataset.setting){$(b.dataset.setting)?.click();return;}
switch(b.dataset.home){
case 'back':home();break;
case 'race':$('fidget-new-home').classList.add('hidden');$('overlay')?.classList.remove('hidden');break;
case 'garage':launch('garageButton');break;
case 'championship':launch('teamButton');break;
case 'chat':$('fidget-new-home').classList.add('hidden');$('fidget-chat-screen').classList.remove('hidden');break;
case 'settings':$('fidget-new-home').classList.add('hidden');$('fidget-settings-screen').classList.remove('hidden');break;
}
});
$('fidget-chat-form').addEventListener('submit',function(e){e.preventDefault();const input=$('fidget-chat-input');if(!input.value.trim())return;const div=document.createElement('div');div.textContent='You: '+input.value;$('fidget-chat-messages').appendChild(div);input.value='';div.scrollIntoView({block:'nearest'});});
const oldReturn=window.returnToMenu;
if(typeof oldReturn==='function')window.returnToMenu=function(){oldReturn.apply(this,arguments);home();};
})();
</script>
"""
if '</body>' not in s: raise SystemExit("Game HTML body missing")
s=s.replace('</body>',addon+'</body>',1)
p.write_text(s,encoding="utf-8")
print("Added five-button menu and chat UI")
