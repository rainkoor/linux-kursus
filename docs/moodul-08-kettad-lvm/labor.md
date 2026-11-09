# Laboritöö 8. Kettad, failisüsteemid ja LVM

| | |
|---|---|
| **Distro** | AlmaLinux |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | AlmaLinuxi virtuaalmasin `sudo` õigusega kasutajaga, **kaks lisaketast** (soovitatavalt 5 GiB ja 3 GiB), ligipääs masina konsoolile |
| **Eesmärk** | Harjutada partitsioneerimist, failisüsteeme, püsivat haakimist, saaleala ja LVM-i |

**Aruanne:** vasta küsimustele **K1–K18**.

### Lisaketaste lisamine

**Proxmoxis:** vali virtuaalmasin → *Hardware* → *Add* → *Hard Disk*. Lisa kaks ketast suurusega 5 GiB ja 3 GiB (siini tüüp SCSI). Kettaid saab lisada ka töötavale masinale.

**VirtualBoxis:** masin peab olema välja lülitatud. *Settings* → *Storage* → kontrolleri juures *Add Hard Disk*.

Selles juhendis on lisakettad **`/dev/sdb`** (5 GiB) ja **`/dev/sdc`** (3 GiB). Kui sinu masinas on need `/dev/vdb` ja `/dev/vdc` või muud nimed, kasuta neid. **Kontrolli enne iga ohtlikku käsku `lsblk`-iga, et töötad õige kettaga - süsteemiketast ei tohi puutuda!**

---
## 1. osa. Olemasoleva süsteemi uurimine

**1.1** Uuri plokkseadmeid ja failisüsteeme:

```bash
lsblk
lsblk -f
df -hT
findmnt -t xfs,ext4,vfat
```

**K1.** Joonista (või kirjelda) süsteemiketta struktuur: millised partitsioonid on, millised failisüsteemid neil on ja kuhu need on haagitud. Kas süsteem kasutab LVM-i?

**1.2** Uuri LVM-i ja saaleala:

```bash
sudo pvs
sudo vgs
sudo lvs
swapon --show
free -h
cat /etc/fstab
```

**K2.** Kuidas on juurfailisüsteem ja saaleala failis `/etc/fstab` kirjeldatud - UUID või LVM-i köite tee järgi? Kui palju on köitegrupis vaba ruumi?

**1.3** Kontrolli, et lisakettad on olemas ja tühjad:

```bash
lsblk /dev/sdb /dev/sdc
sudo fdisk -l /dev/sdb /dev/sdc
```

---
## 2. osa. Partitsioonid ja failisüsteemid

Jaga ketas `/dev/sdb` kaheks partitsiooniks: 2 GiB ext4 ja ülejäänu XFS.

**2.1** Loo GPT-partitsioonitabel ja partitsioonid. Võid kasutada `parted`-it:

```bash
sudo parted -s /dev/sdb mklabel gpt
sudo parted -s /dev/sdb mkpart andmed ext4 1MiB 2GiB
sudo parted -s /dev/sdb mkpart arhiiv xfs 2GiB 100%
sudo parted /dev/sdb print
lsblk /dev/sdb
```

või interaktiivset `fdisk`-i (`g`, `n`, `n`, `p`, `w`).

**K3.** Millised on partitsioonide suurused? Miks algab esimene partitsioon 1 MiB juurest, mitte ketta päris algusest?

**2.2** Loo failisüsteemid:

```bash
sudo mkfs.ext4 -L andmed /dev/sdb1
sudo mkfs.xfs -L arhiiv /dev/sdb2
lsblk -f /dev/sdb
```

**2.3** Haagi failisüsteemid ajutiselt ja proovi neid:

```bash
sudo mkdir -p /mnt/andmed /srv/arhiiv
sudo mount /dev/sdb1 /mnt/andmed
sudo mount /dev/sdb2 /srv/arhiiv
df -hT /mnt/andmed /srv/arhiiv
sudo cp -r /etc /srv/arhiiv/
ls /srv/arhiiv/etc | head
```

**2.4** Proovi haakepunkti „peitmist“:

```bash
sudo umount /mnt/andmed
echo "Olen kataloogis, mitte kettal" | sudo tee /mnt/andmed/peidus.txt
sudo mount /dev/sdb1 /mnt/andmed
ls /mnt/andmed
sudo umount /mnt/andmed
ls /mnt/andmed
```

**K4.** Mis juhtus failiga `peidus.txt`, kui ketas oli haagitud? Kas fail kadus?

**2.5** Proovi lahti haakida kataloogi, kus oled:

```bash
cd /srv/arhiiv
sudo umount /srv/arhiiv
sudo fuser -vm /srv/arhiiv
cd
sudo umount /srv/arhiiv
```

**K5.** Mis veateate said ja miks? Mida näitas `fuser`?

---
## 3. osa. Püsiv haakimine

**3.1** Leia partitsioonide UUID-d:

```bash
lsblk -f /dev/sdb
sudo blkid /dev/sdb1 /dev/sdb2
```

**3.2** Lisa failisüsteemid faili `/etc/fstab`. Tee kõigepealt varukoopia:

```bash
sudo cp /etc/fstab /etc/fstab.varu
sudo nano /etc/fstab
```

Lisa read (kasuta oma UUID-sid):

```text
UUID=<sdb1 UUID>  /mnt/andmed  ext4  defaults,nofail  0  2
UUID=<sdb2 UUID>  /srv/arhiiv  xfs   defaults,nofail  0  0
```

**3.3** Kontrolli ja rakenda **enne** taaskäivitust:

```bash
sudo findmnt --verify
sudo systemctl daemon-reload
sudo mount -a
df -hT /mnt/andmed /srv/arhiiv
```

**3.4** Taaskäivita masin ja kontrolli, kas failisüsteemid haagiti.

**K6.** Miks kasutatakse failis `fstab` UUID-d, mitte seadme nime `/dev/sdb1`? Miks on XFS-i real viimane väli `0`?

**3.5** Tee fstab-i meelega viga: muuda esimese rea UUID-s üks märk. Kontrolli:

```bash
sudo findmnt --verify
sudo umount /mnt/andmed
sudo mount -a
```

**K7.** Mida näitasid `findmnt --verify` ja `mount -a`? Mis juhtuks taaskäivitusel, kui real **ei oleks** valikut `nofail`?

Paranda viga ja kontrolli uuesti käsuga `findmnt --verify`.

---
## 4. osa. Saaleala

**4.1** Loo 512 MiB saalefail:

```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=512
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
swapon --show
free -h
```

**K8.** Kui palju on nüüd saaleala kokku? Miks peavad saalefaili õigused olema `600`?

**4.2** Lisa saalefail faili `/etc/fstab` ja kontrolli:

```text
/swapfile  none  swap  defaults  0  0
```

```bash
sudo swapoff /swapfile
sudo swapon -a
swapon --show
```

---
## 5. osa. LVM

Loo teisele kettale köitegrupp ja loogilised köited.

**5.1** Valmista ketas `/dev/sdc` ette ja loo köitegrupp:

```bash
sudo pvcreate /dev/sdc
sudo vgcreate vg_andmed /dev/sdc
sudo pvs
sudo vgs
```

**5.2** Loo kaks köidet:

```bash
sudo lvcreate -n lv_veeb -L 1G vg_andmed
sudo lvcreate -n lv_db -L 1G vg_andmed
sudo lvs
sudo vgs
```

**K9.** Kui palju ruumi jäi köitegruppi vabaks?

**5.3** Loo köidetele failisüsteemid ja haagi need püsivalt:

```bash
sudo mkfs.xfs /dev/vg_andmed/lv_veeb
sudo mkfs.ext4 /dev/vg_andmed/lv_db
sudo mkdir -p /srv/veeb /srv/db
```

Lisa faili `/etc/fstab` (LVM-i köidete puhul on köite tee püsiv, UUID-d pole vaja):

```text
/dev/vg_andmed/lv_veeb  /srv/veeb  xfs   defaults,nofail  0  0
/dev/vg_andmed/lv_db    /srv/db    ext4  defaults,nofail  0  2
```

```bash
sudo findmnt --verify
sudo systemctl daemon-reload
sudo mount -a
df -hT /srv/veeb /srv/db
```

**5.4** Täida veebiköide andmetega ja suurenda seda **töö ajal**:

```bash
sudo dd if=/dev/zero of=/srv/veeb/suur.fail bs=1M count=700
df -h /srv/veeb
sudo lvextend -r -L +500M /dev/vg_andmed/lv_veeb
df -h /srv/veeb
```

**K10.** Mis oli köite suurus ja täituvus enne ja pärast laiendamist? Kas fail `suur.fail` jäi alles? Mida tegi võti `-r`?

**5.5** Proovi XFS-köidet vähendada:

```bash
sudo lvreduce -r -L -200M /dev/vg_andmed/lv_veeb
```

**K11.** Mis juhtus? Miks? (Vasta küsimusele „Do you want to…“ `n`, kui küsitakse.)

### Uue ketta lisamine köitegruppi

Ketta `sdb` partitsioonid ei ole enam vajalikud. Lisad selle ketta köitegruppi `vg_andmed`.

**5.6** Eemalda `sdb` failisüsteemid kasutusest:

```bash
sudo umount /mnt/andmed /srv/arhiiv
sudo nano /etc/fstab        # kustuta või kommenteeri välja sdb1 ja sdb2 read
sudo systemctl daemon-reload
sudo wipefs -a /dev/sdb2 /dev/sdb1
sudo wipefs -a /dev/sdb
lsblk /dev/sdb
```

**K12.** Mida teeb `wipefs`? Miks oli vaja enne kustutada fstab-i read?

**5.7** Lisa ketas köitegruppi ja kasuta kogu vaba ruum andmebaasi köite jaoks:

```bash
sudo pvcreate /dev/sdb
sudo vgextend vg_andmed /dev/sdb
sudo vgs
sudo lvextend -r -l +100%FREE /dev/vg_andmed/lv_db
sudo lvs
df -h /srv/db
lsblk
```

**K13.** Kui suur on nüüd köitegrupp ja köide `lv_db`? Millistel füüsilistel ketastel köide `lv_db` asub (`sudo lvs -o +devices`)?

### Hetktõmmis

**5.8** Loo andmebaasi köitele faile, tee hetktõmmis ja „riku“ andmed:

```bash
echo "Oluline andmebaas" | sudo tee /srv/db/andmed.txt
sudo lvcreate -s -n lv_db_snap -L 300M /dev/vg_andmed/lv_db
sudo lvs
echo "Rikutud!" | sudo tee /srv/db/andmed.txt
```

**5.9** Haagi hetktõmmis ainult lugemiseks ja taasta sealt fail:

```bash
sudo mkdir -p /mnt/snap
sudo mount -o ro /dev/vg_andmed/lv_db_snap /mnt/snap
cat /mnt/snap/andmed.txt
sudo cp /mnt/snap/andmed.txt /srv/db/andmed.txt
cat /srv/db/andmed.txt
sudo umount /mnt/snap
sudo lvremove -y /dev/vg_andmed/lv_db_snap
```

**K14.** Mis oli hetktõmmise failis? Miks ei ole hetktõmmis varukoopia asendus?

---
## 6. osa. Kettakasutuse analüüs

**6.1** Leia, mis süsteemis ruumi võtab:

```bash
df -h
sudo du -h --max-depth=1 /var 2>/dev/null | sort -h
sudo find / -xdev -type f -size +50M -exec ls -lh {} \; 2>/dev/null
journalctl --disk-usage
dnf clean all
```

**K15.** Milline kataloog kataloogis `/var` on suurim? Leia kolm suurimat faili juurfailisüsteemis.

**6.2** Kustutatud, kuid avatud fail:

```bash
sudo dd if=/dev/zero of=/srv/veeb/logi.log bs=1M count=200
df -h /srv/veeb
sudo tail -f /srv/veeb/logi.log &
sudo rm /srv/veeb/logi.log
df -h /srv/veeb
sudo lsof +L1 | grep logi
sudo pkill -f "tail -f /srv/veeb/logi.log"
df -h /srv/veeb
```

**K16.** Millal ruum vabanes - pärast `rm`-i või pärast protsessi lõpetamist? Miks?

---
## 7. osa. Krüpteeritud köide LUKS-iga

Harjutame faili peal, et lisakettaid mitte puutuda.

**7.1** Loo LUKS konteiner (teooria punkt 8.10):

```bash
sudo dnf install -y cryptsetup
truncate -s 500M /var/tmp/salajane.img
sudo losetup -f --show /var/tmp/salajane.img          # nt /dev/loop0
sudo cryptsetup luksFormat /dev/loop0                  # kirjuta YES ja vali parool
sudo cryptsetup open /dev/loop0 salajane
sudo mkfs.ext4 /dev/mapper/salajane
sudo mkdir -p /srv/salajane
sudo mount /dev/mapper/salajane /srv/salajane
echo "Konfidentsiaalne" | sudo tee /srv/salajane/fail.txt
lsblk /dev/loop0
```

**7.2** Sule konteiner ja proovi andmeid otse failist leida:

```bash
sudo umount /srv/salajane
sudo cryptsetup close salajane
sudo strings /dev/loop0 | grep -i konfidentsiaalne
sudo cryptsetup luksDump /dev/loop0 | head -30
```

**K17.** Kas teksti leidus krüpteeritud seadmest? Milline krüpteerimisalgoritm ja mitu võtmepesa on kasutusel?

**7.3** Lisa teine parool, kontrolli, et mõlemaga saab avada, ja tee päisest varukoopia:

```bash
sudo cryptsetup luksAddKey /dev/loop0
sudo cryptsetup open --test-passphrase /dev/loop0 && echo OK
sudo cryptsetup luksHeaderBackup /dev/loop0 --header-backup-file /root/salajane-header.img
```

**K18.** Miks on päise varukoopia oluline? Kus tohib seda hoida ja kus mitte?

**7.4** Koristamine:

```bash
sudo losetup -d /dev/loop0
rm /var/tmp/salajane.img
```

---

## Koristamine

Kui õpetaja ei ole teisiti öelnud, jäta LVM-i seadistus alles. Iseõppija võib eemaldada:

```bash
sudo swapoff /swapfile && sudo rm /swapfile
sudo umount /srv/veeb /srv/db
sudo lvremove -y vg_andmed
sudo vgremove vg_andmed
sudo pvremove /dev/sdb /dev/sdc
```

ning kustutada failist `/etc/fstab` vastavad read (või taastada varukoopia `sudo cp /etc/fstab.varu /etc/fstab`).

---
## Lisaülesanne (valikuline)

1. **Juurfailisüsteemi suurendamine:** suurenda Proxmoxis süsteemiketast 2 GiB võrra (*Hardware* → ketas → *Disk Action* → *Resize*). Suurenda seejärel partitsioon, PV, juurköide ja failisüsteem (vt teooria punkt 8.9).
2. **Püsiv LUKS-köide:** krüpteeri LVM-i köide `lv_db` (andmed kaovad - varunda enne!), lisa see faili `/etc/crypttab` võtmefailiga (`/root/db.key`, õigused `400`) ja `/etc/fstab`-i ning kontrolli, et see avaneb taaskäivitusel automaatselt.

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 8. Kettad, failisüsteemid ja LVM](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 8. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
