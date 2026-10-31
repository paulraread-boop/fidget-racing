from pathlib import Path
p=Path("app/src/main/assets/index.html")
s=p.read_text(encoding="utf-8")
assert 'id="b431Field"' in s and 'b431-pick-field-js' in s, "B431 Pick Your Field not found"
s=s.replace('🏁 PICK YOUR FIELD · B431','🏁 PICK YOUR FIELD · B432')
s=s.replace('const launcher=document.createElement(\'button\');launcher.id=\'b431Launch\';',"""// Move the modal outside the zoomed body, keeping it viewport-sized.
 document.documentElement.appendChild(panel);
 const launcher=document.createElement('button');launcher.id='b431Launch';""")
css="""<style id="b432-field-layout">
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
print("B432 layout applied")
