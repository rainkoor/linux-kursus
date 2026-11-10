<!-- navigatsioon -->
[← Laboritöö 9. Varundus ja taastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Proovieksam: põhiosa →](../proovieksam-pohiosa.md)
<!-- /navigatsioon -->

# Moodul 9. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Selgita varunduse 3-2-1 reeglit. Miks on oluline taastamist testida?

<details>
<summary>Vastus</summary>

Kolm koopiat, kahel eri andmekandjal, üks mujal. Taastamist tuleb testida, sest alles siis on näha, kas varukoopia on täielik, loetav ja kas taastamise sammud on teada.

</details>

**2.** Mis on RPO ja RTO? Kooli e-õppekeskkonda varundatakse igal ööl kell 02.00 ja taastamine võtab 3 tundi. Milline on halvimal juhul andmekadu ja kas see sobib, kui RTO on 2 tundi?

<details>
<summary>Vastus</summary>

RPO - lubatud andmekadu ajas; RTO - lubatud taastumisaeg. Rike vahetult enne järgmist varundust tähendab kuni ~24 h andmekadu. 3-tunnine taastamine ei mahu 2-tunnise RTO sisse - vaja on kiiremat taastamist (nt valmis VM-i varukoopia, varuserver) või tuleb RTO-s kokku leppida uuesti.

</details>

**3.** Nimeta kolm ohtu, mille eest RAID ei kaitse. Miks ei ole hetktõmmis ega `rsync --delete` peegel varukoopia?

<details>
<summary>Vastus</summary>

Inimviga (kustutamine), lunavara, tarkvaraviga, tulekahju/vargus. Hetktõmmis asub samas masinas ja kaob koos sellega; peegel kopeerib ka kustutamised ja krüpteeritud failid teise kohta.

</details>

**4.** Mis vahe on täis-, juurdekasvu- ja diferentsiaalvarundusel? Mida on vaja taastamiseks?

<details>
<summary>Vastus</summary>

Täis: kõik, taastamiseks üks koopia. Juurdekasv: muutused eelmisest varundusest, taastamiseks täisvarundus ja kõik järgnevad juurdekasvud. Diferentsiaal: muutused viimasest täisvarundusest, taastamiseks täisvarundus ja viimane diferentsiaal.

</details>

**5.** Mida tähendab deduplitseerimine ja miks on see varunduses kasulik?

<details>
<summary>Vastus</summary>

Andmed jagatakse tükkideks ja iga tükk salvestatakse ainult üks kord. Iga varundus salvestab ainult uued tükid (kiire ja väike nagu juurdekasv), kuid igast hetktõmmisest saab taastada nagu täisvarundusest.

</details>

**6.** Mis on GFS-säilitamine? Too näide.

<details>
<summary>Vastus</summary>

*Grandfather-father-son*: hoitakse alles nt 7 päevast, 4 nädalast ja 12 kuust koopiat. Nii saab taastada nii eilse kui ka mitme kuu taguse seisu ilma kõiki koopiaid alles hoidmata (restic: `forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12`).

</details>

**7.** Miks taastatakse varukoopia kõigepealt ajutisse kataloogi? Milliseid `tar`-i ja `rsync`-i valikuid on vaja, et õigused ja ACL-id säiliksid?

<details>
<summary>Vastus</summary>

Et kontrollida koopia sisu ja mitte kirjutada kogemata üle päris andmeid (nt uuemaid faile). `tar --acls --xattrs -p` ning `rsync -aAX`.

</details>

**8.** Kuidas töötab `rsync --link-dest` ja miks võtab iga päeva koopia vähe ruumi?

<details>
<summary>Vastus</summary>

Muutmata failid luuakse uude kataloogi kõvaviidetena eelmise päeva koopia failidele (sama i-sõlm), seega kopeeritakse ja salvestatakse ainult muutunud failid. Iga päeva kataloog näeb välja nagu täiskoopia.

</details>

**9.** Mida teevad systemd taimeris `Persistent=true` ja teenuses `OnFailure=`? Miks on need varunduses olulised?

<details>
<summary>Vastus</summary>

`Persistent=true` käivitab vahele jäänud töö kohe pärast masina käivitamist (masin oli ajastatud ajal väljas). `OnFailure=` käivitab vea korral teise üksuse, mis teatab veast - muidu võib varundus kuid vaikselt ebaõnnestuda.

</details>

**10.** Mida teeb restic'u `forget --prune` ja `check`?

<details>
<summary>Vastus</summary>

`forget` märgib säilitusreeglitest välja jäävad hetktõmmised kustutamiseks ja `--prune` vabastab nende andmetükkide ruumi. `check` kontrollib hoidla terviklikkust (`--read-data-subset` loeb osa andmetest läbi).

</details>

**11.** Kuidas kaitsta varukoopiaid lunavara eest?

<details>
<summary>Vastus</summary>

Vähemalt üks koopia peab olema muudetamatu või võrgust eraldatud: varundusserver tõmbab andmed ise (*pull*), *append-only* hoidla, S3 *Object Lock*, lahtiühendatud ketas; varundusserveri paroolid ja võtmed ei tohi olla varundatavas masinas kättesaadavad kustutamiseks.

</details>

**12.** Mis on taastamistest ja kui tihti seda tehakse?

<details>
<summary>Vastus</summary>

Päris taastamine testkeskkonda või ajutisse kataloogi koos aja mõõtmise ja tulemuse kontrolliga. Regulaarselt (nt kord kvartalis) ja pärast varunduse muutmist; tulemus ja kulunud aeg kirjutatakse dokumentatsiooni.

</details>

## Praktilised miniülesanded

**1.** Varunda `/etc` koos ACL-ide ja SELinuxi märgistega arhiivi, mille nimes on kuupäev, ning taasta sellest ainult fail `/etc/hosts` kataloogi `/tmp/t`.

<details>
<summary>Lahendus</summary>

```bash
sudo tar --acls --xattrs -czpf /varu/etc-$(date +%F).tar.gz /etc
sudo mkdir -p /tmp/t
sudo tar -xzpf /varu/etc-$(date +%F).tar.gz -C /tmp/t etc/hosts
```

</details>

**2.** Kirjuta systemd taimer, mis käivitab teenuse `varundus.service` iga päev kell 01:15 ja ka siis, kui masin oli sel ajal väljas.

<details>
<summary>Lahendus</summary>

```ini
[Timer]
OnCalendar=*-*-* 01:15:00
Persistent=true

[Install]
WantedBy=timers.target
```

Seejärel `sudo systemctl daemon-reload` ja `sudo systemctl enable --now varundus.timer`.

</details>

**3.** Kustuta kataloogist `/varu` üle 30 päeva vanad failid nimega `*.tar.gz` (kontrolli enne, mida kustutataks).

<details>
<summary>Lahendus</summary>

```bash
find /varu -name '*.tar.gz' -mtime +30 -print     # kontroll
find /varu -name '*.tar.gz' -mtime +30 -delete
```

</details>

**4.** Kuva restic'u hoidlast kõik hetktõmmised ja taasta eelviimasest failid kataloogist `/etc/nginx`.

<details>
<summary>Lahendus</summary>

```bash
# 3
sudo -E restic snapshots
sudo -E restic restore <eelviimase ID> --target /tmp/taaste --include /etc/nginx
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 9. Varundus ja taastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Proovieksam: põhiosa →](../proovieksam-pohiosa.md)
<!-- /navigatsioon -->
