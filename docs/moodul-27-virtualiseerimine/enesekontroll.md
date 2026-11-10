<!-- navigatsioon -->
[← Laboritöö 27. KVM, Proxmox VE ja XCP-ng](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 28. Kubernetes: k3s →](../moodul-28-kubernetes/index.md)
<!-- /navigatsioon -->

# Moodul 27. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis vahe on tüüp 1 ja tüüp 2 hüperviisoril? Too kummastki kaks näidet.

<details>
<summary>Vastus</summary>

Tüüp 1 töötab otse riistvaral (Proxmox VE/KVM, XCP-ng/Xen, ESXi, Hyper-V); tüüp 2 tavalise OS-i peal programmina (VirtualBox, VMware Workstation).

</details>

**2.** Milliseid protsessori laiendusi virtualiseerimine vajab ja kuidas nende olemasolu Linuxis kontrollida?

<details>
<summary>Vastus</summary>

Intel VT-x või AMD-V (seadmete läbisuunamiseks VT-d/AMD-Vi): `grep -cE 'vmx|svm' /proc/cpuinfo`, `lscpu`, `/dev/kvm`.

</details>

**3.** Mis on pesastatud virtualiseerimine ja millal seda vaja on?

<details>
<summary>Vastus</summary>

Hüperviisori käitamine virtuaalmasinas - nt Proxmoxi või XCP-ng harjutamine laboris, WSL Windowsi VM-is.

</details>

**4.** Mis vahe on virtuaalmasinal, LXC konteineril ja Podmani konteineril?

<details>
<summary>Vastus</summary>

VM-il on oma kernel ja terve OS; LXC on süsteemikonteiner (oma init, teenused, nagu väike VM), mis jagab hosti kernelit; Podmani konteiner on rakenduskonteiner, tavaliselt üks protsess/teenus.

</details>

**5.** Mis on VirtIO ja miks Windowsi VM vajab eraldi draivereid?

<details>
<summary>Vastus</summary>

Paravirtualiseeritud seadmed (ketas, võrk, mälu), mis on palju kiiremad kui emuleeritud riistvara. Linuxi kernelis on draiverid olemas, Windowsis mitte - need tulevad virtio-win ISO-lt.

</details>

**6.** Selgita KVM-i, QEMU ja libvirt'i rolle.

<details>
<summary>Vastus</summary>

KVM - kerneli moodul, mis kasutab protsessori virtualiseerimislaiendusi; QEMU - emuleerib ülejäänud riistvara ja käitab VM-i protsessina; libvirt - haldusteek ja teenus (`virsh`, virt-manager).

</details>

**7.** Millist Debiani versiooni kasutab Proxmox VE 8 ja millist 9? Kuidas see mõjutab põhiversiooni uuendust?

<details>
<summary>Vastus</summary>

Proxmox VE 8 - Debian 12 „bookworm“, 9 - Debian 13 „trixie“. Põhiversiooni uuendus on ühtlasi Debiani väljalaske uuendus: hoidlates vahetatakse koodnimi ja tehakse `apt dist-upgrade`, kontrollskriptiga (`pve8to9`) eelnevalt.

</details>

**8.** Miks seadistatakse laboris no-subscription hoidla ja miks see tootmises ei ole soovitatav?

<details>
<summary>Vastus</summary>

Ilma tellimuseta ei pääse enterprise-hoidlale; no-subscription on tasuta, kuid vähem testitud ja ilma toeta.

</details>

**9.** Mis vahe on täielikul ja lingitud kloonil?

<details>
<summary>Vastus</summary>

Täielik kloon on iseseisev koopia; lingitud kloon kasutab malli ketast alusena ja salvestab ainult erinevused - kiire ja säästlik, kuid malli ei tohi kustutada.

</details>

**10.** Miks tuleb varukoopiast uue masina loomisel märkida *Unique*?

<details>
<summary>Vastus</summary>

Et uus masin saaks uue MAC-aadressi ja muud unikaalsed parameetrid, muidu tekivad võrgukonfliktid.

</details>

**11.** Miks hetktõmmis ei ole varukoopia? Miks tehakse laboris hetktõmmis väljalülitatud masinast ilma RAM-ita?

<details>
<summary>Vastus</summary>

Hetktõmmis asub samal salvestusel ja sõltub algsest kettast. Väljalülitatud masinast ilma RAM-ita on hetktõmmis kiire ega lukusta masinat.

</details>

**12.** Kuidas pääsevad eraldi silla (`vmbr10`) masinad internetti? Millised read selleks `/etc/network/interfaces`-i lisatakse?

<details>
<summary>Vastus</summary>

Hosti NAT-iga: `post-up echo 1 > /proc/sys/net/ipv4/ip_forward` ja `post-up iptables -t nat -A POSTROUTING -s '<võrk>' -o vmbr0 -j MASQUERADE` (+ vastav `post-down`).

</details>

**13.** Mis on kvoorum ja miks vajab HA-klaster vähemalt kolme sõlme?

<details>
<summary>Vastus</summary>

Kvoorum on üle poole sõlmede häältest; ilma selleta lukustab klaster seadistuse, et vältida *split brain*-i. Kolme sõlmega jääb ühe rikke korral alles enamus.

</details>

**14.** Mis on Xenis dom0 ja domU?

<details>
<summary>Vastus</summary>

dom0 - privilegeeritud haldus-Linux, mis haldab seadmeid ja XAPI-t; domU - tavalised külalismasinad.

</details>

**15.** Mis on Xen Orchestra ja mis vahe on XOA-l ning lähtekoodist paigaldatud XO-l?

<details>
<summary>Vastus</summary>

XCP-ng serverite ja kogumite veebihaldus. XOA on valmis seade (tasuta versioon piiratud, tasuline tugi); XO lähtekoodist sisaldab kõiki funktsioone, kuid ilma toeta ja tuleb ise uuendada.

</details>

**16.** Mille poolest erineb Proxmox Backup Server tavalisest `vzdump` failivarundusest? Nimeta vähemalt neli eelist.

<details>
<summary>Vastus</summary>

Deduplitseerimine (sama tükki hoitakse üks kord, ka eri masinate vahel), inkrementaalne varundus muutunud plokkidega (kiire), kliendipoolne krüpteerimine, regulaarne kontroll (verify), üksikfailide taastamine, sünkroonimine teise PBS-i, eraldi õigused (varundaja ei saa kustutada), ka tavaliste Linuxi masinate varundus `proxmox-backup-client`-iga.

</details>

**17.** Mis vahe on PBS-i töödel *Prune*, *Garbage collection* ja *Verify*? Miks ei vabane ruum kohe pärast vana varukoopia kustutamist?

<details>
<summary>Vastus</summary>

Prune kustutab säilitusreegli järgi varukoopiate kirjed; Garbage collection kustutab tükid, millele ükski varukoopia enam ei viita (alles siis vabaneb ruum); Verify kontrollib tükkide kontrollsummasid. Prune eemaldab ainult viited, sest sama tükki võivad kasutada teised varukoopiad.

</details>

## Praktilised miniülesanded

**1.** Kirjuta käsud, mis näitavad Proxmoxi sõlme kõiki VM-e ja konteinereid.

<details>
<summary>Lahendus</summary>

```bash
qm list
pct list
```

</details>

**2.** Muuda VM-i 105 mälu 4 GiB-ks ja tuumade arvu 2-ks käsurealt.

<details>
<summary>Lahendus</summary>

```bash
qm set 105 --memory 4096 --cores 2
```

</details>

**3.** Tee VM-ist 105 varukoopia režiimis *stop* ja taasta see uue ID-ga 150 nii, et MAC-aadress muutuks.

<details>
<summary>Lahendus</summary>

```bash
vzdump 105 --mode stop --compress zstd --storage local
qmrestore /var/lib/vz/dump/vzdump-qemu-105-<aeg>.vma.zst 150 --unique
```

</details>

**4.** Loo XCP-ng-s kohalik ISO-repositoorium kataloogi `/var/opt/xen/ISO_Store`.

<details>
<summary>Lahendus</summary>

```bash
mkdir -p /var/opt/xen/ISO_Store
xe sr-create name-label=LocalISO type=iso device-config:location=/var/opt/xen/ISO_Store \
    device-config:legacy_mode=true content-type=iso
```

</details>

**5.** Kontrolli Debianis, kas KVM on kasutatav ja mitu virtuaalmasinat libvirt'is töötab.

<details>
<summary>Lahendus</summary>

```bash
ls -l /dev/kvm
virsh -c qemu:///system list
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 27. KVM, Proxmox VE ja XCP-ng](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 28. Kubernetes: k3s →](../moodul-28-kubernetes/index.md)
<!-- /navigatsioon -->
