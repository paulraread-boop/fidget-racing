from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text()
# Remove the earlier labels; a single authoritative build marker appears on all screens.
s=s.replace('<span style="display:block;text-align:center;font-size:11px;opacity:.65;margin-top:8px">Build 431</span>','')
s=s.replace("tag.textContent='Build 432'","tag.textContent='BUILD 433'")
# Keep the existing game and multiplayer menu; ensure old overlay is not left on screen.
anchor='</body>'
assert anchor in s
script="""<script>
(function(){
 const BUILD='BUILD 433';
 function badge(){
  let b=document.getElementById('fidgetBuildVersion433');
  if(!b){
   b=document.createElement('div');b.id='fidgetBuildVersion433';
   b.style.cssText='position:fixed;right:8px;bottom:6px;z-index:2147483647;font:700 12px Arial,sans-serif;color:#fff;background:#142942dd;border:1px solid #6689ab;border-radius:5px;padding:4px 7px;pointer-events:none';
   document.body.appendChild(b);
  }
  b.textContent=BUILD;
 }
 function ensureMenu(){
  const candidates=Array.from(document.querySelectorAll('button,[role="button"]'));
  for(const b of candidates){
   if(/multiplayer/i.test((b.textContent||'').trim())&&b.id!=='startShared'){
    b.hidden=false;b.style.display='';b.style.visibility='visible';
   }
  }
 }
 function repairSinglePlayer(){
  // Multiplayer must not retain control over ordinary single-player navigation.
  const buttons=Array.from(document.querySelectorAll('button'));
  for(const b of buttons){
   if(/^(quick race|race)$/i.test((b.textContent||'').trim())){
    b.addEventListener('click',()=>{if(typeof netRole!=='undefined'&&netRole!=='host'&&netRole!=='client')return;},false);
   }
  }
 }
 function init(){badge();repairSinglePlayer();ensureMenu();
  const observer=new MutationObserver(()=>{badge();ensureMenu();});
  observer.observe(document.body,{attributes:true,subtree:false,childList:true});
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>"""
s=s.replace(anchor,script+anchor,1)
p.write_text(s)
print('Build 433: single unmistakable version badge, menu button visibility restoration')
