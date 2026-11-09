# Moodul 11. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mida tähendab kihiline kaitse? Too näide kolmest kihist.
2. Miks on automaatsed turvauuendused olulised? Millise tööriistaga need Ubuntus ja AlmaLinuxis seadistatakse?
3. Mis on CVE?
4. Kuidas töötab fail2ban? Miks kirjutatakse seadistus faili `jail.local`, mitte `jail.conf`?
5. Kus on autentimislogid Ubuntus ja AlmaLinuxis? Kuidas neid Debianis lugeda?
6. Mida teeb logrotate? Selgita valikuid `rotate 7`, `compress` ja `delaycompress`.
7. Miks on kasulik saata logid teise serverisse?
8. Mis vahe on valikulisel (DAC) ja kohustuslikul (MAC) juurdepääsukontrollil?
9. Mis vahe on SELinuxi režiimidel enforcing, permissive ja disabled?
10. Fail on SELinuxiga süsteemis teisaldatud kodukataloogist veebikataloogi ja veebiserver annab vea `403`. Miks? Kuidas parandada?
11. Kuidas lubada veebiserveril kasutada mittestandardset kataloogi püsivalt?
12. Kuidas leida, mida SELinux keelas?
13. Mille poolest erineb AppArmor SELinuxist?
14. Mis vahe on AppArmori enforce- ja complain-režiimil?
15. Mida teeb käsk `auditctl -w /etc/shadow -p wa -k shadow`? Kuidas sündmusi hiljem leida?
16. Mis on SIEM ja mille poolest erineb see igas serveris eraldi töötavast fail2ban-ist ja `auditd`-st?
17. Kas fail2ban on vajalik, kui SSH lubab ainult võtmeid? Millal on see endiselt kasulik ja millised on alternatiivid?
18. Mis on Wazuhi automaatne reageerimine (*active response*) ja millist ohtu see endaga kaasa toob?

## Praktilised miniülesanded

1. (Ubuntu) Leia viimase 24 tunni jooksul kõik ebaõnnestunud SSH-sisselogimised ja loenda IP-aadresside kaupa.
2. (AlmaLinux) Leia, millised SELinuxi tõeväärtused on seotud Samba (`samba`) teenusega.
3. (AlmaLinux) Luba SSH-serveril SELinuxi poolt kuulata porti 2222.
4. (Kõik) Loo logrotate'i reegel failile `/var/log/varundus.log`: iganädalane rotatsioon, alles 8 koopiat, pakkimine.
5. (Kõik) Lisa püsiv auditireegel, mis jälgib kataloogi `/etc/ssh/` muutmist võtmega `ssh-seadistus`.
6. (Ubuntu) Leia, millises režiimis on profiil `tcpdump` jaoks.

---

## Vastused

1. Mitu teineteist täiendavat kaitsekihti, nii et ühe läbimurdmisel peavad teised ründaja peatama. Näiteks tulemüür, SSH võtmepõhine autentimine ja SELinux, mis piirab ülevõetud teenust.
2. Enamik rünnakuid kasutab ära teadaolevaid turvaauke, millele on parandus olemas. Ubuntus `unattended-upgrades`, AlmaLinuxis `dnf-automatic`.
3. *Common Vulnerabilities and Exposures* - turvaaukude rahvusvaheline tunnus (nt `CVE-2024-3094`).
4. fail2ban jälgib logisid ja blokeerib tulemüüris IP-aadressid, millelt tuleb määratud aja jooksul liiga palju ebaõnnestunud katseid. `jail.conf` kirjutatakse paketi uuendamisel üle, `jail.local` jääb alles.
5. Ubuntus `/var/log/auth.log`, AlmaLinuxis `/var/log/secure`. Debianis journal'ist, nt `journalctl _COMM=sshd` või `journalctl -u ssh`.
6. Nimetab logifailid regulaarselt ümber, pakib vanad ja kustutab kõige vanemad. `rotate 7` - hoia alles 7 vana faili; `compress` - paki vanad failid; `delaycompress` - paki eelmine fail alles järgmisel rotatsioonil (nii saab programm, mis seda veel kirjutab, töö lõpetada).
7. Ründaja, kes saab serveris juurkasutaja õigused, võib kohalikud logid kustutada või muuta. Kaugserveris olevad logid jäävad alles. Lisaks on mitme serveri logisid ühes kohas lihtsam analüüsida.
8. DAC-is otsustab faili omanik, kes faili kasutada tohib, ja juurkasutajale piirangud ei kehti. MAC-is kehtib süsteemne poliitika, millest ei saa mööda ka juurkasutaja õigustes töötav programm.
9. Enforcing - poliitika kehtib ja keelud blokeeritakse; permissive - keelud ainult logitakse; disabled - SELinux on välja lülitatud.
10. `mv` säilitas faili SELinuxi konteksti (`user_home_t`), mida veebiserver (`httpd_t`) ei tohi lugeda. Parandus: `restorecon -v fail`.
11. `semanage fcontext -a -t httpd_sys_content_t "/kataloog(/.*)?"` ja seejärel `restorecon -Rv /kataloog`.
12. `ausearch -m AVC -ts recent` (selgitusega `| audit2why`) või `journalctl -t setroubleshoot`.
13. SELinux kasutab märgiseid, mis on kõigil failidel, protsessidel ja portidel, ning hõlmab kogu süsteemi. AppArmor kasutab failiteede põhiseid profiile ja piirab ainult neid programme, millel on profiil. AppArmor on lihtsam, SELinux võimsam.
14. Enforce-režiimis keelatud tegevused blokeeritakse ja logitakse, complain-režiimis ainult logitakse.
15. Jälgib faili `/etc/shadow` kirjutamist (`w`) ja atribuutide muutmist (`a`) ning märgib sündmused võtmega `shadow`. Sündmused leiab käsuga `ausearch -k shadow -i`.
16. SIEM (nt Wazuh) kogub kõigi masinate logid ja sündmused ühte kohta, analüüsib neid reeglitega, seostab sündmusi eri masinatest ja annab häireid. Logid on alles ka siis, kui ründaja kohalikud logid kustutab; lisaks haavatavuste ja seadistuse kontroll.
17. SSH jaoks pole see hädavajalik (parooliga sisse ei saa), kuid vähendab logide müra. Peamine kasu on paroolipõhiste teenuste (veebirakenduse sisselogimine, e-post) kaitsmisel. Alternatiivid: SSH piiramine tulemüüris, OpenSSH 9.8+ `PerSourcePenalties`, CrowdSec, Wazuhi automaatne reageerimine.
18. Server käivitab reegli peale agendis käsu, nt `firewall-drop` blokeerib ründaja IP mõneks ajaks. Oht: valepositiivne sündmus võib blokeerida administraatori või partneri - haldusvõrk tuleb lisada erandiks ja reaktsiooni enne testida.

### Miniülesannete lahendused

```bash
# 1
journalctl -u ssh --since "24 hours ago" | grep -E "Failed|Invalid user" \
    | grep -oE "from [0-9.]+" | sort | uniq -c | sort -rn
# 2
getsebool -a | grep samba
# 3
sudo semanage port -a -t ssh_port_t -p tcp 2222
```

```text
# 4: /etc/logrotate.d/varundus
/var/log/varundus.log {
    weekly
    rotate 8
    compress
    missingok
    notifempty
}
```

```bash
# 5
echo "-w /etc/ssh/ -p wa -k ssh-seadistus" | sudo tee /etc/audit/rules.d/91-ssh.rules
sudo augenrules --load
# 6
sudo aa-status | grep -A1 -i tcpdump
```

<!-- navigatsioon -->
---

[← Laboritöö 11. Turvalisus ja logid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 12. Konteinerid →](../moodul-12-konteinerid/index.md)
<!-- /navigatsioon -->
