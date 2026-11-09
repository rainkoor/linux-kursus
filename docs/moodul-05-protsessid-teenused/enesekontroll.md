# Moodul 5. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis on protsess, PID ja PPID?
2. Milline protsess on PID 1 ja mis on selle roll?
3. Mida tähendavad protsessi olekud `R`, `S`, `T` ja `Z`?
4. Mida näitab koormus (*load average*)? Millal on see murettekitav?
5. Mis vahe on signaalidel `SIGTERM` ja `SIGKILL`? Kumba peaks kasutama esimesena ja miks?
6. Kuidas saata juba töötav käsk taustale?
7. Miks lõpevad kesta taustatööd väljalogimisel? Kuidas seda vältida?
8. Mida tähendab nice-väärtus 19? Kes saab nice-väärtust vähendada?
9. Mis vahe on käskudel `systemctl start` ja `systemctl enable`?
10. Mis vahe on käskudel `systemctl restart` ja `systemctl reload`?
11. Miks ei tohi muuta faile kataloogis `/usr/lib/systemd/system/`? Kuidas teenuse seadistust õigesti muuta?
12. Millal on vaja käivitada `systemctl daemon-reload`?
13. Kuidas näha teenuse `nginx` viimase tunni logisid?
14. Selgita crontab'i rida `15 3 * * 1 /usr/local/bin/puhastus.sh`.
15. Nimeta kaks systemd taimeri eelist cron'i ees.
16. Mis vahe on cron-il, systemd taimeril ja `at`-il?
17. Miks ei mõju `/etc/security/limits.conf` systemd teenustele ja kuidas teenuse ressursse piirata?

## Praktilised miniülesanded

1. Leia kolm kõige rohkem protsessorit kasutavat protsessi.
2. Leia, mitu protsessi töötab juurkasutaja õigustes.
3. Käivita `sleep 500` taustal madalaima prioriteediga ja kontrolli selle nice-väärtust.
4. Leia kõik teenused, mis on lubatud automaatselt käivituma.
5. Kuva praeguse alglaadimise hoiatused ja vead.
6. Loo crontab'i kirje, mis kustutab iga päev kell 04:00 kataloogist `~/tmp` failid, mis on vanemad kui 7 päeva.

---

## Vastused

1. **Protsess** on töötav programm. **PID** on protsessi unikaalne number. **PPID** on vanemprotsessi (selle protsessi käivitanud protsessi) PID.
2. **systemd** - esimene protsess, mille kernel käivitab. See käivitab ja haldab kõiki teenuseid ning on kõigi protsesside puu juur.
3. `R` - töötab või ootab protsessorit, `S` - magab ja ootab sündmust, `T` - peatatud, `Z` - zombie: on lõpetanud, kuid vanem pole veel tulemust kätte saanud.
4. Viimase 1, 5 ja 15 minuti keskmine protsesside arv, mis töötavad või ootavad protsessorit (või ketast). Murettekitav on, kui see on püsivalt suurem kui protsessorituumade arv.
5. `SIGTERM` palub protsessil lõpetada ja laseb tal korrektselt koristada (salvestada andmed, sulgeda failid). `SIGKILL` lõpetab protsessi kohe ja seda ei saa ignoreerida. Esimesena tuleks kasutada `SIGTERM`-i, `SIGKILL`-i alles siis, kui protsess ei reageeri.
6. Vajuta **Ctrl+Z** (peatab) ja kirjuta `bg` (jätkab taustal).
7. Väljalogimisel saavad kesta tööd signaali `SIGHUP`. Vältimiseks: `nohup`, `tmux`/`screen` või püsiva programmi puhul systemd teenus.
8. Madalaim prioriteet - protsess annab protsessori meelsasti teistele. Nice-väärtust vähendada (prioriteeti tõsta) saab ainult juurkasutaja.
9. `start` käivitab teenuse kohe. `enable` määrab, et teenus käivitub automaatselt alglaadimisel. Kumbki ei tee teise tööd; mõlema jaoks korraga on `enable --now`.
10. `restart` peatab teenuse ja käivitab uuesti (lühike katkestus). `reload` palub teenusel seadistus uuesti lugeda ilma peatumata (kui teenus seda toetab).
11. Paketi uuendus kirjutab need failid üle ja muudatus kaob. Õige viis: `systemctl edit teenus` (loob muudatusfaili kataloogis `/etc/systemd/system/teenus.service.d/`) või koopia kataloogis `/etc/systemd/system/`.
12. Pärast üksuse failide käsitsi loomist või muutmist (`systemctl edit` teeb selle ise).
13. `journalctl -u nginx --since "1 hour ago"`
14. Iga esmaspäeva kell 03:15 käivitatakse skript `/usr/local/bin/puhastus.sh`.
15. Näiteks: logid on automaatselt journal'is; `Persistent=true` käivitab vahelejäänud töö; olekut ja järgmist käivitust näeb käsuga `systemctl list-timers`; töö saab käivitada käsitsi `systemctl start`-iga.
16. cron ja taimer käivitavad tööd korduvalt kindla ajakava järgi; `at` käivitab töö ühe korra määratud ajal.
17. `limits.conf`-i rakendab `pam_limits` kasutaja sisselogimisel; teenused käivitab systemd ilma PAM-ita. Teenustele: üksuse seaded `MemoryMax=`, `CPUQuota=`, `TasksMax=`, `LimitNOFILE=` (`systemctl edit` või `set-property`).

### Miniülesannete lahendused

```bash
ps -eo pid,%cpu,cmd --sort=-%cpu | head -4
ps -U root -u root --no-headers | wc -l
nice -n 19 sleep 500 &
ps -o pid,ni,cmd -C sleep
systemctl list-unit-files --type=service --state=enabled
journalctl -b -p warning
```

Crontab'i kirje (`crontab -e`):

```text
0 4 * * * /usr/bin/find /home/KASUTAJA/tmp -type f -mtime +7 -delete
```
