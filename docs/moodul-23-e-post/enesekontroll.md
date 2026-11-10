<!-- navigatsioon -->
[← Laboritöö 23. E-posti server](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. Kataloogiteenused: OpenLDAP →](../moodul-24-openldap/index.md)
<!-- /navigatsioon -->

# Moodul 23. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Selgita MUA, MSA, MTA ja MDA rolle ning nimeta kummagi kohta üks programm.

<details>
<summary>Vastus</summary>

MUA - kasutaja programm (Thunderbird); MSA - võtab kasutaja kirja vastu autentimisega (Postfix pordil 587); MTA - edastab kirju serverite vahel (Postfix, Exim); MDA - paneb kirja postkasti (Dovecot LMTP). IMAP-server (Dovecot) annab postkastile ligipääsu.

</details>

**2.** Milliseid porte kasutavad e-posti server ja klient ning milleks?

<details>
<summary>Vastus</summary>

25 - SMTP serverilt serverile; 587 - kasutaja kirjade saatmine (STARTTLS + autentimine); 465 - sama kohe TLS-iga; 993 - IMAP üle TLS-i; 143 - IMAP STARTTLS-iga.

</details>

**3.** Mis vahe on ümbriku aadressidel (`MAIL FROM`, `RCPT TO`) ja päise aadressidel (`From:`, `To:`)?

<details>
<summary>Vastus</summary>

Serverid edastavad kirja ümbriku järgi; päis on kirja osa, mida kasutaja näeb. Need võivad erineda (Bcc, postiloendid, võltsimine) - SPF kontrollib ümbriku domeeni, DMARC seob kontrolli `From:` päisega.

</details>

**4.** Kuidas leiab saatev server, kuhu saata kiri aadressile `jaan@hkhk.edu.ee`?

<details>
<summary>Vastus</summary>

Küsib DNS-ist domeeni `hkhk.edu.ee` MX-kirjed, valib väikseima eelistusnumbriga serveri, lahendab selle A/AAAA-kirje ja ühendub pordile 25. Kui server ei vasta, proovib järgmist MX-i ja hiljem uuesti (kiri jääb järjekorda).

</details>

**5.** Selgita SPF, DKIM ja DMARC ülesandeid.

<details>
<summary>Vastus</summary>

SPF - DNS-is loetelu serveritest, mis tohivad domeeni nimel saata; DKIM - kirja krüptograafiline allkiri, mida kontrollitakse DNS-is oleva avaliku võtmega; DMARC - poliitika, mida teha kirjaga, mis ei läbi SPF-i/DKIM-i domeeniga klappivalt, ja kuhu saata aruanded.

</details>

**6.** Mis on avatud relee ja millise Postfixi seadega seda välditakse?

<details>
<summary>Vastus</summary>

Server, mis edastab ükskõik kelle kirju võõrastesse domeenidesse; seda kasutatakse rämpsposti saatmiseks ja server satub mustadesse nimekirjadesse. Postfixis `smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, defer_unauth_destination` ja `mynetworks` ainult localhost.

</details>

**7.** Miks kasutavad kliendid kirjade saatmiseks porti 587 ja mitte 25?

<details>
<summary>Vastus</summary>

Port 587 (*submission*) nõuab autentimist ja TLS-i, nii et ainult serveri kasutajad saavad kirju välja saata; paljud võrgud blokeerivad pordi 25 rämpsposti tõttu. Port 25 on serveritevaheliseks suhtluseks.

</details>

**8.** Milleks on Postfixil vaja Dovecoti, kui Postfix ise kirju vastu võtab?

<details>
<summary>Vastus</summary>

Dovecot hoiab ja annab IMAP-ligipääsu postkastidele ning autendib kasutajad - ka Postfixile (SASL läbi pesa `private/auth`), nii et kasutajate paroolid kontrollitakse ühes kohas.

</details>

**9.** Mida tähendavad SMTP vastuskoodid 2xx, 4xx ja 5xx? Mis juhtub kirjaga 4xx korral?

<details>
<summary>Vastus</summary>

2xx - õnnestus; 4xx - ajutine viga: saatev server jätab kirja järjekorda ja proovib hiljem uuesti (`deferred`); 5xx - püsiv viga: kiri tagastatakse saatjale (`bounced`).

</details>

**10.** Miks on pöördkirje (PTR) e-posti serverile oluline?

<details>
<summary>Vastus</summary>

Saaja server kontrollib, kas saatja IP pöördkirje on olemas ja klapib serveri nimega (FCrDNS). Ilma selleta liigitatakse kiri sageli rämpspostiks või lükatakse tagasi.

</details>

**11.** Mis on Maildir ja miks on see mugav?

<details>
<summary>Vastus</summary>

Postkasti vorming, kus iga kiri on eraldi fail kataloogides `new`, `cur`, `tmp`. Pole vaja ühte suurt faili lukustada, kirjad ei lähe katki samaaegsel kirjutamisel ja varundamisel kopeeritakse ainult uued kirjad.

</details>

**12.** Too kolm argumenti oma e-posti serveri ja kolm pilveposti kasuks.

<details>
<summary>Vastus</summary>

Oma server: andmed asutuse kontrolli all, pole kasutajapõhist tasu, täielik paindlikkus. Pilv: kättetoimetavus ja maine on teenusepakkuja mure, rämpsposti ja viiruste tõrje, kõrge kättesaadavus ja varundus, vähem hooldustööd ja turvaauke.

</details>

## Praktilised miniülesanded

**1.** Kirjuta tsooni `kool.example` kirjed: MX serverile `post.kool.example` (`10.0.83.70`), SPF, mis lubab ainult MX-serveril saata, ja DMARC poliitikaga `quarantine`.

<details>
<summary>Lahendus</summary>

```text
@       IN  MX   10 post.kool.example.
post    IN  A    10.0.83.70
@       IN  TXT  "v=spf1 mx -all"
_dmarc  IN  TXT  "v=DMARC1; p=quarantine; rua=mailto:postmaster@kool.example"
```

</details>

**2.** Leia Postfixi logist kõik kirjad, mille saatmine lükati edasi, ja proovi järjekord kohe uuesti saata.

<details>
<summary>Lahendus</summary>

```bash
sudo grep "status=deferred" /var/log/mail.log | tail
mailq
sudo postqueue -f
```

</details>

**3.** Kontrolli, kas server pakub pordil 587 STARTTLS-i ja milline sertifikaat on kasutusel, ning saada autentimisega testkiri.

<details>
<summary>Lahendus</summary>

```bash
openssl s_client -connect mail.lab.example:587 -starttls smtp </dev/null | openssl x509 -noout -subject -enddate
swaks --to jaan@lab.example --from mari@lab.example --server mail.lab.example:587 --tls --auth-user mari
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 23. E-posti server](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. Kataloogiteenused: OpenLDAP →](../moodul-24-openldap/index.md)
<!-- /navigatsioon -->
