<!-- navigatsioon -->
[← Laboritöö 19. Kooli väikeserver, IV osa: faili- ja prindiserver, varundus ja dokumentatsioon](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 20. Automatiseerimine: Ansible, Vagrant ja infrastruktuur koodina →](../moodul-20-automatiseerimine/index.md)
<!-- /navigatsioon -->

# Moodul 19. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on NFS-i `root_squash` ja miks see vaikimisi sees on?

<details>
<summary>Vastus</summary>

Kliendi juurkasutaja muudetakse serveris õigusteta kasutajaks `nobody`. Muidu saaks iga kliendi juurkasutaja serveri jagatud failidega teha kõike.

</details>

**2.** Miks on Sambal oma paroolid?

<details>
<summary>Vastus</summary>

SMB-protokoll kasutab autentimiseks teist meetodit kui Linuxi sisselogimine, mistõttu Samba vajab kasutajate jaoks oma räsisid. (Active Directory domeenis autenditakse kasutajad domeenikontrolleri kaudu.)

</details>

**3.** Millal valiksid failiserveriks TrueNASi ja millal ise seadistatud Debiani Samba ja NFS-iga? Miks peaks TrueNAS nägema päris kettaid?

<details>
<summary>Vastus</summary>

TrueNAS: palju kettaid, ZFS-i töökindlus, hetktõmmised ja replikatsioon veebiliidesest, eraldi salvestusseade. Oma Debian: kui samas masinas on ka muud teenused, vaja on täielikku kontrolli või õpitakse seadistamist. ZFS jälgib ketaste tervist ja parandab vigu ainult siis, kui tal on otseligipääs ketastele; virtuaalketaste all olevat riket ta ei näe.

</details>

**4.** Mis on autofs ja mille poolest on see parem kui NFS-i rida `/etc/fstab`-is?

<details>
<summary>Vastus</summary>

autofs haagib jagamise alles siis, kui kataloogi poole pöördutakse, ja haagib lahti tegevusetuse järel. Alglaadimine ei sõltu failiserverist ja kodukataloogid saab metamärgiga (`*`, `&`) haakida kõigile kasutajatele.

</details>

**5.** Mille poolest erineb käsiraamat (*runbook*) tavalisest serveri dokumentatsioonist? Milleks on otsuste logi?

<details>
<summary>Vastus</summary>

Dokumentatsioon kirjeldab, kuidas süsteem on ehitatud; käsiraamat annab sammhaaval tegevusjuhised kindlateks olukordadeks (rike, hooldus), mida saab järgida ka süsteemi mittetundev inimene. Otsuste logi talletab, miks midagi valiti, et hilisemad muudatused ei kordaks vanu vigu.

</details>

**6.** Mis vahe on failitasandi jagamisel (NFS, SMB) ja plokitasandi jagamisel (iSCSI)?

<details>
<summary>Vastus</summary>

NFS-i ja SMB-ga haldab failisüsteemi server ja sama kausta võivad kasutada mitu klienti korraga. iSCSI jagab plokkseadet: klient teeb sellele ise failisüsteemi ja üldjuhul tohib seda kasutada ainult üks klient korraga.

</details>

**7.** Mida teeb `/etc/exports`-is rida `/srv/data 10.0.83.0/24 (rw)` (tühikuga sulu ees) ja miks see on ohtlik?

<details>
<summary>Vastus</summary>

Tühik eraldab kaks kirjet: võrk `10.0.83.0/24` saab vaikeõigused (`ro`) ja `(rw)` ilma aadressita kehtib **kõigile** - kogu maailm saab kirjutada. Õige on `10.0.83.0/24(rw)` ilma tühikuta.

</details>

**8.** Miks vajab ühiskaust lisaks SGID-ile ka vaikimisi ACL-i?

<details>
<summary>Vastus</summary>

SGID tagab, et uued failid kuuluvad kataloogi grupile, kuid õigused määrab looja `umask` (tavaliselt `022` → grupil ainult lugemine). Vaikimisi ACL (`setfacl -d -m g:grupp:rwx`) annab grupile kirjutusõiguse kõigile uutele failidele.

</details>

**9.** Miks ei ole RAID, hetktõmmised ega Samba prügikast varukoopia?

<details>
<summary>Vastus</summary>

Need asuvad samas masinas: masina, ruumi või lunavara rünnaku korral kaovad koos andmetega. RAID kaitseb ketta rikke eest, hetktõmmised ja prügikast kiire taastamise jaoks, kuid varukoopia peab olema teises masinas ja asukohas (moodul 9).

</details>

**10.** Mida peab failiserveri varundusel lisaks failide sisule varundama?

<details>
<summary>Vastus</summary>

Õigused ja ACL-id (restic, `tar --acls`), jagamiste seadistuse (`/etc/exports`, `smb.conf`) ja Samba kasutajate andmebaasi (`/var/lib/samba/private/`), muidu tuleb pärast taastamist õigusi ja kasutajaid käsitsi parandada.

</details>

**11.** Mis on CUPS ja millist protokolli ning porti see printerite jagamiseks kasutab?

<details>
<summary>Vastus</summary>

CUPS on Linuxi (ja macOS-i) printimissüsteem. Printereid jagatakse protokolliga IPP, port 631 (TCP). Samal pordil on ka veebiliides.

</details>

**12.** Milliste käskudega näed printereid ja ootel töid, prindid faili ja tühistad töö?

<details>
<summary>Vastus</summary>

`lpstat -p -d` (printerid ja vaikeprinter), `lpstat -o` (ootel tööd), `lp -d printer fail` (prindi), `cancel töö-ID` (tühista).

</details>

**13.** Miks kasutada prindiserverit, mitte lasta igal arvutil otse printerisse printida?

<details>
<summary>Vastus</summary>

Printer ja draiver seadistatakse ühes kohas, kliendid saavad valmis järjekorra, haldur näeb ja tühistab töid keskselt, logidest on näha, kes kui palju printis, ja ligipääsu saab piirata.

</details>

## Praktilised miniülesanded

**1.** Kirjuta `/etc/exports` rida, mis jagab kataloogi `/srv/iso` kogu võrgule `10.0.0.0/8` ainult lugemiseks.

<details>
<summary>Lahendus</summary>

```text
# 2
/srv/iso  10.0.0.0/8(ro,sync,no_subtree_check)
```

</details>

**2.** Loo ühiskaust `/srv/jagatud/it`, kus grupp `it` saab kõiki faile muuta (ka teiste loodud) ja grupp `juhtkond` saab ainult lugeda.

<details>
<summary>Lahendus</summary>

```bash
sudo mkdir -p /srv/jagatud/it
sudo chown root:it /srv/jagatud/it
sudo chmod 2770 /srv/jagatud/it
sudo setfacl -m g:it:rwx,g:juhtkond:rx /srv/jagatud/it
sudo setfacl -d -m g:it:rwx,g:juhtkond:rx /srv/jagatud/it
getfacl /srv/jagatud/it
```

</details>

**3.** Kirjuta Samba jagamine `it` kataloogile `/srv/jagatud/it`, mida näevad ainult grupi `it` liikmed ja kus kustutatud failid lähevad prügikasti.

<details>
<summary>Lahendus</summary>

```ini
[it]
   path = /srv/jagatud/it
   valid users = @it
   read only = no
   inherit acls = yes
   vfs objects = recycle
   recycle:repository = .prugikast/%U
   recycle:keeptree = yes
```

Seejärel `testparm` ja `sudo systemctl reload smbd`.

</details>

**4.** Seadista autofs nii, et NFS-jagamine `debian1:/srv/iso` haagitakse ainult lugemiseks kataloogi `/mnt/auto/iso` kasutamisel.

<details>
<summary>Lahendus</summary>

```bash
echo "/mnt/auto  /etc/auto.iso  --timeout=300" | sudo tee /etc/auto.master.d/iso.autofs
echo "iso  -ro  debian1:/srv/iso" | sudo tee /etc/auto.iso
sudo systemctl restart autofs
ls /mnt/auto/iso
```

</details>

**5.** Lisa Linuxi kliendis võrguprinter, mis on jagatud serveris `debian1.lab.example` nimega `kontor`, ja prindi fail `/etc/hostname`.

<details>
<summary>Lahendus</summary>

```bash
sudo lpadmin -p kontor -E -v ipp://debian1.lab.example:631/printers/kontor -m everywhere
lp -d kontor /etc/hostname
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 19. Kooli väikeserver, IV osa: faili- ja prindiserver, varundus ja dokumentatsioon](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 20. Automatiseerimine: Ansible, Vagrant ja infrastruktuur koodina →](../moodul-20-automatiseerimine/index.md)
<!-- /navigatsioon -->
