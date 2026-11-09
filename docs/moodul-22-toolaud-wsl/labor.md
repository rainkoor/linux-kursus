<!-- navigatsioon -->
[← Moodul 22. Linux töölaual ja WSL](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 22. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 22. Linux töölaual, Kali ja WSL

| | |
|---|---|
| **Distrod** | Ubuntu Desktop 24.04 (HKHK Proxmoxi laboris graafiline Ubuntu VM), Kali Linux, Windows 11 (WSL) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Graafiline Ubuntu VM (2 vCPU, 4 GiB RAM, *Display*: SPICE või VirtIO-GPU), Kali VM isoleeritud laborivõrgus, Windows 11 arvuti või VM pesastatud virtualiseerimisega (6. osa). Oma arvutisse SPICE-i jaoks `virt-viewer` (valikuline) |
| **Eesmärk** | Tutvuda töölaua Linuxi ülesehituse ja haldusega, kasutada Kalit vastutustundlikult ja töötada Linuxiga Windowsi sees |

**Aruanne:** vasta küsimustele **K1–K20**.

> [!WARNING]
> Tee enne alustamist Ubuntu VM-ist **hetktõmmis**.

---

## 1. osa. Graafiline süsteem

**1.1** Logi Ubuntu töölauale sisse Proxmoxi konsooli kaudu (noVNC või SPICE). Ava terminal (**Ctrl+Alt+T**) ja uuri:

```bash
echo $XDG_SESSION_TYPE
echo $XDG_CURRENT_DESKTOP
loginctl
loginctl show-session $XDG_SESSION_ID -p Type -p Desktop
systemctl get-default
systemctl status gdm --no-pager
ps -e | grep -E "gnome-shell|Xwayland"
free -h
```

**K1.** Kas seanss on Wayland või X11? Milline programm on sisselogimishaldur? Kas töötab ka XWayland ja miks? Kui palju mälu töölaud kasutab?

**1.2** Paigalda VM-i külalisagendid ja vaata, mis muutub (SPICE-konsoolis: lõikelaud, akna suurus):

```bash
sudo apt install qemu-guest-agent spice-vdagent
sudo systemctl enable --now qemu-guest-agent
```

**K2.** Mida võimaldab `spice-vdagent`? Mida näed nüüd Proxmoxi VM-i *Summary* lehel (IP-aadressid)?

## 2. osa. Tarkvara: apt, Snap ja Flatpak

**2.1** Vaata, mis on juba paigaldatud:

```bash
snap list
apt list --installed 2>/dev/null | wc -l
```

**2.2** Paigalda sama programm (GIMP) kahel viisil:

```bash
sudo apt install gimp
sudo apt install flatpak gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub org.gimp.GIMP
apt policy gimp | head -3
flatpak info org.gimp.GIMP | grep -E "Version|Installed"
flatpak info --show-permissions org.gimp.GIMP
du -sh /var/lib/flatpak
```

**K3.** Võrdle versioone ja ruumikasutust. Milliseid õigusi Flatpaki GIMP saab? Kumb paigaldusviis on sinu arvates parem koolis kasutamiseks ja miks?

**2.3** Eemalda apt-i GIMP (`sudo apt remove gimp`) ja leia rakenduste menüüst, kas GIMP käivitub endiselt.

## 3. osa. Teine töölauakeskkond

**3.1** Paigalda kerge töölaud Xfce:

```bash
sudo apt install xfce4 xfce4-goodies
```

Kui küsitakse sisselogimishaldurit, jäta **gdm3**. Logi välja, vali sisselogimisekraanil (hammasratas) seanss *Xfce Session* ja logi sisse.

```bash
echo $XDG_SESSION_TYPE $XDG_CURRENT_DESKTOP
free -h
```

**K4.** Kas Xfce töötab Waylandis või X11-s? Võrdle mälukasutust GNOME-iga. Millal eelistaksid kergemat töölauda?

Logi tagasi GNOME-sse.

## 4. osa. Kaugtöölaud ja haldus

**4.1** Luba Ubuntus RDP: *Settings* → *System* → *Remote Desktop* → *Remote Login* (määra kasutajanimi ja parool). Ava tulemüür, kui see on sees:

```bash
sudo ss -tlpn | grep 3389
sudo ufw allow from VORK to any port 3389 proto tcp
```

Ühendu Windowsist (`mstsc`) või Linuxist (Remmina) aadressile `UBUNTU_IP`.

**K5.** Kas ühendus õnnestus? Mis on RDP eelis Proxmoxi konsooli ees ja mis on riskid, kui RDP port on internetist kättesaadav?

**4.2** Lisa virtuaalne PDF-printer ja prindi testleht:

```bash
sudo apt install printer-driver-cups-pdf
lpstat -p -d
echo "Tere, CUPS" | lp -d PDF
ls ~/PDF/
```

Ava ka CUPS-i veebiliides `http://localhost:631` Ubuntu brauseris.

**4.3** Kontrolli püsivara uuendusi ja automaatseid uuendusi:

```bash
fwupdmgr get-devices
systemctl status unattended-upgrades --no-pager
```

**4.4** Paigalda Timeshift, tee süsteemist hetktõmmis (rsync-režiim), paigalda mõni pakett (nt `cowsay`) ja taasta hetktõmmis:

```bash
sudo apt install timeshift
sudo timeshift --create --comments "enne katset"
sudo apt install cowsay
sudo timeshift --list
```

Taasta graafilisest liidesest (või `sudo timeshift --restore`) ja kontrolli, kas `cowsay` on pärast taaskäivitust alles.

**K6.** Mida Timeshift vaikimisi varundab ja mida mitte (vaata seadeid *Users*)? Mis vahe on Timeshiftil ja Proxmoxi hetktõmmisel?

**4.5** (Valikuline, vajab kaardilugejat ja ID-kaarti) Paigalda Eesti ID-tarkvara id.ee juhendi järgi, suuna USB-kaardilugeja VM-ile ja kontrolli:

```bash
pcsc_scan
```

Ava DigiDoc4 ja Firefoxis lehe id.ee kontrolliteenus.

**K7.** Kas kaart tuvastati? Milliseid pakette ja teenuseid paigaldusjuhend lisas?

## 5. osa. Kali Linux

> [!WARNING]
> **Tee see osa ainult isoleeritud laborivõrgus ja ainult masinatega, mille õpetaja on lubanud.**

**5.1** Logi Kali VM-i sisse, muuda vaikeparool ja uuenda:

```bash
passwd
sudo apt update && sudo apt full-upgrade -y
cat /etc/os-release
dpkg -l | grep -c "^ii"
apt-cache search kali-tools | head -20
```

**K8.** Millisel Debiani harul Kali põhineb? Mitu paketti on paigaldatud? Milliseid tööriistade rühmi (`kali-tools-*`) leidsid?

**5.2** Uuri laborivõrku (ainult oma masinad või õpetaja määratud sihtmärk):

```bash
ip -br a
sudo netdiscover -r VORK -P
sudo nmap -sV -O SIHT_IP
```

**K9.** Milliseid masinaid ja teenuseid leidsid? Kuidas tuvastas `nmap` operatsioonisüsteemi ja teenuste versioonid?

**5.3** Ava Ubuntu serveris (nt laboritöö 11 masinas) `sudo tail -f /var/log/auth.log` või `journalctl -f` ja käivita Kalist sama masina vastu `nmap -sS`. Vaata, kas skaneerimine jättis jälje logidesse (või fail2ban / ufw logidesse).

**K10.** Kas skaneerimist oli serveri poolelt näha? Miks peab testimiseks alati olema luba?

## 6. osa. WSL

Tee see osa oma Windows 11 arvutis või laboris Windowsi VM-is (vajab pesastatud virtualiseerimist, vt teooria punkt 22.9).

**6.1** Paigalda Debian (PowerShell administraatorina):

```powershell
wsl --list --online
wsl --install -d Debian
wsl --list --verbose
wsl --status
```

Loo esimesel käivitamisel kasutaja. Seejärel Debianis:

```bash
cat /etc/os-release
uname -r
ps -p 1 -o comm=
ip -br a
df -h /
```

**K11.** Mis kernel töötab (`uname -r`)? Kas PID 1 on `systemd` või `init`? Mis on WSL-i masina IP-aadress ja kuidas see erineb Windowsi omast?

**6.2** Kui PID 1 ei ole `systemd`, lülita see sisse (`/etc/wsl.conf`, punkt 22.9), käivita PowerShellis `wsl --shutdown` ja kontrolli uuesti `systemctl status`.

**6.3** Failid kahe süsteemi vahel:

```bash
ls /mnt/c/Users/
echo "WSL-ist" > ~/test.txt
explorer.exe .
notepad.exe ~/test.txt
```

PowerShellis:

```powershell
wsl -d Debian -- ls -la ~
Get-Content \\wsl.localhost\Debian\home\<kasutaja>\test.txt
```

**6.4** Võrdle failioperatsioonide kiirust Linuxi ja Windowsi failisüsteemis:

```bash
time (for i in $(seq 1000); do echo $i > ~/kiirus_$i; done); rm ~/kiirus_*
mkdir -p /mnt/c/Temp/wsl && time (for i in $(seq 1000); do echo $i > /mnt/c/Temp/wsl/kiirus_$i; done); rm -r /mnt/c/Temp/wsl
```

**K12.** Kui suur oli erinevus? Kuhu peaksid seega hoidma oma Giti projekte, kui töötad WSL-is?

**6.5** Käivita Linuxi graafiline programm (WSLg):

```bash
sudo apt install -y x11-apps gedit
xeyes &
gedit &
```

**6.6** Varunda ja klooni distro:

```powershell
wsl --shutdown
wsl --export Debian $env:USERPROFILE\debian-varu.tar
wsl --import DebianTest $env:USERPROFILE\WSL\DebianTest $env:USERPROFILE\debian-varu.tar
wsl -l -v
wsl -d DebianTest -- cat ~/test.txt
wsl --unregister DebianTest
```

**K13.** Mis on `wsl --export` faili suurus? Millise kasutajana DebianTest käivitus ja miks (vihje: `[user]` jaotis `wsl.conf`-is)? Mida teeb `--unregister` ja miks peab sellega ettevaatlik olema?

**6.7** Kasuta WSL-i kursuse tööriistana: paigalda Debianis `git`, `ansible`, `shellcheck` ja ühendu SSH-ga oma laborimasinasse.

```bash
sudo apt install -y git ansible shellcheck openssh-client
ssh-keygen -t ed25519
ssh kasutaja@SERVER_IP
```

**K14.** Milliseid kursuse mooduleid saaks WSL-is täielikult läbi teha ja milliseid mitte? Too kummastki vähemalt kaks näidet ja põhjenda.

## 7. osa. Kokkuvõte

**K15.** Joonista Ubuntu töölaua kihid riistvarast rakendusteni ja märgi, millised programmid sinu masinas igal kihil töötavad.

**K16.** Kirjelda, kuidas Proton võimaldab Windowsi mänge Linuxis mängida. Mis on SteamOS-i kui muutumatu distro eelised tavakasutajale?

**K17.** Kool kaalub ühe arvutiklassi viimist Windowsilt Linuxile. Too kolm argumenti poolt ja kolm vastu (nt tarkvara, koolitus, haldus, kulud, sõltumatus, eksamid ja ID-kaart).

**K18.** Milliseid kooli tunnis kasutatavaid programme saab Linuxis kasutada otse, milliseid alternatiiviga ja milliseid ainult brauseris või virtuaalmasinas?

**K19.** Millal kasutaksid Linuxit WSL-is, millal virtuaalmasinas ja millal otse riistvaral? Too igaühe kohta näide.

**K20.** Miks ei soovitata Kalit igapäevaseks töölauaks?

---

## Lisaülesanne (valikuline)

1. **Live-USB:** tee Ubuntu või Linux Mint live-USB (Ventoy, Balena Etcher või `dd`) ja käivita sellelt oma arvuti. Kas WiFi, heli, ekraan ja klaviatuuri eesti paigutus töötavad?
2. **Bazzite või SteamOS:** paigalda virtuaalmasinasse muutumatu distro (Bazzite, Fedora Silverblue). Uuri `rpm-ostree status`, tee uuendus ja proovi eelmisele versioonile tagasi minna.
3. **Steam:** kui sul on Linuxi arvuti graafikakaardiga, paigalda Steam, luba Proton ja proovi mõnda mängu. Vaata selle hinnangut ProtonDB-s.
4. **Mitu distrot WSL-is:** paigalda WSL-i ka AlmaLinux, tee mõlemas sama ülesanne (nt paigalda `nginx` ja ava see Windowsi brauseris `http://localhost`) ja võrdle käske.

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 22. Linux töölaual ja WSL](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 22. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
