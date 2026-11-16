<!-- navigatsioon -->
[← Laboritöö 18. DHCP-server](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 19. Faili- ja prindiserverid →](../moodul-19-failiserverid/index.md)
<!-- /navigatsioon -->

# Moodul 18. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mida tähendab DORA? Miks on DHCPDISCOVER leviedastus?

<details>
<summary>Vastus</summary>

Discover, Offer, Request, Acknowledge - nelja sõnumiga vahetus. DISCOVER on leviedastus, sest kliendil pole veel aadressi ja ta ei tea DHCP-serveri aadressi.

</details>

**2.** Miks töötab DHCP vaikimisi ainult ühes võrgusegmendis? Mis on DHCP relee?

<details>
<summary>Vastus</summary>

Leviedastused ei läbi ruutereid. DHCP relee (nt ruuteris) võtab leviedastuse vastu ja edastab selle teises võrgus asuvale DHCP-serverile.

</details>

**3.** Mis juhtub kliendiga, kui DHCP-server rendiaja keskel kaob?

<details>
<summary>Vastus</summary>

Klient kasutab aadressi edasi kuni rendi aegumiseni ja proovib vahepeal korduvalt renti uuendada. Kui rent aegub, kaotab klient aadressi.

</details>

**4.** Miks soovitatakse uutel süsteemidel ISC DHCP asemel Kea-d?

<details>
<summary>Vastus</summary>

ISC DHCP arendus on lõpetatud ja turvaparandusi ei tule; Kea on aktiivselt arendatav, toetab REST API-d ja on näiteks RHEL 10 ja OPNsense'i soovitatud lahendus.

</details>

**5.** Millise käsuga kontrollid Kea seadistuse õigsust?

<details>
<summary>Vastus</summary>

`kea-dhcp4 -t /etc/kea/kea-dhcp4.conf`.

</details>

**6.** Mis on DHCP reserveering ja kuidas see erineb staatilisest aadressist?

<details>
<summary>Vastus</summary>

DHCP-server annab kindla MAC-aadressiga kliendile alati sama aadressi; seadistus on serveris. Staatiline aadress on seadistatud masinas endas ega sõltu DHCP-serverist.

</details>

**7.** Klient sai aadressi `169.254.37.12`. Mida see tähendab ja mida kontrollid?

<details>
<summary>Vastus</summary>

See on kohtvõrgu (*link-local*) aadress, mille klient andis endale ise, sest DHCP-server ei vastanud. Kontrolli, kas DHCP-teenus töötab, kas see kuulab õigel liidesel, kas tulemüür lubab UDP porti 67 ja kas klient on serveriga samas võrgus (`tcpdump port 67 or port 68`).

</details>

**8.** Miks ei tohi samas võrgus olla kahte eri seadistusega DHCP-serverit? Mis on *rogue DHCP*?

<details>
<summary>Vastus</summary>

Klient võtab vastu esimese pakkumise, seega saavad kliendid juhuslikult ühe või teise serveri seadistuse (aadress, vaikelüüs, DNS) ja osa neist ei tööta. *Rogue DHCP* on volitamata DHCP-server; ründaja saab sellega suunata klientide liikluse läbi enda masina. Kommutaatorites kaitseb selle eest DHCP snooping.

</details>

**9.** Mida pead DHCP-serverist varundama ja mille kaotus on kõige valusam?

<details>
<summary>Vastus</summary>

Seadistusfaili `/etc/kea/kea-dhcp4.conf` (alamvõrgud, valikud, reserveeringud) ja võrguplaani. Rentide fail on vähem oluline - kliendid küsivad aadressi uuesti. Reserveeringuid ei saa mujalt taastada.

</details>

**10.** Millal valid pika, millal lühikese rendiaja?

<details>
<summary>Vastus</summary>

Pikk rent (nt 24 h) sobib püsivate seadmetega võrku: vähem liiklust ja kliendid töötavad edasi ka serveri lühikese rikke ajal. Lühike rent (nt 1 h) sobib võrku, kus seadmed vahetuvad sageli (külaliste WiFi), sest aadressid vabanevad kiiresti.

</details>

## Praktilised miniülesanded

**1.** Lisa Kea seadistusse teine alamvõrk `10.0.84.0/24` vahemikuga `.100–.150` ja vaikelüüsiga `.1`.

<details>
<summary>Lahendus</summary>

```json
{
  "id": 2,
  "subnet": "10.0.84.0/24",
  "pools": [ { "pool": "10.0.84.100 - 10.0.84.150" } ],
  "option-data": [ { "name": "routers", "data": "10.0.84.1" } ]
}
```

(lisa massiivi `subnet4`)

</details>

**2.** Lisa Kea seadistusse globaalne NTP-serveri valik `10.0.83.1`.

<details>
<summary>Lahendus</summary>

```json
{ "name": "ntp-servers", "data": "10.0.83.1" }
```

(lisa globaalsesse massiivi `option-data`)

</details>

**3.** Kirjuta ISC DHCP reserveering masinale `printer` (MAC `00:11:22:33:44:55`, IP `10.0.83.20`).

<details>
<summary>Lahendus</summary>

```text
host printer {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 10.0.83.20;
}
```

</details>

**4.** Püüa serveris DHCP-liiklust ja uuenda Ubuntu kliendis renti. Kirjuta mõlemad käsud.

<details>
<summary>Lahendus</summary>

```bash
sudo tcpdump -ni ens18 -v port 67 or port 68     # serveris
sudo networkctl renew ens18                       # kliendis
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 18. DHCP-server](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 19. Faili- ja prindiserverid →](../moodul-19-failiserverid/index.md)
<!-- /navigatsioon -->
