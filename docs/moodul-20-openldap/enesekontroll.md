# Moodul 20. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Milliseid probleeme lahendab tsentraalne kasutajate kataloog võrreldes kohalike kontodega?
2. Mis on DIT, DN ja RDN? Too näide.
3. Mis on objektiklass? Mis vahe on kohustuslikul ja valikulisel atribuudil?
4. Milliseid objektiklasse vajab Linuxi kasutaja LDAP-is ja milleks igaüht?
5. Millised on LDAP-i pordid ja mis vahe on StartTLS-il ja LDAPS-il?
6. Mis on `cn=config` ja miks ei muudeta OpenLDAP-i seadistust tekstifailis?
7. Mida tähendab `ldapmodify -Y EXTERNAL -H ldapi:///`?
8. Mida teeb filter `(&(objectClass=posixAccount)(!(loginShell=/usr/sbin/nologin)))`?
9. Miks ei tohi kasutajate parooli räsi olla anonüümselt loetav?
10. Mis on SSSD roll Linuxi kliendis? Kuidas see seostub NSS-i ja PAM-iga?
11. Mida teeb `cache_credentials = true` ja milline on selle eelis ning risk?
12. Miks peavad UID- ja GID-numbrid olema kõigis masinates samad?
13. Kuidas luuakse LDAP-i kasutajale kodukataloog esimesel sisselogimisel (Ubuntu ja AlmaLinux)?
14. Miks pole AlmaLinuxis OpenLDAP-serverit ja mis on selle alternatiivid RHEL-i maailmas?
15. Kuidas varundad ja taastad OpenLDAP-i?

## Praktilised miniülesanded

1. Kirjuta LDIF, mis lisab kasutajale `uid=jaan,ou=People,dc=lab,dc=example` atribuudi `mail` väärtusega `jaan@lab.example`.
2. Kirjuta `ldapsearch` käsk, mis leiab kõik grupid, mille liige on `mari`, ja kuvab ainult nende nime.
3. Kirjuta LDIF, mis lisab grupi `opetajad` (GID 10100) ilma liikmeteta.
4. Kirjuta käsk, millega kontrollid kliendis, kas SSSD näeb kasutajat `kati` ja tema gruppe.
5. Kirjuta käsk, mis kustutab kasutaja `uid=test,ou=People,dc=lab,dc=example`.

---

## Vastused

1. Üks konto ja parool kõigis masinates, kasutaja loomine ja kustutamine ühes kohas, ühtsed UID/GID-numbrid (NFS), lihtsam paroolipoliitika ja auditeerimine.
2. DIT - kataloogipuu; DN - kirje täisnimi puus (nt `uid=mari,ou=People,dc=lab,dc=example`); RDN - DN-i vasakpoolseim osa (`uid=mari`).
3. Objektiklass määrab, milliseid atribuute kirje peab (MUST) ja võib (MAY) sisaldada. Kohustuslikuta kirjet ei saa lisada.
4. `inetOrgPerson` - nimi, e-post jm isikuandmed; `posixAccount` - UID, GID, kodukataloog, kest; `shadowAccount` - parooli aegumise andmed.
5. 389 - LDAP (StartTLS-iga krüpteeritakse ühendus pärast ühendumist samas pordis); 636 - LDAPS (TLS kohe ühendumisel).
6. Dünaamiline seadistus, mis on ise LDAP-puu; muudatused jõustuvad kohe, ilma teenust taaskäivitamata.
7. Ühendus kohaliku Unixi sokli kaudu, autentimine operatsioonisüsteemi kasutaja järgi (root → kataloogi haldaja `cn=config` jaoks).
8. Leiab kõik kasutajad, kelle kest ei ole `/usr/sbin/nologin`.
9. Räsi saab võrguühenduseta (offline) murda; nõrgad paroolid leitakse kiiresti.
10. SSSD on vahelüli: NSS küsib temalt kasutaja ja grupi infot (`getent`, `id`), PAM autentimist; SSSD suhtleb LDAP-iga ja hoiab vahemälu.
11. Kasutaja saab sisse logida ka siis, kui server pole kättesaadav. Risk: kataloogis keelatud või muudetud parool võib vahemälus veel mõnda aega kehtida.
12. Failide omanik salvestatakse numbrina; erinevad numbrid tähendaksid, et NFS-is või kettal kuuluvad failid valele kasutajale.
13. Ubuntu: `pam-auth-update --enable mkhomedir`; AlmaLinux: `authselect select sssd with-mkhomedir --force` ja teenus `oddjobd`.
14. Red Hat lõpetas OpenLDAP-serveri tarnimise; alternatiivid on 389 Directory Server ja FreeIPA / Red Hat IdM. Kliendid ja `openldap-clients` on olemas.
15. `slapcat -n 0` (seadistus) ja `slapcat -n 1` (andmed); taastamisel peata `slapd`, tühjenda andmekataloog ja kasuta `slapadd`, siis paranda omanik (`openldap`).

### Miniülesannete lahendused

```text
dn: uid=jaan,ou=People,dc=lab,dc=example
changetype: modify
add: mail
mail: jaan@lab.example
```

```bash
ldapsearch -x -LLL -b ou=Groups,dc=lab,dc=example "(memberUid=mari)" cn
```

```text
dn: cn=opetajad,ou=Groups,dc=lab,dc=example
objectClass: posixGroup
cn: opetajad
gidNumber: 10100
```

```bash
id kati
getent passwd kati
```

```bash
ldapdelete -x -D cn=admin,dc=lab,dc=example -W "uid=test,ou=People,dc=lab,dc=example"
```
