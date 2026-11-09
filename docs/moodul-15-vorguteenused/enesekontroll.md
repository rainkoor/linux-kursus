# Moodul 15. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis vahe on autoriteetsel ja rekursiivsel DNS-serveril?
2. Selgita DNS-kirjeid `A`, `CNAME`, `MX` ja `NS`.
3. Miks tuleb tsoonifaili muutmisel suurendada seerianumbrit?
4. Mis on NFS-i `root_squash` ja miks see vaikimisi sees on?
5. Miks on Sambal oma paroolid?
6. Selgita varunduse 3-2-1 reeglit. Miks on oluline taastamist testida?
7. Võrdle BIND9-t, dnsmasq-i, CoreDNS-i ja Pi-hole'i: milleks igaüks sobib?
8. Millal valiksid failiserveriks TrueNASi ja millal ise seadistatud Debiani Samba ja NFS-iga? Miks peaks TrueNAS nägema päris kettaid?
9. Milleks on serveris vaja MTA-d (nt Postfix), kui see ei ole e-posti server? Mis on relee (*smarthost*)?
10. Miks peab Postfixi `inet_interfaces` olema laborserveris `loopback-only`?
11. Mis on autofs ja mille poolest on see parem kui NFS-i rida `/etc/fstab`-is?
12. Mis on RPO ja RTO? Kooli e-õppekeskkonda varundatakse igal ööl kell 02.00 ja taastamine võtab 3 tundi. Milline on halvimal juhul andmekadu ja kas see sobib, kui RTO on 2 tundi?
13. Mille poolest erineb käsiraamat (*runbook*) tavalisest serveri dokumentatsioonist? Milleks on otsuste logi?

## Praktilised miniülesanded

1. Lisa tsooni `lab.example` e-posti server `mail.lab.example` (IP `10.0.83.58`) koos MX-kirjega.
2. Kirjuta `/etc/exports` rida, mis jagab kataloogi `/srv/iso` kogu võrgule `10.0.0.0/8` ainult lugemiseks.
3. Kuva restic'u hoidlast kõik hetktõmmised ja taasta eelviimasest failid kataloogist `/etc/nginx`.

---

## Vastused

1. Autoriteetne server vastab oma tsooni nimede kohta. Rekursiivne server küsib klientide eest vastuseid teistelt serveritelt ja hoiab vahemälu.
2. `A` - nimi → IPv4-aadress; `CNAME` - nimi on teise nime alias; `MX` - domeeni e-posti server; `NS` - tsooni nimeserver.
3. Seerianumber on tsooni versioon. Sekundaarsed serverid uuendavad tsooni ainult siis, kui seerianumber on suurenenud.
4. Kliendi juurkasutaja muudetakse serveris õigusteta kasutajaks `nobody`. Muidu saaks iga kliendi juurkasutaja serveri jagatud failidega teha kõike.
5. SMB-protokoll kasutab autentimiseks teist meetodit kui Linuxi sisselogimine, mistõttu Samba vajab kasutajate jaoks oma räsisid. (Active Directory domeenis autenditakse kasutajad domeenikontrolleri kaudu.)
6. Kolm koopiat, kahel eri andmekandjal, üks mujal. Taastamist tuleb testida, sest alles siis on näha, kas varukoopia on täielik, loetav ja kas taastamise sammud on teada.
7. BIND9 - täisfunktsionaalne autoriteetne ja rekursiivne server suurematele tsoonidele; dnsmasq - kerge edastav DNS + DHCP väikevõrku; CoreDNS - ühe failiga seadistatav, pistikprogrammidega, sobib konteineritesse ja Gitiga hallatavaks (Kubernetese DNS); Pi-hole - filtreeriv DNS, mis blokeerib reklaami- ja jälitusdomeene kogu võrgule.
8. TrueNAS: palju kettaid, ZFS-i töökindlus, hetktõmmised ja replikatsioon veebiliidesest, eraldi salvestusseade. Oma Debian: kui samas masinas on ka muud teenused, vaja on täielikku kontrolli või õpitakse seadistamist. ZFS jälgib ketaste tervist ja parandab vigu ainult siis, kui tal on otseligipääs ketastele; virtuaalketaste all olevat riket ta ei näe.
9. Et serveri enda programmid (cron, systemd, `smartd`, skriptid) saaksid teateid saata. Relee on teine SMTP-server (asutuse või pakkuja oma), mille kaudu server kirjad edastab, selle asemel et neid ise otse adressaatide serveritesse saata.
10. Server ei tohi võtta võrgust kirju vastu ega edastada neid - avatud releed kasutatakse rämpsposti saatmiseks ja server satub mustadesse nimekirjadesse.
11. autofs haagib jagamise alles siis, kui kataloogi poole pöördutakse, ja haagib lahti tegevusetuse järel. Alglaadimine ei sõltu failiserverist ja kodukataloogid saab metamärgiga (`*`, `&`) haakida kõigile kasutajatele.
12. RPO - lubatud andmekadu ajas; RTO - lubatud taastumisaeg. Rike vahetult enne järgmist varundust tähendab kuni ~24 h andmekadu. 3-tunnine taastamine ei mahu 2-tunnise RTO sisse - vaja on kiiremat taastamist (nt valmis VM-i varukoopia, varuserver) või tuleb RTO-s kokku leppida uuesti.
13. Dokumentatsioon kirjeldab, kuidas süsteem on ehitatud; käsiraamat annab sammhaaval tegevusjuhised kindlateks olukordadeks (rike, hooldus), mida saab järgida ka süsteemi mittetundev inimene. Otsuste logi talletab, miks midagi valiti, et hilisemad muudatused ei kordaks vanu vigu.

### Miniülesannete lahendused

```text
; 1 (tsoonifaili, suurenda seerianumbrit)
@       IN  MX  10 mail.lab.example.
mail    IN  A   10.0.83.58
```

```text
# 2
/srv/iso  10.0.0.0/8(ro,sync,no_subtree_check)
```

```bash
# 3
sudo -E restic snapshots
sudo -E restic restore <eelviimase ID> --target /tmp/taaste --include /etc/nginx
```

<!-- navigatsioon -->
---

[← Laboritöö 15. Kooli väikeserver, III osa: DNS, failid, e-post ja varundus](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 16. Automatiseerimine: Ansible, Vagrant ja infrastruktuur koodina →](../moodul-16-automatiseerimine/index.md)
<!-- /navigatsioon -->
