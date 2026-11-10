<!-- navigatsioon -->
[← Laboritöö 15. Veebiserverid (kooli väikeserver, I osa)](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 16. Andmebaasid →](../moodul-16-andmebaasid/index.md)
<!-- /navigatsioon -->

# Moodul 15. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Kirjelda üldist töövoogu uue serveriteenuse paigaldamisel.

<details>
<summary>Vastus</summary>

Paigalda → seadista (varukoopia algsest failist) → kontrolli süntaksit → käivita ja luba → ava tulemüür → testi kohalikult ja väljast → vaata logisid → seadista varundus → dokumenteeri.

</details>

**2.** Mis on virtuaalhost ja kuidas valib nginx, millist saiti näidata?

<details>
<summary>Vastus</summary>

Üks veebiserver teenindab mitut saiti. Brauser saadab päringus päise `Host:`, nginx valib selle järgi serveriploki, mille `server_name` sobib. Kui ükski ei sobi, kasutatakse pordi vaikeserverit.

</details>

**3.** Miks käivitatakse enne `systemctl reload nginx` käsku `nginx -t`?

<details>
<summary>Vastus</summary>

`nginx -t` kontrollib seadistuse süntaksit. Vigane seadistus võib teenuse taaskäivitamisel saidi maha võtta.

</details>

**4.** Mis on pöördpuhverserver ja milleks seda kasutatakse?

<details>
<summary>Vastus</summary>

Server, mis võtab päringud vastu ja edastab need taustal töötavale rakendusele. Kasutatakse TLS-i lõpetamiseks, mitme rakenduse jagamiseks ühe aadressi taga ja rakenduse peitmiseks otse internetist.

</details>

**5.** Mida tõendab TLS-sertifikaat? Miks usaldab brauser Let's Encrypti sertifikaati, kuid mitte iseallkirjastatut?

<details>
<summary>Vastus</summary>

Et server on see, kelleks ta end nimetab (sertifikaadis olev nimi), ja et seda on tõendanud CA. Let's Encrypti juur-CA on brauseri usaldatud CA-de loendis, iseallkirjastatud sertifikaati pole keegi usaldusväärne tõendanud.

</details>

**6.** Mis on SAN ja miks see oluline on?

<details>
<summary>Vastus</summary>

*Subject Alternative Name* - sertifikaadi väli, kus on nimed, millele sertifikaat kehtib. Brauserid kontrollivad serveri nime just selle välja järgi.

</details>

**7.** Millal kasutada oma CA-d ja millal Let's Encrypti?

<details>
<summary>Vastus</summary>

Oma CA sobib sisevõrgule ja laborile, kus nimed ei ole avalikud ja CA-d saab klientides usaldada. Let's Encrypt sobib avalikele saitidele, millel on avalik DNS-nimi.

</details>

**8.** Mis vahe on nginx-il ja Apache'il? Millal eelistaksid Apache'it?

<details>
<summary>Vastus</summary>

nginx on sündmuspõhine ja kerge, sobib staatilistele failidele ja pöördpuhvriks; Apache on moodulipõhine ja paindlik ning toetab `.htaccess`-i. Apache'it eelistan, kui rakendus (nt vanem PHP-rakendus) või selle juhend seda eeldab.

</details>

**9.** Mida teevad käsud `a2ensite`, `a2enmod` ja `apache2ctl configtest`? Mis on nende vasted AlmaLinuxis?

<details>
<summary>Vastus</summary>

`a2ensite` lubab saidi (viide `sites-enabled/`), `a2enmod` lubab mooduli, `apache2ctl configtest` kontrollib süntaksit. AlmaLinuxis on saidid failid `conf.d/` kataloogis (eraldi lubamist pole), moodulid `conf.modules.d/`, kontroll `apachectl configtest`.

</details>

**10.** Mis on `.htaccess` ja miks seda peetakse nii mugavaks kui ka problemaatiliseks?

<details>
<summary>Vastus</summary>

Kataloogis asuv fail, millega saab Apache'i seadistust kataloogi kaupa muuta ilma serveri seadistust puutumata (mugav jagatud hostingus). Probleem: Apache peab iga päringu juures neid faile otsima (aeglasem) ja seadistus on laiali.

</details>

**11.** Mis on Caddy eripära? Mida tähendab Caddyfile'is `tls internal`?

<details>
<summary>Vastus</summary>

Automaatne HTTPS: avaliku nimega saidile hangib ja uuendab Caddy sertifikaadi ise; väga lühike seadistus. `tls internal` kasutab Caddy enda CA-d (sisevõrgu nimedele).

</details>

**12.** Milleks kasutatakse lighttpd-d?

<details>
<summary>Vastus</summary>

Väga väikese mälukasutusega veebiserver manussüsteemidele, ruuteritele ja väikestele seadmetele.

</details>

**13.** Mis on koormusejaotur ja tervisekontroll? Too kaks koormuse jaotamise algoritmi.

<details>
<summary>Vastus</summary>

Koormusejaotur jagab päringud mitme taustserveri vahel; tervisekontroll kontrollib regulaarselt, kas taustserver vastab, ja jätab rikkis serveri välja. Algoritmid: round robin, least connections (ka source/IP hash).

</details>

**14.** Miks näeb taustserver logis koormusejaoturi IP-d ja kuidas saada kliendi tegelik aadress?

<details>
<summary>Vastus</summary>

TCP-ühendus tuleb jaoturist. Jaotur lisab päise `X-Forwarded-For` (HAProxy `option forwardfor`, nginx `proxy_set_header X-Forwarded-For`) ja taustserver seadistatakse seda usaldama (nginx `real_ip_header`).

</details>

**15.** Mis on Traefiki eripära võrreldes nginx-i ja HAProxyga?

<details>
<summary>Vastus</summary>

Traefik leiab teenused automaatselt konteinerite siltidelt (Docker, Kubernetes) ja hangib sertifikaadid ise - sobib dünaamiliselt muutuvasse konteinerikeskkonda.

</details>

**16.** Kirjelda avaliku veebisaidi sertifikaadi hankimist algusest lõpuni: mida on vaja enne, kuidas CA domeeni kontrollib, kuidas sertifikaat uueneb?

<details>
<summary>Vastus</summary>

Vaja on avalikku domeeni ja DNS-kirjet serveri avalikule IP-le. ACME klient (certbot) taotleb sertifikaati, CA esitab väljakutse (HTTP-01: fail veebiserveris pordil 80; DNS-01: TXT-kirje), klient täidab selle ja CA väljastab DV-sertifikaadi. systemd taimer uuendab sertifikaati enne aegumist ja laadib veebiserveri uuesti; aegumist jälgitakse seiresüsteemiga.

</details>

**17.** Mis vahe on ACME väljakutsetel HTTP-01 ja DNS-01? Millal on DNS-01 ainus võimalus?

<details>
<summary>Vastus</summary>

HTTP-01 vajab, et server oleks internetist pordil 80 kättesaadav; DNS-01 tõendab domeeni kontrolli DNS-kirjega ja vajab DNS-i halduse ligipääsu. DNS-01 on ainus võimalus wildcard-sertifikaadiks ja sobib sisevõrgu serverile, mis ei ole internetist kättesaadav.

</details>

**18.** Mis on vahesertifikaat ja miks peab nginx-i `ssl_certificate` olema `fullchain.pem`?

<details>
<summary>Vastus</summary>

Juur-CA ei allkirjasta serveri sertifikaate otse - seda teeb vahe-CA, mille sertifikaadi on allkirjastanud juur-CA. Klient vajab kogu ahelat; kui server saadab ainult oma sertifikaadi, ei saa paljud kliendid (curl, telefonid) ahelat kontrollida.

</details>

**19.** Miks lühenevad sertifikaatide kehtivusajad ja mida see administraatorile tähendab?

<details>
<summary>Vastus</summary>

Lühem kehtivus vähendab lekkinud võtmete ja vigaste sertifikaatide kahju ning sunnib automatiseerima. Administraatorile: kõik sertifikaadid peavad uuenema automaatselt (ACME) ja aegumist tuleb jälgida; käsitsi uuendamine ei ole enam realistlik.

</details>

**20.** Mis on üksik rikkepunkt (*single point of failure*) ja kuidas aitab keepalived seda koormusejaoturi puhul vältida?

<details>
<summary>Vastus</summary>

Komponent, mille rikkel lakkab kogu teenus töötamast. Ühe HAProxy korral on selleks jaotur ise. keepalived hoiab kahe jaoturi vahel virtuaalset IP-d: kui põhimasin või selle HAProxy rikneb (`vrrp_script`), võtab varumasin VIP-i üle ja kliendid jätkavad sama aadressiga.

</details>

**21.** Kuidas VRRP otsustab, milline masin virtuaalset IP-aadressi hoiab? Mis juhtub, kui tulemüür VRRP-teated blokeerib?

<details>
<summary>Vastus</summary>

Masinad saadavad VRRP-teateid; VIP on suurima `priority`-ga töötava masina (MASTER) küljes. Kui varumasin teateid enam ei saa, võtab ta aadressi üle. Kui tulemüür blokeerib protokolli 112, ei näe masinad üksteist ja mõlemad muutuvad MASTER-iks (lõhestunud aju) - VIP on kahes kohas korraga.

</details>

**22.** Milliseid näitajaid vaatad koormustesti (`ab`) väljundis ja miks on protsentiilid olulisemad kui keskmine?

<details>
<summary>Vastus</summary>

`Requests per second` (läbilaskevõime), `Failed requests` (peab olema 0) ja vastamisaegade jaotus. Keskmine peidab aeglased päringud: kui 95% vastab 20 ms-ga ja 5% 3 sekundiga, on keskmine hea, aga iga kahekümnes kasutaja ootab kaua.

</details>

## Praktilised miniülesanded

**1.** Leia, millal aegub serveri `www.debian.org` sertifikaat ja kes selle välja andis.

<details>
<summary>Lahendus</summary>

```bash
echo | openssl s_client -connect www.debian.org:443 -servername www.debian.org 2>/dev/null \
    | openssl x509 -noout -issuer -enddate
```

</details>

**2.** Kirjuta nginx-i serveriplokk, mis suunab kõik nime `vana.lab.example` päringud aadressile `https://kool.lab.example`.

<details>
<summary>Lahendus</summary>

```nginx
server {
    listen 80;
    server_name vana.lab.example;
    return 301 https://kool.lab.example$request_uri;
}
```

</details>

**3.** Kirjuta Caddyfile, mis teenindab nime `info.lab.example` kataloogist `/var/www/info` Caddy enda sertifikaadiga.

<details>
<summary>Lahendus</summary>

```text
info.lab.example {
    tls internal
    root * /var/www/info
    file_server
}
```

</details>

**4.** Kirjuta HAProxy taustserverite plokk, mis jagab päringud serveritele `10.0.83.52` ja `10.0.83.55` (port 80) vähima ühenduste arvu järgi ja kontrollib nende tervist.

<details>
<summary>Lahendus</summary>

```text
backend koolisait
    balance leastconn
    server debian1 10.0.83.52:80 check
    server alma    10.0.83.55:80 check
```

</details>

**5.** Luba Debianis Apache'i moodulid `rewrite` ja `headers` ning kontrolli seadistust.

<details>
<summary>Lahendus</summary>

```bash
sudo a2enmod rewrite headers
sudo apache2ctl configtest && sudo systemctl reload apache2
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 15. Veebiserverid (kooli väikeserver, I osa)](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 16. Andmebaasid →](../moodul-16-andmebaasid/index.md)
<!-- /navigatsioon -->
