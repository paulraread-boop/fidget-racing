from pathlib import Path
import re,zipfile
root=Path('work433')
files=list(root.rglob('*.html'))
assert files, 'V426 archive contained no HTML'
p=max(files,key=lambda f:f.stat().st_size)
s=p.read_text(encoding='utf-8',errors='replace')
print('Source:',p,'bytes',len(s))
# Remove ONLY 20-picture scrolling concept-car gallery entry; preserve cover/intro and car showroom.
s,n=re.subn(r'(<button\b[^>]*>\s*(?:[^<]*)(?:WATCH 20 CONCEPT CARS|Watch 20 Concept Cars)(?:[^<]*)</button>)','',s,flags=re.I)
print('Gallery menu controls removed:',n)
# Remove gallery access links without touching unrelated showroom/gallery assets.
s,n2=re.subn(r'(<button\b[^>]*>[^<]*(?:20 scrolling pictures|20 picture gallery)[^<]*</button>)','',s,flags=re.I)
print('Other gallery controls:',n2)
# Support: avoid overflow and force messages to wrap within the dialog rather than overlap fields.
style="""<style id="support-layout-fix-434">
[id*="support" i] [class*="notice" i],
[id*="support" i] [class*="message" i],
[id*="support" i] [class*="banner" i],
[class*="support" i] [class*="notice" i],
[class*="support" i] [class*="message" i]{
position:static!important;float:none!important;transform:none!important;
max-width:100%!important;width:auto!important;white-space:normal!important;
overflow-wrap:anywhere!important;line-height:1.4!important;
margin:10px 0!important;box-sizing:border-box!important;
}
[id*="support" i] input,[id*="support" i] select,[id*="support" i] textarea{
max-width:100%!important;box-sizing:border-box!important;
}
</style>"""
s=s.replace('</head>',style+'</head>',1)
# A build number ONLY in the menu, never a floating overlay.
s=s.replace('</body>',"""<script>
(function(){
 function showVersion(){
  var menu=document.querySelector('#menuOverlay, #menuModal, #mainMenu, [id*="menu" i][class*="modal" i]');
  if(!menu)return;
  if(document.getElementById('version434'))return;
  var b=document.createElement('small');b.id='version434';b.textContent='BUILD 434';
  b.style.cssText='display:block;text-align:right;font-size:11px;opacity:.7;margin:5px 10px;pointer-events:none';
  menu.appendChild(b);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',showVersion);else showVersion();
})();
</script></body>""",1)
out=Path('Fidget_Racing_V434_Gallery_Support_Chrome.html')
out.write_text(s,encoding='utf-8')
with zipfile.ZipFile('Fidget_Racing_V434_Gallery_Support_Source.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:z.write(out,'index.html')
print('Created:',out,'and source zip')
