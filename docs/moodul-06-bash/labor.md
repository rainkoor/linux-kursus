<!-- navigatsioon -->
[← Moodul 6. Bashi skriptimine ja Git](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 6. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 6. Halduskriptid ja Git

| | |
|---|---|
| **Distro** | Debian |
| **Kestus** | 5 × 90 minutit |
| **Vajalik** | Debiani virtuaalmasin, `sudo` õigusega kasutaja. Laboritöö 2 logifail `~/labor02/juurdepaas.log` (kui seda pole, loo see uuesti laboritöö 2 punkti 1.2 järgi) |
| **Eesmärk** | Kirjutada töökindlaid Bashi skripte tüüpiliste haldusülesannete jaoks |

> **Esitamine:** kõik skriptid kataloogis `~/bin` ning aruanne küsimuste **K1–K16** vastustega. Skriptid peavad olema ka 7. osas loodud Git-hoidlas. Iga skript peab läbima ShellCheck'i kontrolli ilma vigade ja hoiatusteta. Infotaseme märkused (*info*, nt SC2012) on lubatud, kui oskad selgitada, miks sa need teadlikult alles jätsid. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

**Töövõte:** kirjuta skript osade kaupa ja testi pärast iga muudatust. Ära kirjuta kogu skripti korraga valmis - vigu on siis raske leida.

---

## 1. osa. Ettevalmistus

**1.1** Paigalda ShellCheck ja loo skriptide kataloog:

```bash
sudo apt install shellcheck
mkdir -p ~/bin
```

**1.2** Logi välja ja uuesti sisse. Kontrolli, kas `~/bin` on muutujas `PATH`:

```bash
echo "$PATH" | tr ':' '\n'
```

> **K1.** Millised kataloogid on muutujas `PATH`? Miks oli vaja uuesti sisse logida? (Vihje: vaata faili `~/.profile`.)

**1.3** Loo esimene skript `~/bin/minuinfo`:

```bash
#!/bin/bash
# Näitab infot kasutaja ja süsteemi kohta
echo "Kasutaja:   $USER"
echo "Masin:      $HOSTNAME"
echo "Distro:     $(. /etc/os-release && echo "$PRETTY_NAME")"
echo "Kernel:     $(uname -r)"
echo "Töötanud:   $(uptime -p)"
echo "Ketas /:    $(df -h --output=used,size,pcent / | tail -1)"
```

Tee see käivitatavaks ja käivita nime järgi (ilma `./`-ta):

```bash
chmod +x ~/bin/minuinfo
minuinfo
```

**1.4** Proovi jutumärkide erinevust:

```bash
fail="minu fail.txt"
touch "$fail"
ls -l $fail
ls -l "$fail"
echo 'Kasutaja on $USER'
echo "Kasutaja on $USER"
```

> **K2.** Selgita kummagi `ls` käsu tulemust. Mis vahe on ülakomadel ja jutumärkidel?

---

## 2. osa. Argumendid ja tingimused

### Skript `tervita`

Kirjuta skript `~/bin/tervita`, mis:

1. ootab ühte argumenti - nime;
2. kui argumenti pole, kirjutab **standardveaväljundisse** kasutusjuhendi `Kasutus: tervita NIMI` ja lõpetab väljumiskoodiga 1;
3. tervitab kellaajast sõltuvalt: enne kella 12 „Tere hommikust“, 12–18 „Tere päevast“, hiljem „Tere õhtust“;
4. lisab tänase kuupäeva kujul `pp.kk.aaaa`.

```text
$ tervita Mari
Tere päevast, Mari! Täna on 08.11.2026.
$ tervita
Kasutus: tervita NIMI
$ echo $?
1
```

Vihje: `date +%H` annab tunni, `date +%d.%m.%Y` kuupäeva.

> **K3.** Kuidas kontrollisid, kas argument on olemas? Miks on oluline, et veateade läheb standardveaväljundisse ja väljumiskood on 1?

### Skript `failiinfo`

Kirjuta skript `~/bin/failiinfo`, mis saab **ükskõik kui palju** teid argumentidena ja ütleb iga kohta:

- kas see on tavaline fail (koos suurusega baitides), kataloog (koos kirjete arvuga), muu fail või seda pole olemas (viimane veaväljundisse);
- kas sinul on sellele lugemis-, kirjutus- ja käivitusõigus.

```text
$ failiinfo /etc/hostname /tmp /olematu
/etc/hostname: tavaline fail, 7 baiti
  loetav
/tmp: kataloog, 5 kirjet
  loetav
  kirjutatav
  käivitatav
/olematu: ei ole olemas
```

Vihjed: `for tee in "$@"`, `[ -f ]`, `[ -d ]`, `[ -e ]`, `[ -r ]`, `stat -c %s`, `ls -A | wc -l`.

> **K4.** Käivita `failiinfo /etc/shadow /usr/bin/passwd /dev/null`. Selgita tulemust.

---

## 3. osa. Tsüklid ja failist lugemine: kasutajate loomine

Kooli IT-tugi saab igal sügisel uute õppijate nimekirja. Kirjuta skript, mis loob kasutajad automaatselt.

**3.1** Loo fail `~/kasutajad.csv`:

```text
kasutajanimi,eesnimi,perenimi,grupp
mmaasikas,Mari,Maasikas,tarkvara
jtamm,Jaan,Tamm,tarkvara
kkask,Kati,Kask,turundus
```

**3.2** Kirjuta skript `~/bin/loo_kasutajad`, mis:

1. algab reaga `set -euo pipefail`;
2. saab argumendina CSV-faili nime ja kontrollib, kas fail on loetav;
3. jätab vahele esimese (päise) rea;
4. loob iga rea kohta kasutaja: kodukataloog, kest `/bin/bash`, kirjeldusse ees- ja perenimi, lisagrupiks veerus olev grupp;
5. loob grupi, kui seda veel pole;
6. jätab vahele kasutajad, kes on juba olemas, ja teatab sellest;
7. lõpus kirjutab, mitu kasutajat loodi ja mitu jäeti vahele;
8. **toetab võtit `-n` (proovirežiim)**, mille korral käske ei käivitata, vaid ainult kuvatakse.

Vihjed:

```bash
while IFS=, read -r kasutaja eesnimi perenimi grupp; do
    ...
done < <(tail -n +2 "$fail")
```

```bash
id "$kasutaja" &>/dev/null          # väljumiskood 0, kui kasutaja on olemas
getent group "$grupp" &>/dev/null   # väljumiskood 0, kui grupp on olemas
```

Proovirežiimi saab teha funktsiooniga, mis kas käivitab oma argumendid või ainult kuvab need:

```bash
kaivita() {
    if [ "$proov" -eq 1 ]; then
        echo "[PROOV] $*"
    else
        "$@"
    fi
}

kaivita useradd -m ...
```

**3.3** Testi kõigepealt proovirežiimis, seejärel päriselt ja siis veel kord päriselt:

```bash
sudo loo_kasutajad -n ~/kasutajad.csv
sudo loo_kasutajad ~/kasutajad.csv
id jtamm
sudo loo_kasutajad ~/kasutajad.csv
```

Kui `sudo` ei leia sinu skripti, kasuta täielikku teed: `sudo ~/bin/loo_kasutajad`.

> **K5.** Miks on proovirežiim sellise skripti puhul oluline? Mis juhtus kolmandal käivitusel?

> **K6.** Miks ei leia `sudo` skripti `~/bin` kataloogist ilma täieliku teeta? (Vihje: `sudo` kasutab oma turvalist `PATH`-i - vaata `sudo grep secure_path /etc/sudoers`.)

**3.4** Kustuta testkasutajad ja grupid (`userdel -r`, `groupdel`).

---

## 4. osa. Funktsioonid: varundus koos rotatsiooniga

Kirjuta skript `~/bin/varunda`, mis varundab kataloogi ja hoiab alles ainult viimased N varukoopiat.

Nõuded:

1. kasutus: `varunda KATALOOG [ARV]`, kus `ARV` on alles hoitavate koopiate arv (vaikimisi 5);
2. varukoopiad salvestatakse kataloogi, mille annab keskkonnamuutuja `VARUNDUS_SIHT`, vaikimisi `~/varukoopiad`;
3. arhiivi nimi on `KATALOOGINIMI-AAAA-KK-PP-TTMMSS.tar.gz`;
4. skriptis on funktsioonid `logi` (kirjutab teate koos kuupäeva ja kellaajaga) ja `viga` (kirjutab veateate veaväljundisse ja lõpetab koodiga 1);
5. kontrollib, et kataloog on olemas ja `ARV` on positiivne täisarv;
6. kustutab vanimad varukoopiad nii, et alles jääb `ARV` uusimat;
7. logib iga sammu.

```text
$ varunda ~/labor02 2
2026-11-08 17:03:54 Varundan /home/mari/labor02 -> /home/mari/varukoopiad/labor02-2026-11-08-170354.tar.gz
2026-11-08 17:03:54 Valmis, suurus 4.0K
```

Vihjed:

- `"${VARUNDUS_SIHT:-$HOME/varukoopiad}"`, `"${2:-5}"`;
- täisarvu kontroll: `[[ "$arv" =~ ^[0-9]+$ ]]`;
- `basename` ja `dirname` annavad tee viimase osa ja ülejäänu;
- `tar -czf ARHIIV -C ÜLEMKATALOOG KATALOOGINIMI` - nii ei salvestata arhiivi absoluutset teed;
- vanimate leidmine: `ls -1t` sorteerib uusimast vanimani, `tail -n +K` alustab K-ndast reast.

**4.1** Testi:

```bash
for i in 1 2 3 4; do varunda ~/labor02 2; sleep 1; done
ls -l ~/varukoopiad
varunda /olematu; echo "Väljumiskood: $?"
varunda ~/labor02 kaks; echo "Väljumiskood: $?"
VARUNDUS_SIHT=/tmp/proov varunda ~/labor02
```

> **K7.** Mitu arhiivi jäi alles ja miks? Mida tegi viimane käsk?

> **K8.** Miks on arhiivi loomisel kasulik võti `-C`? Mis oleks ilma selleta teisiti (vaata `tar -tzf`)?

**4.2** Ajasta varundus systemd taimeriga iga päev kell 01:00 (vt moodul 5). Kasuta teenuse failis keskkonnamuutujat:

```ini
[Service]
Type=oneshot
Environment=VARUNDUS_SIHT=/srv/varundus
ExecStart=/usr/local/bin/varunda /etc 7
```

Kopeeri selleks skript kataloogi `/usr/local/bin` ja loo kataloog `/srv/varundus`. Testi teenust käsitsi (`sudo systemctl start varunda.service`) ja vaata logi.

> **K9.** Kirjuta mõlema faili (`varunda.service`, `varunda.timer`) sisu aruandesse.

---

## 5. osa. case: logianalüüsi tööriist

Kirjuta skript `~/bin/logianalyys`, mis teeb laboritöö 2 analüüsid ühe tööriistaga:

```text
Kasutus: logianalyys KÄSK LOGIFAIL

Käsud:
  ip      päringute arv IP-aadresside kaupa
  olek    HTTP olekukoodide statistika
  vead    kliendi- ja serverivigadega (4xx, 5xx) päringud
  lehed   10 populaarseimat lehekülge
  kokku   lühike kokkuvõte
```

Nõuded:

- kasuta käsu valimiseks `case`-konstruktsiooni;
- kasutusjuhendit näitab eraldi funktsioon `abi`, mida kutsutakse nii vale käsu korral kui ka käsuga `-h`;
- kontrolli, et logifail on loetav;
- käsk `kokku` kuvab päringute arvu, unikaalsete IP-de arvu, vigade arvu ja andmemahu.

```text
$ logianalyys kokku ~/labor02/juurdepaas.log
Päringuid kokku:    20
Unikaalseid IP-sid: 6
Vigu (4xx/5xx):     7
Andmemaht (baiti):  191548
```

Vihje: `awk '$9 >= 400' fail` valib read, kus 9. väli on vähemalt 400. Mitmerealise teksti väljastamiseks sobib *here document* (`cat <<EOF ... EOF`).

> **K10.** Miks on `case` siin parem kui `if`-`elif`-ahel?

---

## 6. osa. Vigade leidmine ja parandamine

**6.1** Loo fail `~/vigane.sh`:

```bash
#!/bin/bash
# Kopeerib kõik .txt failid varukataloogi
siht=$1
mkdir $siht
cd $siht/..
for fail in $(ls *.txt); do
    cp $fail $siht
done
read vastus
echo "Kopeeritud `date`"
```

**6.2** Loo testkeskkond ja käivita skript:

```bash
mkdir -p ~/vigatest && cd ~/vigatest
touch "minu fail.txt" aruanne.txt
bash ~/vigane.sh "/tmp/minu varu"
```

**6.3** Kontrolli skripti ShellCheck'iga ja silu seda:

```bash
shellcheck ~/vigane.sh
bash -x ~/vigane.sh "/tmp/minu varu"
```

> **K11.** Loetle kõik ShellCheck'i hoiatused (koodid ja lühike selgitus eesti keeles). Mis läks testi käigus valesti ja miks?

**6.4** Paranda skript nii, et ShellCheck ei anna hoiatusi ja skript töötab tühikutega failinimede ja kataloogidega. Lisa `set -euo pipefail`, argumendi kontroll ja kasutusjuhend. Eemalda mõttetu `read`.

> **K12.** Lisa parandatud skript aruandesse.

---

## 7. osa. Skriptid Git-hoidlasse

**7.1** Paigalda Git ja seadista see:

```bash
sudo apt install git
git config --global user.name "Ees Perenimi"
git config --global user.email "sinu@e-post.ee"
git config --global init.defaultBranch main
git config --global core.editor nano
```

**7.2** Loo hoidla, kuhu kogud kõik selle kursuse skriptid ja seadistused (seda hoidlat kasutad edasi moodulites 12 ja 16):

```bash
mkdir ~/infra && cd ~/infra
git init
echo "# Minu laborite infrastruktuur" > README.md
printf '*.log\n*.retry\nsaladused.txt\n' > .gitignore
git status
git add README.md .gitignore
git commit -m "Lisa README ja .gitignore"
git log
```

**7.3** Lisa hoidlasse selle laboritöö skriptid:

```bash
mkdir -p skriptid
cp ~/bin/* skriptid/
ls skriptid
git add skriptid
git commit -m "Lisa laboritöö 6 halduskriptid"
```

**7.4** Muuda üht skripti (nt lisa kommentaar), vaata muudatust ja salvesta:

```bash
nano skriptid/varunda
git status
git diff
git add -p                     # vaata ja kinnita muudatused tükkhaaval (y/n)
git commit -m "Täienda varundusskripti kommentaare"
git log --oneline
```

> **K13.** Mis vahe on käskudel `git diff` ja `git diff --staged`? Miks on kasulik muudatused enne sissekannet üle vaadata?

**7.5** Proovi saladuse kaitset:

```bash
echo "parool=Salajane123" > saladused.txt
git status
```

> **K14.** Kas Git näitas faili `saladused.txt`? Miks? Mis juhtuks, kui oleksid parooli kogemata sisse kandnud ja hoidla avalikuks teinud?

### Harud ja konflikt

**7.6** Loo seadistusfail ja kaks haru, mis muudavad sama rida:

```bash
echo "PIIR=80" > seire.conf
git add seire.conf && git commit -m "Lisa seire seadistus"

git switch -c tundlikum
sed -i 's/80/70/' seire.conf
git commit -am "Alanda seire piiri 70%-le"

git switch main
sed -i 's/80/90/' seire.conf
git commit -am "Tõsta seire piiri 90%-le"

git merge tundlikum
```

**7.7** Uuri konflikti ja lahenda see: määra piiriks `75`, eemalda konfliktimärgid ja salvesta:

```bash
cat seire.conf
git status
nano seire.conf
git add seire.conf
git commit -m "Lahenda konflikt: seire piir 75%"
git log --oneline --graph
git branch -d tundlikum
```

> **K15.** Kuidas nägi fail `seire.conf` konflikti ajal välja? Mida tähendavad märgid `<<<<<<<`, `=======` ja `>>>>>>>`? Kopeeri `git log --oneline --graph` väljund aruandesse.

### Kaughoidla

**7.8** Kaughoidla võib olla teises masinas (SSH kaudu, moodul 7), GitHubis või harjutamiseks samas masinas teises kataloogis:

```bash
git init --bare -b main ~/hoidlad/infra.git
git remote add origin ~/hoidlad/infra.git
git push -u origin main
```

**7.9** Klooni hoidla teise kataloogi, muuda seal faili ja saada muudatus tagasi:

```bash
cd ~ && git clone ~/hoidlad/infra.git infra-koopia
cd infra-koopia
echo "Laboritöö 6 tehtud" >> README.md
git commit -am "Uuenda README"
git push
cd ~/infra
git pull
cat README.md
```

> **K16.** Mida tegid `git push` ja `git pull`? Miks on kasulik, et seadistus on kaughoidlas (teises masinas või GitHubis)?

**7.10** (Valikuline, pärast moodulit 7) Loo GitHubis privaatne hoidla, lisa oma SSH avalik võti GitHubi seadistustes ja lisa teine kaughoidla:

```bash
ssh -T git@github.com
git remote add github git@github.com:<kasutaja>/infra.git
git push -u github main
```

---

## Lisaülesanne (valikuline)

1. Täienda `loo_kasutajad` nii, et see genereerib igale kasutajale juhusliku parooli (`openssl rand -base64 12`), määrab selle (`chpasswd`), sunnib esimesel sisselogimisel parooli vahetama (`chage -d 0`) ja kirjutab kasutajanimed ja paroolid faili, millel on õigused `600`.
2. Kirjuta skript `seire`, mis kontrollib ketta täituvust, mälu ja koormust ning kirjutab hoiatuse, kui mõni ületab skripti alguses määratud piiri. Kasuta väljumiskoode: 0 - kõik korras, 1 - hoiatus, 2 - kriitiline.
3. Muuda `logianalyys` nii, et logifaili võib anda ka torust: `cat juurdepaas.log | logianalyys kokku -`.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Millised kataloogid on muutujas `PATH`? Miks oli vaja uuesti sisse logida? (Vihje: vaata faili `~/.profile`.)
- **K2.** *(punkt 1.4)* Selgita kummagi `ls` käsu tulemust. Mis vahe on ülakomadel ja jutumärkidel?
- **K3.** *(2. osa)* Kuidas kontrollisid, kas argument on olemas? Miks on oluline, et veateade läheb standardveaväljundisse ja väljumiskood on 1?
- **K4.** *(2. osa)* Käivita `failiinfo /etc/shadow /usr/bin/passwd /dev/null`. Selgita tulemust.
- **K5.** *(punkt 3.3)* Miks on proovirežiim sellise skripti puhul oluline? Mis juhtus kolmandal käivitusel?
- **K6.** *(punkt 3.3)* Miks ei leia `sudo` skripti `~/bin` kataloogist ilma täieliku teeta? (Vihje: `sudo` kasutab oma turvalist `PATH`-i - vaata `sudo grep secure_path /etc/sudoers`.)
- **K7.** *(punkt 4.1)* Mitu arhiivi jäi alles ja miks? Mida tegi viimane käsk?
- **K8.** *(punkt 4.1)* Miks on arhiivi loomisel kasulik võti `-C`? Mis oleks ilma selleta teisiti (vaata `tar -tzf`)?
- **K9.** *(punkt 4.2)* Kirjuta mõlema faili (`varunda.service`, `varunda.timer`) sisu aruandesse.
- **K10.** *(5. osa)* Miks on `case` siin parem kui `if`-`elif`-ahel?
- **K11.** *(punkt 6.3)* Loetle kõik ShellCheck'i hoiatused (koodid ja lühike selgitus eesti keeles). Mis läks testi käigus valesti ja miks?
- **K12.** *(punkt 6.4)* Lisa parandatud skript aruandesse.
- **K13.** *(punkt 7.4)* Mis vahe on käskudel `git diff` ja `git diff --staged`? Miks on kasulik muudatused enne sissekannet üle vaadata?
- **K14.** *(punkt 7.5)* Kas Git näitas faili `saladused.txt`? Miks? Mis juhtuks, kui oleksid parooli kogemata sisse kandnud ja hoidla avalikuks teinud?
- **K15.** *(punkt 7.7)* Kuidas nägi fail `seire.conf` konflikti ajal välja? Mida tähendavad märgid `<<<<<<<`, `=======` ja `>>>>>>>`? Kopeeri `git log --oneline --graph` väljund aruandesse.
- **K16.** *(punkt 7.9)* Mida tegid `git push` ja `git pull`? Miks on kasulik, et seadistus on kaughoidlas (teises masinas või GitHubis)?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 6. Bashi skriptimine ja Git](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 6. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
