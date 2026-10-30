from pathlib import Path
import re,zipfile
root=Path('work433')
files=list(root.rglob('*.html'))
assert files,'Pre-multiplayer HTML missing'
p=max(files,key=lambda f:f.stat().st_size)
s=p.read_text(encoding='utf-8',errors='replace')
# Gallery: remove the actual menu control and gallery containers; never touch showroom, yellow #14 artwork, or racing.
menu_pat=r'<(?:button|a)\\b[^>]*>[\\s\\S]{0,250}?(?:WATCH\\s*20\\s*CONCEPT\\s*CARS)[\\s\\S]{0,100}?</(?:button|a)>'
s,removed=re.subn(menu_pat,'',s,flags=re.I)
# Some menus use div controls instead of buttons. Keep removal tightly bounded.
s,removed2=re.subn(r'<div\\b[^>]*\\b(?:onclick|role)=[^>]*>[\\s\\S]{0,180}?WATCH\\s*20\\s*CONCEPT\\s*CARS[\\s\\S]{0,80}?</div>','',s,flags=re.I)
print('Gallery menu controls removed',removed+removed2)
assert removed+removed2>0,'Gallery menu control not found: refusing to publish an ineffective build'
# Remove gallery media markup when it is in a dedicated gallery element; do not touch the official cover.
for pat in [r'<section\\b(?=[^>]*(?:id|class)=[\\x22\\x27][^\\x22\\x27]*(?:conceptGallery|conceptCarsGallery|scrollingGallery|gallery20)[^\\x22\\x27]*[\\x22\\x27])[^>]*>[\\s\\S]*?</section>',r'<div\\b(?=[^>]*(?:id|class)=[\\x22\\x27][^\\x22\\x27]*(?:conceptGallery|conceptCarsGallery|scrollingGallery|gallery20)[^\\x22\\x27]*[\\x22\\x27])[^>]*>[\\s\\S]*?</div>']:
 s,n=re.subn(pat,'',s,flags=re.I);print('Dedicated gallery sections removed:',n)
# Player Support: eliminate the free-floating warning banner that overlays the fields.
# Its information remains available as a short, ordinary paragraph inside the support dialog.
s,n=re.subn(r'<(?:div|p|span)\\b[^>]*>\\s*Reports are saved only on this device[\\s\\S]{0,500}?</(?:div|p|span)>','',s,flags=re.I)
print('Overlapping support warning removed:',n)
css="""<style id="support-layout-435">
[id*="support" i] *,[class*="support" i] *{box-sizing:border-box;max-width:100%}
[id*="support" i] label,[class*="support" i] label{white-space:normal!important;overflow-wrap:anywhere;line-height:1.35}
[id*="support" i] input,[id*="support" i] select,[id*="support" i] textarea{display:block;max-width:100%;width:100%}
[id*="support" i] [class*="notice" i],[id*="support" i] [class*="message" i],
[class*="support" i] [class*="notice" i],[class*="support" i] [class*="message" i]{
position:static!important;transform:none!important;white-space:normal!important;
overflow-wrap:anywhere!important;width:auto!important;line-height:1.35!important;
}
</style>"""
s=s.replace('</head>',css+'</head>',1)
# Only menu build identification, not a global overlay.
s=s.replace('</body>',"""<script>
document.addEventListener('DOMContentLoaded',function(){
 const menu=document.querySelector('#menuOverlay,#menuModal,#mainMenu');
 if(menu&&!document.getElementById('build435')){
  const b=document.createElement('small');b.id='build435';b.textContent='BUILD 435';
  b.style.cssText='display:block;text-align:right;font-size:11px;opacity:.7;margin:4px 10px;pointer-events:none';
  menu.appendChild(b);
 }
});
</script></body>""",1)
out=Path('Fidget_Racing_V435_Gallery_Removed_Support_Fixed.html')
out.write_text(s,encoding='utf-8')
print('V435 HTML written',len(s))
