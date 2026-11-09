# Laboritöö 10. Alglaadimine, kernel ja taastamine

| | |
|---|---|
| **Distro** | Debian |
| **Kestus** | 4 × 90 minutit (9. osa kompileerimine võib kesta kauem - selle võib teha ka iseseisvalt) |
| **Vajalik** | Debiani virtuaalmasin `sudo` õigusega kasutajaga ja **ligipääs masina konsoolile** (nt Proxmoxi veebiliides). Enne alustamist tee masinast **hetktõmmis** (*snapshot*). 9. osa jaoks soovitatavalt vähemalt 4 protsessorituuma, 4 GiB mälu ja 15 GiB vaba kettaruumi |
| **Eesmärk** | Uurida alglaadimist ja kernelit, muuta GRUB-i ja kerneli seadistust ning taastada mittekäivituv süsteem |

**Aruanne:** vasta küsimustele **K1–K30**.

> [!WARNING]
> **Selles laboris rikud teadlikult oma süsteemi.** Tee enne alustamist virtuaalmasinast hetktõmmis (Proxmoxis: masin → *Snapshots* → *Take Snapshot*). Kui midagi läheb lootusetult valesti, saad selle taastada. Osad 5–8 ja 10 tehakse **konsoolis**, mitte SSH kaudu.

---

## 1. osa. Kernel ja riistvara

**1.1** Uuri kernelit:

```bash
uname -a
uname -r
cat /proc/version
cat /proc/cmdline
ls -lh /boot
```

**K1.** Mis on kerneli versioon? Millised kerneli parameetrid anti käivitamisel? Mitu kernelit on kataloogis `/boot`?

**1.2** Kas masin käivitus BIOS-i või UEFI-ga?

```bash
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "BIOS"
lsblk -f
```

**1.3** Uuri riistvara failisüsteemide `/proc` ja `/sys` kaudu ning abikäskudega:

```bash
grep -c processor /proc/cpuinfo
grep "model name" /proc/cpuinfo | head -1
lscpu | head -15
grep -E "MemTotal|MemAvailable" /proc/meminfo
cat /proc/uptime /proc/loadavg
ls /sys/class/net/
cat /sys/class/net/*/address
sudo apt install pciutils
lspci
```

**K2.** Mitu protsessorituuma ja kui palju mälu on masinal? Mille järgi on näha, et tegu on virtuaalmasinaga (`lspci`, `lscpu` rida `Hypervisor vendor`)?

**1.4** Uuri oma kesta protsessi:

```bash
echo $$
cat /proc/$$/cmdline | tr '\0' ' '; echo
ls -l /proc/$$/cwd
ls -l /proc/$$/fd
```

**K3.** Mida näitavad `cwd` ja `fd`? Miks on failikirjeldajad 0, 1 ja 2 seotud terminaliga?

---

## 2. osa. Alglaadimise analüüs

**2.1** Analüüsi alglaadimise kiirust:

```bash
systemd-analyze
systemd-analyze blame | head -10
systemd-analyze critical-chain
systemctl get-default
```

**K4.** Kui kaua alglaadimine kestis (kernel ja kasutajaruum eraldi)? Milline teenus käivitus kõige kauem? Mis on vaike-eesmärk?

**2.2** Uuri alglaadimise logisid:

```bash
journalctl --list-boots
journalctl -b -p warning --no-pager | head -30
sudo dmesg -T | head -30
sudo dmesg -T --level=err,warn
```

**K5.** Mitu alglaadimist on journal'is? Leia `dmesg` väljundist rida, kus kernel tuvastab süsteemiketta (otsi `sda` või `vda`). Kas logis on vigu?

**K6.** Proovi `dmesg` ilma `sudo`-ta. Mis juhtus? Milline `sysctl` parameeter seda põhjustab?

---

## 3. osa. Kerneli moodulid

**3.1** Uuri laaditud mooduleid:

```bash
lsmod | head -20
lsmod | wc -l
lsmod | grep -E "virtio|ext4"
modinfo ext4 | head
```

**3.2** Laadi testmoodul `dummy`, mis loob virtuaalse võrguliidese:

```bash
ip -br link
sudo modprobe dummy
lsmod | grep dummy
ip -br link
modinfo dummy
sudo modprobe -r dummy
ip -br link
```

**K7.** Mis juhtus võrguliidestega pärast mooduli laadimist ja eemaldamist? Mis on mooduli `dummy` failitee (`modinfo` rida `filename`)?

**3.3** Sea moodul alglaadimisel laaditavaks ja kontrolli taaskäivituse järel:

```bash
echo dummy | sudo tee /etc/modules-load.d/dummy.conf
sudo systemctl reboot
```

Pärast taaskäivitust: `lsmod | grep dummy`.

**3.4** Keela mooduli laadimine, eemalda see ja proovi uuesti laadida:

```bash
sudo rm /etc/modules-load.d/dummy.conf
echo "blacklist dummy" | sudo tee /etc/modprobe.d/blacklist-dummy.conf
sudo modprobe -r dummy
sudo modprobe dummy && lsmod | grep dummy
```

**K8.** Kas `modprobe dummy` laadis mooduli vaatamata `blacklist`-reale? Mida `blacklist` tegelikult takistab? (Vihje: `man modprobe.d`.)

Eemalda pärast fail `/etc/modprobe.d/blacklist-dummy.conf` ja moodul.

---

## 4. osa. Kerneli parameetrid

**4.1** Uuri parameetreid:

```bash
sysctl -a 2>/dev/null | wc -l
sysctl net.ipv4.ip_forward vm.swappiness kernel.hostname
cat /proc/sys/vm/swappiness
```

**4.2** Muuda parameetrit ajutiselt. Teises masinas (või oma arvutis) käivita `ping DEBIAN_IP` ja jälgi:

```bash
sudo sysctl -w net.ipv4.icmp_echo_ignore_all=1
# vaata, mis juhtub ping'iga
sudo sysctl -w net.ipv4.icmp_echo_ignore_all=0
```

**K9.** Mis juhtus `ping`-iga? Kas see on hea viis masina „peitmiseks“? Miks?

**4.3** Muuda püsivalt: luba pakettide edastamine ja vähenda saaleala kasutamist:

```bash
sudo nano /etc/sysctl.d/90-labor.conf
```

```text
net.ipv4.ip_forward = 1
vm.swappiness = 10
```

```bash
sudo sysctl --system | tail -5
sysctl net.ipv4.ip_forward vm.swappiness
```

Taaskäivita ja kontrolli, kas väärtused püsisid.

**K10.** Milleks on `net.ipv4.ip_forward = 1` vaja? Nimeta kaks olukorda.

---

## 5. osa. GRUB (konsoolis)

**5.1** Uuri GRUB-i seadistust:

```bash
cat /etc/default/grub
ls -l /boot/grub/grub.cfg
head -20 /boot/grub/grub.cfg
```

**K11.** Miks ei tohi faili `/boot/grub/grub.cfg` käsitsi muuta? Kust see tuleb?

**5.2** Muuda GRUB-i seadistust: menüü ooteaeg 15 sekundit ja eemalda parameeter `quiet`, et näeksid alglaadimise teateid:

```bash
sudo cp /etc/default/grub /etc/default/grub.varu
sudo nano /etc/default/grub
```

```text
GRUB_TIMEOUT=15
GRUB_CMDLINE_LINUX_DEFAULT=""
```

```bash
sudo update-grub
```

**5.3** Ava masina **konsool** ja taaskäivita (`sudo systemctl reboot`). Jälgi GRUB-i menüüd ja alglaadimise teateid. Uuri menüüd „Advanced options for Debian“.

**K12.** Mida näitas menüü „Advanced options“? Mis vahe oli alglaadimisel nüüd võrreldes `quiet` parameetriga?

**5.4** Taasta algne seadistus (`sudo cp /etc/default/grub.varu /etc/default/grub && sudo update-grub`) või jäta ooteaeg 15 sekundiks - see teeb järgmised osad lihtsamaks.

---

## 6. osa. Taastamis- ja hädaolukorra režiim (konsoolis)

**6.1** Taastamisrežiimi sisenemiseks peab juurkasutajal olema parool. Kontrolli ja vajadusel määra:

```bash
sudo passwd -S root
sudo passwd root
```

**6.2** Taaskäivita, vajuta GRUB-i menüüs **e**, lisa rea `linux` lõppu `systemd.unit=rescue.target` ja vajuta **Ctrl+X**.

Taastamisrežiimis uuri:

```bash
systemctl list-units --type=service --state=running
ip -br address
findmnt /
exit
```

**K13.** Millised teenused taastamisrežiimis töötasid? Kas võrk töötas? Kas juurfailisüsteem oli kirjutatav? Mis juhtus pärast `exit`-i?

**6.3** Riku süsteem: lisa faili `/etc/fstab` olematu ketas **ilma** valikuta `nofail`:

```bash
sudo cp /etc/fstab /etc/fstab.varu
echo "UUID=00000000-0000-0000-0000-000000000000 /mnt/olematu ext4 defaults 0 2" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo systemctl reboot
```

**6.4** Jälgi konsoolis alglaadimist. Pärast ooteaega (kuni 90 sekundit) satub süsteem **hädaolukorra režiimi**. Logi sisse juurkasutaja parooliga ja paranda viga:

```bash
journalctl -xb -p err | tail -20
findmnt /
mount -o remount,rw /
nano /etc/fstab               # kustuta vigane rida (või: cp /etc/fstab.varu /etc/fstab)
systemctl daemon-reload
systemctl default
```

**K14.** Milline teade näitas logis vea põhjust? Miks oli vaja juurfailisüsteem kirjutatavaks haakida? Kuidas oleks valik `nofail` olukorda muutnud?

---

## 7. osa. Juurkasutaja parooli lähtestamine (konsoolis)

Kujutle, et oled unustanud nii juurkasutaja kui ka oma kasutaja parooli.

**7.1** Taaskäivita, vajuta GRUB-i menüüs **e**, lisa rea `linux` lõppu `init=/bin/bash` ja vajuta **Ctrl+X**.

**7.2** Uuri olukorda ja lähtesta paroolid:

```bash
whoami
echo $$
findmnt /
mount -o remount,rw /
passwd
passwd <sinu kasutaja>
sync
exec /sbin/init
```

**7.3** Logi sisse uue parooliga.

**K15.** Mis oli kesta PID ja miks? Miks küsis süsteem paroolita juurkasutaja õigusi? Mida see ütleb füüsilise ligipääsu ja konsoolile ligipääsu kohta? Kuidas saaks seda takistada?

**7.4** Kui juurkasutajal enne laborit parooli polnud, lukusta konto uuesti: `sudo passwd -l root`.

---

## 8. osa. Kernelite vahetamine (konsoolis)

**8.1** Paigalda teine kernel, et oleks, mille vahel valida. Lihtsaim on lubada Debiani **backports** hoidla ja paigaldada sealt uuem kernel. Vaata oma Debiani koodnime (`. /etc/os-release; echo $VERSION_CODENAME`) ja lisa hoidla:

```bash
. /etc/os-release
echo "deb http://deb.debian.org/debian ${VERSION_CODENAME}-backports main" | sudo tee /etc/apt/sources.list.d/backports.list
sudo apt update
apt policy linux-image-amd64
sudo apt install -t ${VERSION_CODENAME}-backports linux-image-amd64
ls /boot/vmlinuz-*
```

Kui backports'is uuemat kernelit pole (nt kohe pärast uue Debiani väljalaset), jäta see samm vahele - 9. osas kompileerid niikuinii teise kerneli - ja tee 8. osa pärast 9. osa.

**K16.** Millised kernelid on nüüd paigaldatud? Kumb neist käivitub järgmisel alglaadimisel ja miks?

**8.2** Leia GRUB-i menüükirjete nimed:

```bash
grep -E "^\s*(menuentry|submenu) '" /boot/grub/grub.cfg | cut -d"'" -f2
```

**8.3** Sea failis `/etc/default/grub` `GRUB_DEFAULT=saved` ja käivita `sudo update-grub`. Seejärel vali **ainult järgmiseks** alglaadimiseks vanem kernel:

```bash
sudo grub-reboot "Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux <vanem versioon>"
sudo systemctl reboot
```

Pärast alglaadimist: `uname -r`. Taaskäivita veel kord ja kontrolli uuesti.

**K17.** Milline kernel töötas esimese ja milline teise taaskäivituse järel? Milleks on `grub-reboot` kasulik serveris, millele sul füüsilist ligipääsu ei ole?

**8.4** Sea vanem kernel püsivalt vaikimisi kerneliks (`grub-set-default`), kontrolli taaskäivitusega ja taasta seejärel uusim kernel vaikimisi valikuks (`sudo grub-set-default 0`).

---

## 9. osa. Oma kerneli kompileerimine

Kompileerid kerneli lähtekoodist ja paigaldad selle `.deb` paketina. Kasuta võimalusel virtuaalmasinat, millel on rohkem protsessorituumi (Proxmoxis saab neid lisada *Hardware* → *Processors*).

**9.1** Paigalda tööriistad ja kontrolli ressursse:

```bash
sudo apt install build-essential bc bison flex libssl-dev libelf-dev \
    libncurses-dev dwarves cpio kmod rsync debhelper xz-utils wget
nproc
free -h
df -h ~
```

**9.2** Ava brauseris **kernel.org** ja vali uusim **longterm** versioon (või õpetaja antud versioon). Laadi see alla ja paki lahti:

```bash
mkdir -p ~/kernel && cd ~/kernel
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-<versioon>.tar.xz
tar -xf linux-<versioon>.tar.xz
cd linux-<versioon>
ls
du -sh .
```

**K18.** Millise versiooni valisid ja miks? Kui suur on lahtipakitud lähtekood? Nimeta kolm alamkataloogi ja arva, mida need sisaldavad (vihje: `drivers`, `fs`, `net`, `arch`).

**9.3** Seadista kernel. Kasuta aluseks töötava kerneli seadistust ja jäta alles ainult laaditud moodulid, et kompileerimine oleks kiirem:

```bash
cp /boot/config-$(uname -r) .config
make olddefconfig
make localmodconfig
scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
scripts/config --set-str SYSTEM_REVOCATION_KEYS ""
scripts/config --set-str LOCALVERSION "-<sinu nimi>"
make olddefconfig
grep -c "=m" .config
grep -c "=y" .config
```

`make localmodconfig` võib küsida mõne uue valiku kohta - vajuta Enter (vaikeväärtus).

**9.4** Ava menüüpõhine seadistus ja uuri seda (ära muuda midagi, kui pole kindel):

```bash
make menuconfig
```

Otsi klahviga **/** valikut `EXT4_FS` ja `BTRFS_FS`. Välju salvestades (**Exit** → **Yes**).

**K19.** Mitu valikut on seadistuses moodulina (`=m`) ja mitu sisse ehitatud (`=y`)? Kas `EXT4_FS` ja `BTRFS_FS` on sisse ehitatud, moodulina või välja jäetud? Miks võis `localmodconfig` jätta `BTRFS_FS` välja?

**9.5** Kompileeri. Kasuta `time`-i, et mõõta kestust, ja `tmux`-i (või konsooli), et SSH-ühenduse katkemine kompileerimist ei katkestaks:

```bash
sudo apt install tmux
tmux
time make -j$(nproc) bindeb-pkg
```

Kompileerimise ajal võid tmux-ist lahti ühenduda (**Ctrl+B**, siis **d**) ja hiljem tagasi tulla (`tmux attach`). Jälgi teises aknas koormust (`top`).

**9.6** Paigalda kernel:

```bash
ls -lh ~/kernel/*.deb
sudo apt install ~/kernel/linux-image-*-<sinu nimi>_*.deb
ls /boot
grep -E "^\s*menuentry '" /boot/grub/grub.cfg | cut -d"'" -f2
```

**K20.** Kui kaua kompileerimine kestis (`real` aeg) ja mitu protsessorituuma kasutasid? Millised `.deb` failid tekkisid? Milliseid faile lisas paigaldus kataloogi `/boot`?

**9.7** Taaskäivita (konsoolis) ja kontrolli:

```bash
uname -r
cat /proc/version
lsmod | wc -l
systemd-analyze
```

**9.8** Kontrolli, kas kõik töötab: võrk, SSH, kettad. Seejärel ühenda virtuaalmasinale mõni seade, mida enne polnud (nt Proxmoxis lisa USB-seade või uus võrgukaart muu mudeliga), ja vaata, kas sinu kernel tunneb selle ära (`dmesg`, `lsblk`, `ip link`).

**K21.** Kas sinu kernel töötas? Kuidas erines see distro kernelist (moodulite arv, alglaadimise aeg)? Mis on `localmodconfig` kasutamise risk?

**9.9** Lõpuks käivita uuesti distro kernel (GRUB-i „Advanced options“ või `grub-reboot`) ja eemalda oma kernel:

```bash
uname -r                                   # peab olema distro kernel
sudo apt remove linux-image-<versioon>-<sinu nimi>
rm -rf ~/kernel                            # vabasta kettaruum
```

---

## 10. osa. GRUB-i parandamine (konsoolis)

> [!WARNING]
> **Tee enne seda osa uus hetktõmmis!** Selles osas muudad masina käivitumatuks ja parandad selle paigaldusmeedialt.

**10.1** Kontrolli, kas masin kasutab BIOS-i või UEFI-t ja milline on süsteemiketas:

```bash
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "BIOS"
lsblk -f
sudo fdisk -l /dev/sda | head
```

**10.2** Riku alglaadija.

**BIOS** (Proxmoxi vaikimisi SeaBIOS): kirjuta üle ketta esimese sektori alglaadimiskood (esimesed 440 baiti). Partitsioonitabel jääb puutumata.

```bash
sudo dd if=/dev/zero of=/dev/sda bs=440 count=1
sync
```

**UEFI:** nimeta ümber GRUB-i kataloog EFI süsteempartitsioonil:

```bash
sudo mv /boot/efi/EFI/debian /boot/efi/EFI/debian.katki
```

Taaskäivita masin ja vaata konsooli.

**K22.** Mida masin käivitamisel näitas? Miks jäid andmed ja partitsioonitabel alles?

**10.3** **Parandus taastamisrežiimis.** Lisa Proxmoxis masinale Debiani netinst ISO (*Hardware* → *CD/DVD Drive* → *Edit*) ja käivita sellelt (käivitamisel **Esc** → vali CD). Vali *Advanced options* → *Rescue mode*, läbi keele- ja võrgusammud, vali juurfailisüsteem ja seejärel *Reinstall GRUB boot loader* → `/dev/sda`. Taaskäivita kõvakettalt.

> [!NOTE]
> UEFI puhul vali taastamisrežiimis *Execute a shell in /dev/sda…* ja käivita `grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=debian` ning `update-grub`. Seejärel kustuta kataloog `debian.katki`.

**10.4** **Parandus `chroot`-iga.** Riku alglaadija uuesti (punkt 11.2), käivita jälle paigaldusmeedialt taastamisrežiim, aga vali seekord *Do not use a root file system* ja *Execute a shell in the installer environment*. Haagi süsteem ja paranda GRUB käsitsi:

```bash
mount /dev/sda1 /target                # sinu juurpartitsioon (vaata lsblk või blkid)
mount --bind /dev /target/dev
mount --bind /proc /target/proc
mount --bind /sys /target/sys
chroot /target /bin/bash
grub-install /dev/sda
update-grub
exit
umount /target/sys /target/proc /target/dev /target
reboot
```

Kui sinu Debianil on eraldi `/boot` või `/var` partitsioon, haagi need enne `chroot`-i (`mount /dev/sdaX /target/boot`). Eemalda ISO ja kontrolli, et masin käivitub.

**K23.** Miks seoti enne `chroot`-i kataloogid `/dev`, `/proc` ja `/sys`? Mis vahe on variantidel *Reinstall GRUB boot loader* ja käsitsi `chroot`-il? Millal on vaja käsitsi varianti?

---

## 11. osa. systemd süvitsi

Selles osas kasutad teooria punkti 10.11 näiteid. Kõik failid lähevad kataloogi `/etc/systemd/system/` ja pärast iga muudatust käivita `sudo systemctl daemon-reload`.

**11.1 Sõltuvused**

```bash
systemctl list-dependencies multi-user.target | head -20
systemctl list-dependencies --reverse ssh.service
systemctl show -p Wants,Requires,After,Type ssh.service
systemctl show -p Type chrony.service cron.service
```

**K24.** Mis on `ssh.service` seadete `Wants`/`Requires` ja `After` väärtused ning mille poolest need erinevad? Mis juhtuks, kui teenusel oleks `Requires=mariadb.service`, kuid puuduks `After=mariadb.service`? Millist `Type=` kasutavad `ssh`, `chrony` ja `cron`?

**11.2 Mall** - loo teooria näite järgi `tervitaja@.service` ja käivita kaks eksemplari:

```bash
sudo systemctl daemon-reload
sudo systemctl start tervitaja@mari tervitaja@jaan
systemctl list-units 'tervitaja@*'
journalctl -u 'tervitaja@*' --since "1 min ago"
ps -o user,pid,cmd -C bash | grep Tere
sudo systemctl stop 'tervitaja@*'
```

**K25.** Mitu protsessi töötas ja millise kasutajana (`DynamicUser=yes`)? Kas see kasutaja on failis `/etc/passwd`? Too üks näide mallist, mida süsteem ise kasutab (`systemctl list-units '*@*'`).

**11.3 Pesa aktiveerimine** - loo `kell.socket` ja `kell@.service` teooria järgi:

```bash
sudo apt install -y netcat-openbsd
sudo systemctl daemon-reload
sudo systemctl enable --now kell.socket
sudo ss -tlnp | grep 2000
systemctl list-units 'kell@*'
nc localhost 2000
nc localhost 2000
journalctl -u 'kell@*' --since "5 min ago" | tail
```

**K26.** Milline protsess kuulas pordil 2000 enne esimest ühendust? Mitu `kell@` eksemplari tekkis ja kas need jäid tööle? Nimeta kaks pesa aktiveerimise eelist.

**11.4 Failide jälgimine** - loo `tootle.path` ja `tootle.service` teooria järgi:

```bash
sudo mkdir -p /srv/sisend /srv/valmis
sudo systemctl daemon-reload
sudo systemctl enable --now tootle.path
sudo touch /srv/sisend/aruanne1.txt /srv/sisend/aruanne2.txt
sleep 2
ls /srv/sisend /srv/valmis
journalctl -u tootle.service --since "5 min ago"
```

**K27.** Mitu korda teenus käivitus ja mida see logis? Miks peab teenus kataloogi tühjendama? Too üks näide, kus `.path` üksus oleks halduses kasulik.

**11.5 Teenuse karastamine** - loo karastamata teenus:

```bash
sudo mkdir -p /var/lib/aeg
sudo tee /etc/systemd/system/aeg.service <<'EOT'
[Unit]
Description=Kirjutab kellaaja faili

[Service]
Type=exec
ExecStart=/bin/bash -c 'while true; do date >> /var/lib/aeg/aeg.txt; sleep 30; done'

[Install]
WantedBy=multi-user.target
EOT
sudo systemctl daemon-reload
sudo systemctl enable --now aeg.service
systemd-analyze security aeg.service | tail -3
```

Lisa seejärel karastus drop-in failina (`sudo systemctl edit aeg.service`):

```ini
[Service]
DynamicUser=yes
StateDirectory=aeg
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
PrivateDevices=yes
PrivateNetwork=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
CapabilityBoundingSet=
RestrictAddressFamilies=AF_UNIX
RestrictNamespaces=yes
RestrictRealtime=yes
RestrictSUIDSGID=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
SystemCallArchitectures=native
SystemCallFilter=@system-service
UMask=0077
```

```bash
sudo rm -rf /var/lib/aeg                 # StateDirectory loob kataloogi ise
sudo systemctl restart aeg.service
systemctl status aeg.service
sleep 35; sudo tail -3 /var/lib/aeg/aeg.txt
systemd-analyze security aeg.service | tail -3
sudo systemd-run --wait -p ProtectSystem=strict -p DynamicUser=yes touch /etc/proov
```

**K28.** Mis oli teenuse turvahinne enne ja pärast karastamist? Kas teenus töötas edasi? Kus asub `aeg.txt` nüüd tegelikult (`ls -l /var/lib/ | grep aeg`)? Miks ebaõnnestus `systemd-run` katse?

**11.6 Tõrkeotsing** - loo kaks vigast teenust:

```bash
sudo tee /etc/systemd/system/vigane1.service <<'EOT'
[Service]
ExecStart=/usr/local/bin/olematu-programm
EOT
sudo tee /etc/systemd/system/vigane2.service <<'EOT'
[Service]
ExecStart=/bin/false
Restart=always
RestartSec=1
EOT
sudo systemctl daemon-reload
sudo systemctl start vigane1; systemctl status vigane1 | head -8
systemd-analyze verify /etc/systemd/system/vigane1.service
sudo systemctl start vigane2; sleep 10; systemctl status vigane2 | head -8
journalctl -xeu vigane2 | tail -15
sudo systemctl reset-failed vigane2
```

**K29.** Millise oleku ja koodi (`status=…`) näitas `vigane1` ning mida ütles `systemd-analyze verify`? Mis juhtus `vigane2`-ga umbes viie sekundi pärast ja miks? Mida teeb `reset-failed`?

---

## 12. osa. Kokkuvõte

**K30.** Täida tabel: millises alglaadimise etapis tekib probleem ja millise tööriista või meetodiga seda uurida/lahendada?

| Sümptom | Etapp | Uurimine / lahendus |
|---|---|---|
| Ekraanil on `grub rescue>` | | |
| *Kernel panic - not syncing: VFS: Unable to mount root fs* | | |
| „You are in emergency mode“ | | |
| Masin käivitub, kuid veebiserver ei tööta | | |
| Alglaadimine kestab 3 minutit | | |
| Uus kernel ei käivitu pärast uuendust | | |

---

## Koristamine

- Taasta failid `/etc/default/grub` ja `/etc/fstab` (kui veel tegemata) ning käivita `sudo update-grub`.
- Eemalda `/etc/sysctl.d/90-labor.conf` ja käivita `sudo sysctl --system`, kui õpetaja ei ole teisiti öelnud.
- Eemalda backports'i hoidla fail `/etc/apt/sources.list.d/backports.list`, kui sa seda enam ei vaja, ja sea `GRUB_DEFAULT=0`.
- Eemalda 11. osa harjutused: `sudo systemctl disable --now kell.socket tootle.path aeg.service`, kustuta failid `tervitaja@.service`, `kell.socket`, `kell@.service`, `tootle.*`, `aeg.service` (ja kataloog `aeg.service.d`), `vigane1.service`, `vigane2.service` kataloogist `/etc/systemd/system/` ning käivita `sudo systemctl daemon-reload`.
- Kui kõik töötab, kustuta laborieelne hetktõmmis (Proxmoxis *Snapshots* → *Remove*), et see ei võtaks ruumi.

---

## Lisaülesanne (valikuline)

1. Genereeri alglaadimise ajajoon pildina (`systemd-analyze plot > alglaadimine.svg`), kopeeri see oma arvutisse (`scp`) ja ava brauseris. Milline teenus on pudelikael?
2. Kaitse GRUB parooliga (vt Debiani wiki „GRUB“ või `man grub-mkpasswd-pbkdf2`), nii et menüü kirjete muutmine nõuab parooli. Proovi seejärel uuesti `init=/bin/bash` meetodit.
3. AlmaLinuxis: lähtesta juurkasutaja parool meetodiga `rd.break` (vt teooria punkt 10.9). Mis juhtub, kui jätad `touch /.autorelabel` tegemata?
4. Kompileeri kernel uuesti, kuid jäta `make menuconfig`-is välja kõik, mida sinu virtuaalmasin ei vaja (heli, Bluetooth, WiFi, ebavajalikud failisüsteemid). Kui väikeseks suudad kerneli (`/boot/vmlinuz-*`) ja initramfs-i teha nii, et masin endiselt käivitub?

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 10. Kuidas Linux töötab: alglaadimine ja kernel](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 10. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
