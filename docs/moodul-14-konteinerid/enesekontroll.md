<!-- navigatsioon -->
[← Laboritöö 14. Konteinerid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 15. Veebiserverid →](../moodul-15-veebiserverid/index.md)
<!-- /navigatsioon -->

# Moodul 14. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis vahe on konteineril ja virtuaalmasinal?

<details>
<summary>Vastus</summary>

Virtuaalmasinal on oma kernel ja terve operatsioonisüsteem (tugevam isolatsioon, rohkem ressursse). Konteiner jagab hosti kernelit ja sisaldab ainult rakendust koos sõltuvustega (kerge, kiire).

</details>

**2.** Millistel Linuxi kerneli võimalustel konteinerid põhinevad?

<details>
<summary>Vastus</summary>

Nimeruumid (isoleerivad protsessid, võrgu, haakepunktid, kasutajad) ja cgroups (piiravad ressursse); lisaks SELinux/AppArmor ja seccomp.

</details>

**3.** Mis vahe on pildil ja konteineril?

<details>
<summary>Vastus</summary>

Pilt on muutumatu mall (rakendus koos failisüsteemiga). Konteiner on pildist käivitatud töötav eksemplar, millel on oma kirjutatav kiht.

</details>

**4.** Miks ei tohiks tootmises kasutada pildisilti `latest`?

<details>
<summary>Vastus</summary>

`latest` võib iga kord tähendada uut versiooni, mis võib käitumist ootamatult muuta. Konkreetne versioon tagab korratavuse.

</details>

**5.** Mis vahe on Podmanil ja Dockeril? Mis on juurkasutajata konteinerite eelis?

<details>
<summary>Vastus</summary>

Podman töötab ilma taustateenuseta ja vaikimisi juurkasutaja õigusteta. Docker kasutab juurkasutajana töötavat teenust `dockerd`. Juurkasutajata konteinerist välja murdnud ründajal on ainult tavakasutaja õigused.

</details>

**6.** Miks kaovad konteineri sisse kirjutatud andmed? Kuidas andmeid püsivalt hoida?

<details>
<summary>Vastus</summary>

Konteineri kirjutatav kiht kustutatakse koos konteineriga. Püsivad andmed hoitakse köidetes (`-v nimi:/tee`) või hosti kataloogides.

</details>

**7.** Mida teeb AlmaLinuxis köite valik `:Z`?

<details>
<summary>Vastus</summary>

Märgistab hosti kataloogi SELinuxi tüübiga, mida konteiner tohib kasutada (ainult selle konteineri jaoks; `:z` - jagatud mitme konteineri vahel).

</details>

**8.** Milleks on Compose? Kuidas leiavad Compose'i konteinerid üksteist?

<details>
<summary>Vastus</summary>

Mitme konteineri rakenduse kirjeldamine ja käivitamine ühe failiga. Konteinerid leiavad üksteist teenuse nime järgi (nt `db`).

</details>

**9.** Mis on Quadlet ja miks seda kasutada?

<details>
<summary>Vastus</summary>

Podmani võimalus kirjeldada konteiner systemd üksusena (`.container` fail). Nii käivitub konteiner alglaadimisel, taaskäivitub vea korral ja on hallatav `systemctl`/`journalctl` abil.

</details>

**10.** Kuidas uuendab Podman Quadleti konteinereid automaatselt ja mis juhtub, kui uus pilt ei käivitu?

<details>
<summary>Vastus</summary>

Quadleti failis `AutoUpdate=registry` (täieliku pildinimega); `podman auto-update` (või taimer `podman-auto-update.timer`) laadib sama sildiga uuema pildi ja taaskäivitab teenuse. Kui teenus uue pildiga ei käivitu, võetakse muudatus tagasi ja kasutatakse vana pilti.

</details>

**11.** Mis on `chroot` ja miks ei ole see konteineri samaväärne asendus?

<details>
<summary>Vastus</summary>

`chroot` käivitab protsessi nii, et valitud kataloog paistab talle juurkataloogina. See eraldab ainult failisüsteemi: protsessid, võrk ja kasutajad on hostiga ühised, ressursse ei piirata ja juurkasutaja saab sealt välja murda. Konteiner lisab nimeruumid, cgroupid ja turvapiirangud.

</details>

**12.** Miks ei saa juurkasutajata Podmani konteiner kuulata porti 80 ja kuidas seda lahendada? Mida teeb `loginctl enable-linger`?

<details>
<summary>Vastus</summary>

Tavakasutaja ei tohi avada porte alla 1024. Kasuta kõrget porti (`-p 8080:80`) ja vajadusel pöördpuhvrit või tulemüüri suunamist pordilt 80; teine võimalus on konteiner juurkasutajana. `loginctl enable-linger kasutaja` laseb kasutaja teenustel (ka konteineritel) töötada ilma sisse logimata ja käivituda alglaadimisel.

</details>

**13.** Mis vahe on köitel (`-v nimi:/tee`) ja hosti kataloogi sidumisel (`-v /srv/veeb:/tee`)? Millal kasutad kumba?

<details>
<summary>Vastus</summary>

Köidet haldab Podman (`podman volume`), selle asukoht ja õigused on konteineri jaoks õiged; sobib andmebaasi andmetele. Hosti kataloog on tavaline kataloog, mida saab hostis otse muuta ja varundada; sobib nt veebisaidi failidele ja seadistusele (AlmaLinuxis vajab `:Z`/`:z`).

</details>

**14.** Mis vahe on `-p 8080:80` ja `-p 127.0.0.1:8080:80` vahel? Miks on andmebaasi konteineri puhul teine turvalisem?

<details>
<summary>Vastus</summary>

Esimene avaldab pordi kõigil hosti aadressidel (võrgust kättesaadav), teine ainult hostist endast. Andmebaasi ei pea võrku avama, kui rakendus töötab samas masinas või samas Compose'i võrgus.

</details>

**15.** Konteiner käivitub ja kustub kohe. Milliste käskudega leiad põhjuse?

<details>
<summary>Vastus</summary>

`podman ps -a` (olek ja väljumiskood), `podman logs <nimi>` (rakenduse veateade), `podman inspect <nimi>` (seaded, nt keskkonnamuutujad, köited); Quadleti puhul `systemctl status` ja `journalctl -u`. Sageli puudub kohustuslik keskkonnamuutuja (nt andmebaasi parool) või on köite õigused valed.

</details>

## Praktilised miniülesanded

**1.** Käivita PostgreSQL-i konteiner nimega `pg`, mis kasutab köidet `pgandmed` ja on kättesaadav ainult hostist (`127.0.0.1`) pordil 5432.

<details>
<summary>Lahendus</summary>

```bash
podman run -d --name pg -e POSTGRES_PASSWORD=Salajane-123 \
    -v pgandmed:/var/lib/postgresql/data -p 127.0.0.1:5432:5432 \
    docker.io/library/postgres:17
```

</details>

**2.** Kirjuta `Containerfile`, mis põhineb pildil `docker.io/library/python:3.12-slim`, kopeerib faili `rakendus.py` kataloogi `/app` ja käivitab selle.

<details>
<summary>Lahendus</summary>

```dockerfile
FROM docker.io/library/python:3.12-slim
WORKDIR /app
COPY rakendus.py .
CMD ["python", "rakendus.py"]
```

</details>

**3.** Kirjuta `compose.yaml`, mis käivitab nginx-i (pordil 8080) ja Valkey (`docker.io/valkey/valkey:8`, ainult sisevõrgus, andmed köites `valkeyandmed`).

<details>
<summary>Lahendus</summary>

```yaml
services:
  veeb:
    image: docker.io/library/nginx:1.27-alpine
    ports:
      - "8080:80"
    restart: unless-stopped
  valkey:
    image: docker.io/valkey/valkey:8
    volumes:
      - valkeyandmed:/data
    restart: unless-stopped

volumes:
  valkeyandmed:
```

Valkey'le pole `ports:` kirjet, seega on see kättesaadav ainult Compose'i võrgus nime `valkey` järgi.

</details>

**4.** Kirjuta Quadleti fail, mis käivitab süsteemi käivitumisel konteineri `docker.io/traefik/whoami` hosti pordil 8090 ja taaskäivitab selle rikke korral.

<details>
<summary>Lahendus</summary>

```ini
# /etc/containers/systemd/whoami.container
[Unit]
Description=whoami testteenus

[Container]
Image=docker.io/traefik/whoami
PublishPort=8090:80

[Service]
Restart=always

[Install]
WantedBy=multi-user.target
```

Seejärel `sudo systemctl daemon-reload && sudo systemctl start whoami`.

</details>

<!-- navigatsioon -->
---

[← Laboritöö 14. Konteinerid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 15. Veebiserverid →](../moodul-15-veebiserverid/index.md)
<!-- /navigatsioon -->
