<!-- navigatsioon -->
[← Laboritöö 23. PXE ja iSCSI](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. E-posti server →](../moodul-24-e-post/index.md)
<!-- /navigatsioon -->

# Moodul 23. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Milliseid DHCP-valikuid vajab PXE?

<details>
<summary>Vastus</summary>

Valik 66 / `next-server` (TFTP-serveri aadress) ja valik 67 / `boot-file-name` (alglaadimisfail).

</details>

**2.** Mis on TFTP ja iPXE roll PXE alglaadimisel?

<details>
<summary>Vastus</summary>

TFTP on lihtne protokoll, millega PXE-püsivara laadib alglaadimisfaili. iPXE on täiustatud alglaadimisprogramm, mis oskab HTTP-d, skripte ja menüüsid ning laadib edasi kerneli või paigaldaja.

</details>

**3.** Miks vajavad BIOS- ja UEFI-kliendid eri alglaadimisfaile?

<details>
<summary>Vastus</summary>

BIOS ja UEFI käivitavad eri vormingus programme: BIOS-il on PXE-ROM-i jaoks `.kpxe`/`.pxe`, UEFI-l EFI-rakendus `.efi`.

</details>

**4.** Mida teeb FOG ja kuidas see klassiruumis kasulik on?

<details>
<summary>Vastus</summary>

FOG salvestab etalonarvuti kettatõmmise ja paigaldab selle PXE kaudu teistele arvutitele (ka grupile korraga). Klassiruumis saab kõik arvutid kiiresti ühesuguseks või algolekusse taastada.

</details>

**5.** Mis vahe on iSCSI-l ja NFS-il?

<details>
<summary>Vastus</summary>

NFS jagab faile (failitasemel, mitu klienti korraga); iSCSI jagab plokkseadmeid - klient näeb seda nagu oma ketast ja haldab failisüsteemi ise.

</details>

**6.** Selgita mõisteid sihtmärk, initsiaator, LUN ja IQN.

<details>
<summary>Vastus</summary>

Sihtmärk - server, mis jagab kettaid; initsiaator - klient; LUN - üks jagatav ketas; IQN - unikaalne nimi kujul `iqn.AAAA-KK.pööratud.domeen:nimi`.

</details>

**7.** Kuidas tagab iSCSI sihtmärk, et ainult õige klient saab LUN-i kasutada?

<details>
<summary>Vastus</summary>

ACL-iga (lubatud initsiaatorite IQN-id) ja soovi korral CHAP-autentimisega.

</details>

**8.** Miks ei tohi ühte LUN-i korraga kasutada kaks initsiaatorit?

<details>
<summary>Vastus</summary>

Tavaline failisüsteem eeldab, et ainult üks süsteem kirjutab - kaks samaaegset kirjutajat rikuvad failisüsteemi ja andmed hävivad.

</details>

**9.** Miks kasutatakse iSCSI ketta haakimisel fstab-is valikut `_netdev`?

<details>
<summary>Vastus</summary>

Et haakimist proovitaks alles pärast võrgu ja iSCSI seansi tekkimist; muidu ebaõnnestub haakimine alglaadimisel.

</details>

**10.** Mis on vastustefail? Nimeta AlmaLinuxi, Debiani ja Ubuntu vastustefaili vormingud ning kuidas paigaldaja faili leiab.

<details>
<summary>Vastus</summary>

Fail, mis vastab paigaldaja küsimustele ette, et paigaldus toimuks ilma inimeseta. AlmaLinux: kickstart (`inst.ks=URL`), Debian: preseed (`url=URL` koos `auto=true priority=critical`), Ubuntu: autoinstall (`autoinstall ds=nocloud;s=URL`). Fail jagatakse tavaliselt HTTP kaudu ja aadress antakse kerneli parameetrina (nt iPXE skriptis).

</details>

**11.** Miks ei panda domeeni administraatori parooli kickstarti faili ja kuidas masin siis domeeniga liidetakse?

<details>
<summary>Vastus</summary>

Fail on loetav kõigile, kes pääsevad veebiserverisse (ja jääb sageli paigaldatud masinasse alles). Vastustefail paigaldab vajalikud paketid ja SSH-võtme; liitmise teeb pärast käivitust Ansible, mille parool on Vaultis (või kasutatakse ühekordset liitumisparooli).

</details>

## Praktilised miniülesanded

**1.** Loo `targetcli`-s LVM-köitel `/dev/vg_san/lv_db` põhinev taust nimega `db`.

<details>
<summary>Lahendus</summary>

```text
/> backstores/block create db /dev/vg_san/lv_db
```

</details>

**2.** Kuva AlmaLinuxis kõik aktiivsed iSCSI seansid ja logi kõigist välja.

<details>
<summary>Lahendus</summary>

```bash
sudo iscsiadm -m session
sudo iscsiadm -m node --logoutall=all
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 23. PXE ja iSCSI](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. E-posti server →](../moodul-24-e-post/index.md)
<!-- /navigatsioon -->
