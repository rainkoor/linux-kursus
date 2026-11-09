# Laboritöö 23. KVM, Proxmox VE ja XCP-ng

| | |
|---|---|
| **Platvormid** | Debian (KVM ja libvirt), Proxmox VE, XCP-ng ja Debian (Xen Orchestra) |
| **Kestus** | 5 × 90 minutit |
| **Vajalik** | Kooli Proxmoxis pesastatud virtualiseerimisega VM-id (protsessori tüüp `host`): Debian (2 vCPU, 4 GiB RAM, 20 GiB), Proxmox VE (4 vCPU, 8 GiB RAM, 64 GiB), XCP-ng (2 vCPU, 4 GiB, 64 GiB) Debian Xen Orchestra jaoks (2 vCPU, 3 GiB) ja Proxmox Backup Server (2 vCPU, 4 GiB RAM, süsteemiketas 32 GiB + andmeketas 32 GiB, nt `10.0.83.65`). Füüsiline server (nt aines „Majutuskeskkonna riistvara“) sobib veel paremini |
| **Eesmärk** | Mõista, kuidas Linux virtualiseerib, ning paigaldada ja hallata kahte avatud hüperviisorit |

**Aruanne:** vasta küsimustele **K1–K18**.

> Pesastatud hüperviisor on aeglasem kui päris riistvaral. Kasuta väikeseid testmasinaid (Alpine, Debiani pilvetõmmis) ja lülita masinad pärast tundi välja.

---

## 1. osa. KVM ja libvirt (Debian)

**1.1** Kontrolli riistvaralist tuge:

```bash
grep -cE 'vmx|svm' /proc/cpuinfo
lscpu | grep -i -E "virtualization|model name"
ls -l /dev/kvm
lsmod | grep kvm
```

**K1.** Kas virtualiseerimise tugi oli VM-is olemas? Mis juhtuks, kui Proxmoxis oleks VM-i protsessori tüüp `x86-64-v2-AES` (mitte `host`)?

**1.2** Paigalda KVM ja libvirt ning loo masin Debiani pilvetõmmisest (teooria punkt 23.2):

```bash
sudo apt install -y qemu-system-x86 qemu-utils libvirt-daemon-system virtinst
sudo usermod -aG libvirt,kvm $USER      # logi välja ja uuesti sisse
virsh -c qemu:///system net-list --all
```

Laadi alla pilvetõmmis, loo sellest ketas ja käivita `virt-install`-iga masin `test1` (teooria punkt 23.2). Kontrolli:

```bash
virsh -c qemu:///system list --all
virsh -c qemu:///system domifaddr test1
virsh -c qemu:///system console test1
ps aux | grep -c [q]emu-system
```

**K2.** Mis on `test1` IP-aadress ja millises võrgus see asub (`virbr0`)? Kuidas paistab virtuaalmasin hostis (`ps`)?

**1.3** Tee hetktõmmis, muuda masinas midagi ja taasta:

```bash
virsh -c qemu:///system snapshot-create-as test1 puhas
virsh -c qemu:///system snapshot-list test1
virsh -c qemu:///system snapshot-revert test1 puhas
qemu-img info /var/lib/libvirt/images/test1.qcow2
```

**K3.** Mida näitas `qemu-img info` ketta tegeliku suuruse ja tagatõmmise (*backing file*) kohta? Miks oli uue masina loomine nii kiire?

## 2. osa. Proxmox VE paigaldus ja uuendused

**2.1** Paigalda Proxmox VE VM-i (teooria punkt 23.3): ZFS RAID0 või ext4, **staatiline IP** oma võrguplaanist, FQDN hostinimi (nt `pve1.lab.example`), e-posti aadress, mis ei lõpe `.invalid`-iga.

**2.2** Logi veebiliidesesse (`https://<IP>:8006`, *Linux PAM*) ja SSH-ga sisse. Seadista no-subscription hoidla, keela enterprise-hoidlad ja uuenda:

```bash
pveversion -v | head -5
apt update
apt full-upgrade
```

**K4.** Mis viga andis `apt update` enne hoidlate muutmist ja miks? Millal oleks õige kasutada enterprise-hoidlat?

**2.3** Uuri Proxmoxi „kapoti all“:

```bash
systemctl list-units --type=service | grep -E "pve|corosync"
ls /etc/pve
cat /etc/network/interfaces
pvesm status
zpool status 2>/dev/null || lvs
```

**K5.** Millised on Proxmoxi põhiteenused? Mis on kataloog `/etc/pve` ja miks on see eriline? Milline sild (`vmbr0`) ühendab VM-e füüsilise võrguga?

## 3. osa. Virtuaalmasinad ja konteinerid Proxmoxis

**3.1** Laadi ISO-fail (nt Alpine Linux või Debian netinst) salvestusse *Download from URL* abil. Loo veebiliideses VM 100 (512 MiB RAM, 4 GiB ketas, QEMU agent sees) ja paigalda OS.

**3.2** Halda masinat käsurealt:

```bash
qm list
qm config 100
qm set 100 --memory 1024 --description "Labori testmasin"
qm snapshot 100 puhas
qm listsnapshot 100
qm shutdown 100
```

**3.3** Loo LXC konteiner (teooria punkt 23.3):

```bash
pveam update
pveam available --section system | grep -E "debian|alpine"
pveam download local <mallinimi>
pct create 200 local:vztmpl/<mallinimi> --hostname ct1 --memory 512 \
    --rootfs local-lvm:4 --net0 name=eth0,bridge=vmbr0,ip=dhcp --unprivileged 1 --password
pct start 200
pct enter 200
```

Konteineris: `cat /etc/os-release; uname -r; ps aux`. Proxmoxis: `uname -r`.

**K6.** Võrdle VM-i ja LXC konteineri käivitusaega, mälukasutust ja kernelit (`uname -r`). Millal kasutaksid kumba?

**K7.** Mida tähendab `--unprivileged 1`? Mis on konteineri `root`-i UID hostis (vihje: `ps -o user,pid,cmd -C bash` hostis, kui konteineris töötab kest)?

## 4. osa. Varundus, mall, kloonid ja Proxmox Backup Server

**4.1** Tee masinast 100 varukoopia ja taasta see uue masinana:

```bash
vzdump 100 --mode stop --compress zstd --storage local
ls -lh /var/lib/vz/dump/
qmrestore /var/lib/vz/dump/vzdump-qemu-100-*.vma.zst 110 --unique
qm config 110 | grep net0
qm config 100 | grep net0
```

**K8.** Kas masinate 100 ja 110 MAC-aadressid erinesid? Mis juhtuks samas võrgus kahe sama MAC-aadressiga masinaga?

**4.2** Muuda masin 110 malliks ja tee sellest üks täielik ja üks lingitud kloon:

```bash
qm template 110
qm clone 110 121 --name kloon-full --full
qm clone 110 122 --name kloon-linked
pvesm list local-lvm
```

**K9.** Mis vahe oli kloonide loomise kiirusel ja ruumikasutusel? Miks ei tohi lingitud klooni malli kustutada?

**4.3 Proxmox Backup Server.** Paigalda PBS ISO-st eraldi VM-i (teooria punkt 23.3, *Proxmox Backup Server*): staatiline IP (nt `10.0.83.65`), seejärel ava `https://10.0.83.65:8007`. Lülita hoidlad *no-subscription* peale ja uuenda (`apt update && apt full-upgrade`). Loo andmekettale andmehoidla `andmed` (*Administration* → *Storage / Disks* → *Directory*, *Add as Datastore*).

**4.4** PBS-i konsoolis loo Proxmoxi jaoks kasutaja ja vaata sõrmejälge:

```bash
proxmox-backup-manager user create pve@pbs --password 'Pikk-parool-2026'
proxmox-backup-manager acl update /datastore/andmed DatastoreBackup --auth-id pve@pbs
proxmox-backup-manager cert info | grep Fingerprint
```

Lisa PBS laboritöö Proxmoxis salvestuseks (*Datacenter* → *Storage* → *Add* → *Proxmox Backup Server*, ID `pbs`). **Ära lülita** selles harjutuses krüpteerimist sisse (või salvesta võti kindlasti alles).

**4.5** Varunda töötav masin 100 PBS-i kaks korda järjest ja võrdle:

```bash
time vzdump 100 --storage pbs --mode snapshot
time vzdump 100 --storage pbs --mode snapshot
pvesm list pbs
```

Vaata PBS-i veebiliideses andmehoidla *Summary* (deduplitseerimistegur) ja *Content*. Seadista andmehoidlale *Prune & GC* (nt *keep-last 3, keep-daily 7*) ja käivita *Verify* käsitsi.

**K10.** Kui kaua võttis esimene ja teine varukoopia ning kui palju andmeid kumbki kord saadeti (vt `vzdump` väljundit)? Mis on deduplitseerimistegur? Miks oli teine varukoopia kiirem?

**4.6** Taasta failid ja masin:

1. Kustuta masinas 100 mõni fail (nt `/etc/motd`).
2. Proxmoxis vali salvestus `pbs` → viimane varukoopia → *File Restore*, leia fail ja laadi see alla.
3. Taasta kogu masin uue ID-ga: varukoopia → *Restore*, VM ID `130`, märgi *Unique*. Käivita masin 130 ja kontrolli, et see töötab.

**K11.** Mis on PBS-i õiguse `DatastoreBackup` eelis võrreldes `root`-iga, kui ründaja saab Proxmoxi enda üle kontrolli? Miks ei ole hea mõte paigaldada PBS samasse Proxmoxi, mida see varundab? Kui kaua võttis kogu masina taastamine?

## 5. osa. Proxmoxi võrk: sild ja NAT

**5.1** Loo sild `vmbr10` võrguga `10.0.222.0/24` (Proxmox `10.0.222.1`) ja NAT (teooria punkt 23.3). Rakenda `ifreload -a`.

**5.2** Ühenda konteiner 200 sillaga `vmbr10`, anna talle staatiline aadress `10.0.222.10/24`, vaikelüüs `10.0.222.1`, ja kontrolli internetiühendust:

```bash
pct set 200 --net0 name=eth0,bridge=vmbr10,ip=10.0.222.10/24,gw=10.0.222.1
pct enter 200
ping -c2 10.0.222.1
ping -c2 1.1.1.1
```

Proxmoxis:

```bash
iptables -t nat -L POSTROUTING -n -v
sysctl net.ipv4.ip_forward
```

**K12.** Kas konteiner pääses internetti? Mida teeb reegel `MASQUERADE` ja miks oli vaja `ip_forward`-i? Võrdle seda OPNsense'iga (moodul 18).

## 6. osa. Klaster (valikuline, kaks Proxmoxi VM-i)

**6.1** Paigalda teine Proxmox (`pve2`). Loo `pve1`-s klaster ja liida `pve2`:

```bash
pvecm create labor          # pve1
pvecm add <pve1 IP>         # pve2
pvecm status
pvecm nodes
```

**6.2** Migreeri konteiner või väljalülitatud VM `pve2`-le (*Migrate*). Lülita `pve2` välja ja vaata `pve1`-s `pvecm status`.

**K13.** Mitu häält (*votes*) klastris on ja kas pärast `pve2` väljalülitamist on kvoorum? Miks on HA jaoks vaja vähemalt kolme sõlme?

## 7. osa. XCP-ng ja Xen Orchestra

**7.1** Paigalda XCP-ng VM-i (teooria punkt 23.4): staatiline IP, hostinimi, NTP `pool.ntp.org`. Uuri konsoolis `xsconsole`-i menüüd ning SSH-ga:

```bash
xe host-list
xe sr-list
xe network-list
xl info | head        # Xeni enda tööriist
```

**K14.** Mis on dom0 ja mille poolest erineb Xeni ülesehitus KVM-ist?

**7.2** Loo kohalik ISO-repositoorium (teooria punkt 23.4) ja kopeeri sinna väike ISO (`scp`).

**7.3** Paigalda Debiani VM-i Xen Orchestra lähtekoodist (teooria punkt 23.4), logi sisse, **muuda vaikeparool** ja lisa XCP-ng server.

**7.4** Loo Xen Orchestras VM, paigalda OS ja külalistööriistad (`guest-tools.iso`). Kontrolli, et XO näitab VM-i IP-aadressi.

**K15.** Mida näitas XO enne ja pärast külalistööriistade paigaldust? Milline on Proxmoxis samaväärne komponent?

## 8. osa. Kokkuvõte

**K16.** Täida tabel Proxmox VE ja XCP-ng kohta: paigaldus, haldusliides, käsurida, konteinerid, varundus, mis meeldis, mis oli keeruline.

**K17.** Kool kaalub laborikeskkonna kolimist VMware'ilt avatud hüperviisorile. Too kolm küsimust, millele peaks enne otsustamist vastama.

**K18.** Selgita, kuidas selle kursuse teemad seostuvad hüperviisoriga: too vähemalt neli näidet (nt Debian ja `apt`, ZFS, Linuxi sillad, LXC, `vzdump`, systemd, iSCSI).

---

## Koristamine

Kustuta testmasinad (`virsh undefine test1 --remove-all-storage`, `qm destroy`, `pct destroy`) ja lülita pesastatud hüperviisorid välja, et need ei kulutaks kooli Proxmoxi ressursse.

---

## Lisaülesanne (valikuline)

1. **PBS-i krüpteerimine ja teine koopia:** loo PBS-i salvestusele krüpteerimisvõti, tee krüpteeritud varukoopia ja proovi seda taastada. Paigalda teine PBS, lisa esimene sinna *Remote*'iks ja seadista *Sync Job*. Varunda `proxmox-backup-client`-iga ka üks tavaline Linuxi server (nt `debian1` kataloog `/etc`).
2. **Cloud-init mall:** tee Debiani pilvetõmmisest Proxmoxi mall koos cloud-initiga (teooria punkt 23.3, *Cloud-init mall*) ja klooni sellest kolm masinat, mis saavad kohe õige nime, IP ja SSH-võtme.
3. **Proxmoxi API:** loo API-võti ja küsi `curl`-iga masinate loetelu (teooria punkt 23.3, *API ja skriptid*). Kirjuta Bashi skript (moodul 6), mis käivitab kõik ühe kogumi (*pool*) masinad.
4. **Ansible ja Proxmox:** kasuta Ansible'i kogumit `community.general` (moodulid `proxmox_kvm` ja `proxmox`), et luua masinaid koodina (moodul 16).

---

## Õpetajale: kontrollvastused

| Küsimus | Vastus |
|---|---|
| K1 | Pesastamisega VM-is on `vmx`/`svm` olemas ja `/dev/kvm` olemas; muu protsessori tüübi puhul ei pruugi laiendused külalisele näha olla ja KVM ei tööta (QEMU kasutaks väga aeglast emulatsiooni) |
| K2 | Aadress vahemikust `192.168.122.0/24` (libvirt'i vaikimisi NAT-võrk); VM on hostis tavaline `qemu-system-x86_64` protsess |
| K3 | Ketas on qcow2 *backing file*'iga - algul väike, hoiab ainult erinevusi; pilvetõmmis on valmis süsteem, paigaldust pole vaja |
| K4 | `401 Unauthorized` enterprise-hoidla kohta (tellimus puudub); enterprise - tootmises koos tellimuse ja toega |
| K5 | `pvedaemon`, `pveproxy`, `pvestatd`, `pve-cluster`, `corosync` (klastris), `pve-firewall`; `/etc/pve` on pmxcfs - klastri ühine andmebaasil põhinev failisüsteem (FUSE), mis sünkroonitakse kõigi sõlmede vahel; `vmbr0` |
| K6 | Konteiner käivitub sekundiga, kasutab vähem mälu ja sama kernelit mis host; VM - oma kernel, eri OS-id, tugevam isolatsioon |
| K7 | Konteineri UID-d on hostis nihutatud (vaikimisi 100000+); konteineri `root` on hostis õigusteta kasutaja |
| K8 | Jah (`--unique`); sama MAC tekitaks ARP-i ja DHCP konflikte, ühendused katkeksid |
| K9 | Lingitud kloon sekundiga ja peaaegu ilma ruumita, täielik kopeerib kogu ketta; lingitud kloon kasutab malli ketast alusena |
| K10 | Esimene varukoopia saadab kogu kasutatud ketta, teine ainult muutunud plokid (*dirty bitmap*) ja võtab sekundeid. Tegur sõltub masinast; kahe järjestikuse varukoopia korral ligikaudu 2 või rohkem. Teine on kiirem, sest QEMU teab, millised plokid on muutunud, ja PBS-is juba olemas olevaid tükke uuesti ei saadeta |
| K11 | `DatastoreBackup` võimaldab varundada ja taastada, kuid mitte varukoopiaid kustutada - ründaja ei saa ajalugu hävitada. Sama Proxmoxi rikke (ketas, tulekahju, lunavara) korral kaoksid masinad ja varukoopiad korraga. Taastamise aeg sõltub masina suurusest ja võrgust (laboris tavaliselt minutid) |
| K12 | Jah; MASQUERADE asendab väljuvate pakettide lähteaadressi hosti `vmbr0` aadressiga, `ip_forward` lubab kernelil pakette liideste vahel edastada; OPNsense teeb sama (NAT + tulemüür) eraldi seadmena |
| K13 | 2 häält; ühe sõlmega on 1/2 - kvoorumit pole, `/etc/pve` on ainult lugemiseks; kolmega jääb ühe rikke korral alles enamus (2/3) |
| K14 | dom0 on privilegeeritud haldus-VM (Linux), mis haldab seadmeid ja teisi VM-e; Xen käivitub enne Linuxit, KVM-is on hüperviisor Linuxi kerneli osa |
| K15 | Ilma tööriistadeta: IP puudub, hoiatus *Management agent not detected*; pärast: IP, mälu, viisakas sulgemine. Proxmoxis QEMU Guest Agent (`qemu-guest-agent`) |

> **Märkus õpetajale:** laboritööd ei ole testitud. Pesastatud Proxmoxi ja XCP-ng jaoks peab kooli Proxmoxi sõlmes olema pesastamine lubatud ja VM-ide protsessori tüüp `host`. XCP-ng pesastatult KVM-i peal töötab, kuid aeglasemalt. Malli- ja ISO-nimed (`pveam available`) muutuvad - kontrolli need enne tundi.
