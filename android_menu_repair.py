from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text(encoding="utf-8")
patch=r"""
<style id="fidget-menu-action-repair">
#gameMenuItems:not(.menu-open){display:none!important;pointer-events:none!important}
#gameMenuItems.menu-open{display:grid!important;position:fixed!important;top:calc(env(safe-area-inset-top,0px) + 52px)!important;right:8px!important;left:auto!important;bottom:auto!important;width:min(290px,calc(100vw - 16px))!important;max-height:calc(100dvh - env(safe-area-inset-top,0px) - 65px)!important;overflow-y:auto!important;z-index:1001!important}
#floatingMenuToggle{position:fixed!important;right:8px!important;top:calc(env(safe-area-inset-top,0px) + 8px)!important;left:auto!important;z-index:1002!important}
#gameMenuItems button{pointer-events:auto!important;touch-action:manipulation!important}
body:has(#garagePanel:not(.hidden)) #gameMenuItems,
body:has(#customCarPanel:not(.hidden)) #gameMenuItems,
body:has(#teamPanel:not(.hidden)) #gameMenuItems,
body:has(#raceSetup:not(.hidden)) #gameMenuItems,
body:has(#networkPanel:not(.hidden)) #gameMenuItems{display:none!important;pointer-events:none!important}
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
