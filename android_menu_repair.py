from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text(encoding="utf-8")
patch=r"""
<style id="fidget-menu-action-repair">
#gameMenuItems:not(.menu-open){display:none!important;pointer-events:none!important}
#gameMenuItems.menu-open{display:grid!important;position:fixed!important;top:calc(env(safe-area-inset-top,0px) + 52px)!important;right:8px!important;left:auto!important;bottom:auto!important;width:min(290px,calc(100vw - 16px))!important;max-height:calc(100dvh - env(safe-area-inset-top,0px) - 65px)!important;overflow-y:auto!important;z-index:1001!important}
#floatingMenuToggle{position:fixed!important;right:8px!important;top:calc(env(safe-area-inset-top,0px) + 8px)!important;left:auto!important;z-index:1002!important}
#gameMenuItems button{pointer-events:auto!important;touch-action:manipulation!important}
body:has(#customCarPanel:not(.hidden)) #gameMenuItems,
body:has(#teamPanel:not(.hidden)) #gameMenuItems,
body:has(#raceSetup:not(.hidden)) #gameMenuItems,
body:has(#networkPanel:not(.hidden)) #gameMenuItems{display:none!important;pointer-events:none!important}
/* Keep modal headers and close controls accessible in landscape Android. */
#customCarPanel,#garagePanel,#raceSetup,#teamPanel,#networkPanel{box-sizing:border-box!important;padding:8px!important;align-items:stretch!important;overflow:hidden!important}
#customCarPanel .network-card,#garagePanel .network-card,#raceSetup .network-card,#teamPanel .network-card,#networkPanel .network-card{box-sizing:border-box!important;width:min(100%,1000px)!important;max-width:100%!important;max-height:100%!important;height:100%!important;overflow-y:auto!important;overscroll-behavior:contain!important;padding:10px 14px 76px!important;margin:auto!important}
#customCarPanel .network-top,#garagePanel .network-top,#raceSetup .network-top,#teamPanel .network-top,#networkPanel .network-top{position:sticky!important;top:-10px!important;z-index:5!important;background:#142630!important;padding:8px 2px!important}
#customCarPanel .network-top button,#garagePanel .network-top button,#raceSetup .network-top button{min-width:46px!important;min-height:42px!important;flex-shrink:0!important}
#fidgetReturnRace{position:fixed!important;right:10px!important;bottom:12px!important;z-index:2005!important;background:#12455b!important;color:#fff!important;border:2px solid #75faff!important;border-radius:12px!important;padding:10px 14px!important;font-weight:800!important;min-height:44px!important;box-shadow:0 4px 20px #000a!important}
#fidgetCreditBalance{font-size:17px!important;color:#7fffe5!important;font-weight:900!important;margin:8px 0!important}
</style>
<script id="fidget-menu-action-repair-script">
(function(){
function init(){
 const menu=document.getElementById('gameMenuItems');
 const toggle=document.getElementById('floatingMenuToggle');
 if(!menu||!toggle)return;
 const close=()=>{menu.classList.remove('menu-open');toggle.textContent='☰ MENU';toggle.setAttribute('aria-expanded','false')};
 // Close menu before the original button handlers execute, not after.
 menu.addEventListener('click',e=>{
   const button=e.target.closest('button');if(!button)return;
   close();
   if(button.id==='spectate' && !document.body.classList.contains('spectating')){
     for(const id of ['garagePanel','teamPanel','customCarPanel','raceSetup','networkPanel']){
       const panel=document.getElementById(id);if(panel)panel.classList.add('hidden');
     }
   }
 },true);
 // Opening a feature panel always clears any floating menu.
 for(const id of ['customCarButton','garageButton','teamButton','tracksButton','multiplayer']){
   const button=document.getElementById(id);
   if(button)button.addEventListener('click',close,true);
 }
 // Ensure the garage can always close and the other menu items become available.
 const garage=document.getElementById('garagePanel');
 const closeGarage=document.getElementById('closeGarage');
 if(garage&&closeGarage){
   closeGarage.addEventListener('click',()=>{
     garage.classList.add('hidden');
     menu.classList.add('menu-open');
     toggle.textContent='✕ MENU';
     toggle.setAttribute('aria-expanded','true');
   });
 }
 // A visible garage must not trap the player away from the main menu.
 if(garage){
   const back=document.createElement('button');
   back.type='button';
   back.textContent='← Back to Menu';
   back.id='garageBackToMenu';
   back.style.cssText='display:block;width:100%;min-height:44px;margin-top:10px;background:#214b61;color:white;border:2px solid #75faff;border-radius:8px';
   back.addEventListener('click',()=>{
     garage.classList.add('hidden');
     menu.classList.add('menu-open');
     toggle.textContent='✕ MENU';
     toggle.setAttribute('aria-expanded','true');
   });
   const card=garage.querySelector('.network-card');
   if(card&&!document.getElementById('garageBackToMenu'))card.appendChild(back);
 }
 // Always-accessible way out of every feature panel.
 const panels=['garagePanel','customCarPanel','raceSetup','teamPanel','networkPanel'];
 const backRace=document.createElement('button');
 backRace.id='fidgetReturnRace';backRace.type='button';backRace.textContent='← Back to Race';
 backRace.addEventListener('click',()=>{
   for(const id of panels){const p=document.getElementById(id);if(p)p.classList.add('hidden')}
   close();
 });
 document.body.appendChild(backRace);
 const refreshBack=()=>{if(garage&&!garage.classList.contains('hidden'))refreshCredits();backRace.style.display=panels.some(id=>{const p=document.getElementById(id);return p&&!p.classList.contains('hidden')})?'block':'none'};
 const observer=new MutationObserver(refreshBack);
 for(const id of panels){const p=document.getElementById(id);if(p)observer.observe(p,{attributes:true,attributeFilter:['class']})}
 refreshBack();
 // Read the existing earned RC balance; do not modify awards or upgrade prices.
 const credits=document.createElement('div');
 credits.id='fidgetCreditBalance';
 const career=document.getElementById('careerInfo');
 if(career){career.insertAdjacentElement('afterend',credits)}
 const refreshCredits=()=>{
   if(!credits.isConnected)return;
   let amount=0;try{amount=Math.max(0,Number(localStorage.getItem('fidgetCredits')||0)||0)}catch(e){}
   credits.textContent='Racing Credits (RC): '+Math.floor(amount).toLocaleString();
 };
 refreshCredits();
 if(garage)observer.observe(garage,{attributes:true,attributeFilter:['class']});
 if(garage)garage.addEventListener('click',()=>requestAnimationFrame(refreshCredits));
 // Reopen only by tapping the compact MENU button.
 close();
 document.addEventListener('visibilitychange',()=>{if(document.hidden)close()});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
"""
s=s.replace("</body>",patch+"</body>")
p.write_text(s,encoding="utf-8")
