<!-- navigatsioon -->
[← Laboritöö 29. FreeBSD server](labor.md) · [Sisukord](../../README.md#sisukord) · [Laborikeskkond ja serverite paigaldus →](../lisad/paigaldus.md)
<!-- /navigatsioon -->

# Moodul 29. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on FreeBSD baassüsteem ja mille poolest erineb see Linuxi distrost?

<details>
<summary>Vastus</summary>

Baassüsteem on kernel, C-teek, põhikäsud, alglaadija ja dokumentatsioon, mida arendatakse ühes hoidlas ja väljastatakse koos ühe versioonina. Linuxi distro paneb kokku kerneli ja eri projektide tööriistad.

</details>

**2.** Miks on FreeBSD-s lisatarkvara seadistusfailid kataloogis `/usr/local/etc`, mitte `/etc`?

<details>
<summary>Vastus</summary>

Baassüsteem ja kolmanda osapoole tarkvara on rangelt eraldatud: baassüsteem `/`, `/usr`, `/etc`; paketid `/usr/local`. Nii ei kirjuta baassüsteemi uuendus pakettide faile üle ja vastupidi ning on selge, mis kust pärineb.

</details>

**3.** Mis vahe on `pkg`-l, portidel ja `freebsd-update`-il? Mida tähendab pkgbase?

<details>
<summary>Vastus</summary>

`pkg` paigaldab ja uuendab valmis kolmanda osapoole pakette; pordid on retseptid, millest saab tarkvara ise kompileerida (ka teiste valikutega); `freebsd-update` uuendab traditsioonilise paigalduse baassüsteemi ja kernelit. pkgbase - baassüsteem on samuti pakettidena ja kogu süsteemi uuendab `pkg`.

</details>

**4.** Mis vahe on pakihoidla harudel `quarterly` ja `latest`?

<details>
<summary>Vastus</summary>

`quarterly` - stabiilne haru, uued versioonid kord kvartalis, vahepeal ainult turva- ja veaparandused (vaikimisi); `latest` - alati värskeimad versioonid.

</details>

**5.** Kuidas lubad teenuse käivitumise alglaadimisel ja käivitad selle kohe? Milline fail seda seadistust hoiab?

<details>
<summary>Vastus</summary>

`sysrc teenus_enable=YES` ja `service teenus start`; seade on failis `/etc/rc.conf`.

</details>

**6.** Mis on `/etc/master.passwd` ja miks muudetakse kasutajafaile `vipw`-ga?

<details>
<summary>Vastus</summary>

Kasutajakontode põhifail koos parooliräsidega (Linuxi `/etc/shadow` vaste); sellest genereeritakse `/etc/passwd` ja andmebaasid. `vipw` lukustab faili, kontrollib seda ja käivitab `pwd_mkdb`.

</details>

**7.** Mis tingimusel saab FreeBSD-s `su`-ga juurkasutajaks? Mis on `doas`?

<details>
<summary>Vastus</summary>

Kasutaja peab kuuluma gruppi `wheel`. `doas` on OpenBSD-st pärit lihtne `sudo` alternatiiv, mida seadistatakse failis `/usr/local/etc/doas.conf` (nt `permit persist :wheel`).

</details>

**8.** Kuidas seadistad FreeBSD-s püsiva staatilise IPv4 aadressi ja vaikelüüsi?

<details>
<summary>Vastus</summary>

`sysrc ifconfig_vtnet0="inet 10.0.83.66/24"`, `sysrc defaultrouter="10.0.83.1"`, DNS `/etc/resolv.conf`; rakendamiseks `service netif restart && service routing restart`.

</details>

**9.** Mis on alglaadimiskeskkond ja kuidas see aitab uuendusi turvaliselt teha? Mida see tagasi ei võta?

<details>
<summary>Vastus</summary>

ZFS-i juurfailisüsteemi kloon, millest saab alglaadida. Enne uuendust luuakse keskkond; kui uuendus ebaõnnestub, aktiveeritakse vana ja taaskäivitatakse. Eraldi andmekogumid (kodukataloogid, logid) ei lähe tagasi.

</details>

**10.** Mida tähendab pf-is „viimane sobiv reegel kehtib“? Milleks on `quick`?

<details>
<summary>Vastus</summary>

Pakettidele rakendatakse reegel, mis faili järjekorras **viimasena** sobib (erinevalt nftables'ist ja iptables'ist). `quick` lõpetab kontrolli kohe sellel reeglil.

</details>

**11.** Miks võib pf-i esmakordne sisselülitamine SSH kaudu ühenduse katkestada ja kuidas seda vältida?

<details>
<summary>Vastus</summary>

Olemasoleva SSH-ühenduse pakettidel pole pf-i olekutabelis kirjet ja `block in all` võib need blokeerida. Lülita pf sisse konsoolist või kasuta ajutist laadimist (`pfctl -f …; sleep 60; pfctl -d`).

</details>

**12.** Mis on jail ja mille poolest erineb see virtuaalmasinast ning Linuxi konteinerist?

<details>
<summary>Vastus</summary>

Isoleeritud keskkond oma failisüsteemi juure, IP-aadressi, kasutajate ja protsessidega, kuid sama kerneliga. VM-il on oma kernel ja virtuaalne riistvara (raskem, isoleeritum). Linuxi konteiner kasutab nimeruume ja cgroupe ning tavaliselt registrist pärit pilte; jail on kerneli eraldi alamsüsteem ja põhineb baassüsteemi koopial või ZFS-i kloonil.

</details>

**13.** Miks kirjutatakse FreeBSD-s skripti algusesse `#!/bin/sh` või `#!/usr/bin/env bash`, mitte `#!/bin/bash`?

<details>
<summary>Vastus</summary>

Bash ei ole baassüsteemis; pakett paigaldab selle `/usr/local/bin/bash`. `#!/bin/sh` on alati olemas; `#!/usr/bin/env bash` leiab bashi `PATH`-ist.

</details>

**14.** Nimeta kolm GNU ja BSD tööriistade erinevust, millega tuleb skriptides arvestada.

<details>
<summary>Vastus</summary>

Nt `sed -i` vajab BSD-s argumenti (`sed -i ''`); `ls --color` asemel `ls -G`; `grep -P` puudub; `date -d` asemel `date -v`/`-j -f`; `stat` võtmed erinevad (`stat -f`); `find` ja `xargs` võtmed erinevad osaliselt.

</details>

## Praktilised miniülesanded

**1.** Kirjuta käsud, mis paigaldavad PostgreSQL-i serveri paketi, lubavad selle alglaadimisel ja käivitavad.

<details>
<summary>Lahendus</summary>

```sh
pkg search postgresql | grep server           # vali versioon, nt postgresql17-server
pkg install -y postgresql17-server
sysrc postgresql_enable=YES
service postgresql initdb
service postgresql start
```

</details>

**2.** Kirjuta käsud, mis loovad grupi `arendajad`, kasutaja `liis` (kodukataloog, kest `sh`) ja lisavad `liis`-i gruppidesse `arendajad` ja `wheel`.

<details>
<summary>Lahendus</summary>

```sh
pw groupadd arendajad
pw useradd liis -m -s /bin/sh -G arendajad,wheel
passwd liis
```

</details>

**3.** Kirjuta `pf.conf`, mis blokeerib kõik sissetuleva, lubab väljuva liikluse ning sissetuleva SSH ainult võrgust `10.0.83.0/24`.

<details>
<summary>Lahendus</summary>

```text
ext_if = "vtnet0"
set skip on lo0
block in all
pass out all keep state
pass in on $ext_if proto tcp from 10.0.83.0/24 to port ssh keep state
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 29. FreeBSD server](labor.md) · [Sisukord](../../README.md#sisukord) · [Laborikeskkond ja serverite paigaldus →](../lisad/paigaldus.md)
<!-- /navigatsioon -->
