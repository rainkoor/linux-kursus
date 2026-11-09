# Moodul 25. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis on FreeBSD baassüsteem ja mille poolest erineb see Linuxi distrost?
2. Miks on FreeBSD-s lisatarkvara seadistusfailid kataloogis `/usr/local/etc`, mitte `/etc`?
3. Mis vahe on `pkg`-l, portidel ja `freebsd-update`-il? Mida tähendab pkgbase?
4. Mis vahe on pakihoidla harudel `quarterly` ja `latest`?
5. Kuidas lubad teenuse käivitumise alglaadimisel ja käivitad selle kohe? Milline fail seda seadistust hoiab?
6. Mis on `/etc/master.passwd` ja miks muudetakse kasutajafaile `vipw`-ga?
7. Mis tingimusel saab FreeBSD-s `su`-ga juurkasutajaks? Mis on `doas`?
8. Kuidas seadistad FreeBSD-s püsiva staatilise IPv4 aadressi ja vaikelüüsi?
9. Mis on alglaadimiskeskkond ja kuidas see aitab uuendusi turvaliselt teha? Mida see tagasi ei võta?
10. Mida tähendab pf-is „viimane sobiv reegel kehtib“? Milleks on `quick`?
11. Miks võib pf-i esmakordne sisselülitamine SSH kaudu ühenduse katkestada ja kuidas seda vältida?
12. Mis on jail ja mille poolest erineb see virtuaalmasinast ning Linuxi konteinerist?
13. Miks kirjutatakse FreeBSD-s skripti algusesse `#!/bin/sh` või `#!/usr/bin/env bash`, mitte `#!/bin/bash`?
14. Nimeta kolm GNU ja BSD tööriistade erinevust, millega tuleb skriptides arvestada.

## Praktilised miniülesanded

1. Kirjuta käsud, mis paigaldavad PostgreSQL-i serveri paketi, lubavad selle alglaadimisel ja käivitavad.
2. Kirjuta käsud, mis loovad grupi `arendajad`, kasutaja `liis` (kodukataloog, kest `sh`) ja lisavad `liis`-i gruppidesse `arendajad` ja `wheel`.
3. Kirjuta `pf.conf`, mis blokeerib kõik sissetuleva, lubab väljuva liikluse ning sissetuleva SSH ainult võrgust `10.0.83.0/24`.

---

## Vastused

1. Baassüsteem on kernel, C-teek, põhikäsud, alglaadija ja dokumentatsioon, mida arendatakse ühes hoidlas ja väljastatakse koos ühe versioonina. Linuxi distro paneb kokku kerneli ja eri projektide tööriistad.
2. Baassüsteem ja kolmanda osapoole tarkvara on rangelt eraldatud: baassüsteem `/`, `/usr`, `/etc`; paketid `/usr/local`. Nii ei kirjuta baassüsteemi uuendus pakettide faile üle ja vastupidi ning on selge, mis kust pärineb.
3. `pkg` paigaldab ja uuendab valmis kolmanda osapoole pakette; pordid on retseptid, millest saab tarkvara ise kompileerida (ka teiste valikutega); `freebsd-update` uuendab traditsioonilise paigalduse baassüsteemi ja kernelit. pkgbase - baassüsteem on samuti pakettidena ja kogu süsteemi uuendab `pkg`.
4. `quarterly` - stabiilne haru, uued versioonid kord kvartalis, vahepeal ainult turva- ja veaparandused (vaikimisi); `latest` - alati värskeimad versioonid.
5. `sysrc teenus_enable=YES` ja `service teenus start`; seade on failis `/etc/rc.conf`.
6. Kasutajakontode põhifail koos parooliräsidega (Linuxi `/etc/shadow` vaste); sellest genereeritakse `/etc/passwd` ja andmebaasid. `vipw` lukustab faili, kontrollib seda ja käivitab `pwd_mkdb`.
7. Kasutaja peab kuuluma gruppi `wheel`. `doas` on OpenBSD-st pärit lihtne `sudo` alternatiiv, mida seadistatakse failis `/usr/local/etc/doas.conf` (nt `permit persist :wheel`).
8. `sysrc ifconfig_vtnet0="inet 10.0.83.66/24"`, `sysrc defaultrouter="10.0.83.1"`, DNS `/etc/resolv.conf`; rakendamiseks `service netif restart && service routing restart`.
9. ZFS-i juurfailisüsteemi kloon, millest saab alglaadida. Enne uuendust luuakse keskkond; kui uuendus ebaõnnestub, aktiveeritakse vana ja taaskäivitatakse. Eraldi andmekogumid (kodukataloogid, logid) ei lähe tagasi.
10. Pakettidele rakendatakse reegel, mis faili järjekorras **viimasena** sobib (erinevalt nftables'ist ja iptables'ist). `quick` lõpetab kontrolli kohe sellel reeglil.
11. Olemasoleva SSH-ühenduse pakettidel pole pf-i olekutabelis kirjet ja `block in all` võib need blokeerida. Lülita pf sisse konsoolist või kasuta ajutist laadimist (`pfctl -f …; sleep 60; pfctl -d`).
12. Isoleeritud keskkond oma failisüsteemi juure, IP-aadressi, kasutajate ja protsessidega, kuid sama kerneliga. VM-il on oma kernel ja virtuaalne riistvara (raskem, isoleeritum). Linuxi konteiner kasutab nimeruume ja cgroupe ning tavaliselt registrist pärit pilte; jail on kerneli eraldi alamsüsteem ja põhineb baassüsteemi koopial või ZFS-i kloonil.
13. Bash ei ole baassüsteemis; pakett paigaldab selle `/usr/local/bin/bash`. `#!/bin/sh` on alati olemas; `#!/usr/bin/env bash` leiab bashi `PATH`-ist.
14. Nt `sed -i` vajab BSD-s argumenti (`sed -i ''`); `ls --color` asemel `ls -G`; `grep -P` puudub; `date -d` asemel `date -v`/`-j -f`; `stat` võtmed erinevad (`stat -f`); `find` ja `xargs` võtmed erinevad osaliselt.

### Miniülesannete lahendused

```sh
pkg search postgresql | grep server           # vali versioon, nt postgresql17-server
pkg install -y postgresql17-server
sysrc postgresql_enable=YES
service postgresql initdb
service postgresql start
```

```sh
pw groupadd arendajad
pw useradd liis -m -s /bin/sh -G arendajad,wheel
passwd liis
```

```text
ext_if = "vtnet0"
set skip on lo0
block in all
pass out all keep state
pass in on $ext_if proto tcp from 10.0.83.0/24 to port ssh keep state
```

<!-- navigatsioon -->
---

[← Laboritöö 25. FreeBSD server](labor.md) · [Sisukord](../../README.md#sisukord) · [Laborikeskkond ja serverite paigaldus →](../lisad/paigaldus.md)
<!-- /navigatsioon -->
