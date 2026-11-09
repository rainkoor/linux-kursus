<!-- navigatsioon -->
[← Laboritöö 10. Alglaadimine, kernel ja taastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 11. Turvalisus ja logid →](../moodul-11-turvalisus-logid/index.md)
<!-- /navigatsioon -->

# Moodul 10. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Nimeta Linuxi alglaadimise etapid õiges järjekorras.
2. Mis vahe on BIOS-il ja UEFI-l? Kuidas teada saada, kumba süsteem kasutas?
3. Milline fail tuleb GRUB-i seadistamiseks muuta ja millise käsuga muudatus Debianis rakendada?
4. Kuidas muuta kerneli parameetreid ainult üheks alglaadimiseks?
5. Mis on initramfs ja miks seda vaja on?
6. Miks jätab pakihaldur kerneli uuendamisel alles ka eelmise kerneli?
7. Mis vahe on eesmärkidel `rescue.target` ja `emergency.target`?
8. Kuidas teada saada, milline teenus alglaadimist kõige rohkem aeglustab?
9. Mis on `/proc` ja `/sys`? Kas need asuvad kettal?
10. Mis on kerneli moodul? Kuidas laadida ja eemaldada moodulit?
11. Mida takistab rida `blacklist moodul` failis `/etc/modprobe.d/`?
12. Kuidas muuta kerneli parameetrit nii, et muudatus jääb püsima ka pärast taaskäivitust?
13. Süsteem käivitub hädaolukorra režiimis. Mis on levinuim põhjus ja kuidas seda parandada?
14. Kirjelda juurkasutaja parooli lähtestamist Debianis.
15. Miks tuleb AlmaLinuxis pärast parooli lähtestamist käivitada `touch /.autorelabel`?
16. Kuidas käivitada Debianis vanem kernel ainult üheks korraks? Mis seadistus on selleks vajalik?
17. Mida teevad käsud `make olddefconfig`, `make localmodconfig` ja `make bindeb-pkg`?
18. Miks on parem paigaldada isekompileeritud kernel `.deb` paketina kui käsuga `make install`?
19. Masin näitab `grub rescue>`. Kirjelda kahte viisi GRUB-i parandamiseks.
20. Miks seotakse enne `chroot`-i kataloogid `/dev`, `/proc` ja `/sys`? Mida tuleb lisaks teha LVM-iga süsteemis?
21. Mis vahe on `Requires=` ja `After=` seadetel? Miks on vaja `Wants=network-online.target` ja `After=network-online.target`, mitte ainult `network.target`?
22. Millal kasutad `Type=oneshot` ja millal `Type=notify`? Mida teeb `RemainAfterExit=yes`?
23. Mis on systemd mall (`nimi@.service`) ja pesa aktiveerimine? Too kummagi kohta üks näide.
24. Mida teevad `DynamicUser=yes`, `ProtectSystem=strict` ja `NoNewPrivileges=yes`? Kuidas hinnata teenuse turvalisust?
25. Teenus näitab `status=203/EXEC` ja teine teatab „Start request repeated too quickly“. Mida need tähendavad ja kuidas edasi uurid?

## Praktilised miniülesanded

1. Leia ühe käsuga, mitu sekundit masin on töötanud (failist `/proc`).
2. Leia kõik kerneli moodulid, mille nimes on `virtio`, ja nende suurused.
3. Kuva kolm teenust, mille käivitamine võttis kõige kauem aega.
4. Kuva eelmise alglaadimise vead.
5. Muuda püsivalt `vm.swappiness` väärtuseks 20 ja kontrolli tulemust.
6. Lisa Debianis kõigile kernelikirjetele püsivalt parameeter `nomodeset`.

---

## Vastused

1. Püsivara (UEFI/BIOS) → alglaadija (GRUB) → kernel ja initramfs → systemd (PID 1) → teenused ja sisselogimine.
2. BIOS on vanem püsivara, mis kasutab tavaliselt MBR-i ja laadib alglaadija ketta esimestest sektoritest. UEFI on tänapäevane standard, kasutab GPT-d, alglaadija on fail EFI süsteempartitsioonil ja toetab turvalist alglaadimist. Kontroll: kui kataloog `/sys/firmware/efi` on olemas, käivitus süsteem UEFI-ga.
3. `/etc/default/grub`, seejärel `sudo update-grub`.
4. GRUB-i menüüs vajuta **e**, lisa parameeter rea `linux` lõppu ja käivita **Ctrl+X**-ga.
5. Väike ajutine failisüsteem, mis laaditakse koos kerneliga mällu ja sisaldab juurfailisüsteemi haakimiseks vajalikke draivereid ja tööriistu (nt LVM, RAID, krüpteering).
6. Et saaks GRUB-i menüüst valida vana kerneli, kui uus ei käivitu.
7. `rescue.target` haagib kõik failisüsteemid ja käivitab põhiteenused (ilma võrguta). `emergency.target` haagib ainult juurfailisüsteemi (sageli ainult lugemiseks) ega käivita peaaegu midagi.
8. `systemd-analyze blame` (teenuste käivitusajad) ja `systemd-analyze critical-chain` (tegelik pudelikael).
9. Virtuaalsed failisüsteemid, mille sisu genereerib kernel lugemise hetkel. Kettal need ei asu. `/proc` sisaldab protsesside ja kerneli infot, `/sys` seadmete ja draiverite infot.
10. Kerneli osa (nt draiver), mida saab laadida ja eemaldada töö ajal. Laadimine `modprobe nimi`, eemaldamine `modprobe -r nimi`.
11. Mooduli **automaatset** laadimist (nt riistvara tuvastamisel aliase järgi). Käsitsi `modprobe nimi` laadib selle siiski.
12. Loo fail kataloogi `/etc/sysctl.d/` (nt `90-minu.conf`) reaga `parameeter = väärtus` ja käivita `sudo sysctl --system`.
13. Vigane `/etc/fstab` (olematu seade ilma `nofail`-ita). Logi sisse juurkasutajana, haagi juurfailisüsteem kirjutatavaks (`mount -o remount,rw /`), paranda fstab ja käivita `systemctl default`.
14. GRUB-is vajuta **e**, lisa rea `linux` lõppu `init=/bin/bash`, käivita **Ctrl+X**. Kestas: `mount -o remount,rw /`, `passwd`, `sync`, `exec /sbin/init`.
15. SELinux märgistab iga faili. `passwd` loob faili `/etc/shadow` uuesti ilma õige SELinuxi märgiseta, mistõttu sisselogimine võib ebaõnnestuda. `/.autorelabel` paneb süsteemi järgmisel alglaadimisel kõik failid uuesti märgistama.

16. Failis `/etc/default/grub` peab olema `GRUB_DEFAULT=saved` (ja `update-grub` käivitatud). Seejärel `sudo grub-reboot "Advanced options for Debian GNU/Linux>…kirje nimi…"` ja taaskäivitus.
17. `olddefconfig` - võtab aluseks olemasoleva `.config`-i ja annab uutele valikutele vaikeväärtused; `localmodconfig` - jätab moodulitest alles ainult praegu laaditud; `bindeb-pkg` - kompileerib kerneli ja loob sellest `.deb` paketid.
18. Pakihaldur teab kernelist: selle saab puhtalt eemaldada (`apt remove`), paigaldamisel genereeritakse automaatselt initramfs ja GRUB-i kirje ning paketti saab kopeerida ja paigaldada teistesse masinatesse.
19. Debiani paigaldusmeedia taastamisrežiim → *Reinstall GRUB boot loader*; või live-meedia: haagi juurfailisüsteem kataloogi `/mnt`, seo `/dev`, `/proc`, `/sys`, `/run`, `chroot /mnt`, `grub-install /dev/sda`, `update-grub`.
20. `chroot`-i sees töötavad programmid vajavad seadmefaile ja kerneli liideseid, mida tühi kataloog ei sisalda. LVM-i puhul tuleb enne haakimist köitegrupid aktiveerida: `vgscan`, `vgchange -ay`.
21. `Requires=` on sõltuvus (käivita ka see; kui see ebaõnnestub, ebaõnnestu ka ise), `After=` ainult järjekord. Ilma `After`-ita käivitatakse mõlemad korraga. `network.target` tähendab ainult võrguhalduse alustamist; `network-online.target` ootab, kuni võrk on päriselt kasutatav - see tuleb `Wants`-iga tõmmata ja `After`-iga oodata.
22. `oneshot` - ühekordne töö, mis lõpetab (varundus, taimeri teenus); systemd ootab lõpetamist. `notify` - programm teatab ise, et on valmis (nt nginx, PostgreSQL), kõige täpsem. `RemainAfterExit=yes` jätab oneshot-teenuse pärast lõpetamist olekusse `active` (nt seadistuse rakendamine).
23. Mall on üksuse fail, millest käivitatakse mitu eksemplari, `%i` asendub eksemplari nimega (`getty@tty1`, `wg-quick@wg0`). Pesa aktiveerimisel kuulab systemd porti ja käivitab teenuse alles ühenduse saabumisel (`ssh.socket` Ubuntus, `kell.socket` laboris).
24. `DynamicUser` - teenus töötab ajutise kasutajana; `ProtectSystem=strict` - failisüsteem on teenusele ainult lugemiseks; `NoNewPrivileges` - teenus ei saa õigusi juurde (SUID). Hinnang: `systemd-analyze security teenus` (0-10, väiksem parem) koos soovitustega.
25. `203/EXEC` - `ExecStart` programmi ei leitud või see pole käivitatav. „Repeated too quickly“ - teenus jooksis korduvalt kokku ja ületas `StartLimitBurst`-i. Uuri `journalctl -xeu teenus` (esimene viga), `systemctl cat`, `systemd-analyze verify`; pärast parandust `systemctl reset-failed` ja uuesti käivitamine.

### Miniülesannete lahendused

```bash
cut -d' ' -f1 /proc/uptime
lsmod | grep virtio
systemd-analyze blame | head -3
journalctl -b -1 -p err
echo "vm.swappiness = 20" | sudo tee /etc/sysctl.d/90-swappiness.conf
sudo sysctl --system && sysctl vm.swappiness
```

Ülesanne 6: muuda failis `/etc/default/grub` rida `GRUB_CMDLINE_LINUX="nomodeset"` ja käivita `sudo update-grub`. Kontrolli pärast taaskäivitust käsuga `cat /proc/cmdline`. (`GRUB_CMDLINE_LINUX` kehtib kõigile kirjetele, ka taastamisrežiimile, `GRUB_CMDLINE_LINUX_DEFAULT` ainult tavalisele käivitusele.)

<!-- navigatsioon -->
---

[← Laboritöö 10. Alglaadimine, kernel ja taastamine](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 11. Turvalisus ja logid →](../moodul-11-turvalisus-logid/index.md)
<!-- /navigatsioon -->
