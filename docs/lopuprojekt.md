<!-- navigatsioon -->
[← Proovieksam: süvendusosa](proovieksam.md) · [Sisukord](../README.md#sisukord) · [Moodul 21. BSD praktikas: OPNsense tulemüür →](moodul-21-opnsense/index.md)
<!-- /navigatsioon -->

# Lõpuprojekt

Lõpuprojektis ehitad iseseisvalt tervikliku Linuxi-lahenduse, kasutades kursusel õpitut. Projekti eesmärk on näidata, et oskad lahendust **planeerida, ehitada, turvata, varundada, automatiseerida ja dokumenteerida** - nii, nagu seda tehakse päris töös.

Projektil on **kolm taset**. Vali tase vastavalt sellele, kui kaugele oled kursusel jõudnud ja millist väljakutset soovid. Õpetaja võib taseme ette anda (nt algtase pärast põhiosa, edasijõudnute tase kursuse lõpus).

| | **Algtase** | **Edasijõudnud** | **Meister** |
|---|---|---|---|
| Eeldused | põhiosa (moodulid 1–9) | moodulid 1–20 | moodulid 1–20 ja vähemalt kaks valikmoodulit |
| Maht | 12 tundi | 16 tundi | 24–32 tundi |
| Masinaid | 1 (+ klient) | 2–4 | 4 või rohkem, sh võrguseade või hüperviisor |
| Distrod | üks | vähemalt kaks perekonda (Debian ja Red Hat) | segakeskkond (Linux, Windows, BSD/OPNsense) |
| Automatiseerimine | Bashi skriptid | Ansible või konteinerid (Compose/Quadlet) | kogu lahendus koodina: Ansible + konteinerid, ehitatav nullist |
| Töökindlus | varukoopia ja taastamine | varundus teise masinasse, seire | kõrge kättesaadavus, rikketest, taastamisplaan |
| Esitlus | 7 min | 10 min | 15 min + kaitsmine |
| Vastab ligikaudu | töökoha praktikandi ülesandele | nooremadministraatori ülesandele | administraatori või DevOps-inseneri projektile |

## Töö käik (kõik tasemed)

| Etapp | Tulemus | Algtase | Edasijõudnud | Meister |
|---|---|---|---|---|
| 1. Teema valik ja plaan | projektiplaan, õpetaja kinnitus | 1 h | 2 h | 3 h |
| 2. Ehitamine | töötav lahendus | 6 h | 8 h | 12–16 h |
| 3. Turvamine ja varundus | karastatud süsteem, testitud taastamine | 2 h | 2 h | 4–6 h |
| 4. Dokumenteerimine | Git-hoidla koos dokumentatsiooniga | 2 h | 2 h | 3–4 h |
| 5. Esitlus | esitlus ja demo | 1 h | 2 h | 2–3 h |

**Projektiplaan** (1 lk): eesmärk, masinad ja nende rollid, IP-plaan (vt [paigalduslisa](lisad/paigaldus.md), punkt 2), teenused, ajakava, riskid („mis võib valesti minna“).

---

## 1. Algtase

**Eeldused:** moodulid 1–9 · **Maht:** 12 tundi · **Distro:** Debian, Ubuntu või AlmaLinux

Algtasemel ehitad ühe serveri, mis on korralikult seadistatud, turvatud, varundatud ja dokumenteeritud. Kõik tehakse käsitsi või Bashi skriptidega. Enne projekti tasub teha [põhiosa proovieksam](proovieksam-pohiosa.md) - see näitab, milliseid teemasid veel korrata.

### Teemad

**A1. Õppegrupi tööserver**

- **Põhinõuded:** kasutajad ja grupid luuakse CSV-failist skriptiga (moodul 6); igal grupil jagatud kataloog õigete õigustega (SGID, `umask`, vajadusel ACL, moodul 3); paroolipoliitika (`pam_pwquality`); SSH ainult võtmetega; tulemüür; eraldi LVM-köide `/srv` jaoks (moodul 8); igaöine varundusskript systemd taimeriga ja testitud taastamine; sisselogimise teade (`/etc/motd`).
- **Lisanõuded:** kettakasutuse ja sisselogimiste aruanne skriptiga (e-postiga või faili); LUKS-iga krüpteeritud varundusketas; ressursipiirangud gruppidele (`limits.conf`).

**A2. Halduskriptide komplekt**

- **Põhinõuded:** vähemalt 4 skripti (nt kasutajate loomine CSV-st, varundus rotatsiooniga, kettakasutuse ja teenuste kontroll, logide analüüs); kõigis `set -euo pipefail`, argumentide kontroll ja `--help`; ShellCheck ilma hoiatusteta; vähemalt kaks skripti ajastatud systemd taimeriga; kõik Gitis.
- **Lisanõuded:** skriptid töötavad nii Debianis kui ka AlmaLinuxis; teavitus probleemi korral; man-leht või põhjalik README.

**A3. Mänguserver või muu teenus systemd teenusena**

Paigalda mõni server-tarkvara, mis ei ole distro hoidlas (nt Minecrafti server, Luanti/Minetest, Terraria, Jitsi testserver - kooskõlasta õpetajaga).

- **Põhinõuded:** teenus töötab eraldi õigusteta kasutajana; oma systemd üksus (käivitub alglaadimisel, taaskäivitub vea korral, logid `journalctl`-is); andmed eraldi LVM-köites; tulemüüris ainult vajalikud pordid; varundus enne uuendust ja igaöine; uuendamise juhend.
- **Lisanõuded:** ressursipiirangud teenusele (`MemoryMax=`, `CPUQuota=`); skript, mis teatab, kui teenus ei vasta; hooldusaken (`at` või taimer, mis teavitab kasutajaid enne taaskäivitust).

### Kohustuslik algtasemel

1. **Turvalisus:** SSH võtmetega ja juurkasutaja sisselogimine keelatud, tulemüür, süsteem uuendatud.
2. **Varundus:** automaatne varundus ja **dokumenteeritud taastamistest**.
3. **Git:** skriptid ja seadistusfailid Git-hoidlas (moodul 6), saladused ei ole hoidlas.
4. **Dokumentatsioon:** `README.md` (eesmärk, masina info, paigaldus- ja seadistussammud, varundus ja taastamine).

---

## 2. Edasijõudnud

**Eeldused:** moodulid 1–20 · **Maht:** 16 tundi · **Distrod:** vähemalt kaks perekonda (Debian/Ubuntu ja AlmaLinux)

Edasijõudnute tasemel ehitad mitmest masinast koosneva teenuse, mis on automatiseeritud, turvatud, varundatud ja seiratud.

### Teemad

**E1. Veebirakenduse platvorm**

Paigalda avatud lähtekoodiga veebirakendus (nt WordPress, Nextcloud, Moodle, Gitea, BookStack) tootmiskõlbulikult.

- **Põhinõuded:** veebiserver + rakendus + andmebaas eraldi masinates (moodulid 15–16); HTTPS oma CA või Caddy `tls internal`-iga (Let's Encrypt ainult siis, kui serveril on avalik DNS-nimi, moodul 15); eraldi andmebaasikasutaja ja andmebaas kättesaadav ainult veebiserverile; DNS-nimi (moodul 17); tulemüür ja SELinux/AppArmor; igaöine varundus teise masinasse koos testitud taastamisega; kättesaadavuse seire (Uptime Kuma, moodul 20).
- **Lisanõuded:** rakendus konteinerites koos Quadletiga (moodul 14); Valkey vahemäluks; fail2ban rakenduse sisselogimisele; Prometheus + Grafana.

> [!NOTE]
> **Näide - WordPress:** `alma` (veebiserver): nginx + PHP-FPM (`php-mysqlnd`, `php-gd`, `php-xml`, `php-mbstring`, `php-intl`, `php-zip`), SELinux lubab veebiserveril andmebaasiga ühenduda (`setsebool -P httpd_can_network_connect_db on`) ja kirjutada üleslaadimiste kataloogi (`semanage fcontext … httpd_sys_rw_content_t`); `debian2` (andmebaas): MariaDB, kus kasutaja `'wordpress'@'10.0.83.55'` ja `bind-address` laborivõrgu aadressil, tulemüüris port 3306 lubatud ainult veebiserverile; `wp-config.php` õigused `640`; HTTPS oma CA sertifikaadiga; igaöine `mariadb-dump` + `wp-content` varundus resticuga; taastamistest uude VM-i. Lisanõudeks sobib WordPressi CLI (`wp-cli`) ja fail2ban WordPressi sisselogimislehele.

**E2. Ansible'iga hallatav serveripark**

Ehita vähemalt kolmest serverist koosnev keskkond, mis seadistatakse täielikult Ansible'iga (moodul 19).

- **Põhinõuded:** vähemalt kaks eri distrot; ühine baasseadistus (kasutajad, SSH karastamine, tulemüür, automaatsed uuendused, ajavöönd, NTP); vähemalt kaks teenust (nt veeb ja andmebaas või DNS); mänguraamat on idempotentne; kõik Gitis.
- **Lisanõuded:** rollid ja `group_vars` (moodul 19); Ansible Vault saladuste jaoks; node_exporter ja Prometheus Ansible'iga (moodul 20); mänguraamat ehitab tühjast masinast töötava serveri; testimine (`ansible-lint`, idempotentsuse test, Molecule, moodul 19).

**E3. Kooli labori infrastruktuuriteenused**

Ehita väikese labori põhiteenused (moodulid 9, 17, 18 ja 20).

- **Põhinõuded:** DNS-server (sisevõrgu tsoon + rekursioon, BIND9 või CoreDNS); failijagamine Linuxile (NFS + autofs) ja Windowsile (Samba); keskne logiserver (rsyslog), kuhu saadavad logisid vähemalt kaks masinat; e-posti teavitused (Postfix); varundus teise masinasse.
- **Lisanõuded:** teine DNS-server; Pi-hole; failiserver TrueNASil koos replikatsiooniga; seire ja häired (Prometheus/Grafana või Zabbix).

**E4. Konteineritel põhinev teenuseplatvorm**

- **Põhinõuded:** vähemalt kolm teenust konteinerites (nt rakendus, andmebaas, haldusliides) Compose'i või Quadletiga (moodul 14); pöördpuhver koos HTTPS-iga (Caddy või Traefik, moodul 15); püsivad andmed köidetes ja nende varundus; teenused käivituvad alglaadimisel; konteinerite logid ja seire (moodul 20); kõik konfiguratsioon Gitis.
- **Lisanõuded:** juurkasutajata (*rootless*) konteinerid; oma konteinerpilt; automaatsed pildiuuendused (`podman auto-update`, moodul 14) koos tagasivõtmisega; Ansible'i mänguraamat, mis ehitab platvormi nullist.

### Kohustuslik edasijõudnute tasemel

1. **Turvalisus:** SSH ainult võtmetega, juurkasutaja sisselogimine keelatud, tulemüür (ainult vajalikud pordid), automaatsed turvauuendused, SELinux/AppArmor sees, paroolipoliitika.
2. **Varundus:** varundusplaan (mida, kuhu, kui tihti), automaatne varundus **teise masinasse** ja **dokumenteeritud taastamistest**.
3. **Automatiseerimine:** vähemalt üks oluline osa on Ansible'i või konteineritega korratav.
4. **Seire:** vähemalt kättesaadavuse jälgimine ja üks häire.
5. **Git:** kõik skriptid, seadistusfailid ja dokumentatsioon Git-hoidlas, mõtestatud sissekannetega (mitte üks suur sissekanne lõpus). Saladused **ei ole** hoidlas.
6. **Dokumentatsioon:** vt allpool.

---

## 3. Meister

**Eeldused:** moodulid 1–20 ja vähemalt kaks valikmoodulit · **Maht:** 24–32 tundi · **Keskkond:** segakeskkond

Meistritasemel ehitad lahenduse, mis võiks töötada päris asutuses: see talub üksikute komponentide riket, on ehitatav nullist koodi järgi, seiratav ja dokumenteeritud nii, et keegi teine saab selle üle võtta. Kõik põhi- ja lisanõuetes nimetatud vahendid on kursusel käsitletud (sulgudes on moodul); meistritaseme raskus on nende **kombineerimises** üheks töökindlaks tervikuks.

### Teemad

**M1. Kõrge kättesaadavusega veebiteenus**

- **Põhinõuded:** vähemalt kaks veebiserverit koormusejaoturi taga (HAProxy või nginx, moodul 15); koormusejaoturi enda rikkekindlus (kaks jaoturit + `keepalived` virtuaalse IP-ga, moodul 15); andmebaasi replikatsioon ja dokumenteeritud ülevõtt (moodul 16); jagatud failisalvestus (NFS, moodul 18); seansid Valkeys (moodul 16); seire ja häired (moodul 20); kogu keskkond Ansible'iga nullist ehitatav; **rikketest**: lülita välja üks veebiserver, üks jaotur ja andmebaasi põhiserver - dokumenteeri, mis juhtus ja kui kaua teenus häiritud oli.
- **Lisanõuded:** käsitsi ülevõtu harjutus koos ajamõõtmisega (moodul 16), automaatne ülevõtt (Galera, MaxScale) kokkuleppel õpetajaga; rakendus konteinerites või k3s klastris (valikmoodul 28); koormustest (`ab`, `wrk`) ja jõudlusanalüüs (moodulid 15 ja 20).

**M2. Virtualiseerimisplatvorm koodina**

- **Põhinõuded:** vähemalt kahesõlmeline Proxmox VE klaster (pesastatult või füüsiliselt, moodul 27) või XCP-ng kogum; jagatud salvestus (NFS, iSCSI või Ceph) või ZFS-i replikatsioon; virtuaalmasinad luuakse koodina (cloud-init mall, moodul 27, + OpenTofu või Ansible'i `community.general.proxmox_kvm`, moodul 19) ja seadistatakse Ansible'iga; varundus Proxmox Backup Serverisse (moodul 27) koos taastamistestiga; kasutajad ja õigused (realm, rollid, kogumid); seire.
- **Lisanõuded:** kõrge kättesaadavus (HA) koos rikketestiga; SDN võrgud; API-põhine haldusskript (moodulid 6 ja 27) õppijate laborite loomiseks.

**M3. Kooli võrk ja kasutajahaldus**

Ühenda valikmoodulite teemad terviklikuks väikeasutuse taristuks (moodulid 21–25).

- **Põhinõuded:** OPNsense ruuter ja tulemüür (VLAN-id serveritele ja klientidele, WireGuard VPN kaugtööks); Samba AD domeen (kaks domeenikontrollerit) või OpenLDAP; DHCP ja DNS integreeritud domeeniga; PXE-paigaldus vastustefailiga (kickstart, preseed või autoinstall, moodul 22), mille järel Ansible liidab uue Linuxi masina domeeniga; failiserver gruppide õigustega; Windowsi ja Linuxi kliendid; GPO-d; tsentraalne logimine; varundus ja taastamisplaan.
- **Lisanõuded:** domeenikontrolleri rikketest; LDAPS/Kerberos kõigil ühendustel; kasutajate elutsükkel skriptiga (loomine CSV-st, lukustamine, kustutamine).

**M4. Turvaseire ja intsidendi lahendamine**

- **Põhinõuded:** isoleeritud laborivõrk (OPNsense); vähemalt kolm sihtserverit, mis on karastatud CIS-i soovituste järgi (Lynis, moodul 12); tsentraalne turvaseire (Wazuh) kõigis masinates; failide terviklikkuse kontroll ja haavatavuste skaneerimine; **intsidendi simulatsioon** Kaliga (moodul 26) isoleeritud võrgus (õpetaja loal): rünnaku avastamine Wazuhis, analüüs, tõkestamine ja intsidendi aruanne.
- **Lisanõuded:** automaatne reageerimine (Wazuh active response, moodul 12); logide säilitamine eraldi serveris, mida rünnatav masin muuta ei saa; turvapoliitika Ansible'iga.

**M5. Kubernetese platvorm**

Eeldab valikmoodulit 28.

- **Põhinõuded:** k3s klaster vähemalt kolmest sõlmest (moodul 28); vähemalt kaks rakendust (nt veebirakendus ja selle andmebaas või eraldi VM-is andmebaas, moodul 16) manifestide või Helmiga; Ingress koos TLS-iga (labori CA, moodul 15); püsiandmed PVC-ga ja nende varundus; ConfigMap'id ja Secret'id (saladused **ei ole** Gitis avatekstina); kõik manifestid ja Helmi `values.yaml` failid Gitis; **rikketest**: sõlme väljalülitamine ja järkjärguline uuendus koos tagasivõtuga; klastri oleku varundus ja taastamisjuhend.
- **Lisanõuded:** kõrge kättesaadavus (kolm serverit etcd-ga + virtuaalne IP, moodulid 15 ja 28); GitOps Argo CD-ga; seire `kube-prometheus-stack`-iga (moodul 20); sõlmed luuakse OpenTofu ja cloud-initiga (moodulid 19 ja 27).

**M6. Oma teema**

Näiteks: Linuxi töölaudadega arvutiklass (keskne kasutajahaldus, tarkvara Flatpaki/Ansible'iga, kaugtugi), e-posti server koos SPF/DKIM/DMARC-iga, oma kerneliga sardsüsteem. Teema peab olema vähemalt sama mahukas kui M1–M5 ja tuleb õpetajaga kooskõlastada. Kui teema vajab vahendeid, mida kursusel ei käsitletud, lepi õpetajaga kokku, kuidas need õpitakse ja kuidas neid hinnatakse.

### Kohustuslik meistritasemel

Kõik edasijõudnute taseme kohustuslikud osad, lisaks:

1. **Kõik koodina:** lahenduse saab tühjadest masinatest uuesti üles ehitada Git-hoidla ja dokumentatsiooni järgi; ehitust tuleb esitluse eel vähemalt korra tõestada (nt uude VM-i või Vagrantiga).
2. **Töökindlus:** vähemalt üks komponent on dubleeritud ja **rikketest** on dokumenteeritud.
3. **Taastamisplaan:** eesmärgid **RPO** (kui palju andmeid tohib kaotada) ja **RTO** (kui kiiresti peab teenus taastuma) ning testitud taastamine, mille tegelik aeg on mõõdetud.
4. **Seire ja häired:** mõõdikud, logid ja vähemalt kolm mõtestatud häiret; teavitus jõuab inimeseni.
5. **Turvalisus:** riskianalüüs (vähemalt 5 riski koos meetmetega); kõik ühendused krüpteeritud; saladuste haldus (Ansible Vault vms).

---

## Dokumentatsioon

| | Algtase | Edasijõudnud | Meister |
|---|---|---|---|
| `README.md`: eesmärk, kirjeldus, kasutatud distrod ja versioonid | ✔ | ✔ | ✔ |
| Paigaldus- ja seadistusjuhend (kuidas nullist üles ehitada) | ✔ | ✔ | ✔ |
| Varundus ja **taastamise juhend** | ✔ | ✔ | ✔ |
| Arhitektuuri joonis (masinad, IP-d, teenused, pordid, andmevood; ASCII või Mermaid) | lihtne | ✔ | ✔ |
| Turvameetmed | lühidalt | ✔ | riskianalüüs |
| Seire ja häired | - | ✔ | ✔ |
| **Käsiraamat** (*runbook*): tüüpilised haldustoimingud ja rikete lahendamine | - | - | ✔ |
| **Otsuste logi**: miks valisid just selle tarkvara või lahenduse (vähemalt 3 otsust) | - | - | ✔ |
| Rikketesti ja taastamistesti protokoll (aeg, tulemus) | - | taastamine | ✔ |
| Teadaolevad piirangud, edasiarenduse ideed, kasutatud allikad | ✔ | ✔ | ✔ |

Lisa kataloogi `dokumentatsioon/` tõendid: ekraanipildid, olulised käsuväljundid, testide tulemused.

## Esitlus

| | Algtase (7 min) | Edasijõudnud (10 min) | Meister (15 min + kaitsmine) |
|---|---|---|---|
| Probleem ja eesmärk | 1 min | 1 min | 2 min |
| Arhitektuur | 1 min | 2 min | 3 min |
| **Otsedemo** | 3 min | 4 min | 5 min, sh **rikketest otse** |
| Mis oli keeruline, kuidas lahendasid | 1 min | 2 min | 3 min |
| Järgmised sammud | 1 min | 1 min | 2 min |

Ole valmis vastama küsimustele, näiteks: „Mis juhtub, kui see ketas rikneb?“, „Kuidas sa teaksid, et teenus ei tööta?“, „Kuidas lisaksid uue kasutaja?“. Meistritasemel järgneb esitlusele **kaitsmine** (10–15 min), kus õpetaja või komisjon küsib lahenduse ülesehituse ja tehtud valikute kohta ning võib paluda midagi otse muuta.

## Hindamine

| Kriteerium | Algtase | Edasijõudnud | Meister |
|---|---|---|---|
| Lahendus töötab ja vastab põhinõuetele | 35% | 30% | 25% |
| Turvalisus | 15% | 15% | 15% |
| Varundus ja testitud taastamine | 20% | 15% | 10% |
| Automatiseerimine ja Git | 10% | 15% | 15% |
| Töökindlus, seire ja rikketest | - | 5% | 15% |
| Dokumentatsioon | 15% | 10% | 10% |
| Esitlus ja küsimustele vastamine | 5% | 10% | 10% |

Lisanõuete täitmine ja eriti hea lahendus võivad hinnet tõsta, kuid ei asenda põhinõudeid. Õpetaja võib edasijõudnute tasemel tehtud väga hea töö eest anda kõrgeima hinde; meistritase on mõeldud neile, kes soovivad endale tõsist väljakutset või ettevalmistust tööks.

## Nõuanded

- **Alusta väikselt.** Saa kõigepealt tööle lihtne versioon, seejärel lisa funktsioone. Meistritasemel ehita esmalt üks komponent lõpuni (koos koodi ja varundusega), siis dubleeri.
- **Tee hetktõmmiseid** enne suuri muudatusi.
- **Kanna sisse tihti.** Iga töötav samm on sissekanne.
- **Dokumenteeri jooksvalt**, mitte lõpus - lõpus ei mäleta sa enam, miks midagi tegid.
- **Testi taastamist päriselt:** kustuta virtuaalmasin (või loo uus) ja ehita lahendus dokumentatsiooni järgi uuesti üles. See on parim test nii varundusele kui ka dokumentatsioonile.
- **Küsi abi** õigel ajal - kirjelda, mida proovisid ja mis veateate said.
- **Ära unusta ressursse:** kooli Proxmoxis on ressursid jagatud - lülita masinad välja, kui sa nendega ei tööta.

## Pärast kursust

Palju õnne - oled läbinud Linuxi ja BSD kursuse nullist süsteemihalduseni! Järgmised sammud võiksid olla:

- **sertifikaat:** LPIC-1 või CompTIA Linux+ (distrost sõltumatu), Red Hat RHCSA (praktiline), hiljem RHCE või LPIC-2;
- **süvenemine:** „UNIX and Linux System Administration Handbook“, „The Linux Programming Interface“, Linux From Scratch;
- **praktika:** oma koduserver (nt Raspberry Pi või vana arvuti), avatud lähtekoodiga projektidesse panustamine, OverTheWire'i järgmised mängud;
- **edasised teemad:** Kubernetese süvendamine (CKA), pilveplatvormid (AWS, Azure), suuremad IaC-projektid (OpenTofu), küberturvalisus.

<!-- navigatsioon -->
---

[← Proovieksam: süvendusosa](proovieksam.md) · [Sisukord](../README.md#sisukord) · [Moodul 21. BSD praktikas: OPNsense tulemüür →](moodul-21-opnsense/index.md)
<!-- /navigatsioon -->
