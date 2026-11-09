<!-- navigatsioon -->
[← Laboritöö 1. Esimesed sammud käsureal](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 2. Failid, tekst ja torud →](../moodul-02-failid-tekst-torud/index.md)
<!-- /navigatsioon -->

# Moodul 1. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis vahe on Linuxi kernelil ja Linuxi distributsioonil?
2. Millisesse perekonda kuuluvad Debian, Ubuntu ja AlmaLinux? Milliseid pakihaldureid need kasutavad?
3. Mis vahe on terminalil ja kestal?
4. Mida tähendab viip `root@server:/etc#`?
5. Kas `ls -la` ja `ls -l -a` annavad sama tulemuse? Miks?
6. Kuidas leida käsu kohta abi, kui sa tead käsu nime? Aga kui sa ei tea?
7. Millises kataloogis asuvad tavaliselt süsteemi konfiguratsioonifailid? Aga logifailid?
8. Mis vahe on absoluutsel ja suhtelisel teel? Too kummagi kohta näide.
9. Oled kataloogis `/home/mari/dokumendid`. Millisesse kataloogi viib käsk `cd ../../jaan`?
10. Mida teeb käsk `cd -`?
11. Kuidas tunned ära peidetud faili? Kuidas seda näha?
12. Miks on käsk `rm -r *` ohtlik? Mida peaks enne selle käivitamist kontrollima?
13. Mida tähendavad metamärgid `*`, `?` ja `[ ]`?
14. Miks ei saa Linuxis faili tüüpi alati laiendi järgi otsustada? Millise käsuga tüüpi kontrollida?
15. Kuidas teada saada, milline distro ja versioon on masinal?

## Praktilised miniülesanded

Tee need ülesanded oma laborimasinas.

1. Loo **ühe käsuga** kataloogid `~/test/2024`, `~/test/2025` ja `~/test/2026`.
2. Loo igasse neist fail `aruanne.txt`.
3. Kopeeri kataloog `~/test/2026` koos sisuga nimega `~/test/2026-varu`.
4. Loetle käsuga `ls` ainult need kataloogid, mille nimi on `2024` või `2025`, kasutades metamärke.
5. Kuva faili `/etc/passwd` viimased 5 rida.
6. Kustuta kataloog `~/test` koos kogu sisuga.

---

## Vastused

1. **Kernel** on operatsioonisüsteemi tuum, mis haldab riistvara ja ressursse. **Distributsioon** on terviklik operatsioonisüsteem, mis koosneb kernelist ja selle ümber valitud tarkvarast, pakihaldurist ja seadistustest.
2. Debian ja Ubuntu kuuluvad **Debiani** perekonda ja kasutavad pakihaldurit `apt`. AlmaLinux kuulub **Red Hati** (RHEL) perekonda ja kasutab pakihaldurit `dnf`.
3. **Terminal** on programm, mis kuvab tekstiakent ja edastab klahvivajutused. **Kest** (nt Bash) on programm, mis tõlgendab käske ja käivitab neid.
4. Kasutaja on `root` (juurkasutaja), masina nimi on `server`, praegune kataloog on `/etc` ja märk `#` näitab, et töötad juurkasutaja õigustes.
5. Jah. Lühikesi võtmeid võib kirjutada kokku, nii et `-la` on sama mis `-l -a`.
6. Kui nimi on teada: `man käsk` või `käsk --help`. Kui nimi pole teada: `man -k märksõna` (ingliskeelne märksõna) või otsing distro dokumentatsioonist.
7. Konfiguratsioonifailid asuvad kataloogis `/etc`, logifailid kataloogis `/var/log`.
8. **Absoluutne tee** algab juurkataloogist ja kehtib igalt poolt, nt `/etc/hostname`. **Suhteline tee** algab praegusest kataloogist, nt `../pildid`.
9. Kataloogi `/home/jaan`.
10. Viib tagasi eelmisesse kataloogi, kus viimati olid.
11. Peidetud faili nimi algab punktiga (nt `.bashrc`). Neid näeb käsuga `ls -a`.
12. See kustutab jäädavalt kõik praeguse kataloogi failid ja alamkataloogid koos sisuga ning prügikasti ei ole. Enne tuleb kontrollida käsuga `pwd`, kus oled, ja käsuga `ls`, mida kustutad.
13. `*` - suvaline hulk mis tahes märke (ka null märki); `?` - täpselt üks suvaline märk; `[ ]` - üks märk sulgudes toodud loetelust.
14. Linuxis on laiend lihtsalt osa failinimest ega määra faili tüüpi. Tüüpi saab kontrollida käsuga `file`, mis uurib faili sisu.
15. `cat /etc/os-release` või `hostnamectl`.

### Miniülesannete lahendused

```bash
mkdir -p ~/test/{2024,2025,2026}
touch ~/test/{2024,2025,2026}/aruanne.txt
cp -r ~/test/2026 ~/test/2026-varu
ls -d ~/test/202[45]
tail -n 5 /etc/passwd
rm -r ~/test
```

Võti `-d` käsus `ls -d` näitab kataloogi ennast, mitte selle sisu.

<!-- navigatsioon -->
---

[← Laboritöö 1. Esimesed sammud käsureal](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 2. Failid, tekst ja torud →](../moodul-02-failid-tekst-torud/index.md)
<!-- /navigatsioon -->
