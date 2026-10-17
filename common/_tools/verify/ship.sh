#!/bin/zsh
# ship.sh <lab> "<commit msg>"  — коммит и пуш по порядку: подмодуль лабы, works, fixes, родитель
cd /Users/mira/Documents/projects/lab-laroboti || exit 1
lab=$1; msg=$2
CO="Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
for m in $lab works fixes; do git -C $m fetch -q; b=$(git -C $m rev-list --count HEAD..origin/main); [ "$b" != 0 ] && { echo "$m отстаёт на $b — стоп"; exit 1; }; done
git -C $lab add $lab.html && git -C $lab commit -qm "$msg

$CO" && git -C $lab push -q origin HEAD:main || { echo "ошибка в $lab"; exit 1; }
git -C works add -A && git -C works commit -qm "Changelog and generated pages: $lab format conversion

$CO" && git -C works push -q origin HEAD:main
git -C fixes add -A && git -C fixes commit -qm "State log and tools: $lab format conversion

$CO" && git -C fixes push -q origin HEAD:main
git add $lab works fixes && git commit -qm "Bump $lab, works, fixes: $lab converted to Caddy format

$CO" && git push -q origin main
for m in $lab works fixes; do [ "$(git ls-tree HEAD $m | awk '{print $3}')" = "$(git -C $m rev-parse origin/main)" ] && echo "$m указатель ok" || echo "$m УКАЗАТЕЛЬ НЕ СОВПАДАЕТ"; done
git status --short
sleep 5; ID=$(gh run list --limit 1 --json databaseId -q '.[0].databaseId'); gh run watch $ID >/dev/null 2>&1; gh run list --limit 2
