# Moodul 23. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis vahe on tüüp 1 ja tüüp 2 hüperviisoril? Too kummastki kaks näidet.
2. Milliseid protsessori laiendusi virtualiseerimine vajab ja kuidas nende olemasolu Linuxis kontrollida?
3. Mis on pesastatud virtualiseerimine ja millal seda vaja on?
4. Mis vahe on virtuaalmasinal, LXC konteineril ja Podmani konteineril?
5. Mis on VirtIO ja miks Windowsi VM vajab eraldi draivereid?
6. Selgita KVM-i, QEMU ja libvirt'i rolle.
7. Millist Debiani versiooni kasutab Proxmox VE 8 ja millist 9? Kuidas see mõjutab põhiversiooni uuendust?
8. Miks seadistatakse laboris no-subscription hoidla ja miks see tootmises ei ole soovitatav?
9. Mis vahe on täielikul ja lingitud kloonil?
10. Miks tuleb varukoopiast uue masina loomisel märkida *Unique*?
11. Miks hetktõmmis ei ole varukoopia? Miks tehakse laboris hetktõmmis väljalülitatud masinast ilma RAM-ita?
12. Kuidas pääsevad eraldi silla (`vmbr10`) masinad internetti? Millised read selleks `/etc/network/interfaces`-i lisatakse?
13. Mis on kvoorum ja miks vajab HA-klaster vähemalt kolme sõlme?
14. Mis on Xenis dom0 ja domU?
15. Mis on Xen Orchestra ja mis vahe on XOA-l ning lähtekoodist paigaldatud XO-l?

## Praktilised miniülesanded

1. Kirjuta käsud, mis näitavad Proxmoxi sõlme kõiki VM-e ja konteinereid.
2. Muuda VM-i 105 mälu 4 GiB-ks ja tuumade arvu 2-ks käsurealt.
3. Tee VM-ist 105 varukoopia režiimis *stop* ja taasta see uue ID-ga 150 nii, et MAC-aadress muutuks.
4. Loo XCP-ng-s kohalik ISO-repositoorium kataloogi `/var/opt/xen/ISO_Store`.
5. Kontrolli Debianis, kas KVM on kasutatav ja mitu virtuaalmasinat libvirt'is töötab.

---

## Vastused

1. Tüüp 1 töötab otse riistvaral (Proxmox VE/KVM, XCP-ng/Xen, ESXi, Hyper-V); tüüp 2 tavalise OS-i peal programmina (VirtualBox, VMware Workstation).
2. Intel VT-x või AMD-V (seadmete läbisuunamiseks VT-d/AMD-Vi): `grep -cE 'vmx|svm' /proc/cpuinfo`, `lscpu`, `/dev/kvm`.
3. Hüperviisori käitamine virtuaalmasinas - nt Proxmoxi või XCP-ng harjutamine laboris, WSL Windowsi VM-is.
4. VM-il on oma kernel ja terve OS; LXC on süsteemikonteiner (oma init, teenused, nagu väike VM), mis jagab hosti kernelit; Podmani konteiner on rakenduskonteiner, tavaliselt üks protsess/teenus.
5. Paravirtualiseeritud seadmed (ketas, võrk, mälu), mis on palju kiiremad kui emuleeritud riistvara. Linuxi kernelis on draiverid olemas, Windowsis mitte - need tulevad virtio-win ISO-lt.
6. KVM - kerneli moodul, mis kasutab protsessori virtualiseerimislaiendusi; QEMU - emuleerib ülejäänud riistvara ja käitab VM-i protsessina; libvirt - haldusteek ja teenus (`virsh`, virt-manager).
7. Proxmox VE 8 - Debian 12 „bookworm“, 9 - Debian 13 „trixie“. Põhiversiooni uuendus on ühtlasi Debiani väljalaske uuendus: hoidlates vahetatakse koodnimi ja tehakse `apt dist-upgrade`, kontrollskriptiga (`pve8to9`) eelnevalt.
8. Ilma tellimuseta ei pääse enterprise-hoidlale; no-subscription on tasuta, kuid vähem testitud ja ilma toeta.
9. Täielik kloon on iseseisev koopia; lingitud kloon kasutab malli ketast alusena ja salvestab ainult erinevused - kiire ja säästlik, kuid malli ei tohi kustutada.
10. Et uus masin saaks uue MAC-aadressi ja muud unikaalsed parameetrid, muidu tekivad võrgukonfliktid.
11. Hetktõmmis asub samal salvestusel ja sõltub algsest kettast. Väljalülitatud masinast ilma RAM-ita on hetktõmmis kiire ega lukusta masinat.
12. Hosti NAT-iga: `post-up echo 1 > /proc/sys/net/ipv4/ip_forward` ja `post-up iptables -t nat -A POSTROUTING -s '<võrk>' -o vmbr0 -j MASQUERADE` (+ vastav `post-down`).
13. Kvoorum on üle poole sõlmede häältest; ilma selleta lukustab klaster seadistuse, et vältida *split brain*-i. Kolme sõlmega jääb ühe rikke korral alles enamus.
14. dom0 - privilegeeritud haldus-Linux, mis haldab seadmeid ja XAPI-t; domU - tavalised külalismasinad.
15. XCP-ng serverite ja kogumite veebihaldus. XOA on valmis seade (tasuta versioon piiratud, tasuline tugi); XO lähtekoodist sisaldab kõiki funktsioone, kuid ilma toeta ja tuleb ise uuendada.

### Miniülesannete lahendused

```bash
qm list
pct list
```

```bash
qm set 105 --memory 4096 --cores 2
```

```bash
vzdump 105 --mode stop --compress zstd --storage local
qmrestore /var/lib/vz/dump/vzdump-qemu-105-<aeg>.vma.zst 150 --unique
```

```bash
mkdir -p /var/opt/xen/ISO_Store
xe sr-create name-label=LocalISO type=iso device-config:location=/var/opt/xen/ISO_Store \
    device-config:legacy_mode=true content-type=iso
```

```bash
ls -l /dev/kvm
virsh -c qemu:///system list
```
