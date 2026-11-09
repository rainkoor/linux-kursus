<!-- navigatsioon -->
[← Laboritöö 2. Logide analüüs ja failide haldus](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 3. Kasutajad, grupid ja õigused →](../moodul-03-kasutajad-oigused/index.md)
<!-- /navigatsioon -->

# Moodul 2. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Kuidas väljuda vim-ist muudatusi salvestamata? Aga salvestades?
2. Nimeta kolm standardvoogu ja nende numbrid.
3. Mis vahe on tähistel `>` ja `>>`?
4. Mida teeb käsk `find / -name "*.log" 2>/dev/null`? Mis on `/dev/null`?
5. Mis vahe on ümbersuunamisel (`>`) ja torul (`|`)?
6. Miks tuleb enne käsku `uniq` sisend tavaliselt sorteerida?
7. Mida teeb käsk `cut -d: -f1,3 /etc/passwd`?
8. Mida teevad `grep` võtmed `-i`, `-v`, `-c` ja `-r`?
9. Mida tähendavad regulaaravaldises `^`, `$`, `.` ja `*`?
10. Miks võib `*` tähendada kestas ja regulaaravaldises eri asju? Too näide.
11. Mis vahe on sümbolviidal ja kõvaviidal?
12. Mida tähendavad `tar` võtmed `c`, `x`, `t`, `z` ja `f`?
13. Mis juhtub algse failiga, kui pakid selle käsuga `gzip`?
14. Kuidas muuta failis kõik sõnad `http` sõnadeks `https` nii, et muudatus salvestatakse faili? Mida peaks enne tegema?
15. Mida teeb käsk `sort | uniq -c | sort -rn | head -5`?
16. Milleks kasutatakse `diff -u` ja `patch`-i? Mida tähendavad `+` ja `-` read?
17. Mida teeb `xargs` ja miks kasutatakse koos sellega `find -print0` ja `xargs -0`?

## Praktilised miniülesanded

1. Loenda, mitu kasutajat on failis `/etc/passwd`.
2. Kuva failist `/etc/passwd` kasutajad, kelle UID on vähemalt 1000, sorteerituna tähestiku järgi.
3. Leia kataloogist `/etc` kõik kataloogid, mille nimi algab tähega `s`.
4. Kuva käsu `df -h` väljundist ainult failisüsteemi nimi ja kasutuse protsent.
5. Asenda failis `test.txt` (loo see enne) kõik sõnad `kass` sõnaga `koer`, kontrollides tulemust enne faili muutmist.
6. Loo kataloogist `/etc/ssh` arhiiv `ssh-varu.tar.gz` oma kodukataloogi. (Vihje: mõnele failile pole tavakasutajal lugemisõigust - mida teed veateadetega?)

---

## Vastused

1. Salvestamata: **Esc**, seejärel `:q!` ja Enter. Salvestades: **Esc**, seejärel `:wq` (või `:x`) ja Enter.
2. **stdin** (0) - standardsisend, **stdout** (1) - standardväljund, **stderr** (2) - standardveaväljund.
3. `>` kirjutab faili üle, `>>` lisab faili lõppu.
4. Otsib kogu failisüsteemist faile, mille nimi lõpeb laiendiga `.log`, ja peidab veateated. `/dev/null` on eriline seadmefail, mis neelab kõik sinna kirjutatu.
5. Ümbersuunamine saadab väljundi **faili**, toru saadab selle **teise käsu** sisendiks.
6. `uniq` eemaldab ainult **järjestikused** korduvad read. Kui sisend pole sorteeritud, jäävad mittekõrvuti asuvad kordused alles.
7. Kuvab failist `/etc/passwd` 1. välja (kasutajanimi) ja 3. välja (UID), kasutades eraldajana koolonit.
8. `-i` - tõstutundetu otsing, `-v` - näita ridu, mis mustrile ei vasta, `-c` - loenda vastavad read, `-r` - otsi rekursiivselt kõigist kataloogi failidest.
9. `^` - rea algus, `$` - rea lõpp, `.` - üks suvaline märk, `*` - eelmine märk null või rohkem korda.
10. Kestas on `*` metamärk, mis tähendab „suvaline hulk mis tahes märke failinimes“ (nt `*.txt`). Regulaaravaldises tähendab `*` „eelmine märk null või rohkem korda“ (nt `ko*t` sobib sõnadega `kt`, `kot`, `koot`). Seepärast tuleb regulaaravaldised panna ülakomadesse, et kest neid ei laiendaks.
11. Sümbolviit viitab faili **nimele** ja läheb katki, kui algne fail kustutatakse; see võib viidata kataloogile ja teisele failisüsteemile. Kõvaviit on sama andmete (i-sõlme) teine nimi; andmed jäävad alles, kuni viimane nimi on kustutatud; see ei saa viidata kataloogile ega teisele failisüsteemile.
12. `c` - loo arhiiv, `x` - paki lahti, `t` - näita sisu, `z` - kasuta gzip-pakkimist, `f` - järgneb arhiivifaili nimi.
13. Algne fail asendatakse pakitud failiga (`fail` → `fail.gz`).
14. `sed -i 's/http/https/g' fail` - kuid enne tuleb muster ilma võtmeta `-i` läbi proovida ja/või failist koopia teha. Tähelepanu: muster `http` sobib ka olemasolevale sõnale `https`, millest saaks `httpss`. Täpsem muster oleks nt `s|http://|https://|g`.
15. Loendab, mitu korda iga rida esineb, ja kuvab 5 kõige sagedamini esinevat rida koos nende arvuga.
16. `diff -u` näitab failide erinevusi ühtses vormingus (paik); `patch` rakendab selle teisele failile. `-` on eemaldatud rida, `+` lisatud rida.
17. `xargs` loeb sisendist sõnu/ridu ja annab need käsule argumentideks. `-print0`/`-0` eraldavad failinimed nullmärgiga, nii et tühikute ja erimärkidega failinimed ei lähe katki.

### Miniülesannete lahendused

```bash
wc -l < /etc/passwd
awk -F: '$3 >= 1000 {print $1}' /etc/passwd | sort
find /etc -maxdepth 1 -type d -name "s*"
df -h | awk '{print $1, $5}'
echo "minu kass ja naabri kass" > test.txt
sed 's/kass/koer/g' test.txt          # kontrolli
sed -i 's/kass/koer/g' test.txt       # muuda
tar -czf ~/ssh-varu.tar.gz /etc/ssh 2>/dev/null
```

Viimases ülesandes jäävad privaatvõtmed (`ssh_host_*_key`) arhiivist välja, sest tavakasutajal pole neile lugemisõigust. Õigustest räägime moodulis 3. Võti `-maxdepth 1` piirab otsingu ainult kataloogi `/etc` enda sisuga.

<!-- navigatsioon -->
---

[← Laboritöö 2. Logide analüüs ja failide haldus](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 3. Kasutajad, grupid ja õigused →](../moodul-03-kasutajad-oigused/index.md)
<!-- /navigatsioon -->
