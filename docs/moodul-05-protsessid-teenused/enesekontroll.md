<!-- navigatsioon -->
[← Laboritöö 5. Protsessid, teenused ja ajastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 6. Bashi skriptimine ja Git →](../moodul-06-bash/index.md)
<!-- /navigatsioon -->

# Moodul 5. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on protsess, PID ja PPID?

<details>
<summary>Vastus</summary>

**Protsess** on töötav programm. **PID** on protsessi unikaalne number. **PPID** on vanemprotsessi (selle protsessi käivitanud protsessi) PID.

</details>

**2.** Milline protsess on PID 1 ja mis on selle roll?

<details>
<summary>Vastus</summary>

**systemd** - esimene protsess, mille kernel käivitab. See käivitab ja haldab kõiki teenuseid ning on kõigi protsesside puu juur.

</details>

**3.** Mida tähendavad protsessi olekud `R`, `S`, `T` ja `Z`?

<details>
<summary>Vastus</summary>

`R` - töötab või ootab protsessorit, `S` - magab ja ootab sündmust, `T` - peatatud, `Z` - zombie: on lõpetanud, kuid vanem pole veel tulemust kätte saanud.

</details>

**4.** Mida näitab koormus (*load average*)? Millal on see murettekitav?

<details>
<summary>Vastus</summary>

Viimase 1, 5 ja 15 minuti keskmine protsesside arv, mis töötavad või ootavad protsessorit (või ketast). Murettekitav on, kui see on püsivalt suurem kui protsessorituumade arv.

</details>

**5.** Mis vahe on signaalidel `SIGTERM` ja `SIGKILL`? Kumba peaks kasutama esimesena ja miks?

<details>
<summary>Vastus</summary>

`SIGTERM` palub protsessil lõpetada ja laseb tal korrektselt koristada (salvestada andmed, sulgeda failid). `SIGKILL` lõpetab protsessi kohe ja seda ei saa ignoreerida. Esimesena tuleks kasutada `SIGTERM`-i, `SIGKILL`-i alles siis, kui protsess ei reageeri.

</details>

**6.** Kuidas saata juba töötav käsk taustale?

<details>
<summary>Vastus</summary>

Vajuta **Ctrl+Z** (peatab) ja kirjuta `bg` (jätkab taustal).

</details>

**7.** Miks lõpevad kesta taustatööd väljalogimisel? Kuidas seda vältida?

<details>
<summary>Vastus</summary>

Väljalogimisel saavad kesta tööd signaali `SIGHUP`. Vältimiseks: `nohup`, `tmux`/`screen` või püsiva programmi puhul systemd teenus.

</details>

**8.** Mida tähendab nice-väärtus 19? Kes saab nice-väärtust vähendada?

<details>
<summary>Vastus</summary>

Madalaim prioriteet - protsess annab protsessori meelsasti teistele. Nice-väärtust vähendada (prioriteeti tõsta) saab ainult juurkasutaja.

</details>

**9.** Mis vahe on käskudel `systemctl start` ja `systemctl enable`?

<details>
<summary>Vastus</summary>

`start` käivitab teenuse kohe. `enable` määrab, et teenus käivitub automaatselt alglaadimisel. Kumbki ei tee teise tööd; mõlema jaoks korraga on `enable --now`.

</details>

**10.** Mis vahe on käskudel `systemctl restart` ja `systemctl reload`?

<details>
<summary>Vastus</summary>

`restart` peatab teenuse ja käivitab uuesti (lühike katkestus). `reload` palub teenusel seadistus uuesti lugeda ilma peatumata (kui teenus seda toetab).

</details>

**11.** Miks ei tohi muuta faile kataloogis `/usr/lib/systemd/system/`? Kuidas teenuse seadistust õigesti muuta?

<details>
<summary>Vastus</summary>

Paketi uuendus kirjutab need failid üle ja muudatus kaob. Õige viis: `systemctl edit teenus` (loob muudatusfaili kataloogis `/etc/systemd/system/teenus.service.d/`) või koopia kataloogis `/etc/systemd/system/`.

</details>

**12.** Millal on vaja käivitada `systemctl daemon-reload`?

<details>
<summary>Vastus</summary>

Pärast üksuse failide käsitsi loomist või muutmist (`systemctl edit` teeb selle ise).

</details>

**13.** Kuidas näha teenuse `nginx` viimase tunni logisid?

<details>
<summary>Vastus</summary>

`journalctl -u nginx --since "1 hour ago"`

</details>

**14.** Selgita crontab'i rida `15 3 * * 1 /usr/local/bin/puhastus.sh`.

<details>
<summary>Vastus</summary>

Iga esmaspäeva kell 03:15 käivitatakse skript `/usr/local/bin/puhastus.sh`.

</details>

**15.** Nimeta kaks systemd taimeri eelist cron'i ees.

<details>
<summary>Vastus</summary>

Näiteks: logid on automaatselt journal'is; `Persistent=true` käivitab vahelejäänud töö; olekut ja järgmist käivitust näeb käsuga `systemctl list-timers`; töö saab käivitada käsitsi `systemctl start`-iga.

</details>

**16.** Mis vahe on cron-il, systemd taimeril ja `at`-il?

<details>
<summary>Vastus</summary>

cron ja taimer käivitavad tööd korduvalt kindla ajakava järgi; `at` käivitab töö ühe korra määratud ajal.

</details>

**17.** Miks ei mõju `/etc/security/limits.conf` systemd teenustele ja kuidas teenuse ressursse piirata?

<details>
<summary>Vastus</summary>

`limits.conf`-i rakendab `pam_limits` kasutaja sisselogimisel; teenused käivitab systemd ilma PAM-ita. Teenustele: üksuse seaded `MemoryMax=`, `CPUQuota=`, `TasksMax=`, `LimitNOFILE=` (`systemctl edit` või `set-property`).

</details>

## Praktilised miniülesanded

**1.** Leia kolm kõige rohkem protsessorit kasutavat protsessi.

<details>
<summary>Lahendus</summary>

```bash
ps -eo pid,%cpu,cmd --sort=-%cpu | head -4
```

</details>

**2.** Leia, mitu protsessi töötab juurkasutaja õigustes.

<details>
<summary>Lahendus</summary>

```bash
ps -U root -u root --no-headers | wc -l
```

</details>

**3.** Käivita `sleep 500` taustal madalaima prioriteediga ja kontrolli selle nice-väärtust.

<details>
<summary>Lahendus</summary>

```bash
nice -n 19 sleep 500 &
ps -o pid,ni,cmd -C sleep
```

</details>

**4.** Leia kõik teenused, mis on lubatud automaatselt käivituma.

<details>
<summary>Lahendus</summary>

```bash
systemctl list-unit-files --type=service --state=enabled
```

</details>

**5.** Kuva praeguse alglaadimise hoiatused ja vead.

<details>
<summary>Lahendus</summary>

```bash
journalctl -b -p warning
```

</details>

**6.** Loo crontab'i kirje, mis kustutab iga päev kell 04:00 kataloogist `~/tmp` failid, mis on vanemad kui 7 päeva.

<details>
<summary>Lahendus</summary>

Crontab'i kirje (`crontab -e`):

```text
0 4 * * * /usr/bin/find /home/KASUTAJA/tmp -type f -mtime +7 -delete
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 5. Protsessid, teenused ja ajastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 6. Bashi skriptimine ja Git →](../moodul-06-bash/index.md)
<!-- /navigatsioon -->
