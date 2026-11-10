<!-- navigatsioon -->
[← Laboritöö 2. Logide analüüs ja failide haldus](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 3. Kasutajad, grupid ja õigused →](../moodul-03-kasutajad-oigused/index.md)
<!-- /navigatsioon -->

# Moodul 2. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Kuidas väljuda vim-ist muudatusi salvestamata? Aga salvestades?

<details>
<summary>Vastus</summary>

Salvestamata: **Esc**, seejärel `:q!` ja Enter. Salvestades: **Esc**, seejärel `:wq` (või `:x`) ja Enter.

</details>

**2.** Nimeta kolm standardvoogu ja nende numbrid.

<details>
<summary>Vastus</summary>

**stdin** (0) - standardsisend, **stdout** (1) - standardväljund, **stderr** (2) - standardveaväljund.

</details>

**3.** Mis vahe on tähistel `>` ja `>>`?

<details>
<summary>Vastus</summary>

`>` kirjutab faili üle, `>>` lisab faili lõppu.

</details>

**4.** Mida teeb käsk `find / -name "*.log" 2>/dev/null`? Mis on `/dev/null`?

<details>
<summary>Vastus</summary>

Otsib kogu failisüsteemist faile, mille nimi lõpeb laiendiga `.log`, ja peidab veateated. `/dev/null` on eriline seadmefail, mis neelab kõik sinna kirjutatu.

</details>

**5.** Mis vahe on ümbersuunamisel (`>`) ja torul (`|`)?

<details>
<summary>Vastus</summary>

Ümbersuunamine saadab väljundi **faili**, toru saadab selle **teise käsu** sisendiks.

</details>

**6.** Miks tuleb enne käsku `uniq` sisend tavaliselt sorteerida?

<details>
<summary>Vastus</summary>

`uniq` eemaldab ainult **järjestikused** korduvad read. Kui sisend pole sorteeritud, jäävad mittekõrvuti asuvad kordused alles.

</details>

**7.** Mida teeb käsk `cut -d: -f1,3 /etc/passwd`?

<details>
<summary>Vastus</summary>

Kuvab failist `/etc/passwd` 1. välja (kasutajanimi) ja 3. välja (UID), kasutades eraldajana koolonit.

</details>

**8.** Mida teevad `grep` võtmed `-i`, `-v`, `-c` ja `-r`?

<details>
<summary>Vastus</summary>

`-i` - tõstutundetu otsing, `-v` - näita ridu, mis mustrile ei vasta, `-c` - loenda vastavad read, `-r` - otsi rekursiivselt kõigist kataloogi failidest.

</details>

**9.** Mida tähendavad regulaaravaldises `^`, `$`, `.` ja `*`?

<details>
<summary>Vastus</summary>

`^` - rea algus, `$` - rea lõpp, `.` - üks suvaline märk, `*` - eelmine märk null või rohkem korda.

</details>

**10.** Miks võib `*` tähendada kestas ja regulaaravaldises eri asju? Too näide.

<details>
<summary>Vastus</summary>

Kestas on `*` metamärk, mis tähendab „suvaline hulk mis tahes märke failinimes“ (nt `*.txt`). Regulaaravaldises tähendab `*` „eelmine märk null või rohkem korda“ (nt `ko*t` sobib sõnadega `kt`, `kot`, `koot`). Seepärast tuleb regulaaravaldised panna ülakomadesse, et kest neid ei laiendaks.

</details>

**11.** Mis vahe on sümbolviidal ja kõvaviidal?

<details>
<summary>Vastus</summary>

Sümbolviit viitab faili **nimele** ja läheb katki, kui algne fail kustutatakse; see võib viidata kataloogile ja teisele failisüsteemile. Kõvaviit on sama andmete (i-sõlme) teine nimi; andmed jäävad alles, kuni viimane nimi on kustutatud; see ei saa viidata kataloogile ega teisele failisüsteemile.

</details>

**12.** Mida tähendavad `tar` võtmed `c`, `x`, `t`, `z` ja `f`?

<details>
<summary>Vastus</summary>

`c` - loo arhiiv, `x` - paki lahti, `t` - näita sisu, `z` - kasuta gzip-pakkimist, `f` - järgneb arhiivifaili nimi.

</details>

**13.** Mis juhtub algse failiga, kui pakid selle käsuga `gzip`?

<details>
<summary>Vastus</summary>

Algne fail asendatakse pakitud failiga (`fail` → `fail.gz`).

</details>

**14.** Kuidas muuta failis kõik sõnad `http` sõnadeks `https` nii, et muudatus salvestatakse faili? Mida peaks enne tegema?

<details>
<summary>Vastus</summary>

`sed -i 's/http/https/g' fail` - kuid enne tuleb muster ilma võtmeta `-i` läbi proovida ja/või failist koopia teha. Tähelepanu: muster `http` sobib ka olemasolevale sõnale `https`, millest saaks `httpss`. Täpsem muster oleks nt `s|http://|https://|g`.

</details>

**15.** Mida teeb käsk `sort | uniq -c | sort -rn | head -5`?

<details>
<summary>Vastus</summary>

Loendab, mitu korda iga rida esineb, ja kuvab 5 kõige sagedamini esinevat rida koos nende arvuga.

</details>

**16.** Milleks kasutatakse `diff -u` ja `patch`-i? Mida tähendavad `+` ja `-` read?

<details>
<summary>Vastus</summary>

`diff -u` näitab failide erinevusi ühtses vormingus (paik); `patch` rakendab selle teisele failile. `-` on eemaldatud rida, `+` lisatud rida.

</details>

**17.** Mida teeb `xargs` ja miks kasutatakse koos sellega `find -print0` ja `xargs -0`?

<details>
<summary>Vastus</summary>

`xargs` loeb sisendist sõnu/ridu ja annab need käsule argumentideks. `-print0`/`-0` eraldavad failinimed nullmärgiga, nii et tühikute ja erimärkidega failinimed ei lähe katki.

</details>

**18.** Selgita UNIX-i filosoofia põhimõtteid käsuahela `cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn` näitel.

<details>
<summary>Vastus</summary>

Iga käsk teeb üht asja (`cut` võtab välja, `sort` sorteerib, `uniq -c` loendab, `sort -rn` järjestab arvu järgi), käsud töötavad koos torude kaudu ja nende vaheline liides on tekst. Ükski käsk ei tea, et tegu on kestadega - sama ahelaga saab loendada ka logide IP-aadresse.

</details>

**19.** Kust pärinevad käsud `ls`, `find` ja `mount`? Kuidas leiad, millisest paketist mõni käsk pärineb?

<details>
<summary>Vastus</summary>

`ls` on GNU paketis `coreutils`, `find` GNU paketis `findutils` ja `mount` Linuxi projekti paketis `util-linux`. Paketi leiab Debianis/Ubuntus käsuga `dpkg -S /usr/bin/ls`, AlmaLinuxis `rpm -qf /usr/bin/ls`; `type käsk` näitab enne, kas tegu on üldse programmiga.

</details>

**20.** Miks võib Linuxis töötav skript FreeBSD-s, macOS-is või Alpine'i konteineris vea anda?

<details>
<summary>Vastus</summary>

Linuxi distrodes on GNU tööriistad, millel on lisavõtmeid (`sed -i`, `grep -P`, `date -d`, pikad võtmed), mida POSIX ei nõua. FreeBSD-s ja macOS-is on BSD tööriistad, Alpine'is BusyBox, kus neid võtmeid pole või need töötavad teisiti. Kõikjal töötav skript peab kasutama ainult POSIX-võtmeid.

</details>

## Praktilised miniülesanded

**1.** Loenda, mitu kasutajat on failis `/etc/passwd`.

<details>
<summary>Lahendus</summary>

```bash
wc -l < /etc/passwd
```

</details>

**2.** Kuva failist `/etc/passwd` kasutajad, kelle UID on vähemalt 1000, sorteerituna tähestiku järgi.

<details>
<summary>Lahendus</summary>

```bash
awk -F: '$3 >= 1000 {print $1}' /etc/passwd | sort
```

</details>

**3.** Leia kataloogist `/etc` kõik kataloogid, mille nimi algab tähega `s`.

<details>
<summary>Lahendus</summary>

```bash
find /etc -maxdepth 1 -type d -name "s*"
```

Võti `-maxdepth 1` piirab otsingu ainult kataloogi `/etc` enda sisuga.

</details>

**4.** Kuva käsu `df -h` väljundist ainult failisüsteemi nimi ja kasutuse protsent.

<details>
<summary>Lahendus</summary>

```bash
df -h | awk '{print $1, $5}'
```

</details>

**5.** Asenda failis `test.txt` (loo see enne) kõik sõnad `kass` sõnaga `koer`, kontrollides tulemust enne faili muutmist.

<details>
<summary>Lahendus</summary>

```bash
echo "minu kass ja naabri kass" > test.txt
sed 's/kass/koer/g' test.txt          # kontrolli
sed -i 's/kass/koer/g' test.txt       # muuda
```

</details>

**6.** Loo kataloogist `/etc/ssh` arhiiv `ssh-varu.tar.gz` oma kodukataloogi. (Vihje: mõnele failile pole tavakasutajal lugemisõigust - mida teed veateadetega?)

<details>
<summary>Lahendus</summary>

```bash
tar -czf ~/ssh-varu.tar.gz /etc/ssh 2>/dev/null
```

Privaatvõtmed (`ssh_host_*_key`) jäävad arhiivist välja, sest tavakasutajal pole neile lugemisõigust. Õigustest räägime moodulis 3.

</details>

<!-- navigatsioon -->
---

[← Laboritöö 2. Logide analüüs ja failide haldus](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 3. Kasutajad, grupid ja õigused →](../moodul-03-kasutajad-oigused/index.md)
<!-- /navigatsioon -->
