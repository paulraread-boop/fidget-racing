from pathlib import Path
p=Path("app/src/main/assets/index.html")
s=p.read_text(encoding="utf-8")
assert 'id="b431Field"' in s and 'b431-pick-field-js' in s, "B431 Pick Your Field not found"
s=s.replace('🏁 PICK YOUR FIELD · B431','🏁 PICK YOUR FIELD · B434')
s=s.replace('const launcher=document.createElement(\'button\');launcher.id=\'b431Launch\';',"""// Move the modal outside the zoomed body, keeping it viewport-sized.
 document.documentElement.appendChild(panel);
 const launcher=document.createElement('button');launcher.id='b431Launch';""")
css="""<style id="b433-field-layout">
#b431Field{position:fixed!important;inset:0!important;width:100vw!important;height:100dvh!important;max-width:none!important;max-height:none!important;overflow:hidden!important;zoom:1!important;transform:none!important;box-sizing:border-box!important;padding: max(12px,env(safe-area-inset-top)) max(12px,env(safe-area-inset-right)) max(12px,env(safe-area-inset-bottom)) max(12px,env(safe-area-inset-left))!important}
#b431Field header{flex:0 0 auto;display:flex!important;flex-wrap:nowrap!important;min-height:44px}
#b431Field header h2{flex:1;min-width:0;font-size:clamp(15px,3.6vw,20px)!important;line-height:1.2}
#b431Field header button{flex:0 0 auto!important;width:auto!important;white-space:nowrap;font-size:13px}
#b431Field p{flex:0 0 auto;line-height:1.35}
#b431Grid{flex:1 1 auto!important;min-height:0!important;overflow-y:auto!important;overflow-x:hidden!important;overscroll-behavior:contain;grid-template-columns:repeat(2,minmax(0,1fr))!important;align-content:start;padding:4px 2px 12px}
#b431Grid button{min-width:0;overflow-wrap:anywhere}
#b431Field .actions{flex:0 0 auto!important;flex-wrap:nowrap;gap:6px;padding-bottom:2px}
#b431Field .actions button{min-width:0;font-size:clamp(10px,2.7vw,14px);padding:10px 4px}
@media(max-width:340px){#b431Field{padding:8px!important}#b431Field h2{font-size:14px!important}#b431Field header button{font-size:11px}}
</style>
"""
s=s.replace('<script id="b431-pick-field-js">',css+'<script id="b431-pick-field-js">',1)
assert 'document.documentElement.appendChild(panel)' in s
p.write_text(s,encoding="utf-8")
# Create a separate, viewport-anchored toolbar instead of relying on the game's scaled header.
toolbar = """<style id="b433-toolbar-css">
#b433Toolbar{position:absolute!important;top:0!important;left:0!important;right:0!important;height:50px!important;z-index:2147483647!important;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:12px!important;padding:5px 18px!important;box-sizing:border-box!important;background:#071625!important;border-bottom:1px solid #35779b!important;transform:none!important;zoom:1!important;font-family:Arial,sans-serif!important}
#b433Toolbar span{font-size:clamp(14px,3vw,20px)!important;font-weight:800!important;color:#f7fbff!important;white-space:nowrap!important}
#b433Toolbar button{position:static!important;flex:0 0 auto!important;padding:7px 16px!important;min-height:34px!important;border:1px solid #69b5e4!important;border-radius:8px!important;background:#173653!important;color:white!important;font-size:14px!important;font-weight:700!important}
#b431Field{padding-top:56px!important}
</style><script id="b433-toolbar-js">
(function(){
function install(){
 var panel=document.getElementById('b431Field');
 if(!panel||document.getElementById('b433Toolbar'))return;
 var candidates=Array.from(panel.querySelectorAll('button'));
 var original=candidates.find(function(b){return /close/i.test(b.textContent||'')});
 var title=Array.from(panel.querySelectorAll('*')).find(function(el){return el.children.length===0 && /PICK YOUR FIELD/.test(el.textContent||'')});
 if(original)original.style.visibility='hidden';
 if(title)title.style.visibility='hidden';
 var bar=document.createElement('div');bar.id='b433Toolbar';
 var heading=document.createElement('span');heading.textContent='🏁 PICK YOUR FIELD · B433';
 var close=document.createElement('button');close.textContent='✕ CLOSE';
 close.onclick=function(){if(original)original.click();else panel.style.display='none';bar.style.display='none'};
 bar.appendChild(heading);bar.appendChild(close);
 panel.appendChild(bar);
 var update=function(){var st=getComputedStyle(panel);bar.style.display=(st.display==='none'||st.visibility==='hidden'||panel.hidden||panel.getAttribute('aria-hidden')==='true')?'none':'flex'};
 var obs=new MutationObserver(update);
 obs.observe(panel,{attributes:true,attributeFilter:['style','class','hidden','aria-hidden']});
 document.addEventListener('click',function(){requestAnimationFrame(update)},true);
 update();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>"""
s=s.replace('</body>',toolbar+'</body>',1)
# Original audio preserved; unsupported music patch removed.
p.write_text(s,encoding="utf-8")
print("B433 fixed header and close layout applied")
