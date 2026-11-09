<!-- navigatsioon -->
[← Laboritöö 22. Linux töölaual, Kali ja WSL](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 23. Virtualiseerimine: KVM, Proxmox VE ja XCP-ng →](../moodul-23-virtualiseerimine/index.md)
<!-- /navigatsioon -->

# Moodul 22. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Too kolm põhjust, miks töölaua Linux on viimastel aastatel populaarsust kogunud.
2. Mis on digitaalne suveräänsus ja kuidas see seostub avatud tarkvaraga? Too üks näide Euroopa avalikust sektorist.
3. Mis vahe on distrol ja töölauakeskkonnal? Too kummastki kolm näidet.
4. Mis on Wayland ja mille poolest see erineb X11-st? Mis on XWayland?
5. Mis on sisselogimishaldur ja millise systemd eesmärgiga see käivitub?
6. Mis vahe on distro hoidla paketil, Flatpakil ja Snapil?
7. Mis on muutumatu (*immutable*) distro? Too kaks näidet.
8. Kuidas töötab Proton? Mis on mängimise peamine piirang Linuxis?
9. Milleks on `fwupd`?
10. Millised on töölaua Linuxi kaugtöölaua võimalused ja millega Proxmoxi VM-is töölaua kasutamine kõige mugavam on?
11. Mida on vaja Eesti ID-kaardi kasutamiseks Linuxis?
12. Mis on Kali Linux ja millised on selle kasutamise reeglid?
13. Mis vahe on WSL 1-l ja WSL 2-l? Mis on WSLg?
14. Kus asuvad WSL-is Windowsi failid ja kuidas pääseda Windowsist Linuxi failidele? Kuhu peaks projekte hoidma?
15. Miks ei sobi WSL kõigi selle kursuse laboritööde tegemiseks?

## Praktilised miniülesanded

1. Kirjuta käsk, mis näitab, kas sinu seanss kasutab Waylandi või X11-t.
2. Lisa Ubuntus Flathubi hoidla ja paigalda sealt LibreOffice (`org.libreoffice.LibreOffice`).
3. Lisa AlmaLinuxi serverile graafiline keskkond ja tee see vaikimisi käivituvaks.
4. Kirjuta PowerShelli käsud, mis paigaldavad WSL-i Ubuntu, näitavad paigaldatud distrosid ja peatavad kõik.
5. Kirjuta `/etc/wsl.conf` sisu, mis lülitab sisse systemd ja määrab vaikekasutajaks `mari`.

---

## Vastused

1. Mängud (Steam Deck, Proton, SteamOS); digitaalne suveräänsus ja avaliku sektori üleminekud; Windows 10 toe lõpp ja vanade arvutite taaskasutus; arendajate tööriistad.
2. Riigi või organisatsiooni võime ise otsustada oma andmete ja IT-süsteemide üle ilma liigse sõltuvuseta ühest (välis)tarnijast. Avatud tarkvara saab ise hallata, auditeerida ja edasi arendada. Näited: Schleswig-Holsteini üleminek LibreOffice'ile ja Linuxile, Prantsuse Gendarmerie Linuxi töölauad, Saksamaa openDesk.
3. Distro on terviklik operatsioonisüsteem (Ubuntu, Fedora, Linux Mint); töölauakeskkond on graafiline kasutajaliides (GNOME, KDE Plasma, Xfce). Sama distro võib pakkuda mitut töölauda.
4. Wayland on uus kuvaprotokoll, kus komposiitor joonistab ekraani ja rakendused ei näe üksteise aknaid ega sisendit - turvalisem ja sobib paremini uute ekraanidega. X11 on vana võrgupõhine protokoll. XWayland käivitab X11 rakendusi Waylandi seansis.
5. Graafiline sisselogimisekraan (GDM, SDDM, LightDM), mis käivitab valitud töölauaseansi; `graphical.target`.
6. Hoidla pakett tuleb distrolt ja uueneb koos süsteemiga; Flatpak ja Snap on distrost sõltumatud, uuemad ja liivakastis, kuid suuremad; Flatpaki peamine pood on Flathub, Snapi oma Canonicali Snap Store.
7. Süsteemi juurosa on ainult lugemiseks ja uuendatakse tervikuna, eelmisele versioonile saab tagasi minna. Näited: SteamOS, Fedora Silverblue, Bazzite.
8. Proton (Wine + DXVK/VKD3D) tõlgib Windowsi API ja DirectX-i kutsed Linuxi ja Vulkani kutseteks. Piirang: osa võistlusmängude petmisvastased süsteemid ei luba Linuxit.
9. Riistvara püsivara (UEFI, SSD, dokid, hiired jm) uuendamiseks Linuxist (LVFS teenus).
10. SPICE (Proxmoxi konsool koos `spice-vdagent`-iga), RDP (GNOME Remote Desktop, xrdp), VNC, RustDesk. Proxmoxis on mugavaim SPICE koos `virt-viewer`-iga või RDP.
11. ID-tarkvara (DigiDoc4, Web eID laiend) id.ee juhendi järgi, kaardilugeja ja teenus `pcscd`; VM-is USB-lugeja suunamine.
12. Debianil põhinev turvatestimise distro sadade tööriistadega. Kasutada ainult isoleeritud laboris või süsteemidega, mille testimiseks on luba; mitte igapäevase töölauana.
13. WSL 1 tõlkis Linuxi süsteemikutsed Windowsi omadeks; WSL 2 käitab päris Linuxi kernelit kerges VM-is (parem ühilduvus, Docker, systemd). WSLg võimaldab Linuxi graafilisi rakendusi Windowsi akendena.
14. Windowsi failid: `/mnt/c/...`; Linuxi failid Windowsist: `\\wsl.localhost\<distro>\...` või `explorer.exe .`. Projektid hoia Linuxi failisüsteemis (`~/`), sest üle piiri on failioperatsioonid aeglased.
15. WSL-il on Microsofti kernel ja virtuaalne riistvara: puuduvad GRUB, päris kettad ja partitsioonid, tavapärane võrguseadistus, tulemüür ja SELinux/AppArmor; teenused ei ole teistele masinatele lihtsalt kättesaadavad.

### Miniülesannete lahendused

```bash
echo $XDG_SESSION_TYPE
```

```bash
sudo apt install flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.libreoffice.LibreOffice
```

```bash
sudo dnf groupinstall "Server with GUI"
sudo systemctl set-default graphical.target
sudo reboot
```

```powershell
wsl --install -d Ubuntu
wsl --list --verbose
wsl --shutdown
```

```ini
[boot]
systemd=true

[user]
default=mari
```

<!-- navigatsioon -->
---

[← Laboritöö 22. Linux töölaual, Kali ja WSL](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 23. Virtualiseerimine: KVM, Proxmox VE ja XCP-ng →](../moodul-23-virtualiseerimine/index.md)
<!-- /navigatsioon -->
