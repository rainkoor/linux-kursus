# Laboritöö 9. Salvestus: RAID, jõudlus, taastamine ja ZFS

| | |
|---|---|
| **Distrod** | AlmaLinux (osad 1–4, laboritöö 8 masin), Ubuntu (osa 5) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Laboritöö 8 AlmaLinuxi masin ja **kaks uut 2 GiB lisaketast** (pluss kolmas 2 GiB ketas 1. osa lõpus), Ubuntu masin |
| **Eesmärk** | Ehitada tarkvaraline RAID ja vahetada ketas, mõõta ja jälgida ketaste jõudlust ning tervist, taastada partitsioonitabel ja tutvuda ZFS-iga |

**Aruanne:** vasta küsimustele **K1–K14**.

> [!WARNING]
> Tee enne alustamist mõlemast masinast hetktõmmis. **Kontrolli enne iga ohtlikku käsku `lsblk`-iga, millise kettaga töötad.**

---

## 1. osa. Tarkvaraline RAID 1 (AlmaLinux)

**1.1** Lisa Proxmoxis masinale kaks 2 GiB ketast (*Hardware* → *Add* → *Hard Disk*). Leia nende nimed (selles juhendis `/dev/sdd` ja `/dev/sde`):

```bash
lsblk
```

**1.2** Loo peegel ja vaata sünkroniseerimist (teooria punkt 9.1):

```bash
sudo dnf install -y mdadm
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdd /dev/sde
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```

**K1.** Kui suur on massiiv? Mida näitab `/proc/mdstat` sünkroniseerimise ajal ja pärast seda (`[UU]`)?

**1.3** Loo failisüsteem, haagi see ja salvesta massiivi seadistus:

```bash
sudo mkfs.xfs /dev/md0
sudo mkdir -p /srv/raid
sudo mount /dev/md0 /srv/raid
sudo cp -r /etc /srv/raid/
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm.conf
```

**1.4** Simuleeri ketta riket:

```bash
sudo mdadm /dev/md0 --fail /dev/sde
cat /proc/mdstat
sudo mdadm --detail /dev/md0 | grep -E "State|Failed|/dev/"
ls /srv/raid/etc | head
sudo mdadm /dev/md0 --remove /dev/sde
```

**K2.** Mis on massiivi olek pärast riket? Kas andmed olid loetavad?

**1.5** Lisa masinale kolmas 2 GiB ketas (`/dev/sdf`) ja lisa see massiivi:

```bash
sudo mdadm /dev/md0 --add /dev/sdf
watch -n1 cat /proc/mdstat          # välju Ctrl+C
```

**K3.** Kui kaua taastamine (*recovery*) kestis? Miks võtab suurte (nt 20 TB) ketaste taastamine päevi ja miks on see risk?

**1.6** Taaskäivita masin ja kontrolli, kas massiiv pandi automaatselt kokku (`cat /proc/mdstat`). Lisa see vajadusel UUID-ga `/etc/fstab`-i (valikuga `nofail`).

**K4.** Mis on riistvaralise ja tarkvaralise RAID-i peamine erinevus, kui server ise (emaplaat või RAID-kontroller) rikneb?

## 2. osa. Ketta kiirus (AlmaLinux)

**2.1** Mõõda `dd`-ga laboritöö 8 köite `lv_veeb` (haagitud `/srv/veeb`) kirjutamise kiirust kahel viisil ja seejärel lugemiskiirust (teooria punkt 9.3):

```bash
sudo dd if=/dev/zero of=/srv/veeb/test bs=1M count=512 oflag=dsync status=progress
sudo dd if=/dev/zero of=/srv/veeb/test bs=1M count=512 conv=fdatasync status=progress
sudo dd if=/srv/veeb/test of=/dev/null bs=1M
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo dd if=/srv/veeb/test of=/dev/null bs=1M
sudo rm /srv/veeb/test
```

**K5.** Pane tulemused tabelisse. Miks oli `oflag=dsync` kiirus väiksem? Miks erinesid kaks lugemise tulemust?

**2.2** Paigalda `fio` ja mõõda 4 KiB juhuslikku lugemist-kirjutamist ning 1 MiB järjestikust kirjutamist (failiga `/srv/veeb/fio.test`, suurus 512M, kestus 30 s). Ava teises terminalis samal ajal `iostat -xz 2` (pakett `sysstat`).

**K6.** Mitu IOPS-i ja MB/s said kummagi testiga? Miks on 4 KiB juhusliku testi MB/s palju väiksem? Mida näitas `iostat` veerg `%util`?

Kustuta testfail: `sudo rm /srv/veeb/fio.test`.

## 3. osa. Ketta tervis (AlmaLinux)

**3.1** Paigalda `smartmontools` ja uuri virtuaalset ketast:

```bash
sudo dnf install -y smartmontools
sudo smartctl -i /dev/sda
sudo smartctl -H /dev/sda
```

**K7.** Mida `smartctl` virtuaalse ketta kohta näitas? Kus tuleks virtuaalmasinate puhul ketaste tervist jälgida? Kui sul on ligipääs mõnele füüsilisele Linuxi arvutile, vaata seal `smartctl -a` väljundist atribuute `Reallocated_Sector_Ct` ja `Power_On_Hours`.

## 4. osa. Partitsioonitabeli taastamine TestDiskiga (AlmaLinux)

Harjutame tõmmisfailiga, et päris kettaid mitte ohustada.

**4.1** Loo tõmmisfail, sellele partitsioon, failisüsteem ja failid:

```bash
sudo dnf install testdisk                 # EPEL (moodul 4)
truncate -s 300M /var/tmp/taaste.img
sudo losetup -fP --show /var/tmp/taaste.img      # nt /dev/loop0
sudo parted -s /dev/loop0 mklabel gpt mkpart andmed ext4 1MiB 100%
sudo mkfs.ext4 -L TAASTE /dev/loop0p1
sudo mkdir -p /mnt/taaste
sudo mount /dev/loop0p1 /mnt/taaste
echo "Väga olulised andmed" | sudo tee /mnt/taaste/oluline.txt
sudo cp -r /etc/ssh /mnt/taaste/
sudo umount /mnt/taaste
```

**4.2** „Õnnetus“: kustuta partitsioonitabel.

```bash
sudo wipefs -a /dev/loop0
sudo losetup -d /dev/loop0
sudo losetup -fP --show /var/tmp/taaste.img
lsblk /dev/loop0
```

**K8.** Kas `loop0p1` on alles? Kas andmed on kustutatud?

**4.3** Taasta partitsioonitabel:

```bash
sudo testdisk /dev/loop0
```

Vali *Create* → ketas → *EFI GPT* → *Analyse* → *Quick Search*. Leitud partitsioonil vajuta **P** ja kontrolli, kas fail `oluline.txt` on näha (**q** - tagasi). Vali *Enter* → *Write* → kinnita **Y**.

```bash
sudo partprobe /dev/loop0
lsblk -f /dev/loop0
sudo mount /dev/loop0p1 /mnt/taaste
cat /mnt/taaste/oluline.txt
```

**K9.** Kas andmed taastusid? Milline oli taastatud partitsiooni algus ja nimi? Miks ei tohi kahjustatud kettale enne taastamist midagi kirjutada?

**4.4** Koristamine:

```bash
sudo umount /mnt/taaste
sudo losetup -d /dev/loop0
rm /var/tmp/taaste.img
```


## 5. osa. ZFS (Ubuntu)

Tee see osa Ubuntu masinas (seal on ZFS kernelis kaasas). Kasutame pärisketaste asemel faile, et midagi katki ei läheks.

```bash
sudo apt install zfsutils-linux
for i in 1 2 3 4; do truncate -s 1G /var/tmp/zd$i.img; done
sudo zpool create labor mirror /var/tmp/zd1.img /var/tmp/zd2.img
zpool status labor
sudo zfs create -o compression=zstd labor/andmed
sudo cp -r /usr/share/doc /labor/andmed/
zfs list -o name,used,compressratio labor/andmed
```

**5.1** Tee hetktõmmis `labor/andmed@esimene`, kustuta kataloog `/labor/andmed/doc/bash`, taasta üks fail kataloogist `.zfs/snapshot/` ja seejärel kogu dataset `zfs rollback`-iga.
**5.2** Laienda poolile teine peegel (`sudo zpool add labor mirror /var/tmp/zd3.img /var/tmp/zd4.img`) ja vaata `zpool list` mahtu.
**5.3** Riku ühte peegli faili (`sudo dd if=/dev/urandom of=/var/tmp/zd1.img bs=1M count=50 seek=10 conv=notrunc`), käivita `sudo zpool scrub labor` ja vaata `zpool status -v` - mida ZFS leidis ja kas andmed jäid terveks?
**5.4** Koristamine: `sudo zpool destroy labor && rm /var/tmp/zd*.img`.

**K10.** Mis oli pakkimise suhe (`compressratio`)? Miks võib pakkimine kettatööd isegi kiirendada?

**K11.** Mitu viga `scrub` leidis ja parandas (veerg `CKSUM`)? Miks ei saaks tavaline RAID 1 (`mdadm`) seda viga ise parandada?

**K12.** Mis vahe on LVM-i ja ZFS-i hetktõmmisel? Miks ei asenda kumbki varukoopiat?


## 6. osa. Kokkuvõte

**K13.** Täida tabel: RAID 1 (`mdadm`), LVM, ZFS mirror - töökindlus, hetktõmmised, andmete kontrollsummad, suurendamine, kus kasutada?

**K14.** Koostasid salvestuse kooli failiserverile, kus on 4 ketast. Milline lahendus (riistvaraline RAID, `mdadm` + LVM, ZFS raidz2 või kaks peeglit) valiksid ja miks? Mis on varunduse plaan?

---

## Koristamine

```bash
sudo umount /srv/raid
sudo mdadm --stop /dev/md0
sudo mdadm --zero-superblock /dev/sdd /dev/sdf
```

Eemalda `/etc/mdadm.conf` ja `/etc/fstab`-ist lisatud read ning seejärel kettad Proxmoxis.

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 9. Salvestus: RAID, ZFS, jõudlus ja taastamine](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 9. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
