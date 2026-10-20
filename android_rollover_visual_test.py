from pathlib import Path
p=Path("android-project/app/src/main/assets/index.html")
s=p.read_text()
old="ctx.rotate(progress*Math.PI*2);ctx.scale(1,Math.max(.18,Math.abs(Math.cos(progress*Math.PI*3))));"
new="""// 2D side-over-side tumble: tip, invert, recover; do not spin flat.
const tilt=Math.sin(progress*Math.PI*2)*0.32;
ctx.rotate(tilt);
const flip=Math.cos(progress*Math.PI*2);
ctx.scale(1,Math.max(.12,Math.abs(flip)));
ctx.translate(0,-5*Math.sin(progress*Math.PI));"""
if old not in s: raise SystemExit("Rollover source mismatch; refusing to change approved game")
s=s.replace(old,new,1)
p.write_text(s)
print("Applied rollover visual test patch; existing collision rules retained")
