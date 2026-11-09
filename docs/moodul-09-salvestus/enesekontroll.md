# Moodul 9. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis vahe on RAID 0, 1, 5, 6 ja 10 tasemel? Mitu ketta riket igaüks talub?
2. Miks ei ole RAID varukoopia?
3. Too riistvaralise ja tarkvaralise RAID-i üks eelis ja üks puudus.
4. Kuidas vahetad `mdadm` massiivis rikkis ketta?
5. Miks on suurte ketastega RAID 5 / raidz1 riskantne?
6. Mis on ZFS-is pool, vdev ja dataset? Miks kaob kogu pool, kui üks vdev hävib?
7. Mida tähendab copy-on-write ja kuidas see aitab ZFS-il?
8. Mida teeb `zpool scrub` ja miks seda regulaarselt käivitatakse?
9. Miks peab ZFS nägema päris kettaid (mitte riistvaralise RAID-kontrolleri loogilist ketast)?
10. Mis vahe on läbilaskevõimel, IOPS-il ja latentsusel?
11. Millise `fio` testiga mõõdad andmebaasiserveri ketast? Mida teeb valik `--direct=1`?
12. Miks võib `dd if=/dev/zero` anda ebarealistlikult häid tulemusi?
13. Millised SMART-i atribuudid viitavad ketta peatsele rikkele?
14. Kogemata kustutati kettalt partitsioonitabel. Mida teed ja mida kindlasti ei tee?
15. Mis vahe on TestDiskil ja PhotoRecil?

## Praktilised miniülesanded

1. Loo kahest kettast (`/dev/sdb`, `/dev/sdc`) RAID 1 massiiv `/dev/md1` ja näita selle olekut.
2. Loo ZFS-i pool `andmed` peeglist (`/dev/sdb`, `/dev/sdc`) ja selles dataset `andmed/kodu` pakkimisega `zstd` ning kvoodiga 50 GiB.
3. Tee dataset'ist `andmed/kodu` hetktõmmis nimega `eile` ja saada see masinasse `varu` pooli `varu`.
4. Kirjuta `fio` käsk, mis mõõdab 60 sekundit 4 KiB juhuslikku lugemist failiga `/srv/test.fio` (1 GiB).
5. Kontrolli ketta `/dev/sda` SMART-i üldist tervist ja käivita lühike enesetest.

---

## Vastused

1. RAID 0 - jaotus, ei talu riket; RAID 1 - peegel, talub n − 1; RAID 5 - jaotus + paarsus, 1 ketas; RAID 6 - topeltpaarsus, 2 ketast; RAID 10 - peegeldatud paaride jaotus, 1 ketas igast paarist.
2. RAID kaitseb ainult ketta riknemise eest. Kogemata kustutatud või lunavaraga krüpteeritud failid kaovad kõigilt ketastelt korraga, samuti ei kaitse RAID tulekahju ega varguse eest.
3. Riistvaraline: läbipaistev OS-ile, akuga vahemälu; puudus: kontrolleri rikke korral on vaja samasugust kontrollerit. Tarkvaraline: tasuta ja kontrollerist sõltumatu; puudus: kasutab protsessorit ega tea andmete õigsusest.
4. `mdadm /dev/md0 --fail /dev/sdX`, `--remove /dev/sdX`, füüsiline vahetus, `--add /dev/sdY`, jälgi `cat /proc/mdstat`.
5. Taastamine kestab kaua ja loeb kõiki ülejäänud kettaid; selle ajal ei ole kaitset ning teise ketta rike või lugemisviga hävitab andmed.
6. Pool - kõigi ketaste ühine ruum; vdev - ketaste rühm (üksik, peegel, raidz); dataset - failisüsteem pooli sees. Andmed jaotatakse kõigi vdev-ide vahel, seega ühe vdev-i kadumisel puudub osa iga faili andmetest.
7. Andmeid ei kirjutata üle, vaid uude kohta ning viide muudetakse lõpuks korraga. Failisüsteem on alati järjepidev ja hetktõmmised on odavad.
8. Loeb kõik andmed ja kontrollib kontrollsummasid; leiab ja parandab vaikse andmeriknemise enne, kui seda vaja läheb.
9. ZFS teeb ise RAID-i ja jälgib ketaste tervist; kontrolleri taga ei näe ta üksikuid kettaid, ei saa vigu parandada ega SMART-i lugeda.
10. Läbilaskevõime - MB/s; IOPS - operatsioone sekundis; latentsus - ühe operatsiooni ooteaeg.
11. Juhuslik 4 KiB lugemine-kirjutamine (`--rw=randrw --bs=4k --iodepth=32 --numjobs=4 --direct=1`). `--direct=1` möödub lehevahemälust, et mõõdetaks ketast, mitte RAM-i.
12. Nullid on hästi pakitavad (ZFS, mõned SSD-d) ja ilma `oflag=dsync`/`conv=fdatasync`-ita mõõdetakse vahemälu.
13. `Reallocated_Sector_Ct`, `Current_Pending_Sector`, `Offline_Uncorrectable`; NVMe-l `Media and Data Integrity Errors` ja `Percentage Used`.
14. Ei kirjuta kettale midagi (ei loo uut partitsiooni ega failisüsteemi); võimalusel teen kettast koopia; taastan partitsioonitabeli TestDiskiga (*Analyse* → *Quick Search* → kontroll **P** → *Write*); faile taastades salvestan need teisele kettale.
15. TestDisk taastab partitsioonitabeli ja failisüsteemide asukohad; PhotoRec taastab üksikuid faile nende sisu järgi ka rikutud failisüsteemist.

### Miniülesannete lahendused

```bash
sudo mdadm --create /dev/md1 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
cat /proc/mdstat; sudo mdadm --detail /dev/md1
```

```bash
sudo zpool create andmed mirror /dev/sdb /dev/sdc
sudo zfs create -o compression=zstd -o quota=50G andmed/kodu
```

```bash
sudo zfs snapshot andmed/kodu@eile
sudo zfs send andmed/kodu@eile | ssh varu sudo zfs receive varu/kodu
```

```bash
fio --name=lugemine --filename=/srv/test.fio --size=1G --rw=randread --bs=4k \
    --iodepth=32 --ioengine=libaio --direct=1 --runtime=60 --time_based
```

```bash
sudo smartctl -H /dev/sda
sudo smartctl -t short /dev/sda
```
