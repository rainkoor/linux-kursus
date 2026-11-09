# Moodul 21. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Millised tehnoloogiad moodustavad Active Directory? Mis on igaühe roll?
2. Mis vahe on domeenil, domeenikontrolleril ja OU-l?
3. Kuidas töötab Kerberose autentimine? Mis on TGT?
4. Miks peab domeeni realm olema suurtähtedega?
5. Miks ei tohi AD domeeni nimi lõppeda `.local`-iga?
6. Miks paigaldatakse DC eraldi masinasse?
7. Milliseid teenuseid tuleb Debianis enne provisioning'ut peatada ja miks?
8. Mida teeb `samba-tool domain provision` valik `--use-rfc2307`?
9. Miks vajab DC `chrony` seadistuses `ntpsigndsocket` rida?
10. Kuidas leiab klient domeenikontrolleri?
11. Mida teeb `realm join`?
12. Mis vahe on SSSD seadetel `ldap_id_mapping = True` ja `False`?
13. Kuidas piirata, millised AD grupid saavad Linuxi masinasse sisse logida?
14. Miks pole AlmaLinuxis Samba AD DC-d ja mis on RHEL-i alternatiiv?
15. Too kolm levinumat põhjust, miks domeeniga liitumine ebaõnnestub.

## Praktilised miniülesanded

1. Loo kasutaja `peeter` ja lisa ta gruppi `opilased`.
2. Lisa DNS-kirje `nas.ad.lab.example → 10.0.83.53`.
3. Kirjuta käsk, mis näitab, kas DNS-is on Kerberose SRV-kirje.
4. Liida AlmaLinuxi masin domeeniga nii, et arvutikonto tekib OU-sse `Linux`.
5. Kirjuta sudoers-rida, mis annab AD grupile `Domain Admins` täisõigused (täisnimedega kasutajad).

---

## Vastused

1. LDAP - kataloog; Kerberos - autentimine; DNS - DC-de leidmine; SMB - failid, SYSVOL, sisselogimisskriptid; GPO - arvutite ja kasutajate seadistuste haldus.
2. Domeen - ühise kataloogi ja poliitikaga haldusala; DC - server, mis hoiab kataloogi ja autendib; OU - kaust objektide rühmitamiseks ja GPO-de sidumiseks.
3. Klient saab sisselogimisel KDC-lt TGT; TGT-ga küsib ta teenusepileteid, mida teenused kontrollivad. Parool ei liigu võrgus. TGT on „sissepääsupilet“, mis kehtib piiratud aja.
4. Kerberose realm on tõstutundlik ja AD tava on suurtähed; väiketähtedega realm ei klapi DC-ga.
5. `.local` on reserveeritud mDNS-ile (Avahi, Bonjour) ja põhjustab nimelahenduse konflikte.
6. DC on ise DNS-server (port 53) ja Kerberose KDC ning peab olema stabiilne; muud DNS/DHCP-teenused samas masinas lähevad konflikti ja turvarisk suureneb.
7. `smbd`, `nmbd` ja `winbind` - DC teenus `samba-ad-dc` käivitab vajalikud protsessid ise ja need pordid oleksid muidu hõivatud.
8. Lisab skeemi Unixi atribuudid (`uidNumber`, `gidNumber`, `loginShell`, `unixHomeDirectory`).
9. Windowsi kliendid nõuavad DC-lt allkirjastatud NTP vastuseid; allkirja annab Samba sokli kaudu.
10. DNS-i SRV-kirjete kaudu (`_ldap._tcp.<domeen>`, `_kerberos._udp.<domeen>`).
11. Avastab domeeni, loob AD-s arvutikonto, kirjutab `/etc/krb5.keytab`-i, seadistab SSSD, Kerberose ja PAM/NSS-i.
12. `True` - UID/GID arvutatakse SID-ist automaatselt; `False` - kasutatakse AD-s salvestatud RFC2307 atribuute.
13. `realm deny --all` ja `realm permit -g <grupp>` (või `simple_allow_groups` / `ad_access_filter` SSSD-s).
14. RHEL-i Samba on ehitatud MIT Kerberosega ja DC rolli ei toetata; alternatiiv on FreeIPA / Red Hat IdM.
15. Kliendi DNS ei osuta DC-le; kellad erinevad; tulemüür blokeerib pordid; vale administraatori parool; hostinimi pole FQDN.

### Miniülesannete lahendused

```bash
sudo samba-tool user create peeter
sudo samba-tool group addmembers opilased peeter
```

```bash
sudo samba-tool dns add dc1 ad.lab.example nas A 10.0.83.53 -U administrator
```

```bash
host -t SRV _kerberos._udp.ad.lab.example
```

```bash
sudo realm join -U Administrator --computer-ou="OU=Linux,DC=ad,DC=lab,DC=example" ad.lab.example
```

```text
%domain\ admins@ad.lab.example ALL=(ALL:ALL) ALL
```
