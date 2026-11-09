# Moodul 13. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Kirjelda üldist töövoogu uue serveriteenuse paigaldamisel.
2. Mis on virtuaalhost ja kuidas valib nginx, millist saiti näidata?
3. Miks käivitatakse enne `systemctl reload nginx` käsku `nginx -t`?
4. Mis on pöördpuhverserver ja milleks seda kasutatakse?
5. Mida tõendab TLS-sertifikaat? Miks usaldab brauser Let's Encrypti sertifikaati, kuid mitte iseallkirjastatut?
6. Mis on SAN ja miks see oluline on?
7. Millal kasutada oma CA-d ja millal Let's Encrypti?
8. Mis vahe on nginx-il ja Apache'il? Millal eelistaksid Apache'it?
9. Mida teevad käsud `a2ensite`, `a2enmod` ja `apache2ctl configtest`? Mis on nende vasted AlmaLinuxis?
10. Mis on `.htaccess` ja miks seda peetakse nii mugavaks kui ka problemaatiliseks?
11. Mis on Caddy eripära? Mida tähendab Caddyfile'is `tls internal`?
12. Milleks kasutatakse lighttpd-d?
13. Mis on koormusejaotur ja tervisekontroll? Too kaks koormuse jaotamise algoritmi.
14. Miks näeb taustserver logis koormusejaoturi IP-d ja kuidas saada kliendi tegelik aadress?
15. Mis on Traefiki eripära võrreldes nginx-i ja HAProxyga?
16. Kirjelda avaliku veebisaidi sertifikaadi hankimist algusest lõpuni: mida on vaja enne, kuidas CA domeeni kontrollib, kuidas sertifikaat uueneb?
17. Mis vahe on ACME väljakutsetel HTTP-01 ja DNS-01? Millal on DNS-01 ainus võimalus?
18. Mis on vahesertifikaat ja miks peab nginx-i `ssl_certificate` olema `fullchain.pem`?
19. Miks lühenevad sertifikaatide kehtivusajad ja mida see administraatorile tähendab?
20. Mis on üksik rikkepunkt (*single point of failure*) ja kuidas aitab keepalived seda koormusejaoturi puhul vältida?
21. Kuidas VRRP otsustab, milline masin virtuaalset IP-aadressi hoiab? Mis juhtub, kui tulemüür VRRP-teated blokeerib?
22. Milliseid näitajaid vaatad koormustesti (`ab`) väljundis ja miks on protsentiilid olulisemad kui keskmine?

## Praktilised miniülesanded

1. Leia, millal aegub serveri `www.debian.org` sertifikaat ja kes selle välja andis.
2. Kirjuta nginx-i serveriplokk, mis suunab kõik nime `vana.lab.example` päringud aadressile `https://kool.lab.example`.
3. Kirjuta Caddyfile, mis teenindab nime `info.lab.example` kataloogist `/var/www/info` Caddy enda sertifikaadiga.
4. Kirjuta HAProxy taustserverite plokk, mis jagab päringud serveritele `10.0.83.52` ja `10.0.83.55` (port 80) vähima ühenduste arvu järgi ja kontrollib nende tervist.
5. Luba Debianis Apache'i moodulid `rewrite` ja `headers` ning kontrolli seadistust.

---

## Vastused

1. Paigalda → seadista (varukoopia algsest failist) → kontrolli süntaksit → käivita ja luba → ava tulemüür → testi kohalikult ja väljast → vaata logisid → seadista varundus → dokumenteeri.
2. Üks veebiserver teenindab mitut saiti. Brauser saadab päringus päise `Host:`, nginx valib selle järgi serveriploki, mille `server_name` sobib. Kui ükski ei sobi, kasutatakse pordi vaikeserverit.
3. `nginx -t` kontrollib seadistuse süntaksit. Vigane seadistus võib teenuse taaskäivitamisel saidi maha võtta.
4. Server, mis võtab päringud vastu ja edastab need taustal töötavale rakendusele. Kasutatakse TLS-i lõpetamiseks, mitme rakenduse jagamiseks ühe aadressi taga ja rakenduse peitmiseks otse internetist.
5. Et server on see, kelleks ta end nimetab (sertifikaadis olev nimi), ja et seda on tõendanud CA. Let's Encrypti juur-CA on brauseri usaldatud CA-de loendis, iseallkirjastatud sertifikaati pole keegi usaldusväärne tõendanud.
6. *Subject Alternative Name* - sertifikaadi väli, kus on nimed, millele sertifikaat kehtib. Brauserid kontrollivad serveri nime just selle välja järgi.
7. Oma CA sobib sisevõrgule ja laborile, kus nimed ei ole avalikud ja CA-d saab klientides usaldada. Let's Encrypt sobib avalikele saitidele, millel on avalik DNS-nimi.
8. nginx on sündmuspõhine ja kerge, sobib staatilistele failidele ja pöördpuhvriks; Apache on moodulipõhine ja paindlik ning toetab `.htaccess`-i. Apache'it eelistan, kui rakendus (nt vanem PHP-rakendus) või selle juhend seda eeldab.
9. `a2ensite` lubab saidi (viide `sites-enabled/`), `a2enmod` lubab mooduli, `apache2ctl configtest` kontrollib süntaksit. AlmaLinuxis on saidid failid `conf.d/` kataloogis (eraldi lubamist pole), moodulid `conf.modules.d/`, kontroll `apachectl configtest`.
10. Kataloogis asuv fail, millega saab Apache'i seadistust kataloogi kaupa muuta ilma serveri seadistust puutumata (mugav jagatud hostingus). Probleem: Apache peab iga päringu juures neid faile otsima (aeglasem) ja seadistus on laiali.
11. Automaatne HTTPS: avaliku nimega saidile hangib ja uuendab Caddy sertifikaadi ise; väga lühike seadistus. `tls internal` kasutab Caddy enda CA-d (sisevõrgu nimedele).
12. Väga väikese mälukasutusega veebiserver manussüsteemidele, ruuteritele ja väikestele seadmetele.
13. Koormusejaotur jagab päringud mitme taustserveri vahel; tervisekontroll kontrollib regulaarselt, kas taustserver vastab, ja jätab rikkis serveri välja. Algoritmid: round robin, least connections (ka source/IP hash).
14. TCP-ühendus tuleb jaoturist. Jaotur lisab päise `X-Forwarded-For` (HAProxy `option forwardfor`, nginx `proxy_set_header X-Forwarded-For`) ja taustserver seadistatakse seda usaldama (nginx `real_ip_header`).
15. Traefik leiab teenused automaatselt konteinerite siltidelt (Docker, Kubernetes) ja hangib sertifikaadid ise - sobib dünaamiliselt muutuvasse konteinerikeskkonda.
16. Vaja on avalikku domeeni ja DNS-kirjet serveri avalikule IP-le. ACME klient (certbot) taotleb sertifikaati, CA esitab väljakutse (HTTP-01: fail veebiserveris pordil 80; DNS-01: TXT-kirje), klient täidab selle ja CA väljastab DV-sertifikaadi. systemd taimer uuendab sertifikaati enne aegumist ja laadib veebiserveri uuesti; aegumist jälgitakse seiresüsteemiga.
17. HTTP-01 vajab, et server oleks internetist pordil 80 kättesaadav; DNS-01 tõendab domeeni kontrolli DNS-kirjega ja vajab DNS-i halduse ligipääsu. DNS-01 on ainus võimalus wildcard-sertifikaadiks ja sobib sisevõrgu serverile, mis ei ole internetist kättesaadav.
18. Juur-CA ei allkirjasta serveri sertifikaate otse - seda teeb vahe-CA, mille sertifikaadi on allkirjastanud juur-CA. Klient vajab kogu ahelat; kui server saadab ainult oma sertifikaadi, ei saa paljud kliendid (curl, telefonid) ahelat kontrollida.
19. Lühem kehtivus vähendab lekkinud võtmete ja vigaste sertifikaatide kahju ning sunnib automatiseerima. Administraatorile: kõik sertifikaadid peavad uuenema automaatselt (ACME) ja aegumist tuleb jälgida; käsitsi uuendamine ei ole enam realistlik.
20. Komponent, mille rikkel lakkab kogu teenus töötamast. Ühe HAProxy korral on selleks jaotur ise. keepalived hoiab kahe jaoturi vahel virtuaalset IP-d: kui põhimasin või selle HAProxy rikneb (`vrrp_script`), võtab varumasin VIP-i üle ja kliendid jätkavad sama aadressiga.
21. Masinad saadavad VRRP-teateid; VIP on suurima `priority`-ga töötava masina (MASTER) küljes. Kui varumasin teateid enam ei saa, võtab ta aadressi üle. Kui tulemüür blokeerib protokolli 112, ei näe masinad üksteist ja mõlemad muutuvad MASTER-iks (lõhestunud aju) - VIP on kahes kohas korraga.
22. `Requests per second` (läbilaskevõime), `Failed requests` (peab olema 0) ja vastamisaegade jaotus. Keskmine peidab aeglased päringud: kui 95% vastab 20 ms-ga ja 5% 3 sekundiga, on keskmine hea, aga iga kahekümnes kasutaja ootab kaua.

### Miniülesannete lahendused

```bash
echo | openssl s_client -connect www.debian.org:443 -servername www.debian.org 2>/dev/null \
    | openssl x509 -noout -issuer -enddate
```

```nginx
server {
    listen 80;
    server_name vana.lab.example;
    return 301 https://kool.lab.example$request_uri;
}
```

```text
info.lab.example {
    tls internal
    root * /var/www/info
    file_server
}
```

```text
backend koolisait
    balance leastconn
    server debian1 10.0.83.52:80 check
    server alma    10.0.83.55:80 check
```

```bash
sudo a2enmod rewrite headers
sudo apache2ctl configtest && sudo systemctl reload apache2
```

<!-- navigatsioon -->
---

[← Laboritöö 13. Veebiserverid (kooli väikeserver, I osa)](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 14. Andmebaasid →](../moodul-14-andmebaasid/index.md)
<!-- /navigatsioon -->
