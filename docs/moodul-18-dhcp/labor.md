<!-- navigatsioon -->
[← Moodul 18. DHCP](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 18. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 18. DHCP-server

| | |
|---|---|
| **Distrod** | Debian (`debian1` - DHCP-server), Ubuntu ja AlmaLinux (kliendid) |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Oma laborivõrk ja võrguplaan ([paigalduslisa](../lisad/paigaldus.md), punkt 2), `debian1` staatilise aadressiga, vähemalt üks klientmasin (nt `ubuntuklient` või mõne masina kloon), soovitatavalt laboritöö 17 DNS-server |
| **Eesmärk** | Seadistada oma laborivõrgule DHCP-server, mis jagab klientidele aadressi, vaikelüüsi ja DNS-serveri, ning osata leida DHCP vigu |

> **Aruanne:** vasta küsimustele **K1–K12**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

> [!WARNING]
> **Tee seda laboritööd ainult oma laborivõrgus!** Kontrolli enne alustamist, et `debian1` võrguliides on Proxmoxis ühendatud sinu enda silda või VNet-i, mitte kooli võrku. Kui sinu võrgus jagab aadresse juba mõni teine seade (nt valikmooduli 22 OPNsense või koduruuter), lülita selle DHCP-server enne Kea käivitamist välja.

Tähised võrguplaani näite järgi: võrk `10.0.83.0/24`, vaikelüüs `10.0.83.1`, `debian1` `10.0.83.52`, DHCP vahemik `10.0.83.80–99`, reserveeringud `10.0.83.98` ja `10.0.83.99`. Asenda oma võrguplaani väärtustega.

---

## 1. osa. Kea DHCP-server

**1.1** Kontrolli `debian1` võrguseadistust - DHCP-serveril endal peab olema staatiline aadress:

```bash
ip -br a
ip r
cat /etc/resolv.conf
```

**1.2** Kontrolli, et võrgus ei ole juba DHCP-serverit. Käivita `debian1`-s püüdmine ja uuenda samal ajal mõne DHCP peale seatud kliendi renti (või taaskäivita klient):

```bash
sudo apt install tcpdump
sudo tcpdump -ni ens18 -v port 67 or port 68
```

> **K1.** Kas nägid kliendi päringuid (DISCOVER)? Kas keegi vastas neile? Miks on see kontroll enne oma DHCP-serveri käivitamist oluline?

**1.3** Paigalda Kea ja tee algsest seadistusest koopia:

```bash
sudo apt install kea-dhcp4-server
sudo cp /etc/kea/kea-dhcp4.conf /etc/kea/kea-dhcp4.conf.orig
wc -l /etc/kea/kea-dhcp4.conf.orig
```

> **K2.** Mitu rida on näidisseadistuses? Miks on parem kirjutada oma lühike seadistus kui muuta pikka näidisfaili?

**1.4** Kirjuta fail `/etc/kea/kea-dhcp4.conf` teooria punkti 18.3 põhjal oma võrguplaani järgi. Reserveeringut veel ära lisa. DNS-serveriks pane oma laboritöö 17 DNS-server (`10.0.83.52`); kui sul seda ei ole, siis vaikelüüs.

**1.5** Kontrolli süntaksit. Tee meelega viga (kustuta mõni koma) ja kontrolli uuesti. Paranda.

```bash
sudo kea-dhcp4 -t /etc/kea/kea-dhcp4.conf
```

> **K3.** Mida näitas kontroll vea korral? Miks on JSON-i puhul nii lihtne viga teha?

**1.6** Käivita Kea ja jälgi logi:

```bash
sudo systemctl restart kea-dhcp4-server
systemctl status kea-dhcp4-server
sudo ufw allow 67/udp          # kui ufw on sees
journalctl -u kea-dhcp4-server -f
```

## 2. osa. Kliendid

**2.1** Seadista Ubuntu klient DHCP-d kasutama (moodul 7, punkt 7.2, „Ubuntu: DHCP“), kui see juba nii ei ole. Uuenda renti ja jälgi samal ajal `debian1` logi:

```bash
sudo networkctl renew <liides>
ip -br a
ip r
resolvectl status | head -15
```

> **K4.** Leia logist DHCP-sõnumite vahetus (DISCOVER, OFFER, REQUEST, ACK - Kea logis `DHCP4_PACKET_RECEIVED`, `DHCP4_LEASE_ALLOC` vms). Millise aadressi, vaikelüüsi ja DNS-serveri klient sai?

**2.2** Vaata rente serveris:

```bash
sudo cat /var/lib/kea/kea-leases4.csv
```

**2.3** Püüa DHCP-liiklust `debian1`-s, kui klient uuendab renti uuesti:

```bash
sudo tcpdump -ni ens18 -v port 67 or port 68
```

> **K5.** Kas nägid leviedastusi (`255.255.255.255`)? Millised DHCP-valikud olid serveri vastuses (ruuter, DNS, domeen, rendiaeg)?

**2.4** Lülita AlmaLinux (`alma`) ajutiselt DHCP peale (moodul 7, punkt 7.2, „AlmaLinux: DHCP“). Tee seda Proxmoxi konsoolist, sest SSH-ühendus katkeb, kui aadress muutub.

> **K6.** Millise aadressi sai `alma`? Mis juhtuks teenustega, mida teised masinad kasutavad `alma` vana aadressi kaudu? Miks on serveritel staatiline aadress?

**2.5** Taasta `alma` staatiline aadress (`10.0.83.55`) ja kontrolli ühendust.

## 3. osa. Reserveering ja valikud

**3.1** Lisa Ubuntu kliendile reserveering võrguplaanis olevale aadressile (`10.0.83.98`) teooria punkti 18.3 juhendi järgi. Kontrolli süntaksit, taaskäivita Kea ja uuenda kliendi renti.

> **K7.** Kas klient sai reserveeritud aadressi kohe? Kui ei, miks (vihje: olemasolev rent)? Kuidas probleemi lahendasid?

**3.2** Muuda rendiaeg lühikeseks (`valid-lifetime` 120, `renew-timer` 60, `rebind-timer` 90), taaskäivita Kea, uuenda kliendi renti ja jälgi logi paar minutit.

> **K8.** Kui tihti klient nüüd renti uuendab? Millal on lühike rendiaeg kasulik ja mis on selle hind?

**3.3** Taasta mõistlik rendiaeg (nt 86400 s) ja lisa globaalne NTP-serveri valik (`ntp-servers`, sinu vaikelüüs või ajaserver). Kontrolli ja taaskäivita.

## 4. osa. Tõrkeotsing

**4.1** Peata Kea ja oota, mis juhtub kliendiga, kui see renti uuendada üritab (`networkctl renew`). Käivita Kea uuesti.

> **K9.** Mis juhtus kliendi aadressiga, kui DHCP-server ei vastanud? Miks ei kaota klient aadressi kohe?

**4.2** Tee seadistusse viga, mida süntaksikontroll ei leia: muuda `interfaces-config` liidese nimi valeks (nt `ens99`). Taaskäivita Kea ja uuenda kliendi renti.

> **K10.** Mida näitas `systemctl status` ja mida logi? Kuidas leidsid vea põhjuse? Paranda seadistus.

**4.3** Vaata, mida näeb klient, kui võrgus oleks kaks DHCP-serverit - **ainult arutle, ära teist serverit käivita.**

> **K11.** Mis juhtuks, kui pinginaaber ühendaks oma DHCP-serveri sinuga samasse võrku? Kuidas saaksid `tcpdump`-iga kindlaks teha, milline server kliendile vastas?

## 5. osa. Varundus ja dokumenteerimine

**5.1** Varunda Kea seadistus ja lisa see oma seadistuste Git-hoidlasse, kui sul see on (moodul 6):

```bash
sudo tar -czf /root/kea-$(date +%F).tar.gz /etc/kea /var/lib/kea
```

**5.2** Täienda võrguplaani.

> **K12.** Lisa aruandesse oma võrguplaan: staatilised aadressid, DHCP vahemik, reserveeringud, DHCP-serveri aadress ja jagatavad valikud (vaikelüüs, DNS, domeen, NTP). Kas staatilised aadressid ja DHCP vahemik kattuvad?

---

## Lisaülesanne (valikuline)

1. **ISC DHCP võrdlus:** seadista samale võrgule (Kea peatatuna) ISC DHCP teooria punkti 18.5 järgi ja võrdle seadistusfaile ning logisid. Lõpuks eemalda ISC DHCP ja käivita Kea.
2. **dnsmasq:** proovi eraldi testvõrgus dnsmasq-i DHCP-d (teooria punkt 18.2) ja kontrolli, et DHCP-ga antud nimi lahendub kohe ka DNS-is.
3. **Windowsi klient:** lisa reserveering Windowsi kliendile (`10.0.83.99`) ja kontrolli käskudega `ipconfig /all`, `ipconfig /release` ja `ipconfig /renew`.

---

## Koristamine

Jäta DHCP-server tööle - seda kasutavad järgmiste laboritööde klientmasinad. Kontrolli, et `alma` on tagasi staatilisel aadressil ja rendiaeg on taastatud.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Kas nägid kliendi päringuid (DISCOVER)? Kas keegi vastas neile? Miks on see kontroll enne oma DHCP-serveri käivitamist oluline?
- **K2.** *(punkt 1.3)* Mitu rida on näidisseadistuses? Miks on parem kirjutada oma lühike seadistus kui muuta pikka näidisfaili?
- **K3.** *(punkt 1.5)* Mida näitas kontroll vea korral? Miks on JSON-i puhul nii lihtne viga teha?
- **K4.** *(punkt 2.1)* Leia logist DHCP-sõnumite vahetus (DISCOVER, OFFER, REQUEST, ACK - Kea logis `DHCP4_PACKET_RECEIVED`, `DHCP4_LEASE_ALLOC` vms). Millise aadressi, vaikelüüsi ja DNS-serveri klient sai?
- **K5.** *(punkt 2.3)* Kas nägid leviedastusi (`255.255.255.255`)? Millised DHCP-valikud olid serveri vastuses (ruuter, DNS, domeen, rendiaeg)?
- **K6.** *(punkt 2.4)* Millise aadressi sai `alma`? Mis juhtuks teenustega, mida teised masinad kasutavad `alma` vana aadressi kaudu? Miks on serveritel staatiline aadress?
- **K7.** *(punkt 3.1)* Kas klient sai reserveeritud aadressi kohe? Kui ei, miks (vihje: olemasolev rent)? Kuidas probleemi lahendasid?
- **K8.** *(punkt 3.2)* Kui tihti klient nüüd renti uuendab? Millal on lühike rendiaeg kasulik ja mis on selle hind?
- **K9.** *(punkt 4.1)* Mis juhtus kliendi aadressiga, kui DHCP-server ei vastanud? Miks ei kaota klient aadressi kohe?
- **K10.** *(punkt 4.2)* Mida näitas `systemctl status` ja mida logi? Kuidas leidsid vea põhjuse? Paranda seadistus.
- **K11.** *(punkt 4.3)* Mis juhtuks, kui pinginaaber ühendaks oma DHCP-serveri sinuga samasse võrku? Kuidas saaksid `tcpdump`-iga kindlaks teha, milline server kliendile vastas?
- **K12.** *(punkt 5.2)* Lisa aruandesse oma võrguplaan: staatilised aadressid, DHCP vahemik, reserveeringud, DHCP-serveri aadress ja jagatavad valikud (vaikelüüs, DNS, domeen, NTP). Kas staatilised aadressid ja DHCP vahemik kattuvad?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 18. DHCP](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 18. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
