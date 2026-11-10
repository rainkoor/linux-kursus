<!-- navigatsioon -->
[← Laboritöö 10. Alglaadimine, kernel ja taastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 11. Turvalisus ja logid →](../moodul-11-turvalisus-logid/index.md)
<!-- /navigatsioon -->

# Moodul 10. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Nimeta Linuxi alglaadimise etapid õiges järjekorras.

<details>
<summary>Vastus</summary>

Püsivara (UEFI/BIOS) → alglaadija (GRUB) → kernel ja initramfs → systemd (PID 1) → teenused ja sisselogimine.

</details>

**2.** Mis vahe on BIOS-il ja UEFI-l? Kuidas teada saada, kumba süsteem kasutas?

<details>
<summary>Vastus</summary>

BIOS on vanem püsivara, mis kasutab tavaliselt MBR-i ja laadib alglaadija ketta esimestest sektoritest. UEFI on tänapäevane standard, kasutab GPT-d, alglaadija on fail EFI süsteempartitsioonil ja toetab turvalist alglaadimist. Kontroll: kui kataloog `/sys/firmware/efi` on olemas, käivitus süsteem UEFI-ga.

</details>

**3.** Milline fail tuleb GRUB-i seadistamiseks muuta ja millise käsuga muudatus Debianis rakendada?

<details>
<summary>Vastus</summary>

`/etc/default/grub`, seejärel `sudo update-grub`.

</details>

**4.** Kuidas muuta kerneli parameetreid ainult üheks alglaadimiseks?

<details>
<summary>Vastus</summary>

GRUB-i menüüs vajuta **e**, lisa parameeter rea `linux` lõppu ja käivita **Ctrl+X**-ga.

</details>

**5.** Mis on initramfs ja miks seda vaja on?

<details>
<summary>Vastus</summary>

Väike ajutine failisüsteem, mis laaditakse koos kerneliga mällu ja sisaldab juurfailisüsteemi haakimiseks vajalikke draivereid ja tööriistu (nt LVM, RAID, krüpteering).

</details>

**6.** Miks jätab pakihaldur kerneli uuendamisel alles ka eelmise kerneli?

<details>
<summary>Vastus</summary>

Et saaks GRUB-i menüüst valida vana kerneli, kui uus ei käivitu.

</details>

**7.** Mis vahe on eesmärkidel `rescue.target` ja `emergency.target`?

<details>
<summary>Vastus</summary>

`rescue.target` haagib kõik failisüsteemid ja käivitab põhiteenused (ilma võrguta). `emergency.target` haagib ainult juurfailisüsteemi (sageli ainult lugemiseks) ega käivita peaaegu midagi.

</details>

**8.** Kuidas teada saada, milline teenus alglaadimist kõige rohkem aeglustab?

<details>
<summary>Vastus</summary>

`systemd-analyze blame` (teenuste käivitusajad) ja `systemd-analyze critical-chain` (tegelik pudelikael).

</details>

**9.** Mis on `/proc` ja `/sys`? Kas need asuvad kettal?

<details>
<summary>Vastus</summary>

Virtuaalsed failisüsteemid, mille sisu genereerib kernel lugemise hetkel. Kettal need ei asu. `/proc` sisaldab protsesside ja kerneli infot, `/sys` seadmete ja draiverite infot.

</details>

**10.** Mis on kerneli moodul? Kuidas laadida ja eemaldada moodulit?

<details>
<summary>Vastus</summary>

Kerneli osa (nt draiver), mida saab laadida ja eemaldada töö ajal. Laadimine `modprobe nimi`, eemaldamine `modprobe -r nimi`.

</details>

**11.** Mida takistab rida `blacklist moodul` failis `/etc/modprobe.d/`?

<details>
<summary>Vastus</summary>

Mooduli **automaatset** laadimist (nt riistvara tuvastamisel aliase järgi). Käsitsi `modprobe nimi` laadib selle siiski.

</details>

**12.** Kuidas muuta kerneli parameetrit nii, et muudatus jääb püsima ka pärast taaskäivitust?

<details>
<summary>Vastus</summary>

Loo fail kataloogi `/etc/sysctl.d/` (nt `90-minu.conf`) reaga `parameeter = väärtus` ja käivita `sudo sysctl --system`.

</details>

**13.** Süsteem käivitub hädaolukorra režiimis. Mis on levinuim põhjus ja kuidas seda parandada?

<details>
<summary>Vastus</summary>

Vigane `/etc/fstab` (olematu seade ilma `nofail`-ita). Logi sisse juurkasutajana, haagi juurfailisüsteem kirjutatavaks (`mount -o remount,rw /`), paranda fstab ja käivita `systemctl default`.

</details>

**14.** Kirjelda juurkasutaja parooli lähtestamist Debianis.

<details>
<summary>Vastus</summary>

GRUB-is vajuta **e**, lisa rea `linux` lõppu `init=/bin/bash`, käivita **Ctrl+X**. Kestas: `mount -o remount,rw /`, `passwd`, `sync`, `exec /sbin/init`.

</details>

**15.** Miks tuleb AlmaLinuxis pärast parooli lähtestamist käivitada `touch /.autorelabel`?

<details>
<summary>Vastus</summary>

SELinux märgistab iga faili. `passwd` loob faili `/etc/shadow` uuesti ilma õige SELinuxi märgiseta, mistõttu sisselogimine võib ebaõnnestuda. `/.autorelabel` paneb süsteemi järgmisel alglaadimisel kõik failid uuesti märgistama.

</details>

**16.** Kuidas käivitada Debianis vanem kernel ainult üheks korraks? Mis seadistus on selleks vajalik?

<details>
<summary>Vastus</summary>

Failis `/etc/default/grub` peab olema `GRUB_DEFAULT=saved` (ja `update-grub` käivitatud). Seejärel `sudo grub-reboot "Advanced options for Debian GNU/Linux>…kirje nimi…"` ja taaskäivitus.

</details>

**17.** Mida teevad käsud `make olddefconfig`, `make localmodconfig` ja `make bindeb-pkg`?

<details>
<summary>Vastus</summary>

`olddefconfig` - võtab aluseks olemasoleva `.config`-i ja annab uutele valikutele vaikeväärtused; `localmodconfig` - jätab moodulitest alles ainult praegu laaditud; `bindeb-pkg` - kompileerib kerneli ja loob sellest `.deb` paketid.

</details>

**18.** Miks on parem paigaldada isekompileeritud kernel `.deb` paketina kui käsuga `make install`?

<details>
<summary>Vastus</summary>

Pakihaldur teab kernelist: selle saab puhtalt eemaldada (`apt remove`), paigaldamisel genereeritakse automaatselt initramfs ja GRUB-i kirje ning paketti saab kopeerida ja paigaldada teistesse masinatesse.

</details>

**19.** Masin näitab `grub rescue>`. Kirjelda kahte viisi GRUB-i parandamiseks.

<details>
<summary>Vastus</summary>

Debiani paigaldusmeedia taastamisrežiim → *Reinstall GRUB boot loader*; või live-meedia: haagi juurfailisüsteem kataloogi `/mnt`, seo `/dev`, `/proc`, `/sys`, `/run`, `chroot /mnt`, `grub-install /dev/sda`, `update-grub`.

</details>

**20.** Miks seotakse enne `chroot`-i kataloogid `/dev`, `/proc` ja `/sys`? Mida tuleb lisaks teha LVM-iga süsteemis?

<details>
<summary>Vastus</summary>

`chroot`-i sees töötavad programmid vajavad seadmefaile ja kerneli liideseid, mida tühi kataloog ei sisalda. LVM-i puhul tuleb enne haakimist köitegrupid aktiveerida: `vgscan`, `vgchange -ay`.

</details>

**21.** Mis vahe on `Requires=` ja `After=` seadetel? Miks on vaja `Wants=network-online.target` ja `After=network-online.target`, mitte ainult `network.target`?

<details>
<summary>Vastus</summary>

`Requires=` on sõltuvus (käivita ka see; kui see ebaõnnestub, ebaõnnestu ka ise), `After=` ainult järjekord. Ilma `After`-ita käivitatakse mõlemad korraga. `network.target` tähendab ainult võrguhalduse alustamist; `network-online.target` ootab, kuni võrk on päriselt kasutatav - see tuleb `Wants`-iga tõmmata ja `After`-iga oodata.

</details>

**22.** Millal kasutad `Type=oneshot` ja millal `Type=notify`? Mida teeb `RemainAfterExit=yes`?

<details>
<summary>Vastus</summary>

`oneshot` - ühekordne töö, mis lõpetab (varundus, taimeri teenus); systemd ootab lõpetamist. `notify` - programm teatab ise, et on valmis (nt nginx, PostgreSQL), kõige täpsem. `RemainAfterExit=yes` jätab oneshot-teenuse pärast lõpetamist olekusse `active` (nt seadistuse rakendamine).

</details>

**23.** Mis on systemd mall (`nimi@.service`) ja pesa aktiveerimine? Too kummagi kohta üks näide.

<details>
<summary>Vastus</summary>

Mall on üksuse fail, millest käivitatakse mitu eksemplari, `%i` asendub eksemplari nimega (`getty@tty1`, `wg-quick@wg0`). Pesa aktiveerimisel kuulab systemd porti ja käivitab teenuse alles ühenduse saabumisel (`ssh.socket` Ubuntus, `kell.socket` laboris).

</details>

**24.** Mida teevad `DynamicUser=yes`, `ProtectSystem=strict` ja `NoNewPrivileges=yes`? Kuidas hinnata teenuse turvalisust?

<details>
<summary>Vastus</summary>

`DynamicUser` - teenus töötab ajutise kasutajana; `ProtectSystem=strict` - failisüsteem on teenusele ainult lugemiseks; `NoNewPrivileges` - teenus ei saa õigusi juurde (SUID). Hinnang: `systemd-analyze security teenus` (0-10, väiksem parem) koos soovitustega.

</details>

**25.** Teenus näitab `status=203/EXEC` ja teine teatab „Start request repeated too quickly“. Mida need tähendavad ja kuidas edasi uurid?

<details>
<summary>Vastus</summary>

`203/EXEC` - `ExecStart` programmi ei leitud või see pole käivitatav. „Repeated too quickly“ - teenus jooksis korduvalt kokku ja ületas `StartLimitBurst`-i. Uuri `journalctl -xeu teenus` (esimene viga), `systemctl cat`, `systemd-analyze verify`; pärast parandust `systemctl reset-failed` ja uuesti käivitamine.

</details>

**26.** Mis on udev ja mida see teeb, kui ühendad masinaga USB-ketta? Kuidas näed seadme omadusi, mille järgi saab udev reegli kirjutada?

<details>
<summary>Vastus</summary>

udev (`systemd-udevd`) saab kernelilt sündmuse uue seadme kohta, laadib vajaliku mooduli, loob seadmefaili kataloogi `/dev` ja püsivad nimed (`/dev/disk/by-uuid/` jt) ning käivitab reeglid kataloogidest `/usr/lib/udev/rules.d/` ja `/etc/udev/rules.d/`. Omadused: `udevadm info /dev/sdb`; sündmusi saab jälgida käsuga `udevadm monitor`.

</details>

## Praktilised miniülesanded

**1.** Leia ühe käsuga, mitu sekundit masin on töötanud (failist `/proc`).

<details>
<summary>Lahendus</summary>

```bash
cut -d' ' -f1 /proc/uptime
```

</details>

**2.** Leia kõik kerneli moodulid, mille nimes on `virtio`, ja nende suurused.

<details>
<summary>Lahendus</summary>

```bash
lsmod | grep virtio
```

</details>

**3.** Kuva kolm teenust, mille käivitamine võttis kõige kauem aega.

<details>
<summary>Lahendus</summary>

```bash
systemd-analyze blame | head -3
```

</details>

**4.** Kuva eelmise alglaadimise vead.

<details>
<summary>Lahendus</summary>

```bash
journalctl -b -1 -p err
```

</details>

**5.** Muuda püsivalt `vm.swappiness` väärtuseks 20 ja kontrolli tulemust.

<details>
<summary>Lahendus</summary>

```bash
echo "vm.swappiness = 20" | sudo tee /etc/sysctl.d/90-swappiness.conf
sudo sysctl --system && sysctl vm.swappiness
```

</details>

**6.** Lisa Debianis kõigile kernelikirjetele püsivalt parameeter `nomodeset`.

<details>
<summary>Lahendus</summary>

Muuda failis `/etc/default/grub` rida `GRUB_CMDLINE_LINUX="nomodeset"` ja käivita `sudo update-grub`. Kontrolli pärast taaskäivitust käsuga `cat /proc/cmdline`. (`GRUB_CMDLINE_LINUX` kehtib kõigile kirjetele, ka taastamisrežiimile, `GRUB_CMDLINE_LINUX_DEFAULT` ainult tavalisele käivitusele.)

</details>

<!-- navigatsioon -->
---

[← Laboritöö 10. Alglaadimine, kernel ja taastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 11. Turvalisus ja logid →](../moodul-11-turvalisus-logid/index.md)
<!-- /navigatsioon -->
