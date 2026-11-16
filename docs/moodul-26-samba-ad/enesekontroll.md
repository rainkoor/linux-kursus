<!-- navigatsioon -->
[← Laboritöö 26. Samba AD domeen](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 27. Linux töölaual ja WSL →](../moodul-27-toolaud-wsl/index.md)
<!-- /navigatsioon -->

# Moodul 26. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Millised tehnoloogiad moodustavad Active Directory? Mis on igaühe roll?

<details>
<summary>Vastus</summary>

LDAP - kataloog; Kerberos - autentimine; DNS - DC-de leidmine; SMB - failid, SYSVOL, sisselogimisskriptid; GPO - arvutite ja kasutajate seadistuste haldus.

</details>

**2.** Mis vahe on domeenil, domeenikontrolleril ja OU-l?

<details>
<summary>Vastus</summary>

Domeen - ühise kataloogi ja poliitikaga haldusala; DC - server, mis hoiab kataloogi ja autendib; OU - kaust objektide rühmitamiseks ja GPO-de sidumiseks.

</details>

**3.** Kuidas töötab Kerberose autentimine? Mis on TGT?

<details>
<summary>Vastus</summary>

Klient saab sisselogimisel KDC-lt TGT; TGT-ga küsib ta teenusepileteid, mida teenused kontrollivad. Parool ei liigu võrgus. TGT on „sissepääsupilet“, mis kehtib piiratud aja.

</details>

**4.** Miks peab domeeni realm olema suurtähtedega?

<details>
<summary>Vastus</summary>

Kerberose realm on tõstutundlik ja AD tava on suurtähed; väiketähtedega realm ei klapi DC-ga.

</details>

**5.** Miks ei tohi AD domeeni nimi lõppeda `.local`-iga?

<details>
<summary>Vastus</summary>

`.local` on reserveeritud mDNS-ile (Avahi, Bonjour) ja põhjustab nimelahenduse konflikte.

</details>

**6.** Miks paigaldatakse DC eraldi masinasse?

<details>
<summary>Vastus</summary>

DC on ise DNS-server (port 53) ja Kerberose KDC ning peab olema stabiilne; muud DNS/DHCP-teenused samas masinas lähevad konflikti ja turvarisk suureneb.

</details>

**7.** Milliseid teenuseid tuleb Debianis enne provisioning'ut peatada ja miks?

<details>
<summary>Vastus</summary>

`smbd`, `nmbd` ja `winbind` - DC teenus `samba-ad-dc` käivitab vajalikud protsessid ise ja need pordid oleksid muidu hõivatud.

</details>

**8.** Mida teeb `samba-tool domain provision` valik `--use-rfc2307`?

<details>
<summary>Vastus</summary>

Lisab skeemi Unixi atribuudid (`uidNumber`, `gidNumber`, `loginShell`, `unixHomeDirectory`).

</details>

**9.** Miks vajab DC `chrony` seadistuses `ntpsigndsocket` rida?

<details>
<summary>Vastus</summary>

Windowsi kliendid nõuavad DC-lt allkirjastatud NTP vastuseid; allkirja annab Samba sokli kaudu.

</details>

**10.** Kuidas leiab klient domeenikontrolleri?

<details>
<summary>Vastus</summary>

DNS-i SRV-kirjete kaudu (`_ldap._tcp.<domeen>`, `_kerberos._udp.<domeen>`).

</details>

**11.** Mida teeb `realm join`?

<details>
<summary>Vastus</summary>

Avastab domeeni, loob AD-s arvutikonto, kirjutab `/etc/krb5.keytab`-i, seadistab SSSD, Kerberose ja PAM/NSS-i.

</details>

**12.** Mis vahe on SSSD seadetel `ldap_id_mapping = True` ja `False`?

<details>
<summary>Vastus</summary>

`True` - UID/GID arvutatakse SID-ist automaatselt; `False` - kasutatakse AD-s salvestatud RFC2307 atribuute.

</details>

**13.** Kuidas piirata, millised AD grupid saavad Linuxi masinasse sisse logida?

<details>
<summary>Vastus</summary>

`realm deny --all` ja `realm permit -g <grupp>` (või `simple_allow_groups` / `ad_access_filter` SSSD-s).

</details>

**14.** Miks pole AlmaLinuxis Samba AD DC-d ja mis on RHEL-i alternatiiv?

<details>
<summary>Vastus</summary>

RHEL-i Samba on ehitatud MIT Kerberosega ja DC rolli ei toetata; alternatiiv on FreeIPA / Red Hat IdM.

</details>

**15.** Too kolm levinumat põhjust, miks domeeniga liitumine ebaõnnestub.

<details>
<summary>Vastus</summary>

Kliendi DNS ei osuta DC-le; kellad erinevad; tulemüür blokeerib pordid; vale administraatori parool; hostinimi pole FQDN.

</details>

## Praktilised miniülesanded

**1.** Loo kasutaja `peeter` ja lisa ta gruppi `opilased`.

<details>
<summary>Lahendus</summary>

```bash
sudo samba-tool user create peeter
sudo samba-tool group addmembers opilased peeter
```

</details>

**2.** Lisa DNS-kirje `nas.ad.lab.example → 10.0.83.153`.

<details>
<summary>Lahendus</summary>

```bash
sudo samba-tool dns add dc1 ad.lab.example nas A 10.0.83.153 -U administrator
```

</details>

**3.** Kirjuta käsk, mis näitab, kas DNS-is on Kerberose SRV-kirje.

<details>
<summary>Lahendus</summary>

```bash
host -t SRV _kerberos._udp.ad.lab.example
```

</details>

**4.** Liida AlmaLinuxi masin domeeniga nii, et arvutikonto tekib OU-sse `Linux`.

<details>
<summary>Lahendus</summary>

```bash
sudo realm join -U Administrator --computer-ou="OU=Linux,DC=ad,DC=lab,DC=example" ad.lab.example
```

</details>

**5.** Kirjuta sudoers-rida, mis annab AD grupile `Domain Admins` täisõigused (täisnimedega kasutajad).

<details>
<summary>Lahendus</summary>

```text
%domain\ admins@ad.lab.example ALL=(ALL:ALL) ALL
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 26. Samba AD domeen](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 27. Linux töölaual ja WSL →](../moodul-27-toolaud-wsl/index.md)
<!-- /navigatsioon -->
