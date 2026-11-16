<!-- navigatsioon -->
[← Laboritöö 1. Esimesed sammud käsureal](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 2. Failid, tekst ja torud →](../moodul-02-failid-tekst-torud/index.md)
<!-- /navigatsioon -->

# Moodul 1. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis vahe on Linuxi kernelil ja Linuxi distributsioonil?

<details>
<summary>Vastus</summary>

**Kernel** on operatsioonisüsteemi tuum, mis haldab riistvara ja ressursse. **Distributsioon** on terviklik operatsioonisüsteem, mis koosneb kernelist ja selle ümber valitud tarkvarast, pakihaldurist ja seadistustest.

</details>

**2.** Millisesse perekonda kuuluvad Debian, Ubuntu ja AlmaLinux? Milliseid pakihaldureid need kasutavad?

<details>
<summary>Vastus</summary>

Debian ja Ubuntu kuuluvad **Debiani** perekonda ja kasutavad pakihaldurit `apt`. AlmaLinux kuulub **Red Hati** (RHEL) perekonda ja kasutab pakihaldurit `dnf`.

</details>

**3.** Mis vahe on terminalil ja kestal?

<details>
<summary>Vastus</summary>

**Terminal** on programm, mis kuvab tekstiakent ja edastab klahvivajutused. **Kest** (nt Bash) on programm, mis tõlgendab käske ja käivitab neid.

</details>

**4.** Mida tähendab viip `root@server:/etc#`?

<details>
<summary>Vastus</summary>

Kasutaja on `root` (juurkasutaja), masina nimi on `server`, praegune kataloog on `/etc` ja märk `#` näitab, et töötad juurkasutaja õigustes.

</details>

**5.** Kas `ls -la` ja `ls -l -a` annavad sama tulemuse? Miks?

<details>
<summary>Vastus</summary>

Jah. Lühikesi võtmeid võib kirjutada kokku, nii et `-la` on sama mis `-l -a`.

</details>

**6.** Kuidas leida käsu kohta abi, kui sa tead käsu nime? Aga kui sa ei tea?

<details>
<summary>Vastus</summary>

Kui nimi on teada: `man käsk` või `käsk --help`. Kui nimi pole teada: `man -k märksõna` (ingliskeelne märksõna) või otsing distro dokumentatsioonist.

</details>

**7.** Millises kataloogis asuvad tavaliselt süsteemi konfiguratsioonifailid? Aga logifailid?

<details>
<summary>Vastus</summary>

Konfiguratsioonifailid asuvad kataloogis `/etc`, logifailid kataloogis `/var/log`.

</details>

**8.** Mis vahe on absoluutsel ja suhtelisel teel? Too kummagi kohta näide.

<details>
<summary>Vastus</summary>

**Absoluutne tee** algab juurkataloogist ja kehtib igalt poolt, nt `/etc/hostname`. **Suhteline tee** algab praegusest kataloogist, nt `../pildid`.

</details>

**9.** Oled kataloogis `/home/mari/dokumendid`. Millisesse kataloogi viib käsk `cd ../../jaan`?

<details>
<summary>Vastus</summary>

Kataloogi `/home/jaan`.

</details>

**10.** Mida teeb käsk `cd -`?

<details>
<summary>Vastus</summary>

Viib tagasi eelmisesse kataloogi, kus viimati olid.

</details>

**11.** Kuidas tunned ära peidetud faili? Kuidas seda näha?

<details>
<summary>Vastus</summary>

Peidetud faili nimi algab punktiga (nt `.bashrc`). Neid näeb käsuga `ls -a`.

</details>

**12.** Miks on käsk `rm -r *` ohtlik? Mida peaks enne selle käivitamist kontrollima?

<details>
<summary>Vastus</summary>

See kustutab jäädavalt kõik praeguse kataloogi failid ja alamkataloogid koos sisuga ning prügikasti ei ole. Enne tuleb kontrollida käsuga `pwd`, kus oled, ja käsuga `ls`, mida kustutad.

</details>

**13.** Mida tähendavad metamärgid `*`, `?` ja `[ ]`?

<details>
<summary>Vastus</summary>

`*` - suvaline hulk mis tahes märke (ka null märki); `?` - täpselt üks suvaline märk; `[ ]` - üks märk sulgudes toodud loetelust.

</details>

**14.** Miks ei saa Linuxis faili tüüpi alati laiendi järgi otsustada? Millise käsuga tüüpi kontrollida?

<details>
<summary>Vastus</summary>

Linuxis on laiend lihtsalt osa failinimest ega määra faili tüüpi. Tüüpi saab kontrollida käsuga `file`, mis uurib faili sisu.

</details>

**15.** Kuidas teada saada, milline distro ja versioon on masinal?

<details>
<summary>Vastus</summary>

`cat /etc/os-release` või `hostnamectl`.

</details>

**16.** Milliste käskudega näed töötavas masinas protsessorit, mälu ja kettaid?

<details>
<summary>Vastus</summary>

`lscpu` (protsessor), `free -h` (mälu), `lsblk` ja `df -h` (kettad ja vaba ruum).

</details>

**17.** Miks ei piisa riistvara valimisel distro miinimumnõuete vaatamisest?

<details>
<summary>Vastus</summary>

Miinimumnõuded ütlevad ainult, et süsteem käivitub. Tegelik vajadus sõltub masina rollist: kasutajate arvust, andmete mahust ja kasvust, teenustest ning sellest, kui kaua tohib masin maas olla.

</details>

**18.** Mille poolest erinevad vastastikune (GPL) ja lubav (MIT, BSD, Apache) litsents?

<details>
<summary>Vastus</summary>

GPL nõuab, et muudetud versiooni levitamisel avaldatakse ka lähtekood sama litsentsiga. Lubav litsents lubab koodi kasutada ka kinnises tootes, kui autoriõiguse märge säilib.

</details>

**19.** Mis vahe on failidel `.iso`, `.img` ja `.qcow2`? Miks kontrollitakse allalaaditud kujutise kontrollsummat?

<details>
<summary>Vastus</summary>

`.iso` on CD/DVD kujutis (paigaldusmeedia), `.img` ketta või mälupulga toorkujutis, `.qcow2` virtuaalmasina ketas (KVM/Proxmox). Kontrollsumma (`sha256sum`) näitab, et fail ei ole allalaadimisel rikutud ega muudetud.

</details>

## Praktilised miniülesanded

**1.** Loo **ühe käsuga** kataloogid `~/test/2024`, `~/test/2025` ja `~/test/2026`.

<details>
<summary>Lahendus</summary>

```bash
mkdir -p ~/test/{2024,2025,2026}
```

</details>

**2.** Loo igasse neist fail `aruanne.txt`.

<details>
<summary>Lahendus</summary>

```bash
touch ~/test/{2024,2025,2026}/aruanne.txt
```

</details>

**3.** Kopeeri kataloog `~/test/2026` koos sisuga nimega `~/test/2026-varu`.

<details>
<summary>Lahendus</summary>

```bash
cp -r ~/test/2026 ~/test/2026-varu
```

</details>

**4.** Loetle käsuga `ls` ainult need kataloogid, mille nimi on `2024` või `2025`, kasutades metamärke.

<details>
<summary>Lahendus</summary>

```bash
ls -d ~/test/202[45]
```

Võti `-d` käsus `ls -d` näitab kataloogi ennast, mitte selle sisu.

</details>

**5.** Kuva faili `/etc/passwd` viimased 5 rida.

<details>
<summary>Lahendus</summary>

```bash
tail -n 5 /etc/passwd
```

</details>

**6.** Kustuta kataloog `~/test` koos kogu sisuga.

<details>
<summary>Lahendus</summary>

```bash
rm -r ~/test
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 1. Esimesed sammud käsureal](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 2. Failid, tekst ja torud →](../moodul-02-failid-tekst-torud/index.md)
<!-- /navigatsioon -->
