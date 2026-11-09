# Laboritöö 19. DHCP, PXE ja iSCSI

| | |
|---|---|
| **Distrod** | Debian (`debian1` - DHCP ja TFTP, `debian2` - iSCSI sihtmärk), AlmaLinux (iSCSI initsiaator), Ubuntu (DHCP-klient) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Laboritöö 18 isoleeritud laborivõrk OPNsense'i taga, võrguplaan, `debian2`-le lisaketas 10 GiB (valikuline), üks tühi virtuaalmasin PXE testimiseks |
| **Eesmärk** | Seadistada laborivõrgule Linuxi DHCP-server, PXE alglaadimine ja iSCSI salvestus |

**Aruanne:** vasta küsimustele **K1–K16**.

> [!WARNING]
> **Tee kõiki selle labori osi ainult isoleeritud laborivõrgus!** Kontrolli enne alustamist, et `debian1` võrguliides on Proxmoxis ühendatud sinu isoleeritud silda/VNet-i, mitte kooli võrku.

Tähised võrguplaani näite järgi: võrk `10.0.83.0/24`, OPNsense `10.0.83.1`, `debian1` `10.0.83.52`, `debian2` `10.0.83.53`, `alma` `10.0.83.55`, DHCP vahemik `10.0.83.80–99`. Asenda oma võrguplaani väärtustega.

---

## 1. osa. Kea DHCP-server

**1.1** Kontrolli `debian1` võrguseadistust (staatiline aadress, vaikelüüs ja DNS = OPNsense):

```bash
ip -br a
ip r
cat /etc/resolv.conf
```

**1.2** Paigalda Kea ja tee algsest seadistusest koopia:

```bash
sudo apt install kea-dhcp4-server
sudo cp /etc/kea/kea-dhcp4.conf /etc/kea/kea-dhcp4.conf.orig
wc -l /etc/kea/kea-dhcp4.conf.orig
```

**K1.** Mitu rida on näidisseadistuses? Miks on parem kirjutada oma lühike seadistus kui muuta pikka näidisfaili?

**1.3** Kirjuta fail `/etc/kea/kea-dhcp4.conf` teooria punkti 19.2 põhjal oma võrguplaani järgi. Reserveeringut veel ära lisa.

**1.4** Kontrolli süntaksit. Tee meelega viga (kustuta mõni koma) ja kontrolli uuesti. Paranda.

```bash
sudo kea-dhcp4 -t /etc/kea/kea-dhcp4.conf
```

**K2.** Mida näitas kontroll vea korral? Miks on JSON-i puhul nii lihtne viga teha?

**1.5** **Lülita OPNsense'is LAN-i DHCP-server välja** (*Services* → DHCP-teenus → *LAN* → keela, salvesta). Seejärel käivita Kea:

```bash
sudo systemctl restart kea-dhcp4-server
systemctl status kea-dhcp4-server
sudo ufw allow 67/udp          # kui ufw on sees
journalctl -u kea-dhcp4-server -f
```

**K3.** Miks tuli OPNsense'i DHCP välja lülitada? Mis juhtuks, kui võrgus oleks kaks DHCP-serverit?

## 2. osa. Klient ja reserveering

**2.1** Uuenda Ubuntu kliendi renti ja jälgi samal ajal `debian1` logi (`journalctl -f`):

```bash
sudo networkctl renew <liides>
ip -br a
```

**K4.** Leia logist DHCP-sõnumite vahetus (DISCOVER, OFFER, REQUEST, ACK - Kea logis `DHCP4_PACKET_RECEIVED`, `DHCP4_LEASE_ALLOC` vms). Millise aadressi klient sai?

**2.2** Vaata rente serveris:

```bash
sudo cat /var/lib/kea/kea-leases4.csv
```

**2.3** Püüa DHCP-liiklust `debian1`-s, kui klient uuendab renti uuesti:

```bash
sudo apt install tcpdump
sudo tcpdump -ni ens18 -v port 67 or port 68
```

**K5.** Kas nägid leviedastusi (`255.255.255.255`)? Millised DHCP-valikud olid serveri vastuses (ruuter, DNS, domeen, rendiaeg)?

**2.4** Lisa Ubuntu kliendile reserveering võrguplaanis olevale aadressile (`10.0.83.98`). Kontrolli süntaksit, taaskäivita Kea ja uuenda kliendi renti.

**K6.** Kas klient sai reserveeritud aadressi kohe? Kui ei, miks (vihje: olemasolev rent)? Kuidas probleemi lahendasid?

**2.5** Peata Kea ja oota, mis juhtub kliendiga, kui see renti uuendada üritab (`networkctl renew`). Käivita Kea uuesti.

**K7.** Mis juhtus kliendi aadressiga, kui DHCP-server ei vastanud? Miks ei kaota klient aadressi kohe?

## 3. osa. PXE alglaadimine (netboot.xyz)

**3.1** Paigalda `debian1`-sse TFTP-server ja laadi alla netboot.xyz alglaadimisfail (BIOS-klientidele):

```bash
sudo apt install tftpd-hpa
ls /srv/tftp
sudo wget -O /srv/tftp/netboot.xyz.kpxe https://boot.netboot.xyz/ipxe/netboot.xyz.kpxe
sudo ufw allow 69/udp
```

**3.2** Testi TFTP-d `debian2`-st:

```bash
sudo apt install tftp-hpa
tftp 10.0.83.52 -c get netboot.xyz.kpxe && ls -l netboot.xyz.kpxe
```

**3.3** Lisa Kea alamvõrgu seadistusse PXE valikud (teooria punkt 19.4) - `next-server` = `debian1` aadress, `boot-file-name` = `netboot.xyz.kpxe`. Kontrolli ja taaskäivita Kea.

**3.4** Loo Proxmoxis tühi virtuaalmasin ilma kettata (või väikese kettaga), võrk isoleeritud silda, BIOS **SeaBIOS**, *Options* → *Boot Order*: `net0` esimeseks. Käivita see ja jälgi konsooli.

**K8.** Mida konsoolis nägid? Kirjelda alglaadimise etappe (PXE → DHCP → TFTP → iPXE → menüü). Millise distro paigaldaja või tööriista netboot.xyz menüüst proovisid käivitada?

**3.5** Muuda masina BIOS UEFI-ks (OVMF) ja proovi uuesti.

**K9.** Kas alglaadimine õnnestus? Miks mitte? Millist faili oleks UEFI klient vajanud ja kuidas saaks Kea jagada BIOS- ja UEFI-klientidele eri faile?

## 4. osa. iSCSI sihtmärk

**4.1** `debian2`-s: kasuta lisaketast (`/dev/sdb`) LVM-iga või failipõhist tausta. Lihtsam variant (fail):

```bash
sudo apt install targetcli-fb
sudo mkdir -p /srv/iscsi
sudo targetcli
```

Loo `targetcli`-s (teooria punkt 19.5):

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

**K10.** Kirjuta aruandesse `targetcli ls` väljund. Selgita, mis on sihtmärk, LUN, ACL ja portaal.

**4.2** Taaskäivita `debian2` ja kontrolli, kas sihtmärk taastus (`sudo targetcli ls`).

## 5. osa. iSCSI initsiaator (AlmaLinux)

**5.1** Paigalda initsiaator ja määra IQN, mis vastab ACL-ile:

```bash
sudo dnf install iscsi-initiator-utils
cat /etc/iscsi/initiatorname.iscsi
echo "InitiatorName=iqn.2026-11.example.lab:alma" | sudo tee /etc/iscsi/initiatorname.iscsi
sudo systemctl restart iscsid
```

**5.2** Avasta sihtmärk, logi sisse ja leia uus ketas:

```bash
sudo iscsiadm -m discovery -t sendtargets -p 10.0.83.53
lsblk
sudo iscsiadm -m node --login
lsblk
sudo iscsiadm -m session -P 3 | grep -E "Target|Attached scsi disk"
```

**K11.** Mis nime sai iSCSI ketas AlmaLinuxis? Kuidas see `lsblk` väljundis kohalikust kettast erineb (vihje: `lsblk -S` veerg `TRAN`)?

**5.3** Proovi esmalt **vale** IQN-iga: muuda faili `initiatorname.iscsi` IQN-i, logi välja (`iscsiadm -m node --logout`), taaskäivita `iscsid` ja logi uuesti sisse.

**K12.** Mis veateate said? Miks? Taasta õige IQN.

**5.4** Loo kettale failisüsteem ja haagi see püsivalt:

```bash
sudo mkfs.xfs /dev/sdX
sudo mkdir -p /mnt/iscsi
sudo blkid /dev/sdX
```

Lisa faili `/etc/fstab` rida (UUID ja `_netdev`) ning sea automaatne sisselogimine (teooria punkt 19.5). Kontrolli:

```bash
sudo findmnt --verify
sudo systemctl daemon-reload
sudo mount -a
df -h /mnt/iscsi
echo "iSCSI töötab" | sudo tee /mnt/iscsi/test.txt
sudo systemctl reboot
```

Pärast taaskäivitust: `df -h /mnt/iscsi && cat /mnt/iscsi/test.txt`.

**K13.** Mis on valiku `_netdev` ülesanne? Mis juhtuks alglaadimisel ilma selleta?

**5.5** (Valikuline) Ühenda sama sihtmärgi **teine LUN** (loo `debian2`-s eraldi taust ja ACL Windowsi initsiaatori IQN-ile) Windowsi kliendist `iscsicpl` abil ja vorminda NTFS-iks.

**K14.** Miks ei tohi sama LUN-i ühendada korraga AlmaLinuxi ja Windowsiga?

## 6. osa. Kokkuvõte

**K15.** Täienda oma võrguplaani: millises masinas töötab DHCP, TFTP ja iSCSI sihtmärk, millised pordid on avatud.

**K16.** Võrdle NFS-i, Sambat (moodul 15) ja iSCSI-t: millisel tasemel need jagavad, kas mitu klienti saab korraga kasutada, millal millist kasutada?

---

## Lisaülesanne (valikuline)

1. **UEFI PXE:** lisa Kea seadistusse kliendiklassid, mis jagavad BIOS-klientidele `netboot.xyz.kpxe` ja UEFI-klientidele `netboot.xyz.efi` (vihje: valik 93, `client-classes`, `test` avaldis `option[93].hex == 0x0007`).
2. **FOG:** paigalda FOG eraldi Debiani masinasse (vähemalt 100 GiB ketast) ja salvesta ning paigalda ühe kliendi kettatõmmis. Seadista Kea `next-server` FOG-i serverile.
3. **Proxmox ja iSCSI:** lisa õpetaja loal `debian2` iSCSI sihtmärk Proxmoxi salvestuseks (*Datacenter* → *Storage* → *Add* → *iSCSI*) ja vaata, kuidas Proxmox seda kasutab.
4. **ISC DHCP võrdlus:** seadista samale võrgule (Kea peatatuna) ISC DHCP teooria punkti 19.3 järgi ja võrdle seadistusfaile ning logisid.
5. **Automaatne paigaldus kickstartiga:** pane `debian2` veebiserverisse `ks.cfg` ja `boot.ipxe` (teooria punkt 19.4), lisa Kea seadistusse iPXE kliendiklass ning käivita uus tühi VM (vähemalt 2 GiB RAM, 20 GiB ketas) võrgust. Mõõda, kui kaua võttis paigaldus nupuvajutusest sisselogimiseni. Kontrolli, et SSH-võtmega saab kohe sisse.

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 19. Võrgu infrastruktuur: DHCP, PXE ja iSCSI](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 19. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
