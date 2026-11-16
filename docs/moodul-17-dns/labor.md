<!-- navigatsioon -->
[← Moodul 17. DNS ja nimelahendus](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 17. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 17. Kooli väikeserver, III osa: DNS

| | |
|---|---|
| **Distro** | Debian (laboritööde 15 ja 16 server `debian1` ja teine Debian `debian2`), klient Ubuntu |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Laboritööde 15 ja 16 server `debian1`, teine Debiani masin `debian2` (sekundaarserver) ja Ubuntu klient |
| **Eesmärk** | Lisada serverile sisevõrgu DNS koos pöördtsooni ja sekundaarserveriga, harjutada DNS-i tõrkeotsingut ja hoida tsoone Gitis |

> **Aruanne:** vasta küsimustele **K1–K10**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

Tähised on samad mis laboritöös 15 (`SERVER_IP`, `KLIENT_IP`, `VORK`, `lab.example`).

---

## 0. osa. Ettevalmistus

```bash
sudo apt install bind9 bind9-dnsutils git
```

Eemalda pärast 1. osa Ubuntu kliendi `/etc/hosts` failist laboritöös 15 lisatud rida - nüüd lahendab nimed sinu DNS-server.

---

## 1. osa. DNS-server

**1.1** Loo tsoon `lab.example` (vt teooria punkt 17.4). Lisa kirjed:

| Nimi | Tüüp | Väärtus |
|---|---|---|
| `ns1` | A | `SERVER_IP` |
| `debian1` | A | `SERVER_IP` |
| `kool` | A | `SERVER_IP` |
| `info` | CNAME | `kool` |
| `www` | CNAME | `kool` |
| `klient` | A | `KLIENT_IP` |

**1.2** Kontrolli ja rakenda:

```bash
sudo named-checkconf
sudo named-checkzone lab.example /etc/bind/db.lab.example
sudo systemctl reload named
dig @localhost kool.lab.example +short
dig @localhost info.lab.example
dig @localhost www.debian.org +short
```

> **K1.** Mida näitab `dig` väljundis `info.lab.example` kohta (sektsioon `ANSWER`)? Kas server lahendab ka internetinimesid? Miks?

**1.3** Seadista **Ubuntu klient** kasutama sinu DNS-serverit (ajutiselt, kuni taaskäivituseni):

```bash
sudo resolvectl dns <liides> SERVER_IP
sudo resolvectl domain <liides> lab.example
resolvectl status <liides>
dig kool.lab.example +short
ping -c2 kool
curl http://info.lab.example
```

**1.4** Lisa tsooni uus kirje `test IN A 192.0.2.10`, **suurenda seerianumbrit**, kontrolli ja laadi uuesti. Kontrolli Ubuntust: `dig test.lab.example +short`.

> **K2.** Mis juhtub, kui muudad tsoonifaili, kuid seerianumbrit ei suurenda? (Ühe serveriga laboris töötab see sageli ikkagi - miks on seerianumber siiski oluline?)


---

## 2. osa. Pöördtsoon

**2.1** Loo `debian1`-s pöördtsoon oma võrgule (teooria punkt 17.4, nt `83.0.10.in-addr.arpa`) ja lisa PTR-kirjed kõigile oma laborimasinatele (`debian1`, `debian2`, `ubuntusrv`, `alma`, klient).

```bash
sudo named-checkzone 83.0.10.in-addr.arpa /etc/bind/db.10.0.83
sudo systemctl reload named
dig @localhost -x SERVER_IP +short
dig @localhost -x KLIENT_IP +short
```

**2.2** Vaata Ubuntu kliendist SSH-ga `debian1`-le sisse logides serveri logi (`sudo journalctl -u ssh -n 5`) ja käsu `last -n 3` väljundit.

> **K3.** Kas logides ja `last`-i väljundis on nüüd IP-aadressi asemel nimi? Miks on pöördkirje tähtis ka e-posti serverile (vihje: rämpspost)?

---

## 3. osa. Sekundaarserver

**3.1** Paigalda `debian2`-sse BIND9 ja seadista see tsoonide `lab.example` ja pöördtsooni **sekundaariks** (teooria punkt 17.5). Seadista `debian1`-s `allow-transfer` ja `also-notify` ning lisa tsooni teine nimeserver `ns2` (`debian2` aadressiga). **Suurenda seerianumbrit.** Kui `debian2`-s on tulemüür, ava port 53 (UDP ja TCP).

```bash
# debian2
sudo journalctl -u named -n 20 | grep -i -E "transfer|zone"
ls -l /var/cache/bind/
dig @localhost kool.lab.example +short
dig @localhost lab.example NS +short
```

> **K4.** Mida näitab `debian2` logi tsooniülekande kohta? Millises vormingus on sekundaari salvestatud tsoonifail (proovi `file` ja `head` - vihje: BIND kasutab vaikimisi binaarvormingut `raw`)?

**3.2** Lisa `debian1` tsooni uus kirje `uus IN A 10.0.83.170`, suurenda seerianumbrit, laadi uuesti ja kontrolli kohe `debian2`-st: `dig @localhost uus.lab.example +short`.

**3.3** Peata `debian1`-s BIND9 (`sudo systemctl stop named`) ja küsi Ubuntu kliendist mõlemalt serverilt:

```bash
dig @debian1.lab.example kool.lab.example +short     # kasuta IP-aadressi, kui nimi ei lahene
dig @DEBIAN2_IP kool.lab.example +short
```

> **K5.** Kas uus kirje jõudis sekundaari kohe? Mis pani selle liikuma (NOTIFY või SOA `refresh`)? Kaua vastab sekundaar ilma primaarita ja milline SOA väli seda määrab? Käivita lõpuks `debian1` BIND9 uuesti.

---

## 4. osa. Tõrkeotsing

Tee kõik vead ükshaaval, kirjelda sümptomit ja paranda viga enne järgmist.

**4.1** Muuda tsoonifailis kirje `www IN CNAME kool` kujule `www IN CNAME kool.lab.example` (punkt puudub lõpust), suurenda seerianumbrit ja laadi uuesti.

```bash
dig @localhost www.lab.example
sudo named-checkzone lab.example /etc/bind/db.lab.example
```

**4.2** Kirjuta tsoonifaili meelega süntaksiviga (nt kustuta SOA-kirje sulg), suurenda seerianumbrit ja laadi uuesti `sudo systemctl reload named`.

```bash
dig @localhost kool.lab.example
sudo journalctl -u named -n 20
```

> **K6.** Mida näitas `dig` (`NOERROR`, `NXDOMAIN` või `SERVFAIL`) kummalgi juhul ja kuhu osutas CNAME 4.1 juhul? Mis oleks kõige kiiremini vea leidnud?

**4.3** Muuda `named.conf.options`-is `allow-recursion` nii, et lubatud on ainult `localhost`, ja küsi Ubuntu kliendist `dig @SERVER_IP www.debian.org`. Seejärel taasta.

> **K7.** Mis vastuse said (vaata `status:` rida)? Miks ei tohi internetist kättesaadav DNS-server olla avatud resolver?

---

## 5. osa. Tsoonid Gitis

**5.1** Loo `debian1`-s kataloogist `/etc/bind` Giti hoidla (juurkasutajana; moodul 6) ja tee esimene sissekanne. Muuda üht kirjet, suurenda seerianumbrit, tee sissekanne ja vaata ajalugu.

```bash
cd /etc/bind
sudo git init
sudo git add .
sudo git -c user.name="Admin" -c user.email="admin@lab.example" commit -m "Tsoonid enne muudatusi"
sudo git log --oneline
sudo git diff HEAD~1          # pärast teist sissekannet
```

**5.2** „Kustuta kogemata“ tsoonifail (`sudo rm db.lab.example`), taasta see Gitist (`sudo git checkout -- db.lab.example`) ja kontrolli `named-checkzone`-ga.

> **K8.** Mis on Giti eelis tavalise varukoopia ees DNS-i seadistuse puhul? Miks ei ole sekundaarserver varukoopia?

> **K9.** Kui palju DNS-servereid ja millises rollis vajaks väike kool (umbes 300 seadet, oma veebileht ja e-post pilves)? Põhjenda.

> **K10.** Joonista (või kirjelda) päringu `www.debian.org` teekond Ubuntu kliendist: millised serverid osalevad ja kus hoitakse vahemälu?

---

## Lisaülesanne (valikuline)

1. **AAAA-kirjed:** lisa tsooni moodulis 13 seadistatud IPv6-aadressid (`fd83::…`) ja kontrolli `dig AAAA`.
2. **SRV-kirje:** lisa kirje `_ssh._tcp IN SRV 0 0 22 debian1.lab.example.` ja küsi `dig SRV _ssh._tcp.lab.example`.
3. **Unbound:** paigalda `ubuntusrv`-sse Unbound rekursiivseks resolveriks, mis suunab `lab.example` päringud `debian1`-le (`forward-zone`) ja ülejäänud otse juurest. Võrdle vastuse kiirust esimesel ja teisel päringul (`dig … | grep "Query time"`).
4. **DNSSEC:** kontrolli `dig +dnssec www.ria.ee` ja `dig dnssec-failed.org` vastuseid oma BIND9 serveri kaudu. Mida tähendab lipp `ad`?

---

# Laboritöö 17B. Teised DNS-serverid: Pi-hole ja CoreDNS (Ubuntu)

| | |
|---|---|
| **Distro** | Ubuntu |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Laboritöö 17 Debiani server BIND9-ga, laboritöö 7 Ubuntu masin (või eraldi Ubuntu VM, nt `ubuntusrv` Dockeriga), 2. osa jaoks Docker või Podman |
| **Eesmärk** | Paigaldada filtreeriv DNS-server ja kasutada sama tsooni CoreDNS-iga |

> **Aruanne:** vasta küsimustele **D1–D10**.

## 1. osa. Pi-hole

**1.1** Kontrolli, mis Ubuntus pordil 53 juba kuulab:

```bash
sudo ss -tulpn | grep ':53 '
resolvectl status | head -20
```

> **D1.** Milline protsess kuulab pordil 53 ja millisel aadressil? Miks see võib Pi-hole'iga konflikti minna?

**1.2** Lülita `systemd-resolved` kohalik kuulaja välja (teooria punkt 17.6, dnsmasq-i märkus) ja seadista masin ise kasutama ajutiselt välist DNS-i:

```bash
sudo mkdir -p /etc/systemd/resolved.conf.d
printf '[Resolve]\nDNSStubListener=no\n' | sudo tee /etc/systemd/resolved.conf.d/pihole.conf
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
sudo systemctl restart systemd-resolved
sudo ss -tulpn | grep ':53 '
```

**1.3** Laadi alla Pi-hole'i paigaldusskript, **loe see läbi** ja käivita. Vali ülemiseks DNS-iks nt Quad9, liides `ens18` (või sinu liides), luba veebiliides ja päringute logi. Määra veebiliidese parool:

```bash
curl -sSL https://install.pi-hole.net -o basic-install.sh
less basic-install.sh
sudo bash basic-install.sh
sudo pihole setpassword
sudo ufw allow from VORK to any port 53
sudo ufw allow from VORK to any port 80 proto tcp
```

> **D2.** Mida skript tegi (paketid, teenused, failid)? Miks on parem skript enne käivitamist läbi lugeda kui kasutada `curl ... | sudo bash`?

**1.4** Testi teisest masinast (nt Debianist):

```bash
dig @PIHOLE_IP www.debian.org +short
dig @PIHOLE_IP doubleclick.net +short
dig @PIHOLE_IP ads.google.com +short
```

> **D3.** Mida vastas Pi-hole blokeeritud domeenidele? Mitu domeeni on blokeerimisloendis (veebiliides → *Dashboard* või `pihole status`)?

**1.5** Ava veebiliides `http://PIHOLE_IP/admin`. Lisa:

- kohalik DNS-kirje `pihole.lab.example → PIHOLE_IP` (*Local DNS*);
- oma blokeeritav domeen (nt `example.org`) ja kontrolli `dig`-iga;
- lubatud domeen (*allowlist*) mõnele blokeeritud domeenile ja kontrolli uuesti;
- suunamine: domeeni `lab.example` päringud saadetakse laboritöö 17 BIND9 serverile (Pi-hole'i v6 seadetes *Conditional forwarding* või *All settings* → `misc.dnsmasq_lines` reaga `server=/lab.example/SERVER_IP`).

```bash
dig @PIHOLE_IP kool.lab.example +short
pihole -q example.org
```

> **D4.** Kas `kool.lab.example` lahenes Pi-hole'i kaudu? Kirjelda päringu teekonda: klient → ? → ?

**1.6** Seadista Debiani server kasutama DNS-ina Pi-hole'i ja ava Debianis mõni veebileht `curl`-iga. Vaata veebiliidese *Query Log*-i.

> **D5.** Milliseid päringuid Debian tegi? Mis on Pi-hole'i eelised ja puudused võrreldes brauseri reklaamiblokeerijaga? Milline privaatsusküsimus kaasneb päringute logiga?

## 2. osa. CoreDNS konteineris

Kasuta moodulis 14 õpitud Compose'i. Pi-hole'i ja CoreDNS-i korraga samal pordil käivitada ei saa - kasuta teist VM-i või peata Pi-hole (`sudo systemctl stop pihole-FTL`).

**2.1** Loo kataloog ja kopeeri sinna laboritöö 17 BIND9 tsoonifail:

```bash
mkdir -p ~/coredns/zones && cd ~/coredns
scp kasutaja@SERVER_IP:/etc/bind/db.lab.example zones/
```

**2.2** Loo `Corefile` (teooria punkt 17.6): tsoon `lab.example` failist ja kõik muu edasi `1.1.1.1`-le. Loo `compose.yaml` ja käivita:

```bash
docker compose up -d          # või: podman compose up -d
docker compose logs -f
dig @localhost kool.lab.example +short
dig @localhost www.debian.org +short
```

> **D6.** Kas CoreDNS vastas mõlemale päringule? Millised read tekkisid logis (`log` pistikprogramm)?

**2.3** Lisa tsoonifaili uus kirje `test IN A 10.0.83.160`, **suurenda seerianumbrit** ja oota ~1 minut ilma konteinerit taaskäivitamata:

```bash
dig @localhost test.lab.example +short
```

> **D7.** Kas uus kirje ilmus ilma taaskäivituseta? Mis juhtub, kui seerianumbrit ei suurenda?

**2.4** Pane `Corefile`, `compose.yaml` ja `zones/` Giti hoidlasse. Kirjuta skript `uuenda.sh`, mis teeb `git pull` ja mille käivitab systemd taimer (moodul 5) iga 5 minuti järel. Muuda kirjet teises masinas, `push`-i ja kontrolli, et CoreDNS-i vastus muutus.

> **D8.** Kuidas tagab selline lahendus, et kaks DNS-serverit annavad sama vastuse? Mis on selle eelis ja puudus võrreldes BIND9 primaar-sekundaar tsooniülekandega (AXFR)?

## 3. osa. Kokkuvõte

> **D9.** Täida tabel: BIND9, dnsmasq, CoreDNS, Pi-hole - kas autoriteetne, kas rekursiivne/edastav, seadistuse vorm, kus sa seda kasutaksid?

> **D10.** Kool tahab laborivõrgule sisevõrgu nimesid ja reklaamide blokeerimist. Kirjelda arhitektuur, kasutades selle laboritöö teenuseid.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Mida näitab `dig` väljundis `info.lab.example` kohta (sektsioon `ANSWER`)? Kas server lahendab ka internetinimesid? Miks?
- **K2.** *(punkt 1.4)* Mis juhtub, kui muudad tsoonifaili, kuid seerianumbrit ei suurenda? (Ühe serveriga laboris töötab see sageli ikkagi - miks on seerianumber siiski oluline?)
- **K3.** *(punkt 2.2)* Kas logides ja `last`-i väljundis on nüüd IP-aadressi asemel nimi? Miks on pöördkirje tähtis ka e-posti serverile (vihje: rämpspost)?
- **K4.** *(punkt 3.1)* Mida näitab `debian2` logi tsooniülekande kohta? Millises vormingus on sekundaari salvestatud tsoonifail (proovi `file` ja `head` - vihje: BIND kasutab vaikimisi binaarvormingut `raw`)?
- **K5.** *(punkt 3.3)* Kas uus kirje jõudis sekundaari kohe? Mis pani selle liikuma (NOTIFY või SOA `refresh`)? Kaua vastab sekundaar ilma primaarita ja milline SOA väli seda määrab? Käivita lõpuks `debian1` BIND9 uuesti.
- **K6.** *(punkt 4.2)* Mida näitas `dig` (`NOERROR`, `NXDOMAIN` või `SERVFAIL`) kummalgi juhul ja kuhu osutas CNAME 4.1 juhul? Mis oleks kõige kiiremini vea leidnud?
- **K7.** *(punkt 4.3)* Mis vastuse said (vaata `status:` rida)? Miks ei tohi internetist kättesaadav DNS-server olla avatud resolver?
- **K8.** *(punkt 5.2)* Mis on Giti eelis tavalise varukoopia ees DNS-i seadistuse puhul? Miks ei ole sekundaarserver varukoopia?
- **K9.** *(punkt 5.2)* Kui palju DNS-servereid ja millises rollis vajaks väike kool (umbes 300 seadet, oma veebileht ja e-post pilves)? Põhjenda.
- **K10.** *(punkt 5.2)* Joonista (või kirjelda) päringu `www.debian.org` teekond Ubuntu kliendist: millised serverid osalevad ja kus hoitakse vahemälu?
- **D1.** *(punkt 1.1)* Milline protsess kuulab pordil 53 ja millisel aadressil? Miks see võib Pi-hole'iga konflikti minna?
- **D2.** *(punkt 1.3)* Mida skript tegi (paketid, teenused, failid)? Miks on parem skript enne käivitamist läbi lugeda kui kasutada `curl ... | sudo bash`?
- **D3.** *(punkt 1.4)* Mida vastas Pi-hole blokeeritud domeenidele? Mitu domeeni on blokeerimisloendis (veebiliides → *Dashboard* või `pihole status`)?
- **D4.** *(punkt 1.5)* Kas `kool.lab.example` lahenes Pi-hole'i kaudu? Kirjelda päringu teekonda: klient → ? → ?
- **D5.** *(punkt 1.6)* Milliseid päringuid Debian tegi? Mis on Pi-hole'i eelised ja puudused võrreldes brauseri reklaamiblokeerijaga? Milline privaatsusküsimus kaasneb päringute logiga?
- **D6.** *(punkt 2.2)* Kas CoreDNS vastas mõlemale päringule? Millised read tekkisid logis (`log` pistikprogramm)?
- **D7.** *(punkt 2.3)* Kas uus kirje ilmus ilma taaskäivituseta? Mis juhtub, kui seerianumbrit ei suurenda?
- **D8.** *(punkt 2.4)* Kuidas tagab selline lahendus, et kaks DNS-serverit annavad sama vastuse? Mis on selle eelis ja puudus võrreldes BIND9 primaar-sekundaar tsooniülekandega (AXFR)?
- **D9.** *(3. osa)* Täida tabel: BIND9, dnsmasq, CoreDNS, Pi-hole - kas autoriteetne, kas rekursiivne/edastav, seadistuse vorm, kus sa seda kasutaksid?
- **D10.** *(3. osa)* Kool tahab laborivõrgule sisevõrgu nimesid ja reklaamide blokeerimist. Kirjelda arhitektuur, kasutades selle laboritöö teenuseid.
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 17. DNS ja nimelahendus](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 17. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
