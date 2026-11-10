<!-- navigatsioon -->
[← Laboritöö 6. Halduskriptid ja Git](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 7. Võrk ja SSH →](../moodul-07-vork-ssh/index.md)
<!-- /navigatsioon -->

# Moodul 6. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on shebang ja miks see vajalik on?

<details>
<summary>Vastus</summary>

Faili esimene rida kujul `#!/bin/bash`, mis määrab, millise programmiga skript käivitatakse.

</details>

**2.** Miks ei saa skripti käivitada lihtsalt nimega `skript.sh`, kui see on praeguses kataloogis?

<details>
<summary>Vastus</summary>

Praegune kataloog ei ole muutujas `PATH`. Tuleb kirjutada `./skript.sh` või panna skript `PATH`-is olevasse kataloogi.

</details>

**3.** Mis on viga reas `nimi = "Mari"`?

<details>
<summary>Vastus</summary>

Võrdusmärgi ümber ei tohi olla tühikuid. Kest tõlgendab `nimi` käsuna. Õige: `nimi="Mari"`.

</details>

**4.** Mis vahe on `"$USER"` ja `'$USER'` väljundil?

<details>
<summary>Vastus</summary>

`"$USER"` asendab muutuja väärtusega (nt `mari`), `'$USER'` väljastab teksti `$USER` muutmata kujul.

</details>

**5.** Miks tuleb muutujad panna jutumärkidesse? Too näide, kus jutumärkide puudumine põhjustab vea.

<details>
<summary>Vastus</summary>

Ilma jutumärkideta jagatakse muutuja väärtus tühikute kohalt osadeks ja metamärgid laiendatakse. Näiteks kui `fail="minu fail.txt"`, proovib `rm $fail` kustutada kaks faili `minu` ja `fail.txt`.

</details>

**6.** Mida sisaldavad `$0`, `$1`, `$#`, `"$@"` ja `$?`?

<details>
<summary>Vastus</summary>

`$0` - skripti nimi, `$1` - esimene argument, `$#` - argumentide arv, `"$@"` - kõik argumendid eraldi sõnadena, `$?` - viimase käsu väljumiskood.

</details>

**7.** Mida tähendab väljumiskood 0? Kuidas skript määrab oma väljumiskoodi?

<details>
<summary>Vastus</summary>

Edu. Skript määrab väljumiskoodi käsuga `exit N` (või on selleks viimase käsu väljumiskood).

</details>

**8.** Mida teevad `käsk1 && käsk2` ja `käsk1 || käsk2`?

<details>
<summary>Vastus</summary>

`&&` käivitab teise käsu ainult siis, kui esimene õnnestus. `||` käivitab teise käsu ainult siis, kui esimene ebaõnnestus.

</details>

**9.** Miks on rida `if [$a -eq 5]; then` vigane?

<details>
<summary>Vastus</summary>

Nurksulgude ümber peavad olema tühikud ja muutuja peaks olema jutumärkides: `if [ "$a" -eq 5 ]; then`.

</details>

**10.** Millal kasutada `case`-konstruktsiooni?

<details>
<summary>Vastus</summary>

Kui üht väärtust on vaja võrrelda paljude võimalike väärtuste või mustritega (nt skripti alamkäsud `start`, `stop`, `status`).

</details>

**11.** Miks ei tohi kirjutada `for f in $(ls *.txt)`? Kuidas õigesti?

<details>
<summary>Vastus</summary>

`ls` väljund jagatakse tühikute kohalt ja tühikutega failinimed lähevad katki. Õige: `for f in *.txt; do ... done`.

</details>

**12.** Kuidas lugeda faili rea kaupa? Miks kasutatakse võtit `read -r`?

<details>
<summary>Vastus</summary>

`while IFS= read -r rida; do ... done < fail`. Võti `-r` takistab kaldkriipsude tõlgendamist erimärkidena.

</details>

**13.** Mida teeb `local` funktsioonis?

<details>
<summary>Vastus</summary>

Muudab muutuja funktsiooni sisemiseks, nii et see ei mõjuta samanimelist muutujat ülejäänud skriptis.

</details>

**14.** Mida teeb `set -euo pipefail`?

<details>
<summary>Vastus</summary>

`-e` - lõpeta skript esimese ebaõnnestunud käsu järel; `-u` - lõpeta, kui kasutatakse defineerimata muutujat; `-o pipefail` - toru ebaõnnestub, kui ükskõik milline selle osa ebaõnnestub.

</details>

**15.** Kuidas leida vigu skriptis, mis ei tööta ootuspäraselt?

<details>
<summary>Vastus</summary>

`shellcheck skript.sh` staatiliseks kontrolliks, `bash -n skript.sh` süntaksi kontrolliks, `bash -x skript.sh` (või `set -x`) iga käsu nägemiseks täitmise ajal.

</details>

**16.** Miks võib `#!/bin/sh`-ga skript töötada AlmaLinuxis, kuid mitte Debianis?

<details>
<summary>Vastus</summary>

AlmaLinuxis on `/bin/sh` viit Bashile, seega töötavad ka Bashi laiendused. Debianis on `/bin/sh` kest `dash`, mis neid ei toeta.

</details>

**17.** Selgita Giti töövoogu: töökataloog, ettevalmistusala, kohalik hoidla, kaughoidla.

<details>
<summary>Vastus</summary>

Muudatused tehakse töökataloogis, `git add` lisab need ettevalmistusalasse, `git commit` salvestab sissekandena kohalikku hoidlasse, `git push` saadab kaughoidlasse ja `git pull` toob sealt teiste muudatused.

</details>

**18.** Mis on hea sissekande kirjeldus? Too näide heast ja halvast.

<details>
<summary>Vastus</summary>

Lühidalt mida ja miks muudeti. Hea: `Lisa nginx-i HTTP → HTTPS suunamine`. Halb: `muudatused`, `parandus`, `asd`.

</details>

**19.** Milleks on fail `.gitignore`? Mida ei tohi kunagi Giti panna?

<details>
<summary>Vastus</summary>

Määrab failid, mida Git ei jälgi (logid, ajutised failid). Kunagi ei tohi Giti panna paroole, privaatvõtmeid ega API-võtmeid.

</details>

**20.** Mis on haru ja millal seda kasutada? Kuidas tekib konflikt?

<details>
<summary>Vastus</summary>

Haru on eraldi arendusliin, mida kasutatakse uue funktsiooni või muudatuse katsetamiseks põhiharu segamata. Konflikt tekib, kui kahes harus on muudetud sama faili sama kohta.

</details>

**21.** Mida tähendab, et kest on POSIX-ühilduv? Miks ei sobi `fish` skriptide kirjutamiseks ega juurkasutaja kestaks?

<details>
<summary>Vastus</summary>

POSIX-ühilduv kest mõistab standardiga kirjeldatud süntaksit (muutujad, `if`, `for`, `$( )`, torud), nii et POSIX-skript töötab igas sellises kestas (`dash`, `bash`, `zsh`, FreeBSD `sh`, BusyBox). `fish` kasutab oma süntaksit (`set nimi väärtus`, `end`), mistõttu Bashi/POSIX-i käsud ja skriptid ei pruugi seal töötada; süsteemi hooldusskriptid ja `su -c` eeldavad POSIX-kesta.

</details>

**22.** Kuidas näed oma sisselogimiskesta ja praegu töötavat kesta? Kuidas muudad oma sisselogimiskesta ja millised kestad on lubatud?

<details>
<summary>Vastus</summary>

`echo $SHELL` (sisselogimiskest), `echo $0` või `ps -p $$` (töötav kest). Muutmine: `chsh -s /usr/bin/zsh` (enda oma) või `sudo usermod -s … kasutaja`; lubatud on failis `/etc/shells` loetletud kestad. Muudatus kehtib järgmisest sisselogimisest.

</details>

**23.** Kasutaja sisselogimiskest on `zsh`. Millise kestaga käivitatakse tema skript, mille esimene rida on `#!/bin/bash`? Miks?

<details>
<summary>Vastus</summary>

Bashiga: skripti käivitab esimesel real (*shebang*) nimetatud programm, mitte kasutaja sisselogimiskest. Seepärast saab interaktiivseks tööks valida mis tahes kesta ja skriptid töötavad ikka ühtemoodi.

</details>

**24.** Mis vahe on sisselogimiskestal ja tavalisel interaktiivsel kestal? Kuhu kirjutad Bashi aliased, et need kehtiksid alati?

<details>
<summary>Vastus</summary>

Sisselogimiskest (SSH, konsool, `su -`) loeb `/etc/profile` ja `~/.profile` (või `~/.bash_profile`); iga interaktiivne Bash loeb `~/.bashrc`. Aliased kirjutatakse faili `~/.bashrc`, sest Debiani ja Ubuntu `~/.profile` loeb selle ka sisselogimisel.

</details>

## Praktilised miniülesanded

**1.** `paaris` - saab argumendina arvu ja ütleb, kas see on paaris või paaritu. Kui argument pole täisarv, kirjutab veateate ja lõpetab koodiga 1.

<details>
<summary>Lahendus</summary>

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

`10#${1#-}` eemaldab arvu eest miinusmärgi ja sunnib selle tõlgendama kümnendarvuna - muidu annaks näiteks `08` vea (vt teooria punkt 6.2). `(( ))` puhul pole `set -e` probleemiks, sest `if`-tingimuses olevad käsud skripti ei lõpeta.

</details>

**2.** `suurimad` - näitab argumendina antud kataloogis (vaikimisi praegune kataloog) 5 suurimat faili.

<details>
<summary>Lahendus</summary>

```bash
#!/bin/bash
# suurimad - 5 suurimat faili kataloogis
set -euo pipefail
kataloog="${1:-.}"
find "$kataloog" -maxdepth 1 -type f -printf '%s\t%p\n' | sort -rn | head -5
```

</details>

**3.** `loenda` - loendab, mitu tavalist faili, kataloogi ja sümbolviita on argumendina antud kataloogis.

<details>
<summary>Lahendus</summary>

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

</details>

**4.** `pingi` - saab argumentidena hostinimed ja kontrollib iga kohta `ping -c1 -W1` abil, kas see vastab, kirjutades `OK` või `MAAS`.

<details>
<summary>Lahendus</summary>

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

</details>

**5.** `kinnita` - küsib „Kas oled kindel? (j/e)“ ja lõpetab koodiga 0, kui vastus algab tähega `j` või `J`, muidu koodiga 1.

<details>
<summary>Lahendus</summary>

```bash
#!/bin/bash
# kinnita - küsib kinnitust
read -r -p "Kas oled kindel? (j/e) " vastus
[[ "$vastus" == [jJ]* ]]
```

Skripti `kinnita` väljumiskoodiks on viimase käsu (`[[ ]]`) väljumiskood, seega `exit` pole vaja. Seda saab kasutada teistes skriptides: `kinnita && rm -r vana_kataloog`.

</details>

**6.** (Git) Näita oma Giti hoidla kolme viimase sissekande muudatusi koos failinimedega.

<details>
<summary>Lahendus</summary>

```bash
git log -3 --stat
```

</details>

**7.** (Git) Taasta failist `seire.conf` versioon, mis oli kaks sissekannet tagasi.

<details>
<summary>Lahendus</summary>

```bash
git checkout HEAD~2 -- seire.conf
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 6. Halduskriptid ja Git](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 7. Võrk ja SSH →](../moodul-07-vork-ssh/index.md)
<!-- /navigatsioon -->
