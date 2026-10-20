from pathlib import Path
p=Path('android-project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
needle="function start(){spectatorMode=false;"
assert s.count(needle)==1, 'Expected Build 32 start function missing'
s=s.replace(needle,"const approvedTitleHTML=$('overlay').innerHTML;\n"+needle,1)
needle="function returnToMenu(){"
assert s.count(needle)==1, 'Expected Build 32 returnToMenu missing'
helper="""function returnToFidgetHome(){
  returnToMenu();
  $('raceSetup').classList.add('hidden');
  $('overlay').innerHTML=approvedTitleHTML;
  $('overlay').classList.remove('hidden');
  $('start').onclick=start;
  $('quickRace').onclick=()=>playSelected(false,true);
  $('watchRace').onclick=startSpectating;
}
"""
s=s.replace(needle,helper+needle,1)
needle="<button class=\"primary\" id=\"again\">RACE AGAIN →</button></div>';$('again').onclick=start;"
assert s.count(needle)==1, 'Expected Build 32 results screen missing'
s=s.replace(needle,"<button class=\"primary\" id=\"again\">RACE AGAIN →</button> <button class=\"primary\" id=\"resultsHome\">BACK TO MAIN MENU</button></div>';$('again').onclick=start;$('resultsHome').onclick=returnToFidgetHome;",1)
p.write_text(s,encoding='utf-8')
print('Applied minimal Build 32 results-to-home repair')
