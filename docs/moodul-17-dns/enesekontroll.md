<!-- navigatsioon -->
[← Laboritöö 17. Kooli väikeserver, III osa: DNS](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 18. Failiserverid →](../moodul-18-failiserverid/index.md)
<!-- /navigatsioon -->

# Moodul 17. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis vahe on autoriteetsel ja rekursiivsel DNS-serveril?

<details>
<summary>Vastus</summary>

Autoriteetne server vastab oma tsooni nimede kohta. Rekursiivne server küsib klientide eest vastuseid teistelt serveritelt ja hoiab vahemälu.

</details>

**2.** Selgita DNS-kirjeid `A`, `CNAME`, `MX` ja `NS`.

<details>
<summary>Vastus</summary>

`A` - nimi → IPv4-aadress; `CNAME` - nimi on teise nime alias; `MX` - domeeni e-posti server; `NS` - tsooni nimeserver.

</details>

**3.** Miks tuleb tsoonifaili muutmisel suurendada seerianumbrit?

<details>
<summary>Vastus</summary>

Seerianumber on tsooni versioon. Sekundaarsed serverid uuendavad tsooni ainult siis, kui seerianumber on suurenenud.

</details>

**4.** Võrdle BIND9-t, dnsmasq-i, CoreDNS-i ja Pi-hole'i: milleks igaüks sobib?

<details>
<summary>Vastus</summary>

BIND9 - täisfunktsionaalne autoriteetne ja rekursiivne server suurematele tsoonidele; dnsmasq - kerge edastav DNS + DHCP väikevõrku; CoreDNS - ühe failiga seadistatav, pistikprogrammidega, sobib konteineritesse ja Gitiga hallatavaks (Kubernetese DNS); Pi-hole - filtreeriv DNS, mis blokeerib reklaami- ja jälitusdomeene kogu võrgule.

</details>

**5.** Miks töötab `ping kool`, kuid `dig kool.lab.example` annab `NXDOMAIN`? Millise käsuga lahendad nime täpselt nii nagu programmid?

<details>
<summary>Vastus</summary>

Nimi on tõenäoliselt failis `/etc/hosts`, mida `ping` (läbi `nsswitch.conf`-i) kasutab, kuid `dig` küsib ainult DNS-serverilt. Programmidega sama tulemuse annab `getent hosts kool`.

</details>

**6.** Selgita, kuidas rekursiivne server leiab vastuse päringule `www.hkhk.edu.ee`, kui vahemälu on tühi.

<details>
<summary>Vastus</summary>

Ta küsib juurserverilt, mis suunab `ee.` nimeserveritele; need suunavad `edu.ee.`/`hkhk.edu.ee.` serveritele (NS-kirjed), mis on autoriteetsed ja annavad A-kirje. Rekursiivne server salvestab vastuse TTL-i ajaks vahemällu ja vastab kliendile. Teekonda näeb `dig +trace`.

</details>

**7.** Mis on TTL ja mida tasub sellega teha enne serveri kolimist uuele IP-aadressile?

<details>
<summary>Vastus</summary>

TTL on aeg sekundites, kui kaua võib kirjet vahemälus hoida. Enne kolimist vähendatakse TTL-i (nt 300 s) vähemalt vana TTL-i võrra ette, et pärast muutmist jõuaks uus aadress kiiresti kõigini; hiljem tõstetakse tagasi.

</details>

**8.** Mis on pöördtsoon ja milleks seda vaja on? Kuidas kirjutatakse võrgu `10.0.83.0/24` pöördtsooni nimi?

<details>
<summary>Vastus</summary>

Pöördtsoon seob IP-aadressi nimega (PTR-kirjed); seda kasutavad logid, diagnostikatööriistad ja e-posti serverid saatja kontrolliks. Nimi on `83.0.10.in-addr.arpa`.

</details>

**9.** Miks peab tsoonil olema vähemalt kaks nimeserverit ja kuidas jõuab muudatus sekundaarserverisse?

<details>
<summary>Vastus</summary>

Üks server on üksik rikkekoht - kui see on maas, ei lahene ükski tsooni nimi. Primaar saadab muudatuse järel NOTIFY; sekundaar võrdleb SOA seerianumbrit ja tõmbab suurema numbri korral tsooni tsooniülekandega (AXFR/IXFR). Ilma NOTIFY-ta kontrollib sekundaar SOA `refresh` aja järel.

</details>

**10.** Mis on avatud resolver ja miks see on ohtlik? Kuidas seda BIND9-s vältida?

<details>
<summary>Vastus</summary>

Rekursiivne server, mis vastab kõigile internetis. Seda kasutatakse DNS-võimendusrünnakuteks (väike võltsitud lähteaadressiga päring → suur vastus ohvrile). BIND9-s piiratakse `allow-recursion { sisevork; };`.

</details>

**11.** Mida tähendavad vastuse olekud `NXDOMAIN`, `SERVFAIL` ja `REFUSED`?

<details>
<summary>Vastus</summary>

`NXDOMAIN` - nime ei ole olemas; `SERVFAIL` - server ei saanud vastust (tsoon ei laadinud, ülemine server ei vasta, DNSSEC-i viga); `REFUSED` - server keeldus (päring või rekursioon pole sellele kliendile lubatud).

</details>

**12.** Mis on DNSSEC ja mis on DoT/DoH? Millist ohtu kumbki maandab?

<details>
<summary>Vastus</summary>

DNSSEC allkirjastab kirjed, nii et resolver saab kontrollida, et vastust pole võltsitud (vahemälu mürgitamise vastu). DoT ja DoH krüpteerivad päringud kliendi ja resolveri vahel (pealtkuulamise vastu). DNSSEC ei krüpteeri, DoT/DoH ei kontrolli kirjete ehtsust.

</details>

## Praktilised miniülesanded

**1.** Lisa tsooni `lab.example` e-posti server `mail.lab.example` (IP `10.0.83.58`) koos MX-kirjega.

<details>
<summary>Lahendus</summary>

```text
; 1 (tsoonifaili, suurenda seerianumbrit)
@       IN  MX  10 mail.lab.example.
mail    IN  A   10.0.83.58
```

</details>

**2.** Lisa pöördtsooni `83.0.10.in-addr.arpa` kirje, mis seob aadressi `10.0.83.66` nimega `fbsd.lab.example`, ja kontrolli seda.

<details>
<summary>Lahendus</summary>

```text
66  IN  PTR fbsd.lab.example.
```

Suurenda seerianumbrit, siis:

```bash
sudo named-checkzone 83.0.10.in-addr.arpa /etc/bind/db.10.0.83
sudo rndc reload
dig @localhost -x 10.0.83.66 +short
```

</details>

**3.** Kirjuta `debian2` BIND9 seadistusse tsooni `lab.example` sekundaarkirjeldus (primaar `10.0.83.52`).

<details>
<summary>Lahendus</summary>

```text
zone "lab.example" {
    type secondary;
    file "/var/cache/bind/db.lab.example";
    primaries { 10.0.83.52; };
};
```

</details>

**4.** Leia, kas kirje `www.lab.example` vastus tuleb serveri enda tsoonist või vahemälust, ning vaata päringu kogu teekonda juurest alates nimele `www.debian.org`.

<details>
<summary>Lahendus</summary>

```bash
dig @10.0.83.52 www.lab.example +norecurse    # lipp aa = autoriteetne vastus
dig www.debian.org +trace
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 17. Kooli väikeserver, III osa: DNS](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 18. Failiserverid →](../moodul-18-failiserverid/index.md)
<!-- /navigatsioon -->
