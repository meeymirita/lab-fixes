#!/bin/zsh
# vcheck.sh <lab>: сравнение видимого текста шагов до (git HEAD) и после, ошибки страницы, число врезок
S=/private/tmp/claude-501/-Users-mira-Documents-projects-lab-laroboti/047a947d-ed46-4108-b1fc-459d43763c11/scratchpad
lab=$1; cd /Users/mira/Documents/projects/lab-laroboti
rm -rf $S/old $S/new; mkdir -p $S/old $S/new
git -C $lab show HEAD:$lab.html > $S/old/$lab.html; cp $lab/$lab.html $S/new/$lab.html
python3 - $lab $S <<'PY'
import sys,json
sys.path.insert(0,'/Users/mira/Documents/projects/lab-laroboti/fixes/common/_tools')
import bundle
lab,S=sys.argv[1:3]
L=json.JSONDecoder().raw_decode(bundle.load(f'/Users/mira/Documents/projects/lab-laroboti/{lab}/{lab}.html')[11:])[0]
open(f'{S}/pw/keys_{lab}.txt','w').write('\n'.join(u['key'] for u in L['units'])+'\n')
PY
(cd $S/old && python3 -m http.server 8771 >/dev/null 2>&1 &); (cd $S/new && python3 -m http.server 8772 >/dev/null 2>&1 &); sleep 1
cd $S/pw && EXE=$(ls -d ~/Library/Caches/ms-playwright/chromium_headless_shell-1243/*/chrome-headless-shell | head -1) node vt.mjs $lab keys_$lab.txt 2>&1 | cut -c1-330
pkill -f "http.server 877"
