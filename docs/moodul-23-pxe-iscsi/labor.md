<!-- navigatsioon -->
[← Moodul 23. Võrgu infrastruktuur: PXE ja iSCSI](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 23. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 23. PXE ja iSCSI

| | |
|---|---|
| **Distrod** | Debian (`debian1` - DHCP ja TFTP, `debian2` - iSCSI sihtmärk), AlmaLinux (iSCSI initsiaator) |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Laboritöö 18 töötav Kea DHCP-server oma laborivõrgus, võrguplaan, `debian2`-le lisaketas 10 GiB (valikuline), üks tühi virtuaalmasin PXE testimiseks |
| **Eesmärk** | Seadistada laborivõrgus PXE alglaadimine ja iSCSI salvestus |

> **Aruanne:** vasta küsimustele **K1–K9**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

> [!WARNING]
> **Tee kõiki selle labori osi ainult isoleeritud laborivõrgus!** Kontrolli enne alustamist, et `debian1` võrguliides on Proxmoxis ühendatud sinu isoleeritud silda/VNet-i, mitte kooli võrku.

Tähised võrguplaani näite järgi: võrk `10.0.83.0/24`, vaikelüüs `10.0.83.1`, `debian1` `10.0.83.52`, `debian2` `10.0.83.53`, `alma` `10.0.83.55`, DHCP vahemik `10.0.83.80–99`. Asenda oma võrguplaani väärtustega.

---

## 1. osa. PXE alglaadimine (netboot.xyz)

**1.1** Paigalda `debian1`-sse TFTP-server ja laadi alla netboot.xyz alglaadimisfail (BIOS-klientidele):

```bash
sudo apt install tftpd-hpa
ls /srv/tftp
sudo wget -O /srv/tftp/netboot.xyz.kpxe https://boot.netboot.xyz/ipxe/netboot.xyz.kpxe
sudo ufw allow 69/udp
```

**1.2** Testi TFTP-d `debian2`-st:

```bash
sudo apt install tftp-hpa
tftp 10.0.83.52 -c get netboot.xyz.kpxe && ls -l netboot.xyz.kpxe
```

**1.3** Lisa Kea alamvõrgu seadistusse PXE valikud (teooria punkt 23.1) - `next-server` = `debian1` aadress, `boot-file-name` = `netboot.xyz.kpxe`. Kontrolli ja taaskäivita Kea.

**1.4** Loo Proxmoxis tühi virtuaalmasin ilma kettata (või väikese kettaga), võrk sinu laborivõrgu silda, BIOS **SeaBIOS**, *Options* → *Boot Order*: `net0` esimeseks. Käivita see ja jälgi konsooli.

> **K1.** Mida konsoolis nägid? Kirjelda alglaadimise etappe (PXE → DHCP → TFTP → iPXE → menüü). Millise distro paigaldaja või tööriista netboot.xyz menüüst proovisid käivitada?

**1.5** Muuda masina BIOS UEFI-ks (OVMF) ja proovi uuesti.

> **K2.** Kas alglaadimine õnnestus? Miks mitte? Millist faili oleks UEFI klient vajanud ja kuidas saaks Kea jagada BIOS- ja UEFI-klientidele eri faile?

## 2. osa. iSCSI sihtmärk

**2.1** `debian2`-s: kasuta lisaketast (`/dev/sdb`) LVM-iga või failipõhist tausta. Lihtsam variant (fail):

```bash
sudo apt install targetcli-fb
sudo mkdir -p /srv/iscsi
sudo targetcli
```

Loo `targetcli`-s (teooria punkt 23.2):

- failipõhine taust `disk01`, 5G, fail `/srv/iscsi/disk01.img`;
- sihtmärk `iqn.2026-11.example.lab:debian2.disk01`;
- LUN taustast `disk01`;
- ACL initsiaatorile `iqn.2026-11.example.lab:alma`;
- `saveconfig`.

```bash
sudo targetcli ls
sudo ss -tlpn | grep 3260
sudo ufw allow 3260/tcp
```

> **K3.** Kirjuta aruandesse `targetcli ls` väljund. Selgita, mis on sihtmärk, LUN, ACL ja portaal.

**2.2** Taaskäivita `debian2` ja kontrolli, kas sihtmärk taastus (`sudo targetcli ls`).

## 3. osa. iSCSI initsiaator (AlmaLinux)

**3.1** Paigalda initsiaator ja määra IQN, mis vastab ACL-ile:

```bash
sudo dnf install iscsi-initiator-utils
cat /etc/iscsi/initiatorname.iscsi
echo "InitiatorName=iqn.2026-11.example.lab:alma" | sudo tee /etc/iscsi/initiatorname.iscsi
sudo systemctl restart iscsid
```

**3.2** Avasta sihtmärk, logi sisse ja leia uus ketas:

```bash
sudo iscsiadm -m discovery -t sendtargets -p 10.0.83.53
lsblk
sudo iscsiadm -m node --login
lsblk
sudo iscsiadm -m session -P 3 | grep -E "Target|Attached scsi disk"
```

> **K4.** Mis nime sai iSCSI ketas AlmaLinuxis? Kuidas see `lsblk` väljundis kohalikust kettast erineb (vihje: `lsblk -S` veerg `TRAN`)?

**3.3** Proovi esmalt **vale** IQN-iga: muuda faili `initiatorname.iscsi` IQN-i, logi välja (`iscsiadm -m node --logout`), taaskäivita `iscsid` ja logi uuesti sisse.

> **K5.** Mis veateate said? Miks? Taasta õige IQN.

**3.4** Loo kettale failisüsteem ja haagi see püsivalt:

```bash
sudo mkfs.xfs /dev/sdX
sudo mkdir -p /mnt/iscsi
sudo blkid /dev/sdX
```

Lisa faili `/etc/fstab` rida (UUID ja `_netdev`) ning sea automaatne sisselogimine (teooria punkt 23.2). Kontrolli:

```bash
sudo findmnt --verify
sudo systemctl daemon-reload
sudo mount -a
df -h /mnt/iscsi
echo "iSCSI töötab" | sudo tee /mnt/iscsi/test.txt
sudo systemctl reboot
```

Pärast taaskäivitust: `df -h /mnt/iscsi && cat /mnt/iscsi/test.txt`.

> **K6.** Mis on valiku `_netdev` ülesanne? Mis juhtuks alglaadimisel ilma selleta?

**3.5** (Valikuline) Ühenda sama sihtmärgi **teine LUN** (loo `debian2`-s eraldi taust ja ACL Windowsi initsiaatori IQN-ile) Windowsi kliendist `iscsicpl` abil ja vorminda NTFS-iks.

> **K7.** Miks ei tohi sama LUN-i ühendada korraga AlmaLinuxi ja Windowsiga?

## 4. osa. Kokkuvõte

> **K8.** Täienda oma võrguplaani: millises masinas töötab TFTP ja iSCSI sihtmärk, millised pordid on avatud.

> **K9.** Võrdle NFS-i, Sambat (moodul 19) ja iSCSI-t: millisel tasemel need jagavad, kas mitu klienti saab korraga kasutada, millal millist kasutada?

---

## Lisaülesanne (valikuline)

1. **UEFI PXE:** lisa Kea seadistusse kliendiklassid, mis jagavad BIOS-klientidele `netboot.xyz.kpxe` ja UEFI-klientidele `netboot.xyz.efi` (vihje: valik 93, `client-classes`, `test` avaldis `option[93].hex == 0x0007`).
2. **FOG:** paigalda FOG eraldi Debiani masinasse (vähemalt 100 GiB ketast) ja salvesta ning paigalda ühe kliendi kettatõmmis. Seadista Kea `next-server` FOG-i serverile.
3. **Proxmox ja iSCSI:** lisa õpetaja loal `debian2` iSCSI sihtmärk Proxmoxi salvestuseks (*Datacenter* → *Storage* → *Add* → *iSCSI*) ja vaata, kuidas Proxmox seda kasutab.
4. **Automaatne paigaldus kickstartiga:** pane `debian2` veebiserverisse `ks.cfg` ja `boot.ipxe` (teooria punkt 23.1), lisa Kea seadistusse iPXE kliendiklass ning käivita uus tühi VM (vähemalt 2 GiB RAM, 20 GiB ketas) võrgust. Mõõda, kui kaua võttis paigaldus nupuvajutusest sisselogimiseni. Kontrolli, et SSH-võtmega saab kohe sisse.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.4)* Mida konsoolis nägid? Kirjelda alglaadimise etappe (PXE → DHCP → TFTP → iPXE → menüü). Millise distro paigaldaja või tööriista netboot.xyz menüüst proovisid käivitada?
- **K2.** *(punkt 1.5)* Kas alglaadimine õnnestus? Miks mitte? Millist faili oleks UEFI klient vajanud ja kuidas saaks Kea jagada BIOS- ja UEFI-klientidele eri faile?
- **K3.** *(punkt 2.1)* Kirjuta aruandesse `targetcli ls` väljund. Selgita, mis on sihtmärk, LUN, ACL ja portaal.
- **K4.** *(punkt 3.2)* Mis nime sai iSCSI ketas AlmaLinuxis? Kuidas see `lsblk` väljundis kohalikust kettast erineb (vihje: `lsblk -S` veerg `TRAN`)?
- **K5.** *(punkt 3.3)* Mis veateate said? Miks? Taasta õige IQN.
- **K6.** *(punkt 3.4)* Mis on valiku `_netdev` ülesanne? Mis juhtuks alglaadimisel ilma selleta?
- **K7.** *(punkt 3.5)* Miks ei tohi sama LUN-i ühendada korraga AlmaLinuxi ja Windowsiga?
- **K8.** *(4. osa)* Täienda oma võrguplaani: millises masinas töötab TFTP ja iSCSI sihtmärk, millised pordid on avatud.
- **K9.** *(4. osa)* Võrdle NFS-i, Sambat (moodul 19) ja iSCSI-t: millisel tasemel need jagavad, kas mitu klienti saab korraga kasutada, millal millist kasutada?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 23. Võrgu infrastruktuur: PXE ja iSCSI](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 23. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
