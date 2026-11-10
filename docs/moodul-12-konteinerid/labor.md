<!-- navigatsioon -->
[← Moodul 12. Konteinerid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 12. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 12. Konteinerid

| | |
|---|---|
| **Distro** | AlmaLinux |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | AlmaLinuxi virtuaalmasin (soovitatavalt 2 GiB mälu), internetiühendus, laboritöö 6 Git-hoidla |
| **Eesmärk** | Käivitada ja hallata teenuseid konteinerites ning hoida nende kirjeldus Gitis |

**Aruanne:** vasta küsimustele **K1–K10**. Esita ka oma Git-hoidla (`git log --oneline --graph` väljund). Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

---

## 1. osa. Ettevalmistus

Too laboritöö 6 Git-hoidla AlmaLinuxi masinasse (klooni see Debianist SSH kaudu või GitHubist) või loo uus:

```bash
sudo dnf install -y git podman podman-compose
git clone kasutaja@DEBIAN_IP:hoidlad/infra.git ~/infra      # või: mkdir ~/infra && cd ~/infra && git init
```

---

## 2. osa. Podman

**2.1** Paigalda Podman ja käivita esimene konteiner:

```bash
sudo dnf install podman
podman --version
podman run --rm docker.io/library/alpine:latest cat /etc/os-release
cat /etc/os-release | head -2
uname -r
podman run --rm docker.io/library/alpine:latest uname -r
```

**K1.** Milline distro oli konteineri sees ja milline hostis? Mis oli kerneli versioon konteineris ja hostis? Mida see konteinerite kohta näitab?

**2.2** Uuri konteineri isolatsiooni:

```bash
podman run -it --rm docker.io/library/alpine:latest sh
```

Konteineri sees:

```sh
ps aux
hostname
ip addr 2>/dev/null || cat /proc/net/dev
id
ls /
exit
```

**K2.** Mitu protsessi nägid konteineris? Kes oli konteineri sees kasutaja? Võrdle hostis: `podman unshare id` ja `id`. Mis on juurkasutajata konteineri eelis?

**2.3** Käivita veebiserver taustal:

```bash
podman run -d --name veeb -p 8080:80 docker.io/library/nginx:alpine
podman ps
curl -s http://localhost:8080 | head -5
podman logs veeb
podman exec -it veeb sh -c 'nginx -v; cat /etc/os-release | head -1'
```

**2.4** Ava tulemüüris port ja proovi oma arvuti brauserist `http://ALMA_IP:8080`:

```bash
sudo firewall-cmd --add-port=8080/tcp
```

**2.5** Muuda konteineri sisu ja vaata, mis juhtub pärast konteineri kustutamist:

```bash
podman exec veeb sh -c 'echo "<h1>Muudetud</h1>" > /usr/share/nginx/html/index.html'
curl -s http://localhost:8080
podman rm -f veeb
podman run -d --name veeb -p 8080:80 docker.io/library/nginx:alpine
curl -s http://localhost:8080 | head -3
```

**K3.** Mis juhtus muudatusega pärast konteineri uuesti loomist? Miks? Kuidas hoida konteineri andmeid püsivalt?

**2.6** Haagi veebisisu hosti kataloogist:

```bash
podman rm -f veeb
mkdir -p ~/sait
echo "<h1>Sait hostist</h1>" > ~/sait/index.html
podman run -d --name veeb -p 8080:80 -v ~/sait:/usr/share/nginx/html:ro,Z docker.io/library/nginx:alpine
curl -s http://localhost:8080
echo "<p>Lisatud hostis</p>" >> ~/sait/index.html
curl -s http://localhost:8080
ls -Z ~/sait
```

**K4.** Kas hostis tehtud muudatus oli kohe konteineris nähtav? Mida tegid valikud `ro` ja `Z`? Mis juhtub ilma `Z`-ta (proovi)?


---

## 3. osa. Oma pilt

**3.1** Loo pildi jaoks kataloog, sait ja `Containerfile`:

```bash
mkdir -p ~/infra/konteinerid/kooli-sait/sait && cd ~/infra/konteinerid/kooli-sait
cat > sait/index.html <<'EOF'
<!doctype html>
<html lang="et"><head><meta charset="utf-8"><title>Kooli sait</title></head>
<body><h1>Haapsalu õppekool</h1><p>See sait töötab konteineris.</p></body></html>
EOF
cat > Containerfile <<'EOF'
FROM docker.io/library/nginx:1.27-alpine
LABEL maintainer="sinu@e-post.ee"
COPY sait/ /usr/share/nginx/html/
EXPOSE 80
EOF
```

**3.2** Ehita ja käivita:

```bash
podman build -t kooli-sait:1.0 .
podman images
podman rm -f veeb
podman run -d --name kooli-sait -p 8080:80 kooli-sait:1.0
curl -s http://localhost:8080
podman history kooli-sait:1.0 | head
```

**3.3** Muuda saiti, ehita versioon `1.1` ja vaheta töötav konteiner uue vastu. Lisa kõik Giti:

```bash
cd ~/infra
git add konteinerid
git commit -m "Lisa kooli saidi konteinerpilt"
```

**K5.** Mis on pildi suurus (`podman images`)? Mida näitab `podman history`? Miks on kasulik hoida `Containerfile` Gitis, aga mitte pilti ennast?


---

## 4. osa. Compose: andmebaas ja haldusliides

**4.1** Paigalda `podman-compose` (EPEL) ja loo rakendus:

```bash
sudo dnf install epel-release
sudo dnf install podman-compose
mkdir -p ~/infra/konteinerid/andmebaas && cd ~/infra/konteinerid/andmebaas
nano compose.yaml
```

Kasuta teooria punkti 12.4 faili (MariaDB + Adminer).

**4.2** Käivita ja kontrolli:

```bash
podman-compose up -d
podman-compose ps
podman-compose logs db | tail -5
podman volume ls
sudo firewall-cmd --add-port=8082/tcp
```

Ava brauseris `http://ALMA_IP:8082`. Logi Adminerisse sisse: süsteem *MySQL/MariaDB*, server `db`, kasutaja `kool`, parool `Kool-Parool-123`, andmebaas `kool`. Loo Adminerist tabel `opilased` ja lisa paar rida.

**K6.** Miks on Adminerisse sisselogimisel serveri nimi `db`, mitte `localhost`? Kas MariaDB port 3306 on hostis avatud (`ss -tlpn | grep 3306`)? Miks see hea on?

**4.3** Testi andmete püsivust:

```bash
podman-compose down
podman ps -a
podman volume ls
podman-compose up -d
```

Kontrolli Adminerist, kas tabel ja andmed on alles.

**K7.** Kas andmed jäid alles? Miks? Mis juhtuks käsuga `podman-compose down -v`?

**4.4** Ära lisa paroole avalikku Giti! Lisa Giti ainult näidisfail ilma päris paroolideta (nt `compose.example.yaml`) ja lisa `compose.yaml` faili `.gitignore`. Arutle aruandes, kuidas paroole paremini hallata (nt `.env` fail, Podmani saladused `podman secret`).


---

## 5. osa. Konteiner teenusena (Quadlet)

**5.1** Loo süsteemne veebisisu ja Quadlet-fail:

```bash
sudo mkdir -p /srv/veeb
echo "<h1>Quadlet töötab</h1>" | sudo tee /srv/veeb/index.html
sudo nano /etc/containers/systemd/veeb.container
```

Kasuta teooria punkti 12.5 faili, kuid port `8083:80`.

**5.2** Käivita teenus:

```bash
sudo systemctl daemon-reload
sudo systemctl start veeb
systemctl status veeb
sudo podman ps
curl -s http://localhost:8083
journalctl -u veeb -n 10
```

**5.3** Testi automaatset taaskäivitust ja alglaadimist:

```bash
sudo podman kill systemd-veeb
sleep 5
systemctl status veeb | head -5
sudo systemctl reboot
```

Pärast taaskäivitust: `curl -s http://localhost:8083`.

**K8.** Mille poolest erineb teenuse `veeb` haldamine tavalisest systemd teenusest? Kas konteiner käivitus pärast taaskäivitust? Miks ei näe `podman ps` (ilma `sudo`-ta) seda konteinerit?

Lisa Quadlet-fail oma Giti hoidlasse (`~/infra/konteinerid/quadlet/veeb.container`).


---

## 6. osa. Kokkuvõte

**K9.** Võrdle konteinerit ja virtuaalmasinat: millal kasutaksid kumba? Too näide kooli Proxmoxi laborist.

**K10.** Mida peaks hoidma Gitis (Containerfile, `compose.yaml`, Quadlet-failid, andmed, pildid, paroolid) ja mida mitte? Põhjenda.

---

## Koristamine

```bash
podman rm -f kooli-sait
cd ~/infra/konteinerid/andmebaas && podman-compose down
sudo systemctl stop veeb && sudo rm /etc/containers/systemd/veeb.container && sudo systemctl daemon-reload
podman system prune -a
```

---

## Lisaülesanne (valikuline)

1. **Kooli saidi pilt registrisse:** saada oma pilt GitHubi konteineriregistrisse (`ghcr.io`) ja käivita see Debiani masinas Podmaniga.
2. **Docker:** paigalda Ubuntu masinasse Docker (Dockeri ametlikust hoidlast) ja käivita sama `compose.yaml` käsuga `docker compose up -d`. Mis on erinev?
3. **Mailpit:** käivita konteinerina kirjapüüdja Mailpit (`axllent/mailpit`, veebiliides pordil 8025). Hiljem laboritöös 15 saad sinna suunata Postfixi kirjad (`relayhost = [127.0.0.1]:1025`).
4. **Automaatne uuendus:** lisa oma Quadleti konteinerile `AutoUpdate=registry`, käivita `podman auto-update --dry-run` ja luba `podman-auto-update.timer`. Millal taimer järgmisena käivitub (`systemctl list-timers`)? Miks on täpne pildisilt turvalisem kui `latest`?

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 2.1)* Milline distro oli konteineri sees ja milline hostis? Mis oli kerneli versioon konteineris ja hostis? Mida see konteinerite kohta näitab?
- **K2.** *(punkt 2.2)* Mitu protsessi nägid konteineris? Kes oli konteineri sees kasutaja? Võrdle hostis: `podman unshare id` ja `id`. Mis on juurkasutajata konteineri eelis?
- **K3.** *(punkt 2.5)* Mis juhtus muudatusega pärast konteineri uuesti loomist? Miks? Kuidas hoida konteineri andmeid püsivalt?
- **K4.** *(punkt 2.6)* Kas hostis tehtud muudatus oli kohe konteineris nähtav? Mida tegid valikud `ro` ja `Z`? Mis juhtub ilma `Z`-ta (proovi)?
- **K5.** *(punkt 3.3)* Mis on pildi suurus (`podman images`)? Mida näitab `podman history`? Miks on kasulik hoida `Containerfile` Gitis, aga mitte pilti ennast?
- **K6.** *(punkt 4.2)* Miks on Adminerisse sisselogimisel serveri nimi `db`, mitte `localhost`? Kas MariaDB port 3306 on hostis avatud (`ss -tlpn | grep 3306`)? Miks see hea on?
- **K7.** *(punkt 4.3)* Kas andmed jäid alles? Miks? Mis juhtuks käsuga `podman-compose down -v`?
- **K8.** *(punkt 5.3)* Mille poolest erineb teenuse `veeb` haldamine tavalisest systemd teenusest? Kas konteiner käivitus pärast taaskäivitust? Miks ei näe `podman ps` (ilma `sudo`-ta) seda konteinerit?
- **K9.** *(6. osa)* Võrdle konteinerit ja virtuaalmasinat: millal kasutaksid kumba? Too näide kooli Proxmoxi laborist.
- **K10.** *(6. osa)* Mida peaks hoidma Gitis (Containerfile, `compose.yaml`, Quadlet-failid, andmed, pildid, paroolid) ja mida mitte? Põhjenda.
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 12. Konteinerid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 12. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
