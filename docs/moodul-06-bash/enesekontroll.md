# Moodul 6. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis on shebang ja miks see vajalik on?
2. Miks ei saa skripti käivitada lihtsalt nimega `skript.sh`, kui see on praeguses kataloogis?
3. Mis on viga reas `nimi = "Mari"`?
4. Mis vahe on `"$USER"` ja `'$USER'` väljundil?
5. Miks tuleb muutujad panna jutumärkidesse? Too näide, kus jutumärkide puudumine põhjustab vea.
6. Mida sisaldavad `$0`, `$1`, `$#`, `"$@"` ja `$?`?
7. Mida tähendab väljumiskood 0? Kuidas skript määrab oma väljumiskoodi?
8. Mida teevad `käsk1 && käsk2` ja `käsk1 || käsk2`?
9. Miks on rida `if [$a -eq 5]; then` vigane?
10. Millal kasutada `case`-konstruktsiooni?
11. Miks ei tohi kirjutada `for f in $(ls *.txt)`? Kuidas õigesti?
12. Kuidas lugeda faili rea kaupa? Miks kasutatakse võtit `read -r`?
13. Mida teeb `local` funktsioonis?
14. Mida teeb `set -euo pipefail`?
15. Kuidas leida vigu skriptis, mis ei tööta ootuspäraselt?
16. Miks võib `#!/bin/sh`-ga skript töötada AlmaLinuxis, kuid mitte Debianis?
17. Selgita Giti töövoogu: töökataloog, ettevalmistusala, kohalik hoidla, kaughoidla.
18. Mis on hea sissekande kirjeldus? Too näide heast ja halvast.
19. Milleks on fail `.gitignore`? Mida ei tohi kunagi Giti panna?
20. Mis on haru ja millal seda kasutada? Kuidas tekib konflikt?

## Praktilised miniülesanded

Kirjuta järgmised skriptid ja kontrolli neid ShellCheck'iga.

1. `paaris` - saab argumendina arvu ja ütleb, kas see on paaris või paaritu. Kui argument pole täisarv, kirjutab veateate ja lõpetab koodiga 1.
2. `suurimad` - näitab argumendina antud kataloogis (vaikimisi praegune kataloog) 5 suurimat faili.
3. `loenda` - loendab, mitu tavalist faili, kataloogi ja sümbolviita on argumendina antud kataloogis.
4. `pingi` - saab argumentidena hostinimed ja kontrollib iga kohta `ping -c1 -W1` abil, kas see vastab, kirjutades `OK` või `MAAS`.
5. `kinnita` - küsib „Kas oled kindel? (j/e)“ ja lõpetab koodiga 0, kui vastus algab tähega `j` või `J`, muidu koodiga 1.
6. (Git) Näita oma Giti hoidla kolme viimase sissekande muudatusi koos failinimedega.
7. (Git) Taasta failist `seire.conf` versioon, mis oli kaks sissekannet tagasi.

---

## Vastused

1. Faili esimene rida kujul `#!/bin/bash`, mis määrab, millise programmiga skript käivitatakse.
2. Praegune kataloog ei ole muutujas `PATH`. Tuleb kirjutada `./skript.sh` või panna skript `PATH`-is olevasse kataloogi.
3. Võrdusmärgi ümber ei tohi olla tühikuid. Kest tõlgendab `nimi` käsuna. Õige: `nimi="Mari"`.
4. `"$USER"` asendab muutuja väärtusega (nt `mari`), `'$USER'` väljastab teksti `$USER` muutmata kujul.
5. Ilma jutumärkideta jagatakse muutuja väärtus tühikute kohalt osadeks ja metamärgid laiendatakse. Näiteks kui `fail="minu fail.txt"`, proovib `rm $fail` kustutada kaks faili `minu` ja `fail.txt`.
6. `$0` - skripti nimi, `$1` - esimene argument, `$#` - argumentide arv, `"$@"` - kõik argumendid eraldi sõnadena, `$?` - viimase käsu väljumiskood.
7. Edu. Skript määrab väljumiskoodi käsuga `exit N` (või on selleks viimase käsu väljumiskood).
8. `&&` käivitab teise käsu ainult siis, kui esimene õnnestus. `||` käivitab teise käsu ainult siis, kui esimene ebaõnnestus.
9. Nurksulgude ümber peavad olema tühikud ja muutuja peaks olema jutumärkides: `if [ "$a" -eq 5 ]; then`.
10. Kui üht väärtust on vaja võrrelda paljude võimalike väärtuste või mustritega (nt skripti alamkäsud `start`, `stop`, `status`).
11. `ls` väljund jagatakse tühikute kohalt ja tühikutega failinimed lähevad katki. Õige: `for f in *.txt; do ... done`.
12. `while IFS= read -r rida; do ... done < fail`. Võti `-r` takistab kaldkriipsude tõlgendamist erimärkidena.
13. Muudab muutuja funktsiooni sisemiseks, nii et see ei mõjuta samanimelist muutujat ülejäänud skriptis.
14. `-e` - lõpeta skript esimese ebaõnnestunud käsu järel; `-u` - lõpeta, kui kasutatakse defineerimata muutujat; `-o pipefail` - toru ebaõnnestub, kui ükskõik milline selle osa ebaõnnestub.
15. `shellcheck skript.sh` staatiliseks kontrolliks, `bash -n skript.sh` süntaksi kontrolliks, `bash -x skript.sh` (või `set -x`) iga käsu nägemiseks täitmise ajal.
16. AlmaLinuxis on `/bin/sh` viit Bashile, seega töötavad ka Bashi laiendused. Debianis on `/bin/sh` kest `dash`, mis neid ei toeta.
17. Muudatused tehakse töökataloogis, `git add` lisab need ettevalmistusalasse, `git commit` salvestab sissekandena kohalikku hoidlasse, `git push` saadab kaughoidlasse ja `git pull` toob sealt teiste muudatused.
18. Lühidalt mida ja miks muudeti. Hea: `Lisa nginx-i HTTP → HTTPS suunamine`. Halb: `muudatused`, `parandus`, `asd`.
19. Määrab failid, mida Git ei jälgi (logid, ajutised failid). Kunagi ei tohi Giti panna paroole, privaatvõtmeid ega API-võtmeid.
20. Haru on eraldi arendusliin, mida kasutatakse uue funktsiooni või muudatuse katsetamiseks põhiharu segamata. Konflikt tekib, kui kahes harus on muudetud sama faili sama kohta.

### Miniülesannete lahendused

```bash
#!/bin/bash
# paaris - kas arv on paaris
set -euo pipefail
if [[ ! "${1:-}" =~ ^-?[0-9]+$ ]]; then
    echo "Kasutus: $0 TÄISARV" >&2
    exit 1
fi
if (( 10#${1#-} % 2 == 0 )); then
    echo "$1 on paaris"
else
    echo "$1 on paaritu"
fi
```

```bash
#!/bin/bash
# suurimad - 5 suurimat faili kataloogis
set -euo pipefail
kataloog="${1:-.}"
find "$kataloog" -maxdepth 1 -type f -printf '%s\t%p\n' | sort -rn | head -5
```

```bash
#!/bin/bash
# loenda - failide, kataloogide ja viitade arv
set -euo pipefail
kataloog="${1:-.}"
[ -d "$kataloog" ] || { echo "Kataloogi $kataloog ei ole" >&2; exit 1; }
echo "Faile:     $(find "$kataloog" -maxdepth 1 -type f | wc -l)"
echo "Katalooge: $(find "$kataloog" -mindepth 1 -maxdepth 1 -type d | wc -l)"
echo "Viitu:     $(find "$kataloog" -maxdepth 1 -type l | wc -l)"
```

```bash
#!/bin/bash
# pingi - kas hostid vastavad
for host in "$@"; do
    if ping -c1 -W1 "$host" &>/dev/null; then
        echo "$host: OK"
    else
        echo "$host: MAAS"
    fi
done
```

```bash
#!/bin/bash
# kinnita - küsib kinnitust
read -r -p "Kas oled kindel? (j/e) " vastus
[[ "$vastus" == [jJ]* ]]
```

Skripti `kinnita` väljumiskoodiks on viimase käsu (`[[ ]]`) väljumiskood, seega `exit` pole vaja. Seda saab kasutada teistes skriptides: `kinnita && rm -r vana_kataloog`.

`10#${1#-}` eemaldab arvu eest miinusmärgi ja sunnib selle tõlgendama kümnendarvuna - muidu annaks näiteks `08` vea (vt teooria punkt 6.2). `(( ))` puhul pole `set -e` probleemiks, sest `if`-tingimuses olevad käsud skripti ei lõpeta.

Git-ülesanded 6 ja 7:

```bash
git log -3 --stat
git checkout HEAD~2 -- seire.conf
```
