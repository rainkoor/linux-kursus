# Moodul 19. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mida tähendab DORA? Miks on DHCPDISCOVER leviedastus?
2. Miks töötab DHCP vaikimisi ainult ühes võrgusegmendis? Mis on DHCP relee?
3. Mis juhtub kliendiga, kui DHCP-server rendiaja keskel kaob?
4. Miks soovitatakse uutel süsteemidel ISC DHCP asemel Kea-d?
5. Millise käsuga kontrollid Kea seadistuse õigsust?
6. Mis on DHCP reserveering ja kuidas see erineb staatilisest aadressist?
7. Milliseid DHCP-valikuid vajab PXE?
8. Mis on TFTP ja iPXE roll PXE alglaadimisel?
9. Miks vajavad BIOS- ja UEFI-kliendid eri alglaadimisfaile?
10. Mida teeb FOG ja kuidas see klassiruumis kasulik on?
11. Mis vahe on iSCSI-l ja NFS-il?
12. Selgita mõisteid sihtmärk, initsiaator, LUN ja IQN.
13. Kuidas tagab iSCSI sihtmärk, et ainult õige klient saab LUN-i kasutada?
14. Miks ei tohi ühte LUN-i korraga kasutada kaks initsiaatorit?
15. Miks kasutatakse iSCSI ketta haakimisel fstab-is valikut `_netdev`?
16. Mis on vastustefail? Nimeta AlmaLinuxi, Debiani ja Ubuntu vastustefaili vormingud ning kuidas paigaldaja faili leiab.
17. Miks ei panda domeeni administraatori parooli kickstarti faili ja kuidas masin siis domeeniga liidetakse?

## Praktilised miniülesanded

1. Lisa Kea seadistusse teine alamvõrk `10.0.84.0/24` vahemikuga `.100–.150` ja vaikelüüsiga `.1`.
2. Lisa Kea seadistusse globaalne NTP-serveri valik `10.0.83.1`.
3. Kirjuta ISC DHCP reserveering masinale `printer` (MAC `00:11:22:33:44:55`, IP `10.0.83.20`).
4. Loo `targetcli`-s LVM-köitel `/dev/vg_san/lv_db` põhinev taust nimega `db`.
5. Kuva AlmaLinuxis kõik aktiivsed iSCSI seansid ja logi kõigist välja.

---

## Vastused

1. Discover, Offer, Request, Acknowledge - nelja sõnumiga vahetus. DISCOVER on leviedastus, sest kliendil pole veel aadressi ja ta ei tea DHCP-serveri aadressi.
2. Leviedastused ei läbi ruutereid. DHCP relee (nt ruuteris) võtab leviedastuse vastu ja edastab selle teises võrgus asuvale DHCP-serverile.
3. Klient kasutab aadressi edasi kuni rendi aegumiseni ja proovib vahepeal korduvalt renti uuendada. Kui rent aegub, kaotab klient aadressi.
4. ISC DHCP arendus on lõpetatud ja turvaparandusi ei tule; Kea on aktiivselt arendatav, toetab REST API-d ja on näiteks RHEL 10 ja OPNsense'i soovitatud lahendus.
5. `kea-dhcp4 -t /etc/kea/kea-dhcp4.conf`.
6. DHCP-server annab kindla MAC-aadressiga kliendile alati sama aadressi; seadistus on serveris. Staatiline aadress on seadistatud masinas endas ega sõltu DHCP-serverist.
7. Valik 66 / `next-server` (TFTP-serveri aadress) ja valik 67 / `boot-file-name` (alglaadimisfail).
8. TFTP on lihtne protokoll, millega PXE-püsivara laadib alglaadimisfaili. iPXE on täiustatud alglaadimisprogramm, mis oskab HTTP-d, skripte ja menüüsid ning laadib edasi kerneli või paigaldaja.
9. BIOS ja UEFI käivitavad eri vormingus programme: BIOS-il on PXE-ROM-i jaoks `.kpxe`/`.pxe`, UEFI-l EFI-rakendus `.efi`.
10. FOG salvestab etalonarvuti kettatõmmise ja paigaldab selle PXE kaudu teistele arvutitele (ka grupile korraga). Klassiruumis saab kõik arvutid kiiresti ühesuguseks või algolekusse taastada.
11. NFS jagab faile (failitasemel, mitu klienti korraga); iSCSI jagab plokkseadmeid - klient näeb seda nagu oma ketast ja haldab failisüsteemi ise.
12. Sihtmärk - server, mis jagab kettaid; initsiaator - klient; LUN - üks jagatav ketas; IQN - unikaalne nimi kujul `iqn.AAAA-KK.pööratud.domeen:nimi`.
13. ACL-iga (lubatud initsiaatorite IQN-id) ja soovi korral CHAP-autentimisega.
14. Tavaline failisüsteem eeldab, et ainult üks süsteem kirjutab - kaks samaaegset kirjutajat rikuvad failisüsteemi ja andmed hävivad.
15. Et haakimist proovitaks alles pärast võrgu ja iSCSI seansi tekkimist; muidu ebaõnnestub haakimine alglaadimisel.
16. Fail, mis vastab paigaldaja küsimustele ette, et paigaldus toimuks ilma inimeseta. AlmaLinux: kickstart (`inst.ks=URL`), Debian: preseed (`url=URL` koos `auto=true priority=critical`), Ubuntu: autoinstall (`autoinstall ds=nocloud;s=URL`). Fail jagatakse tavaliselt HTTP kaudu ja aadress antakse kerneli parameetrina (nt iPXE skriptis).
17. Fail on loetav kõigile, kes pääsevad veebiserverisse (ja jääb sageli paigaldatud masinasse alles). Vastustefail paigaldab vajalikud paketid ja SSH-võtme; liitmise teeb pärast käivitust Ansible, mille parool on Vaultis (või kasutatakse ühekordset liitumisparooli).

### Miniülesannete lahendused

```json
{
  "id": 2,
  "subnet": "10.0.84.0/24",
  "pools": [ { "pool": "10.0.84.100 - 10.0.84.150" } ],
  "option-data": [ { "name": "routers", "data": "10.0.84.1" } ]
}
```

(lisa massiivi `subnet4`)

```json
{ "name": "ntp-servers", "data": "10.0.83.1" }
```

(lisa globaalsesse massiivi `option-data`)

```text
host printer {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 10.0.83.20;
}
```

```text
/> backstores/block create db /dev/vg_san/lv_db
```

```bash
sudo iscsiadm -m session
sudo iscsiadm -m node --logoutall=all
```

<!-- navigatsioon -->
---

[← Laboritöö 19. DHCP, PXE ja iSCSI](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 20. Kataloogiteenused: OpenLDAP →](../moodul-20-openldap/index.md)
<!-- /navigatsioon -->
