<!-- navigatsioon -->
[← Laboritöö 19. DHCP, PXE ja iSCSI](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 20. Kataloogiteenused: OpenLDAP →](../moodul-20-openldap/index.md)
<!-- /navigatsioon -->

# Moodul 19. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mida tähendab DORA? Miks on DHCPDISCOVER leviedastus?

<details>
<summary>Vastus</summary>

Discover, Offer, Request, Acknowledge - nelja sõnumiga vahetus. DISCOVER on leviedastus, sest kliendil pole veel aadressi ja ta ei tea DHCP-serveri aadressi.

</details>

**2.** Miks töötab DHCP vaikimisi ainult ühes võrgusegmendis? Mis on DHCP relee?

<details>
<summary>Vastus</summary>

Leviedastused ei läbi ruutereid. DHCP relee (nt ruuteris) võtab leviedastuse vastu ja edastab selle teises võrgus asuvale DHCP-serverile.

</details>

**3.** Mis juhtub kliendiga, kui DHCP-server rendiaja keskel kaob?

<details>
<summary>Vastus</summary>

Klient kasutab aadressi edasi kuni rendi aegumiseni ja proovib vahepeal korduvalt renti uuendada. Kui rent aegub, kaotab klient aadressi.

</details>

**4.** Miks soovitatakse uutel süsteemidel ISC DHCP asemel Kea-d?

<details>
<summary>Vastus</summary>

ISC DHCP arendus on lõpetatud ja turvaparandusi ei tule; Kea on aktiivselt arendatav, toetab REST API-d ja on näiteks RHEL 10 ja OPNsense'i soovitatud lahendus.

</details>

**5.** Millise käsuga kontrollid Kea seadistuse õigsust?

<details>
<summary>Vastus</summary>

`kea-dhcp4 -t /etc/kea/kea-dhcp4.conf`.

</details>

**6.** Mis on DHCP reserveering ja kuidas see erineb staatilisest aadressist?

<details>
<summary>Vastus</summary>

DHCP-server annab kindla MAC-aadressiga kliendile alati sama aadressi; seadistus on serveris. Staatiline aadress on seadistatud masinas endas ega sõltu DHCP-serverist.

</details>

**7.** Milliseid DHCP-valikuid vajab PXE?

<details>
<summary>Vastus</summary>

Valik 66 / `next-server` (TFTP-serveri aadress) ja valik 67 / `boot-file-name` (alglaadimisfail).

</details>

**8.** Mis on TFTP ja iPXE roll PXE alglaadimisel?

<details>
<summary>Vastus</summary>

TFTP on lihtne protokoll, millega PXE-püsivara laadib alglaadimisfaili. iPXE on täiustatud alglaadimisprogramm, mis oskab HTTP-d, skripte ja menüüsid ning laadib edasi kerneli või paigaldaja.

</details>

**9.** Miks vajavad BIOS- ja UEFI-kliendid eri alglaadimisfaile?

<details>
<summary>Vastus</summary>

BIOS ja UEFI käivitavad eri vormingus programme: BIOS-il on PXE-ROM-i jaoks `.kpxe`/`.pxe`, UEFI-l EFI-rakendus `.efi`.

</details>

**10.** Mida teeb FOG ja kuidas see klassiruumis kasulik on?

<details>
<summary>Vastus</summary>

FOG salvestab etalonarvuti kettatõmmise ja paigaldab selle PXE kaudu teistele arvutitele (ka grupile korraga). Klassiruumis saab kõik arvutid kiiresti ühesuguseks või algolekusse taastada.

</details>

**11.** Mis vahe on iSCSI-l ja NFS-il?

<details>
<summary>Vastus</summary>

NFS jagab faile (failitasemel, mitu klienti korraga); iSCSI jagab plokkseadmeid - klient näeb seda nagu oma ketast ja haldab failisüsteemi ise.

</details>

**12.** Selgita mõisteid sihtmärk, initsiaator, LUN ja IQN.

<details>
<summary>Vastus</summary>

Sihtmärk - server, mis jagab kettaid; initsiaator - klient; LUN - üks jagatav ketas; IQN - unikaalne nimi kujul `iqn.AAAA-KK.pööratud.domeen:nimi`.

</details>

**13.** Kuidas tagab iSCSI sihtmärk, et ainult õige klient saab LUN-i kasutada?

<details>
<summary>Vastus</summary>

ACL-iga (lubatud initsiaatorite IQN-id) ja soovi korral CHAP-autentimisega.

</details>

**14.** Miks ei tohi ühte LUN-i korraga kasutada kaks initsiaatorit?

<details>
<summary>Vastus</summary>

Tavaline failisüsteem eeldab, et ainult üks süsteem kirjutab - kaks samaaegset kirjutajat rikuvad failisüsteemi ja andmed hävivad.

</details>

**15.** Miks kasutatakse iSCSI ketta haakimisel fstab-is valikut `_netdev`?

<details>
<summary>Vastus</summary>

Et haakimist proovitaks alles pärast võrgu ja iSCSI seansi tekkimist; muidu ebaõnnestub haakimine alglaadimisel.

</details>

**16.** Mis on vastustefail? Nimeta AlmaLinuxi, Debiani ja Ubuntu vastustefaili vormingud ning kuidas paigaldaja faili leiab.

<details>
<summary>Vastus</summary>

Fail, mis vastab paigaldaja küsimustele ette, et paigaldus toimuks ilma inimeseta. AlmaLinux: kickstart (`inst.ks=URL`), Debian: preseed (`url=URL` koos `auto=true priority=critical`), Ubuntu: autoinstall (`autoinstall ds=nocloud;s=URL`). Fail jagatakse tavaliselt HTTP kaudu ja aadress antakse kerneli parameetrina (nt iPXE skriptis).

</details>

**17.** Miks ei panda domeeni administraatori parooli kickstarti faili ja kuidas masin siis domeeniga liidetakse?

<details>
<summary>Vastus</summary>

Fail on loetav kõigile, kes pääsevad veebiserverisse (ja jääb sageli paigaldatud masinasse alles). Vastustefail paigaldab vajalikud paketid ja SSH-võtme; liitmise teeb pärast käivitust Ansible, mille parool on Vaultis (või kasutatakse ühekordset liitumisparooli).

</details>

## Praktilised miniülesanded

**1.** Lisa Kea seadistusse teine alamvõrk `10.0.84.0/24` vahemikuga `.100–.150` ja vaikelüüsiga `.1`.

<details>
<summary>Lahendus</summary>

```json
{
  "id": 2,
  "subnet": "10.0.84.0/24",
  "pools": [ { "pool": "10.0.84.100 - 10.0.84.150" } ],
  "option-data": [ { "name": "routers", "data": "10.0.84.1" } ]
}
```

(lisa massiivi `subnet4`)

</details>

**2.** Lisa Kea seadistusse globaalne NTP-serveri valik `10.0.83.1`.

<details>
<summary>Lahendus</summary>

```json
{ "name": "ntp-servers", "data": "10.0.83.1" }
```

(lisa globaalsesse massiivi `option-data`)

</details>

**3.** Kirjuta ISC DHCP reserveering masinale `printer` (MAC `00:11:22:33:44:55`, IP `10.0.83.20`).

<details>
<summary>Lahendus</summary>

```text
host printer {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 10.0.83.20;
}
```

</details>

**4.** Loo `targetcli`-s LVM-köitel `/dev/vg_san/lv_db` põhinev taust nimega `db`.

<details>
<summary>Lahendus</summary>

```text
/> backstores/block create db /dev/vg_san/lv_db
```

</details>

**5.** Kuva AlmaLinuxis kõik aktiivsed iSCSI seansid ja logi kõigist välja.

<details>
<summary>Lahendus</summary>

```bash
sudo iscsiadm -m session
sudo iscsiadm -m node --logoutall=all
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 19. DHCP, PXE ja iSCSI](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 20. Kataloogiteenused: OpenLDAP →](../moodul-20-openldap/index.md)
<!-- /navigatsioon -->
