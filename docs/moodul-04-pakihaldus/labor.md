# Laboritöö 4. Pakihaldus kolmel distrol

| | |
|---|---|
| **Distrod** | Debian, Ubuntu ja AlmaLinux (kõik kolm) |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Kolm virtuaalmasinat (Debian, Ubuntu, AlmaLinux), igaühes `sudo` õigusega kasutaja ja internetiühendus |
| **Eesmärk** | Harjutada pakihaldust kahe perekonna distrodel ja võrrelda nende erinevusi |

**Aruanne:** täida võrdlustabel (1. osa lõpus) ja vasta küsimustele **K1–K16**.

> **Erandina kasutad selles laboris kõiki kolme distrot.** Hoia kolm SSH-seanssi korraga lahti (nt Windows Terminali eri vahekaartidel), et saaksid tulemusi kohe võrrelda. Jälgi viipa, et teaksid, millises masinas oled.

> **Debiani märkus:** kui Debiani paigaldamisel määrati juurkasutaja parool, ei pruugi `sudo` olla paigaldatud ega sinu kasutaja grupis `sudo`. Sel juhul tee järgmist: `su -`, siis `apt install sudo` ja `usermod -aG sudo sinu_kasutaja`, logi välja ja uuesti sisse.

---

## 1. osa. Samad toimingud kolmel distrol

Tee iga sammu kõigis kolmes masinas. Kirjuta kasutatud käsud ja tulemused võrdlustabelisse.

**1.1 Tuvasta süsteem.** Kontrolli distro versiooni ja kerneli versiooni.

```bash
cat /etc/os-release
uname -r
```

**1.2 Uuenda süsteem.** Debianis ja Ubuntus värskenda kõigepealt pakettide loend ja vaata uuendatavaid pakette. AlmaLinuxis kontrolli uuendusi. Seejärel uuenda kõik süsteemid.

**K1.** Mitu paketti oli igas masinas uuendatav? Miks on Debianis ja Ubuntus vaja kahte käsku, AlmaLinuxis aga ühte?

**1.3 Loe hoidlate seadistust.** Leia ja kuva iga distro hoidlate seadistusfail(id).

```bash
ls /etc/apt/sources.list.d/ /etc/apt/sources.list 2>/dev/null   # Debian, Ubuntu
ls /etc/yum.repos.d/                                             # AlmaLinux
```

**K2.** Millised hoidla osad (*components*) on Debianis ja Ubuntus lubatud? Millised hoidlad on AlmaLinuxis lubatud (`dnf repolist`)?

**1.4 Otsi ja uuri.** Otsi paketti `tree` ja kuva selle info (versioon, suurus, kirjeldus).

**1.5 Paigalda.** Paigalda pakett `tree` ja proovi seda: `tree -L 1 /etc | head`.

**1.6 Faili päritolu.** Leia, millisesse paketti kuuluvad failid `/usr/bin/ls` ja `/etc/ssh/ssh_config` (SSH kliendi seadistus).

> Kui Debiani vanemas versioonis `dpkg -S /usr/bin/ls` vastust ei anna, proovi `dpkg -S /bin/ls`. Põhjus: vanemates versioonides registreeris pakihaldur faili vana tee all, kuigi `/bin` on viit kataloogile `/usr/bin`.

**K3.** Kas paketid on kolmes distros samanimelised?

**1.7 Paketi sisu.** Kuva kõik paketi `openssh-server` failid ja loenda need.

**1.8 Paigaldatud pakettide arv.** Loenda paigaldatud paketid:

```bash
dpkg -l | grep '^ii' | wc -l     # Debian, Ubuntu
rpm -qa | wc -l                  # AlmaLinux
```

**K4.** Milline masin sisaldab kõige rohkem pakette? Mis võib olla põhjus?

**1.9 Eemalda.** Eemalda pakett `tree`. Debianis ja Ubuntus kasuta `purge`. Seejärel eemalda mittevajalikud sõltuvused.

**1.10 Ajalugu.** Leia, millal ja mida pakihaldur viimati tegi.

```bash
tail -20 /var/log/apt/history.log    # Debian, Ubuntu
dnf history                          # AlmaLinux
```

### Võrdlustabel

Täida tabel aruandes.

| Tegevus | Debian | Ubuntu | AlmaLinux |
|---|---|---|---|
| Distro versioon ja kernel | | | |
| Süsteemi uuendamise käsk(ud) | | | |
| Uuendatavate pakettide arv | | | |
| Hoidlate seadistusfail | | | |
| Paketi otsimise käsk | | | |
| Paigaldamise käsk | | | |
| Faili `/usr/bin/ls` pakett | | | |
| Faili `ssh_config` pakett | | | |
| Paketi failide loetlemise käsk | | | |
| `openssh-server` failide arv | | | |
| Paigaldatud pakettide arv | | | |
| Eemaldamise käsk | | | |
| Ajaloo vaatamise viis | | | |

---

## 2. osa. AlmaLinux: EPEL ja toimingute tagasivõtmine

**2.1** Otsi paketti `ncdu` (kettakasutuse analüüsi tööriist):

```bash
dnf search ncdu
```

**K5.** Kas pakett leiti? Miks?

**2.2** Luba EPEL-i hoidla ja otsi uuesti:

```bash
sudo dnf install epel-release
dnf repolist
dnf search ncdu
dnf info ncdu
```

**K6.** Millised uued hoidlad lisandusid? Millisest hoidlast `ncdu` pärineb (rida `Repository` või `From repo`)?

**2.3** Paigalda `ncdu` ja proovi seda kataloogil `/usr` (välju klahviga `q`):

```bash
sudo dnf install ncdu
ncdu /usr
```

**2.4** Võta paigaldus tagasi `dnf` ajaloo abil:

```bash
dnf history
sudo dnf history undo <ID>
```

Asenda `<ID>` paketi `ncdu` paigaldamise toimingu numbriga.

**K7.** Kas `ncdu` eemaldati? Mis juhtus EPEL-iga (`dnf repolist`)? Miks?

**2.5** Leia, milline pakett sisaldab käsku `dig`, ja paigalda see:

```bash
dnf provides '*/bin/dig'
```

**K8.** Mis on paketi nimi AlmaLinuxis? Leia Debiani või Ubuntu masinas, mis on sama tööriista paketi nimi (`apt search dnsutils`).

---

## 3. osa. Ubuntu: universe ja Snap

**3.1** Kuva paketi `ncdu` info ja leia, millisest hoidla osast see pärineb:

```bash
apt policy ncdu
apt show ncdu
```

**K9.** Kas `ncdu` on hoidla osas `main` või `universe`? Mis vahe neil on?

**3.2** Uuri Snapi:

```bash
snap list
snap find hello
```

**3.3** Paigalda testprogramm Snapist, käivita see ja eemalda:

```bash
sudo snap install hello-world
hello-world
which hello-world
sudo snap remove hello-world
```

**K10.** Millised snapid olid süsteemis enne sinu paigaldust? Kuhu paigaldati `hello-world` käivitusfail? Kuidas erineb see apt-i paketist?

---

## 4. osa. Debian: kompileerimine lähtekoodist

Selles osas kompileerid GNU projekti näidisprogrammi `hello` ja võrdled seda sama programmi paketiga.

**4.1** Paigalda kompileerimise tööriistad:

```bash
sudo apt install build-essential wget
```

**K11.** Mitu paketti paigaldati koos `build-essential`-iga? Miks nii palju?

**4.2** Laadi lähtekood alla ja paki lahti:

```bash
mkdir -p ~/labor04 && cd ~/labor04
wget https://ftp.gnu.org/gnu/hello/hello-2.12.1.tar.gz
tar -xzf hello-2.12.1.tar.gz
cd hello-2.12.1
ls
```

**4.3** Seadista, kompileeri ja paigalda:

```bash
./configure
make
sudo make install
```

**4.4** Käivita ja leia programm:

```bash
hello
hello --greeting="Tere, Haapsalu!"
which hello
dpkg -S "$(which hello)"
```

**K12.** Kuhu programm paigaldati? Miks ütleb `dpkg -S`, et fail ei kuulu ühtegi paketti?

**4.5** Paigalda nüüd sama programm Debiani hoidlast ja võrdle:

```bash
sudo apt install hello
ls -l /usr/bin/hello /usr/local/bin/hello
which -a hello
hello --version | head -1
/usr/bin/hello --version | head -1
echo $PATH
```

**K13.** Mitu `hello` programmi on nüüd süsteemis ja millised on nende versioonid? Kumb neist käivitub, kui kirjutad lihtsalt `hello`, ja miks? (Vihje: vaata muutujat `PATH`.)

**4.6** Eemalda mõlemad:

```bash
cd ~/labor04/hello-2.12.1
sudo make uninstall
sudo apt purge hello
which -a hello
```

**K14.** Too kolm põhjust, miks on paketist paigaldamine üldjuhul parem kui lähtekoodist kompileerimine.

---

## 5. osa. Kokkuvõte

**K15.** Kujutle, et pead paigaldama serverisse tarkvara, mida distro ametlikus hoidlas ei ole. Järjesta järgmised võimalused alates kõige eelistatumast ja põhjenda: tootja ametlik hoidla, juhusliku inimese PPA või kolmanda osapoole hoidla, lähtekoodist kompileerimine, veebist leitud skript `curl ... | sudo bash`, EPEL (AlmaLinuxis).

**K16.** Mida tuleks teha enne olulise serveri suurt uuendust?

---

## Lisaülesanne (valikuline)

1. Debianis: uuri hoidlate seadistust ja lisa **backports** hoidla (vt Debiani dokumentatsioonist „Backports“). Võrdle mõne paketi versiooni tava- ja backports hoidlas käsuga `apt policy`.
2. AlmaLinuxis: paigalda tarkvaragrupp `"Development Tools"` ja kompileeri `hello` ka seal. Mis on erinev?
3. **Väljalaske uuendus:** paigalda Proxmoxi uus Debian 12 VM (või klooni olemasolev), **tee hetktõmmis** ja uuenda see Debian 13-ks (teooria punkt 4.10). Pane kirja: mitu paketti uuendati, milliste seadistusfailide kohta küsiti ja mis on `cat /etc/debian_version` väljund enne ja pärast. Lõpuks teisenda hoidlad käsuga `apt modernize-sources` ja vaata faili `/etc/apt/sources.list.d/debian.sources`.
4. **AlmaLinux 9 → 10 (ainult analüüs):** AlmaLinux 9 hetktõmmisega VM-is paigalda ELevate ja käivita `sudo leapp preupgrade`. Uuri aruannet `/var/log/leapp/leapp-report.txt`: millised takistused (*inhibitor*) leiti?

---

## Õpetajale: kontrollvastused

| Küsimus | Vastus |
|---|---|
| K1 | `apt update` värskendab ainult pakettide loendit, `apt upgrade` uuendab. `dnf` värskendab loendit automaatselt |
| K3 | Osaliselt: `ls` kuulub kõigis paketti `coreutils` (AlmaLinuxi minimaalses keskkonnas võib olla `coreutils-single`), kuid `ssh_config` kuulub Debianis ja Ubuntus paketti `openssh-client`, AlmaLinuxis paketti `openssh-clients` |
| K5 | Ei leitud: `ncdu` ei ole AlmaLinuxi põhihoidlates, vaid EPEL-is |
| K7 | `undo` eemaldab `ncdu`, EPEL jääb alles, sest see paigaldati eraldi toiminguga |
| K8 | AlmaLinux: `bind-utils`; Debian/Ubuntu: `bind9-dnsutils` (või üleminekupakett `dnsutils`) |
| K9 | `universe` - kogukonna hooldatud; `main` - Canonicali toetatud |
| K10 | Snapi käivitusfail on kataloogis `/snap/bin`; programm töötab isoleeritult koos oma sõltuvustega |
| K12 | `/usr/local/bin/hello`; fail paigaldati käsitsi, pakihaldur sellest ei tea |
| K13 | Kaks; `PATH`-is on `/usr/local/bin` enne `/usr/bin`, seega käivitub käsitsi paigaldatu |
| K14 | Automaatsed (turva)uuendused, sõltuvuste haldus, puhas eemaldamine, allkirjastatud ja testitud paketid |
| K15 | Tootja ametlik hoidla ≈ EPEL → kompileerimine → juhuslik PPA → `curl \| sudo bash` (viimane ainult siis, kui skript on enne läbi loetud) |
| K16 | Varukoopia või hetktõmmis, uuenduste nimekirja ülevaatamine, hooldusaeg ja teavitus, taaskäivitusvalmidus |
