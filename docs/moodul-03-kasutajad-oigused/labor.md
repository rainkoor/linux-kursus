# Laboritöö 3. Kasutajad, grupid ja jagatud kataloogid

| | |
|---|---|
| **Distro** | Ubuntu Server (LTS) |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Ubuntu virtuaalmasin, ligipääs SSH kaudu kasutajana, kellel on `sudo` õigus |
| **Eesmärk** | Harjutada kasutajate ja gruppide haldust, õigusi, jagatud katalooge ja `sudo` reegleid |

**Aruanne:** vasta küsimustele **K1–K20**. Kus küsitakse käsku, kirjuta üles kogu käsk.

**Stsenaarium:** väike IT-ettevõte Näidis OÜ võtab kasutusele uue failiserveri. Sinu ülesanne on luua töötajatele kontod ja seadistada osakondadele kataloogid nii, et igaüks pääseb ligi ainult sellele, mida tal on vaja.

| Töötaja | Kasutajanimi | Osakond | Erinõuded |
|---|---|---|---|
| Mari Maasikas | `mari` | Tarkvara | - |
| Jaan Tamm | `jaan` | Tarkvara | - |
| Kati Kask | `kati` | Turundus | - |
| Toomas Tugi | `toomas` | IT-tugi | Võib uuendada süsteemi, kuid muud halduriõigused puuduvad |

> **Testimine:** selles laboris kontrollid õigusi teiste kasutajate nimel käsuga `sudo -iu kasutaja käsk`, mis käivitab käsu selle kasutaja sisselogimiskeskkonnas. Nii ei pea iga kasutajaga eraldi SSH kaudu sisse logima.

---

## 1. osa. Tutvumine

**1.1** Uuri oma kasutajat:

```bash
whoami
id
groups
```

**K1.** Mis on sinu UID ja millistesse gruppidesse kuulud? Milline grupp annab sulle `sudo` õiguse?

**1.2** Uuri süsteemi kasutajaid:

```bash
cut -d: -f1,3,7 /etc/passwd
```

**K2.** Nimeta kaks süsteemikasutajat (UID alla 1000). Milline on nende sisselogimiskest ja mida see tähendab?

**1.3** Proovi lugeda faili `/etc/shadow` tavakasutajana ja seejärel `sudo`-ga:

```bash
cat /etc/shadow
sudo head -3 /etc/shadow
ls -l /etc/passwd /etc/shadow
```

**K3.** Miks tavakasutaja faili `/etc/shadow` lugeda ei saa? Võrdle mõlema faili õigusi.

**1.4** Kontrolli, kas juurkasutajal on parool:

```bash
sudo passwd -S root
```

**K4.** Mida tähendab väljundis täht `L`? Kuidas Ubuntus halduriõigusi kasutatakse, kui juurkasutaja konto on lukus?

---

## 2. osa. Gruppide ja kasutajate loomine

**2.1** Loo grupid `tarkvara` ja `turundus`.

**2.2** Loo kasutajad `mari`, `jaan` ja `kati` käsuga `useradd` nii, et:

- luuakse kodukataloog;
- sisselogimiskest on `/bin/bash`;
- kirjeldusse kirjutatakse töötaja täisnimi;
- kasutaja lisatakse kohe oma osakonna gruppi.

Näide esimese kasutaja kohta:

```bash
sudo useradd -m -s /bin/bash -c "Mari Maasikas" -G tarkvara mari
```

**K5.** Kirjuta käsud kasutajate `jaan` ja `kati` loomiseks.

**2.3** Määra kõigile kolmele parool:

```bash
sudo passwd mari
```

**2.4** Sunni kõiki kolme kasutajat esimesel sisselogimisel parooli vahetama ja kontrolli tulemust:

```bash
sudo chage -d 0 mari
sudo chage -l mari
```

**2.5** Loo kasutaja `toomas` interaktiivse käsuga `adduser`.

**K6.** Mis vahe on käskudel `useradd` ja `adduser`? Millist neist kasutaksid skriptis ja miks?

**2.6** Kontrolli tulemust:

```bash
id mari
id kati
getent group tarkvara
tail -4 /etc/passwd
ls -l /home
```

**K7.** Mis on kasutaja `mari` põhigrupp ja millised on tema lisagrupid? Millised on kodukataloogide õigused?

---

## 3. osa. Õigused kodukataloogis

**3.1** Proovi, kas `kati` näeb kasutaja `mari` kodukataloogi sisu:

```bash
sudo -iu kati ls /home/mari
```

**K8.** Kas see õnnestus? Selgita tulemust kataloogi `/home/mari` õiguste põhjal.

**3.2** Kasutajana `mari` loo fail ja uuri selle õigusi ning oma umaski:

```bash
sudo -iu mari bash -c 'echo "Salajane plaan" > plaan.txt; ls -l plaan.txt; umask'
```

**K9.** Millised õigused said uus fail ja mis on umask? Arvuta, kuidas umaskist need õigused tulid.

**3.3** Muuda kasutajana `mari` faili `plaan.txt` õigusi nii, et ainult tema saab seda lugeda ja muuta. Tee seda kõigepealt sümbolilisel ja seejärel numbrilisel kujul.

**K10.** Kirjuta mõlemad käsud.

---

## 4. osa. Osakondade kataloogid

Loo järgmine struktuur:

```text
/srv/firma/
├── tarkvara/     # ainult grupp tarkvara, kõik liikmed saavad kõike muuta
├── turundus/     # ainult grupp turundus, kõik liikmed saavad kõike muuta
├── ühine/        # kõik töötajad saavad faile luua, kuid kustutada ainult oma faile
└── teated/       # kõik saavad lugeda, muuta saab ainult toomas
```

**4.1** Loo kataloogid:

```bash
sudo mkdir -p /srv/firma/{tarkvara,turundus,ühine,teated}
```

**4.2** Seadista kataloog `tarkvara`:

```bash
sudo chown root:tarkvara /srv/firma/tarkvara
sudo chmod 2770 /srv/firma/tarkvara
```

**K11.** Selgita kõiki nelja numbrit väärtuses `2770`.

**4.3** Seadista samamoodi kataloog `turundus`.

**4.4** Seadista kataloog `ühine` nii, et kõik saavad sinna kirjutada, kuid teiste faile kustutada ei saa.

**K12.** Kirjuta käsk. Millise süsteemikataloogiga on see seadistus sama?

**4.5** Seadista kataloog `teated`: omanik `toomas`, kõik saavad lugeda ja kataloogi siseneda, kuid ainult `toomas` saab sinna faile luua.

**K13.** Kirjuta käsud. Millised õigused numbrilisel kujul kataloogile andsid?

**4.6** Kontrolli kõike korraga:

```bash
ls -l /srv/firma
```

**K14.** Kopeeri väljund aruandesse ja selgita, miks on kataloogi `tarkvara` grupi õigustes `s` ja kataloogi `ühine` muude õigustes `t`.

---

## 5. osa. Õiguste testimine

Iga testi puhul **ennusta enne käivitamist**, kas see õnnestub, ja kirjuta ennustus ning tegelik tulemus aruandesse.

| Nr | Test | Käsk |
|---|---|---|
| T1 | `mari` loob faili tarkvara kataloogi | `sudo -iu mari touch /srv/firma/tarkvara/kood.py` |
| T2 | `jaan` muudab mari faili | `sudo -iu jaan bash -c 'echo "print(1)" >> /srv/firma/tarkvara/kood.py'` |
| T3 | `kati` vaatab tarkvara kataloogi | `sudo -iu kati ls /srv/firma/tarkvara` |
| T4 | `mari` loob faili ühisesse kataloogi | `sudo -iu mari touch /srv/firma/ühine/mari.txt` |
| T5 | `kati` kustutab mari faili ühisest kataloogist | `sudo -iu kati rm -f /srv/firma/ühine/mari.txt` |
| T6 | `kati` loob faili teadete kataloogi | `sudo -iu kati touch /srv/firma/teated/kati.txt` |
| T7 | `toomas` loob teate | `sudo -iu toomas bash -c 'echo "Server taaskäivitub reedel" > /srv/firma/teated/info.txt'` |
| T8 | `kati` loeb teadet | `sudo -iu kati cat /srv/firma/teated/info.txt` |

**5.1** Vaata faili `kood.py` omanikku ja gruppi:

```bash
ls -l /srv/firma/tarkvara/
```

**K15.** Esita tabel testide T1–T8 ennustuste ja tulemustega. Miks kuulub fail `kood.py` grupile `tarkvara`, mitte grupile `mari`? Miks sai `jaan` seda muuta?

---

## 6. osa. Piiratud sudo õigus

Toomas peab saama süsteemi uuendada, kuid mitte midagi muud halduriõigustes teha.

**6.1** Loo reeglifail käsuga `visudo`:

```bash
sudo visudo -f /etc/sudoers.d/toomas
```

Kirjuta faili rida:

```text
toomas  ALL=(root) /usr/bin/apt update, /usr/bin/apt upgrade
```

Salvesta ja välju. (`visudo` avab vaikimisi redaktori `nano`.)

**6.2** Testi Toomase õigusi:

```bash
sudo -iu toomas sudo -l
```

Toomasel tuleb sisestada oma parool. Seejärel proovi kasutajana `toomas` sisse logida (`su - toomas`) ja käivitada:

```bash
sudo apt update
sudo cat /etc/shadow
exit
```

**K16.** Mis juhtus kummagi käsuga? Miks?

**K17.** Miks tuleb sudoers-faile muuta käsuga `visudo`, mitte otse redaktoriga?

**6.3** Uuri, kus logitakse `sudo` kasutamine:

```bash
sudo journalctl _COMM=sudo | tail -5
```

**K18.** Kas logis on näha Toomase katse lugeda faili `/etc/shadow`?

---

## 7. osa. Muudatused ja koristamine

**7.1** Jaan läheb üle turundusse. Lisa ta gruppi `turundus` ja eemalda grupist `tarkvara`. Kontrolli käsuga `id jaan`.

**K19.** Kirjuta käsud. Miks peab grupi lisamisel kasutama käsus `usermod` võtit `-a`?

**7.2** Leia kõik süsteemi SUID-failid:

```bash
find / -perm -4000 -type f 2>/dev/null
```

**K20.** Nimeta kolm leitud faili. Miks vajab näiteks `passwd` SUID-õigust?

**7.3** Kui õpetaja ei ole teisiti öelnud, jäta kasutajad ja kataloogid alles - neid kontrollitakse. Kui teed laborit iseseisvalt ja tahad koristada:

```bash
sudo userdel -r mari; sudo userdel -r jaan; sudo userdel -r kati; sudo userdel -r toomas
sudo groupdel tarkvara; sudo groupdel turundus
sudo rm /etc/sudoers.d/toomas
sudo rm -r /srv/firma
```

---

## Lisaülesanne (valikuline)

1. Ettevõtte juht Kati peab saama lugeda tarkvaraosakonna faili `kood.py`, kuid mitte muuta ega näha teisi tarkvaraosakonna faile. Lahenda see ACL-ide abil. Vihje: Kati vajab kataloogile `tarkvara` ainult õigust `x` ja failile õigust `r`.
2. Kirjuta üles, mis juhtub, kui jätad punktis 4.2 SGID-õiguse ära (`chmod 770`) ja korrata teste T1–T2.
3. **Paroolipoliitika:** paigalda `libpam-pwquality`, sea `/etc/security/pwquality.conf`-is `minlen = 12` ja `minclass = 3` ning proovi testkasutajana `passwd`-iga seada nõrka parooli. Lisa `/etc/skel`-i fail `LOEMIND.txt` ja loo uus kasutaja - kas fail kopeeriti?

---

## Õpetajale: kontrollvastused

| Küsimus | Vastus |
|---|---|
| K4 | `L` - parool on lukus. Ubuntus kasutatakse halduriõigusi käsuga `sudo` |
| K7 | Põhigrupp `mari`, lisagrupp `tarkvara`. Ubuntu 24.04-s on kodukataloogid `750` (`drwxr-x---`) |
| K8 | Ei õnnestu: kodukataloogi õigused ei anna muudele midagi |
| K9 | Ubuntus tavaliselt umask `0002` → fail `664` |
| K11 | `2` - SGID, `7` - omanik `rwx`, `7` - grupp `rwx`, `0` - muud ei midagi |
| K12 | `chmod 1777 /srv/firma/ühine`; sama nagu `/tmp` |
| K13 | `chown toomas:toomas` (või `toomas:root`), `chmod 755` |
| T1–T8 | ✓ ✓ ✗ ✓ ✗ ✗ ✓ ✓ |
| K16 | `apt update` töötab, `cat /etc/shadow` keelatakse: reegel lubab ainult kaht käsku |

Näidislahendused:

```bash
sudo groupadd tarkvara; sudo groupadd turundus                              # 2.1
sudo useradd -m -s /bin/bash -c "Jaan Tamm" -G tarkvara jaan                # K5
sudo useradd -m -s /bin/bash -c "Kati Kask" -G turundus kati                # K5
chmod u=rw,go= plaan.txt; chmod 600 plaan.txt                               # K10
sudo chown root:turundus /srv/firma/turundus; sudo chmod 2770 /srv/firma/turundus   # 4.3
sudo chmod 1777 /srv/firma/ühine                                            # K12
sudo chown toomas:toomas /srv/firma/teated; sudo chmod 755 /srv/firma/teated   # K13
sudo usermod -aG turundus jaan; sudo gpasswd -d jaan tarkvara               # K19
sudo setfacl -m u:kati:x /srv/firma/tarkvara                                # lisaülesanne 1
sudo setfacl -m u:kati:r /srv/firma/tarkvara/kood.py                        # lisaülesanne 1
```
