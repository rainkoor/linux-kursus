<!-- navigatsioon -->
[← Moodul 15. Veebiserverid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 15. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 15. Veebiserverid (kooli väikeserver, I osa)

| | |
|---|---|
| **Distrod** | Debian (`debian1`, nginx), AlmaLinux (`alma`, Apache), Ubuntu (`ubuntusrv`, Caddy ja HAProxy) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Debiani server `debian1`, AlmaLinux `alma` ja Ubuntu `ubuntusrv` (või laboritöö 7 Ubuntu masin kliendina), oma arvuti brauseriga |
| **Eesmärk** | Paigaldada ja seadistada terviklik serveriteenuste komplekt, varundada see ja testida taastamist |

> **Aruanne:** vasta küsimustele **K1–K14**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

**Stsenaarium:** kool vajab väikest serverit, mis pakub veebisaiti koos õpilaste andmebaasiga, sisevõrgu DNS-i, failide jagamist Linuxi ja Windowsi arvutitele ning igaöist varundust. Selles laboritöös paigaldad veebiserverid, **laboritöös 16** lisad andmebaasid, **laboritöös 17** DNS-i ning **laboritöös 19** failijagamise, varunduse ja dokumentatsiooni.

Laboris kasutatavad tähised:

| Tähis | Tähendus |
|---|---|
| `SERVER_IP` | Debiani serveri IP-aadress |
| `KLIENT_IP` | Ubuntu kliendi IP-aadress |
| `VORK` | Sinu laborivõrk, nt `10.0.83.0/24` |
| `lab.example` | Laboridomeen (õpetaja võib anda teise) |

---

## 0. osa. Ettevalmistus

**0.1** Anna serverile nimi ja kontrolli aadressi:

```bash
sudo hostnamectl set-hostname debian1
ip -br address
```

Lisa faili `/etc/hosts` rida `SERVER_IP  debian1.lab.example debian1`.

**0.2** Uuenda süsteem ja paigalda vajalikud paketid:

```bash
sudo apt update && sudo apt upgrade
sudo apt install nginx curl
```

> **K1.** Millised teenused käivitusid pärast paigaldamist automaatselt? Millistel portidel need kuulavad (`sudo ss -tulpn`)?



---

## 1. osa. Veebiserver ja virtuaalhostid

Loo kaks saiti: `kool.lab.example` (kooli sait) ja `info.lab.example` (infotahvel).

**1.1** Loo saitide failid:

```bash
sudo mkdir -p /var/www/kool /var/www/info
echo "<h1>Haapsalu õppekool</h1><p>Server debian1</p>" | sudo tee /var/www/kool/index.html
echo "<h1>Infotahvel</h1><p>Esmaspäeval on IT-päev!</p>" | sudo tee /var/www/info/index.html
```

**1.2** Loo saidile `kool.lab.example` seadistus failis `/etc/nginx/sites-available/kool.lab.example` (vt teooria punkt 15.2) eraldi logifailidega. Loo samamoodi `info.lab.example`.

**1.3** Luba saidid, keela vaikesait, kontrolli ja rakenda:

```bash
sudo ln -s /etc/nginx/sites-available/kool.lab.example /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/info.lab.example /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

**1.4** Testi `Host:` päisega:

```bash
curl -H "Host: kool.lab.example" http://localhost
curl -H "Host: info.lab.example" http://localhost
curl -H "Host: midagi.muud" http://localhost
```

> **K2.** Mida näitas kolmas päring ja miks? (Vihje: kui ükski `server_name` ei sobi, kasutab nginx pordi **vaikeserverit** - kumb plokk see on?)

**1.5** Tee meelega süntaksiviga (kustuta mõne rea lõpust semikoolon) ja käivita `sudo nginx -t`. Paranda.

> **K3.** Mida näitas `nginx -t`? Miks on oluline kontrollida süntaksit enne `reload`-i?



---

## 2. osa. Nimed klientides

DNS-serveri seadistame moodulis 17. Seni lisa saitide nimed **kõigi masinate** (Ubuntu klient, `alma`, `ubuntusrv`) faili `/etc/hosts`:

```text
SERVER_IP  kool.lab.example info.lab.example www.lab.example debian1.lab.example debian1
10.0.83.155 alma.lab.example alma
10.0.83.154 ubuntusrv.lab.example ubuntusrv caddy.lab.example
```

```bash
getent hosts kool.lab.example
curl http://info.lab.example
```


---

## 3. osa. HTTPS oma sertifitseerimiskeskusega

Tee punktid 3.1–3.3 **juurkasutaja kestas**, sest CA failid on kataloogis `/root/ca`, kuhu tavakasutaja ei pääse:

```bash
sudo -i
```

**3.1** Loo kataloog ja oma CA:

```bash
mkdir -p /root/ca && cd /root/ca
openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
    -keyout labori-ca.key -out labori-ca.crt -subj "/CN=<Sinu nimi> labori CA"
chmod 600 labori-ca.key
```

**3.2** Loo serverile võti ja sertifikaat, mis kehtib nimedele `kool.lab.example`, `info.lab.example` ja `www.lab.example` (vt teooria punkt 15.3). Kontrolli tulemust käskudega `openssl verify` ja `openssl x509 ... -ext subjectAltName`.

**3.3** Paigalda sertifikaat ja võti:

```bash
mkdir -p /etc/ssl/kool
cp kool.crt kool.key /etc/ssl/kool/
chmod 600 /etc/ssl/kool/kool.key
exit
```

**3.4** Muuda saidi `kool.lab.example` seadistust: HTTP suunab HTTPS-ile ja HTTPS kasutab sertifikaati (vt teooria punkt 15.3). Kontrolli ja rakenda (`nginx -t`, `reload`).

**3.5** Testi Ubuntu kliendist:

```bash
curl -I http://kool.lab.example
curl https://kool.lab.example
```

> **K4.** Mida vastas esimene päring (olekukood ja päis `Location`)? Mis veateate andis teine päring ja miks?

**3.6** Kopeeri CA sertifikaat (mitte võti!) Ubuntu kliendile ja usalda seda. Serveris:

```bash
sudo cp /root/ca/labori-ca.crt /tmp/ && sudo chmod 644 /tmp/labori-ca.crt
```

Ubuntu kliendis:

```bash
scp kasutaja@SERVER_IP:/tmp/labori-ca.crt .
sudo cp labori-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
curl https://kool.lab.example
openssl s_client -connect kool.lab.example:443 -servername kool.lab.example </dev/null 2>/dev/null | grep -E "subject=|issuer=|Verify return"
```

> **K5.** Mida näitas `openssl s_client` väljundis `Verify return code`? Miks ei tohi CA privaatvõtit (`labori-ca.key`) kunagi serverist välja anda?

**3.7** (Valikuline) Impordi CA sertifikaat oma arvuti brauserisse ja ava `https://kool.lab.example` (oma arvuti `hosts` failis peab olema nimi).



---

## 4. osa. Apache AlmaLinuxis

**4.1** Paigalda `alma`-sse Apache, ava tulemüür ja kontrolli:

```bash
sudo dnf install -y httpd mod_ssl
sudo systemctl enable --now httpd
sudo firewall-cmd --permanent --add-service={http,https} && sudo firewall-cmd --reload
curl -I http://localhost
```

**4.2** Loo sait `kool.lab.example` kataloogi `/srv/kool` (mitte `/var/www`!) ja virtuaalhost `/etc/httpd/conf.d/kool.conf` (teooria punkt 15.4, AlmaLinuxis `ErrorLog /var/log/httpd/kool.error.log`). Pane avalehele tekst `Server alma`.

```bash
sudo mkdir -p /srv/kool
echo "<h1>Haapsalu õppekool</h1><p>Server alma</p>" | sudo tee /srv/kool/index.html
sudo apachectl configtest && sudo systemctl reload httpd
curl -H "Host: kool.lab.example" http://localhost
```

> **K6.** Mis vastuse said ja miks? Leia põhjus `sudo ausearch -m AVC -ts recent` abil ja paranda see püsivalt (`semanage fcontext` + `restorecon`, moodul 12).

**4.3** Loo kataloogi `.htaccess` fail, mis keelab ligipääsu failile `salajane.txt`, ja luba virtuaalhostis `AllowOverride All`:

```bash
echo "salajane" | sudo tee /srv/kool/salajane.txt
printf '<Files "salajane.txt">\n    Require all denied\n</Files>\n' | sudo tee /srv/kool/.htaccess
sudo systemctl reload httpd
curl -I -H "Host: kool.lab.example" http://localhost/salajane.txt
```

> **K7.** Mis olekukoodi said? Miks ei saa nginx `.htaccess`-faile kasutada ja miks peetakse neid jõudluse mõttes halvemaks?

**4.4** Lisa Apache'ile HTTPS **sama labori CA** sertifikaadiga, mille lõid 3. osas (sertifikaat kehtib nimele `kool.lab.example`, seega sobib ka `alma`-le). Kopeeri `debian1`-st failid `kool.crt` ja `kool.key` `alma`-sse:

```bash
sudo mkdir -p /etc/pki/tls/kool
sudo cp kool.crt kool.key /etc/pki/tls/kool/
sudo chmod 600 /etc/pki/tls/kool/kool.key
sudo restorecon -Rv /etc/pki/tls/kool
```

Lisa faili `/etc/httpd/conf.d/kool.conf` HTTPS-virtuaalhost:

```apache
<VirtualHost *:443>
    ServerName kool.lab.example
    DocumentRoot /srv/kool
    SSLEngine on
    SSLCertificateFile    /etc/pki/tls/kool/kool.crt
    SSLCertificateKeyFile /etc/pki/tls/kool/kool.key
</VirtualHost>
```

```bash
sudo apachectl configtest && sudo systemctl reload httpd
curl --resolve kool.lab.example:443:10.0.83.155 https://kool.lab.example/     # Ubuntu kliendist, labori CA on usaldatud
```

> [!NOTE]
> **Laboris kasutame alati oma sertifikaate** (labori CA või Caddy `tls internal`). Let's Encrypt vajab avalikku DNS-nime ja internetist kättesaadavat porti 80 - laborivõrgus see ei tööta ega ole vajalik.

---

## 5. osa. Caddy ja automaatne HTTPS

**5.1** Paigalda `ubuntusrv`-sse Caddy ja käivita testrakendus:

```bash
sudo apt install -y caddy
mkdir -p ~/rakendus && cd ~/rakendus && echo "<h1>Rakendus pordil 3000</h1>" > index.html
python3 -m http.server 3000 --bind 127.0.0.1 &
```

**5.2** Kirjuta `/etc/caddy/Caddyfile` (teooria punkt 15.5): sait `caddy.lab.example` (`tls internal`, pöördpuhver `localhost:3000`). **Ära jäta `tls internal` välja** - ilma selleta proovib Caddy hankida Let's Encrypti sertifikaati, mis laborivõrgus ebaõnnestub (logis `obtaining certificate … error`). Kontrolli ja rakenda:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
curl -vk https://caddy.lab.example 2>&1 | grep -E "issuer|HTTP/"
```

**5.3** Usalda Caddy CA-d kliendis: kopeeri `ubuntusrv`-st fail `/var/lib/caddy/.local/share/caddy/pki/authorities/local/root.crt` Ubuntu kliendi kataloogi `/usr/local/share/ca-certificates/caddy-labor.crt` ja käivita `sudo update-ca-certificates`. Proovi uuesti ilma `-k`-ta.

> **K8.** Mitu rida oli Caddyfile'is ja mitu rida vajaks sama nginx-is (koos sertifikaadi loomisega)? Kes oli sertifikaadi väljaandja? Mis juhtuks, kui nimi oleks avalik (nt `www.example.ee`) ja server internetis?

**5.4** (Valikuline) Kasuta Caddys Caddy enda CA asemel **3. osa labori CA-d**, et kõik laborimasinad usaldaksid ühte CA-d. Loo `debian1`-s (`/root/ca`) punkti 3.2 eeskujul sertifikaat nimele `caddy.lab.example`, kopeeri `caddy.crt` ja `caddy.key` `ubuntusrv` kataloogi `/etc/caddy/certs/` (omanik `caddy`, võtme õigused `600`) ja muuda Caddyfile'is `tls internal` → `tls /etc/caddy/certs/caddy.crt /etc/caddy/certs/caddy.key`. Kontrolli `curl -v`-ga, et väljaandja on nüüd sinu labori CA.

---

## 6. osa. Koormuse jaotus HAProxyga

**6.1** Veendu, et `debian1` (nginx) ja `alma` (Apache) vastavad mõlemad nimele `kool.lab.example` ja et avalehel on serveri nimi (`Server debian1` / `Server alma`).

**6.2** Paigalda `ubuntusrv`-sse HAProxy ja seadista see pordile 8080 (Caddy kasutab porte 80 ja 443): teooria punkti 15.7 seadistuses muuda `bind *:80` → `bind *:8080`. Kontrolli ja rakenda:

```bash
sudo apt install -y haproxy
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
sudo systemctl reload haproxy
for i in $(seq 6); do curl -s -H "Host: kool.lab.example" http://localhost:8080/ | grep -o "Server [a-z0-9]*"; done
```

> **K9.** Kuidas päringud serverite vahel jagunesid? Miks oli vaja saata päis `Host:`?

**6.3** Ava statistikaleht `http://ubuntusrv:8404`. Peata `alma`-s Apache (`sudo systemctl stop httpd`) ja korda `curl`-tsüklit. Käivita Apache uuesti.

> **K10.** Mida näitas statistikaleht? Mitu päringut ebaõnnestus pärast Apache'i peatamist ja kui kiiresti HAProxy rikke avastas (`option httpchk`, `check`)?

**6.4** Vaata `debian1` nginx-i juurdepääsulogi: mis IP-aadressilt päringud tulid?

> **K11.** Miks on logis HAProxy aadress, mitte kliendi oma? Kuidas saab taustserver teada kliendi tegeliku IP (vihje: `X-Forwarded-For`, HAProxy `option forwardfor`)?

---

## 7. osa. Päris sertifikaadid

Laboris kasutasid oma CA-d ja Caddy CA-d. Selles osas uurid, kuidas näevad välja **avalikud** sertifikaadid (teooria punkt 15.3, plokk „Loe lähemalt: Avaliku sertifikaadi hankimine“). Internetiühendusega masinast:

**7.1** Vaata päris saidi sertifikaati ja ahelat:

```bash
echo | openssl s_client -connect www.debian.org:443 -servername www.debian.org -showcerts 2>/dev/null \
    | grep -E "^ *[0-9] s:|^ *i:"
echo | openssl s_client -connect www.debian.org:443 -servername www.debian.org 2>/dev/null \
    | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

**7.2** Kontrolli DNS-ist, millised CA-d tohivad domeenile sertifikaate väljastada, ja vaata brauseris Certificate Transparency logi:

```bash
dig +short CAA debian.org
dig +short CAA google.com
```

Ava brauseris `https://crt.sh/?q=debian.org` (või oma kooli domeen).

> **K12.** Kes väljastas `www.debian.org` sertifikaadi? Mitu sertifikaati oli ahelas ja mis on vahesertifikaadi roll? Mitu päeva sertifikaat kokku kehtib ja mitu on veel jäänud?

> **K13.** Mida näitas crt.sh? Miks ei tasu sisevõrgu masinate nimedele (`proxmox1.lab.kool.ee`) avalikke sertifikaate küsida? Mis oleks lahendus, kui siiski on vaja avalikult usaldatud sertifikaati sisevõrgu serverile?

---

## 8. osa. Kokkuvõte

> **K14.** Täida tabel: nginx, Apache, Caddy, HAProxy - milleks kasutasid, seadistusfail, süntaksi kontrolli käsk, logide asukoht. Millise valiksid kooli uuele veebisaidile ja millise mõne konteineris töötava haldusliidese ette?

---

## Lisaülesanne (valikuline)

1. **Pöördpuhver nginx-iga:** käivita `debian1`-s Pythoni veebiserver (`python3 -m http.server 3000 --bind 127.0.0.1`) ja tee see nginx-i kaudu kättesaadavaks aadressil `https://rakendus.lab.example` (lisa nimi kliendi `/etc/hosts`-i ja loo labori CA-ga sertifikaat, mille SAN sisaldab ka seda nime).
2. **lighttpd:** paigalda `debian1`-sse lighttpd pordile 8081 (`server.port = 8081`) ja võrdle nginx-i ning lighttpd mälukasutust (`ps -o rss,cmd -C nginx,lighttpd`).
3. **Let's Encrypt staging (kui sul on oma domeen ja DNS-i haldus):** hangi `certbot certonly --manual --preferred-challenges dns --staging -d test.<sinu domeen>` abil testsertifikaat DNS-01 väljakutsega ja vaata, millise TXT-kirje certbot sind looma palub. Uuri tulemust `openssl x509 -noout -issuer -dates`.
4. **HTTPS HAProxys:** lõpeta TLS HAProxys labori CA sertifikaadiga: `cat kool.crt kool.key | sudo tee /etc/haproxy/kool.pem` (õigused `600`) ja `bind *:8443 ssl crt /etc/haproxy/kool.pem`; taustale suuna HTTP-ga.
5. **Traefik:** käivita Traefik ja kaks `whoami` konteinerit siltidega (teooria punkt 15.7) ning vaata, kuidas Traefik need automaatselt leiab.
6. **Rikkekindel jaotur (keepalived):** paigalda HAProxy ka `debian2`-sse sama seadistusega (port 8080) ning mõlemasse masinasse keepalived teooria punkti 15.7 järgi: `ubuntusrv` MASTER (`priority 150`), `debian2` BACKUP (`priority 100`), VIP `10.0.83.150`. Luba tulemüüris VRRP. Käivita kliendist `while true; do curl -s -m 1 http://10.0.83.150:8080/ | grep -o "Server [a-z0-9]*"; sleep 0.5; done` ja peata samal ajal `ubuntusrv`-s HAProxy (`sudo systemctl stop haproxy`). Kui kaua teenus katkes? Kumma masina küljes on VIP (`ip -br a`)? Mis juhtub, kui HAProxy uuesti käivitad?
7. **Koormustest:** mõõda `ab -n 2000 -c 50`-ga kooli saiti otse ühest taustserverist ja HAProxy kaudu. Võrdle `Requests per second` ja 95. protsentiili. Korda testi, kui üks taustserver on peatatud. Mis oli pudelikael (`top` taustserverites)?

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 0.2)* Millised teenused käivitusid pärast paigaldamist automaatselt? Millistel portidel need kuulavad (`sudo ss -tulpn`)?
- **K2.** *(punkt 1.4)* Mida näitas kolmas päring ja miks? (Vihje: kui ükski `server_name` ei sobi, kasutab nginx pordi **vaikeserverit** - kumb plokk see on?)
- **K3.** *(punkt 1.5)* Mida näitas `nginx -t`? Miks on oluline kontrollida süntaksit enne `reload`-i?
- **K4.** *(punkt 3.5)* Mida vastas esimene päring (olekukood ja päis `Location`)? Mis veateate andis teine päring ja miks?
- **K5.** *(punkt 3.6)* Mida näitas `openssl s_client` väljundis `Verify return code`? Miks ei tohi CA privaatvõtit (`labori-ca.key`) kunagi serverist välja anda?
- **K6.** *(punkt 4.2)* Mis vastuse said ja miks? Leia põhjus `sudo ausearch -m AVC -ts recent` abil ja paranda see püsivalt (`semanage fcontext` + `restorecon`, moodul 12).
- **K7.** *(punkt 4.3)* Mis olekukoodi said? Miks ei saa nginx `.htaccess`-faile kasutada ja miks peetakse neid jõudluse mõttes halvemaks?
- **K8.** *(punkt 5.3)* Mitu rida oli Caddyfile'is ja mitu rida vajaks sama nginx-is (koos sertifikaadi loomisega)? Kes oli sertifikaadi väljaandja? Mis juhtuks, kui nimi oleks avalik (nt `www.example.ee`) ja server internetis?
- **K9.** *(punkt 6.2)* Kuidas päringud serverite vahel jagunesid? Miks oli vaja saata päis `Host:`?
- **K10.** *(punkt 6.3)* Mida näitas statistikaleht? Mitu päringut ebaõnnestus pärast Apache'i peatamist ja kui kiiresti HAProxy rikke avastas (`option httpchk`, `check`)?
- **K11.** *(punkt 6.4)* Miks on logis HAProxy aadress, mitte kliendi oma? Kuidas saab taustserver teada kliendi tegeliku IP (vihje: `X-Forwarded-For`, HAProxy `option forwardfor`)?
- **K12.** *(punkt 7.2)* Kes väljastas `www.debian.org` sertifikaadi? Mitu sertifikaati oli ahelas ja mis on vahesertifikaadi roll? Mitu päeva sertifikaat kokku kehtib ja mitu on veel jäänud?
- **K13.** *(punkt 7.2)* Mida näitas crt.sh? Miks ei tasu sisevõrgu masinate nimedele (`proxmox1.lab.kool.ee`) avalikke sertifikaate küsida? Mis oleks lahendus, kui siiski on vaja avalikult usaldatud sertifikaati sisevõrgu serverile?
- **K14.** *(8. osa)* Täida tabel: nginx, Apache, Caddy, HAProxy - milleks kasutasid, seadistusfail, süntaksi kontrolli käsk, logide asukoht. Millise valiksid kooli uuele veebisaidile ja millise mõne konteineris töötava haldusliidese ette?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 15. Veebiserverid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 15. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
