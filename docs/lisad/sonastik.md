<!-- navigatsioon -->
[← UNIX-i ja Linuxi ajalugu](ajalugu.md) · [Sisukord](../../README.md#sisukord) · [Käskude loend →](kasud.md)
<!-- /navigatsioon -->

# Sõnastik

Kursusel kasutatavad mõisted koos ingliskeelse vastega. Sõnastikku täiendatakse koos uute moodulitega.

| Eesti keeles | Inglise keeles | Selgitus |
|---|---|---|
| absoluutne tee | absolute path | Juurkataloogist `/` algav tee |
| access-port | access port | Kommutaatori port, mis edastab ühe VLAN-i kaadreid ilma märgiseta |
| ACL | Access Control List | Täpsem õiguste loend lisaks omanikule ja grupile |
| ACME | Automatic Certificate Management Environment | Protokoll sertifikaatide automaatseks hankimiseks ja uuendamiseks (Let's Encrypt, certbot) |
| ajastaja | scheduler | Programm, mis käivitab töid kindlal ajal (cron) |
| ajavöönd | time zone | Piirkonna ajaarvestus, nt `Europe/Tallinn` |
| Alertmanager | Alertmanager | Prometheuse komponent, mis rühmitab häireid ja saadab teavitusi |
| alglaadija | bootloader | Programm, mis laadib kerneli (nt GRUB) |
| alglaadimine | boot | Arvuti käivitamine kuni operatsioonisüsteemi töövalmiduseni |
| alglaadimiskeskkond | boot environment | ZFS-i juurfailisüsteemi kloon, millest saab alglaadida; võimaldab uuenduse kiiret tagasivõttu (`bectl`) |
| alias (tulemüüris) | alias | Nimega rühm aadresse või porte, mida kasutatakse tulemüürireeglites |
| ALSA | AlmaLinux Security Advisory | AlmaLinuxi turvateade parandatud haavatavuse kohta |
| andmebaas | database | Struktureeritud andmete kogum ja seda haldav server |
| Ansible | Ansible | Agendita automatiseerimisvahend, mis seadistab masinaid SSH kaudu YAML-is kirjutatud mänguraamatute järgi |
| Apache | Apache HTTP Server | Levinud moodulipõhine veebiserver (`apache2`, `httpd`) |
| API | Application Programming Interface | Programmiliides, mille kaudu teine programm saab teenust kasutada (nt Proxmoxi REST API) |
| ARC | Adaptive Replacement Cache | ZFS-i lugemisvahemälu RAM-is |
| Argo CD | Argo CD | GitOps kontroller, mis rakendab Gitis kirjeldatud soovitud oleku Kubernetese klastrisse |
| argument | argument | Käsule antav sisend, nt failinimi |
| arhiiv | archive | Mitu faili ühes failis (nt `.tar`) |
| arvutikonto | computer account | Domeeniga liidetud masina konto Active Directorys |
| `at` | at | Käsk ühekordse töö käivitamiseks kindlal ajal |
| atribuut | attribute | LDAP-kirje väli, nt `uid` või `mail` |
| auditd | Linux Audit daemon | Kerneli auditisündmusi (sh SELinuxi keelamised) logiv teenus; logi `/var/log/audit/audit.log` |
| autofs | automounter | Teenus, mis haagib võrgukettad automaatselt esimesel kasutamisel ja lahutab jõudeolekus |
| avalik võti | public key | Võtmepaari jagatav osa |
| avatud relee | open relay | E-posti server, mis edastab kõigi kirju võõrastesse domeenidesse; rämpsposti tööriist |
| avatud resolver | open resolver | Rekursiivne DNS-server, mis vastab kõigile internetis; kasutatakse rünnakuteks |
| AVC | Access Vector Cache | SELinuxi keelamisteade auditilogis (`ausearch -m AVC`) |
| baassüsteem | base system | FreeBSD-s koos arendatav ja väljastatav kernel, teegid, põhikäsud ja dokumentatsioon |
| backports | backports | Debiani hoidla uuemate pakettide jaoks, mis on stabiilse väljalaske jaoks ümber ehitatud |
| Bastille | BastilleBSD | FreeBSD jail'ide haldamise tööriist |
| BIND | Berkeley Internet Name Domain | Levinuim DNS-serveri tarkvara (`named`, pakett `bind9`) |
| BIOS | Basic Input/Output System | Vana arvuti püsivara liides; asendunud UEFI-ga |
| box | box | Vagranti valmis põhitõmmis virtuaalmasina loomiseks |
| BSD | Berkeley Software Distribution | UNIX-ist pärinev operatsioonisüsteemide perekond (FreeBSD, OpenBSD); OPNsense põhineb FreeBSD-l |
| bsdinstall | bsdinstall | FreeBSD tekstipõhine paigaldusprogramm |
| BusyBox | BusyBox | Üks väike programm, mis asendab sadu tavalisi käske; kasutatakse konteinerites, ruuterites ja päästesüsteemides |
| Caddy | Caddy | Automaatse HTTPS-iga veebiserver |
| cert-manager | cert-manager | Kubernetese lisa, mis hangib ja uuendab TLS-sertifikaate automaatselt (nt ACME kaudu) |
| cgroup | control group | Kerneli mehhanism protsessirühmade ressursside (CPU, mälu, I/O) piiramiseks |
| CHAP | Challenge-Handshake Authentication Protocol | iSCSI ühenduse autentimine ühise saladusega |
| chrony | chrony | Täielik NTP klient ja server |
| chroot | chroot | Protsessi juurkataloogi vahetamine; kasutatakse süsteemi parandamiseks taastemeedialt ja SFTP-kasutajate piiramiseks, konteinerite eelkäija |
| CIFS | Common Internet File System | SMB vanem nimetus; Linuxis haakimise tüüp `cifs` |
| CIS | Center for Internet Security | Organisatsioon, mis avaldab süsteemide karastamise juhiseid (CIS Benchmarks) |
| cloud-init | cloud-init | Tööriist, mis seadistab virtuaalmasina esimesel käivitusel (nimi, IP, kasutaja, SSH-võti) |
| CNCF | Cloud Native Computing Foundation | Kubernetest ja teisi pilvepõhiseid projekte haldav sihtasutus |
| CNI | Container Network Interface | Liides ja pluginad, mis loovad podide võrgu (k3s-is Flannel) |
| Compose | Compose | Mitme konteineri teenuse kirjeldus ühes YAML-failis (`podman compose`, `docker compose`) |
| ConfigMap | ConfigMap | Kubernetese objekt seadistuse andmiseks podile failina või keskkonnamuutujana |
| containerd | containerd | Konteinerikäitur, mida kasutavad k3s ja Docker |
| Containerfile | Containerfile | Juhiste fail konteinerpildi ehitamiseks (sama mis `Dockerfile`) |
| copy-on-write | copy-on-write (CoW) | Andmeid ei kirjutata üle, vaid uude kohta (ZFS, Btrfs) |
| CoreDNS | CoreDNS | Pistikprogrammidega DNS-server, seadistus failis `Corefile` |
| coreutils | GNU core utilities | GNU põhikäskude pakett (`ls`, `cp`, `cat`, `sort` jt) |
| CRB | CodeReady Builder | AlmaLinuxi/RHEL-i lisahoidla arenduspakettidega, vajalik osale EPEL-i paketile |
| CrowdSec | CrowdSec | fail2bani-laadne ründetuvastus, mis jagab ründajate aadresse kogukonnaga |
| CSR | Certificate Signing Request | Sertifikaaditaotlus, mille CA allkirjastab |
| CSV | Comma-Separated Values | Tekstivormingus tabel, kus väljad on eraldatud komaga |
| CUPS | Common UNIX Printing System | Linuxi ja Unixi printimissüsteem |
| CVE | Common Vulnerabilities and Exposures | Turvaaukude rahvusvaheline tunnus |
| DAC | Discretionary Access Control | Tavaline õiguste mudel, kus faili omanik otsustab õiguste üle (rwx); vt MAC |
| dataset | dataset | ZFS-i pooli sees olev failisüsteem oma omadustega |
| deduplitseerimine | deduplication | Sama andmetüki salvestamine ainult üks kord, ka eri failide või varukoopiate vahel (ZFS, PBS, restic) |
| deduplitseerimistegur | deduplication factor | Näitab, mitu korda vähem ruumi andmed deduplitseerimise tõttu võtavad |
| Deployment | Deployment | Kubernetese objekt, mis hoiab rakenduse soovitud arvu pode ja haldab uuendusi |
| DHCP | Dynamic Host Configuration Protocol | Protokoll, millega võrguseadmed saavad automaatselt IP-aadressi ja võrguseaded |
| DHCP relee | DHCP relay | Ruuteri funktsioon, mis edastab DHCP-päringud teise võrgu serverile |
| diferentsiaalvarundus | differential backup | Varundus, mis kopeerib kõik viimasest täisvarundusest muutunud andmed |
| distributsioon, distro | distribution | Kernelist ja tarkvarast koosnev terviklik OS |
| DIT | Directory Information Tree | LDAP-kataloogi puukujuline struktuur |
| DKIM | DomainKeys Identified Mail | Väljuva e-kirja krüptograafiline allkiri, mida saaja kontrollib DNS-ist |
| DKMS | Dynamic Kernel Module Support | Süsteem, mis kompileerib kernelivälised moodulid uue kerneli jaoks automaatselt uuesti |
| DMARC | Domain-based Message Authentication, Reporting and Conformance | DNS-is avaldatud reegel, mida teha kirjaga, mis ei läbi SPF-i ega DKIM-i kontrolli |
| DN | Distinguished Name | LDAP-kirje täisnimi puus, nt `uid=mari,ou=People,dc=lab,dc=example` |
| DNAT | destination NAT | NAT, mis muudab sissetuleva paketi sihtaadressi (pordi edasisuunamine) |
| DNS | Domain Name System | Nimede ja IP-aadresside teisendamise süsteem |
| dnsmasq | dnsmasq | Kerge DNS-, DHCP- ja TFTP-server |
| doas | doas | OpenBSD-st pärit lihtne `sudo` alternatiiv (`/usr/local/etc/doas.conf`) |
| dom0, domU | domain 0, unprivileged domain | Xenis haldus-VM (dom0) ja tavalised külalismasinad (domU) |
| domeenikontroller | domain controller (DC) | Server, mis hoiab AD kataloogi ja autendib kasutajaid |
| domeen (AD) | domain | Ühise kataloogi ja turvapoliitikaga haldusala Active Directorys |
| Dovecot | Dovecot | IMAP- ja POP3-server ning e-posti autentimisteenus |
| DSA | Debian Security Advisory | Debiani turvateade parandatud haavatavuse kohta |
| eesmärk | target | systemd üksuste rühm, mis kirjeldab süsteemi olekut |
| eksportija | exporter | Programm, mis teeb mõõdikud Prometheusele kättesaadavaks (nt node_exporter) |
| eksport (NFS) | export | NFS-serveri jagatud kataloog ja selle õigused (`/etc/exports`) |
| EPEL | Extra Packages for Enterprise Linux | RHEL-i perekonna lisapakettide hoidla |
| esiplaan | foreground | Töö, mille lõppu kest ootab |
| etcd | etcd | Hajus võti-väärtus andmebaas, kus hoitakse Kubernetese klastri olekut |
| ettevalmistusala | staging area, index | Giti vaheala, kuhu `git add` paneb järgmisse sissekandesse minevad muudatused |
| ext4 | fourth extended filesystem | Debiani ja Ubuntu vaikimisi ajakirjaga failisüsteem |
| fail | file | Andmete kogum failisüsteemis |
| fail2ban | fail2ban | Teenus, mis loeb logisid ja blokeerib tulemüüris korduvalt ebaõnnestunud sisselogimisega aadressid |
| failisüsteem | filesystem | Viis andmete korraldamiseks andmekandjal |
| FHS | Filesystem Hierarchy Standard | Standard, mis määrab Linuxi kataloogide (`/etc`, `/var`, `/usr` jne) otstarbe |
| filtreeriv DNS | filtering DNS | DNS, mis blokeerib soovimatuid domeene (nt Pi-hole) |
| fish | friendly interactive shell | Kasutajasõbralik interaktiivne kest, mis ei ole POSIX-ühilduv |
| Flatpak | Flatpak | Distrost sõltumatu liivakastis rakenduste vorming (Flathub) |
| FOG | Free Open-source Ghost | Kettatõmmiste salvestamise ja masspaigalduse lahendus üle võrgu |
| FQDN | Fully Qualified Domain Name | Täielik domeeninimi koos kõigi tasemetega (nt `dc1.ad.lab.example`) |
| freebsd-update | freebsd-update | FreeBSD baassüsteemi ja kerneli binaaruuenduste tööriist |
| funktsioon | function | Nimega korduvkasutatav koodiplokk |
| füüsiline köide | physical volume, PV | LVM-i jaoks ettevalmistatud ketas või partitsioon |
| Galera | Galera Cluster | MariaDB mitme ülemaga sünkroonse replikatsiooni lahendus |
| GID | group ID | Grupi numbriline tunnus |
| GitOps | GitOps | Töövõte, kus süsteemi soovitud olek on Gitis ja kontroller rakendab muudatused automaatselt |
| GNU | GNU's Not Unix | Vaba tarkvara projekt, mille tööriistad (`bash`, `coreutils`, `gcc`) moodustavad koos Linuxi kerneliga tavalise Linuxi süsteemi |
| GnuPG | GNU Privacy Guard (GPG) | Avaliku võtme krüptograafia tööriist failide allkirjastamiseks ja krüpteerimiseks (`gpg`) |
| GPL | GNU General Public License | Copyleft-litsents, mille all on muu hulgas Linuxi kernel |
| GPO, rühmapoliitika | Group Policy Object | Windowsi arvutite ja kasutajate tsentraalselt hallatav seadistus |
| Grafana | Grafana | Mõõdikute visualiseerimise ja töölaudade tööriist |
| grupp | group | Kasutajate kogum ühiste õiguste andmiseks |
| haakepunkt | mount point | Kataloog, kuhu failisüsteem haagitakse |
| haakima | to mount | Failisüsteemi lisamine kataloogipuusse |
| hallatav sõlm | managed node | Masin, mida Ansible SSH kaudu seadistab |
| HAProxy | HAProxy | Kiire TCP/HTTP koormusejaotur |
| haru | branch | Gitis eraldi arendusliin |
| Helm | Helm | Kubernetese pakihaldur; pakett on tabel (*chart*) |
| hetktõmmis | snapshot | Köite või masina seisu jäädvustus kindlal hetkel |
| hoidla | repository | Tarkvarapakettide allikas |
| hoidla (Git) | repository | Projekti kataloog koos muudatuste ajalooga |
| .htaccess | .htaccess | Apache'i kataloogipõhine seadistusfail |
| HWE | Hardware Enablement | Ubuntu LTS-i uuemate kernelite ja draiverite pakk uuema riistvara toetamiseks |
| hädaolukorra režiim | emergency mode | Minimaalne režiim süsteemi parandamiseks |
| häire | alert | Teavitus, mis saadetakse, kui mõõdik ületab lubatud piiri |
| hüperviisor | hypervisor | Tarkvara, mis käitab virtuaalmasinaid (KVM, Xen, ESXi, Hyper-V) |
| hüppeserver | jump host, bastion | Vahepealne server, mille kaudu ühendutakse sisevõrgu masinatesse (`ssh -J`, `ProxyJump`) |
| idempotentsus | idempotence | Korduv rakendamine annab sama tulemuse |
| infrastruktuur koodina | infrastructure as code, IaC | Infrastruktuuri kirjeldamine tekstifailides |
| Ingress | Ingress | Kubernetese reegel, mis suunab HTTP(S) päringud nime ja tee järgi teenustele |
| initramfs | initial RAM file system | Mälus olev ajutine failisüsteem, mis laadib vajalikud moodulid ja haagib päris juurfailisüsteemi |
| initsiaator | initiator | iSCSI klient, mis kasutab võrguketast |
| inventuur | inventory | Ansible'i hallatavate serverite loend |
| IOPS | Input/Output Operations Per Second | Ketta sisend-väljundoperatsioonide arv sekundis |
| IPP | Internet Printing Protocol | Võrguprintimise protokoll (port 631), mida kasutab CUPS |
| iptables | iptables | Vanem Linuxi tulemüüri tööriist; asendunud nftables'iga |
| IPv6 | Internet Protocol version 6 | 128-bitiste aadressidega IP-protokolli versioon |
| iPXE | iPXE | Laiendatud võrgualglaadija, mis oskab laadida ka HTTP kaudu ja käivitada skripte |
| IQN | iSCSI Qualified Name | iSCSI seadme unikaalne nimi, nt `iqn.2026-11.example.lab:disk01` |
| iSCSI | Internet Small Computer Systems Interface | Protokoll plokkseadmete (ketaste) jagamiseks üle IP-võrgu |
| ISO-tõmmis | ISO image | Optilise ketta tõmmisfail, millena levitatakse distrode paigaldusmeediat |
| i-sõlm | inode | Failisüsteemi kirje, mis hoiab faili metaandmeid |
| jagatud teek | shared library | Programmide ühiskasutuses olev kood (`*.so`), mis laaditakse programmi käivitamisel (`ldd`, `ldconfig`) |
| jail | jail | FreeBSD isoleeritud keskkond oma failisüsteemi, IP-aadressi ja protsessidega, kuid hosti kerneliga |
| Jinja2 | Jinja2 | Mallimootor, mida Ansible kasutab muutujatega seadistusfailide loomiseks |
| journald | systemd-journald | systemd logiteenus, mille logisid loetakse käsuga `journalctl` |
| JSON | JavaScript Object Notation | Levinud tekstipõhine andmevorming (API-d, seadistusfailid) |
| juhtsõlm | control node | Masin, kus Ansible töötab ja kust hallatakse teisi masinaid |
| juurdekasvuvarundus | incremental backup | Varundus, mis kopeerib ainult eelmisest varundusest muutunud andmed |
| juurkasutaja | root, superuser | Piiramatute õigustega kasutaja |
| juurkataloog | root directory | Kataloogipuu algus `/` |
| järkjärguline uuendus | rolling update | Uuendus, kus vanad koopiad asendatakse uutega järk-järgult, nii et teenus ei katke |
| kaheastmeline autentimine | two-factor authentication (2FA) | Sisselogimine kahe eri teguriga, nt SSH võti ja telefoni kood |
| Kali Linux | Kali Linux | Turvatestimiseks mõeldud Debianil põhinev distro |
| karastamine | hardening | Süsteemi turvalisemaks muutmine seadistuse abil |
| kasutusjuhend | manual page, man page | Käsu dokumentatsioon (`man`) |
| kataloog | directory | Failide konteiner (Windowsis „kaust“) |
| kataloogiteenus | directory service | Kasutajate, gruppide ja muu info keskne andmebaas (LDAP, AD) |
| kaughoidla | remote | Teises masinas (nt GitHubis) asuv Giti hoidla, kuhu tehakse `push` ja kust `pull` |
| k3s | k3s | Kerge sertifitseeritud Kubernetese distributsioon ühe binaarfailina |
| KDC | Key Distribution Center | Kerberose server, mis väljastab pileteid (AD-s domeenikontroller) |
| Kea | ISC Kea | ISC DHCP-server (asendab vana `isc-dhcp-server`-it) |
| keepalived | keepalived | VRRP-l põhinev teenus, mis tõstab virtuaalse IP-aadressi rikke korral varumasinale |
| Kerberos | Kerberos | Piletitel põhinev võrguautentimise protokoll |
| kerneli moodul | kernel module | Töö ajal laaditav kerneli osa (nt draiver) |
| kernel, tuum | kernel | Operatsioonisüsteemi riistvara haldav osa |
| keskkonnamuutuja | environment variable | Muutuja, mis pärandatakse käivitatavatele programmidele |
| kest | shell | Käske tõlgendav programm, nt Bash, `sh`, `zsh` või `fish`; vt ka sisselogimiskest |
| kickstart | kickstart | Red Hati perekonna automaatse paigalduse vastustefail (`inst.ks=`) |
| kihiline kaitse | defense in depth | Mitme teineteist täiendava kaitsekihi kasutamine |
| kodukataloog | home directory | Kasutaja isiklik kataloog, nt `/home/mari` |
| kohustuslik juurdepääsukontroll | mandatory access control, MAC | Süsteemne poliitika, mida ei saa mööda minna ka juurkasutaja (SELinux, AppArmor) |
| kompileerimine | compiling | Lähtekoodi tõlkimine käivitatavaks programmiks |
| konsool | console | Otse ühendatud ekraan ja klaviatuur või VM-i konsooliaken |
| konteiner | container | Isoleeritud protsess oma failisüsteemiga, jagab hosti kernelit |
| konteinerpilt | container image | Muutumatu mall, millest konteiner käivitatakse |
| kontrollsumma | checksum | Faili sisust arvutatud räsi, millega kontrollitakse, et fail pole muutunud (`sha256sum`) |
| koormus | load average | Protsessorit ootavate protsesside keskmine arv |
| koormusejaotur | load balancer | Jagab päringud mitme taustserveri vahel |
| koormustest | load test | Serveri jõudluse mõõtmine paljude samaaegsete päringutega (`ab`, `wrk`, k6) |
| KPI | Key Performance Indicator | Mõõdetav tulemusnäitaja, mille järgi hinnatakse, kas teenus täidab eesmärki |
| kubeconfig | kubeconfig | `kubectl`-i seadistusfail klastri aadressi ja ligipääsuvõtmetega (k3s-is `/etc/rancher/k3s/k3s.yaml`) |
| kubectl | kubectl | Kubernetese klastri käsurea haldustööriist |
| kubelet | kubelet | Kubernetese sõlme agent, mis käivitab podide konteinerid ja annab olekust teada |
| Kubernetes | Kubernetes | Konteinerite orkestreerimise platvorm mitme serveri klastris |
| kujutisfail | image file | Terve andmekandja või ketta sisu ühes failis (.iso, .img, .qcow2) |
| kuvaprotokoll | display protocol | Rakenduste ja ekraani suhtlusviis (Wayland, X11) |
| KVM | Kernel-based Virtual Machine | Linuxi kerneli virtualiseerimismoodul |
| kvoorum | quorum | Klastri sõlmede enamus, mis on vajalik otsuste tegemiseks |
| kõrge kättesaadavus | high availability (HA) | Lahendus, mis jätkab tööd ka ühe komponendi rikke korral |
| kõvaviit | hard link | Sama faili (i-sõlme) teine nimi |
| käsiraamat | runbook | Sammhaaval juhised tüüpiliste haldustoimingute ja rikete lahendamiseks |
| käsitleja | handler | Ansible'i ülesanne, mis käivitub ainult siis, kui mõni muu ülesanne muutis midagi (nt teenuse taaskäivitus) |
| käsk | command | Programm või kesta sisekäsk |
| käskude asendus | command substitution | Käsu väljundi kasutamine väärtusena (`$( )`) |
| käsuajalugu | command history | Varem sisestatud käskude loend |
| käsurežiim | command-line mode | vim-i režiim (`:`), kus antakse käske, nt `:wq` |
| käsurida | command line | Tekstipõhine töökeskkond |
| kättesaadavus | availability | Osa ajast, mil teenus töötab (nt 99,9%) |
| köide | volume | Püsiv andmehoidla konteineri jaoks |
| köitegrupp | volume group, VG | LVM-is füüsiliste köidete ühendatud ruum |
| LACP | Link Aggregation Control Protocol | Mitme võrguliidese ühendamine üheks loogiliseks liideseks (802.3ad) |
| LAM | LDAP Account Manager | Veebiliides LDAP-i kasutajate ja gruppide haldamiseks |
| LAN | Local Area Network | Kohtvõrk; tulemüüri sisemine võrk |
| LDAP | Lightweight Directory Access Protocol | Kataloogiteenuse päringuprotokoll |
| LDAPS | LDAP over SSL/TLS | TLS-iga krüpteeritud LDAP-ühendus (port 636) |
| LDIF | LDAP Data Interchange Format | Tekstivorming LDAP-kirjete lisamiseks ja muutmiseks |
| leviedastus | broadcast | Pakett, mis saadetakse kõigile kohtvõrgu seadmetele |
| libvirt | libvirt | KVM-i ja teiste hüperviisorite haldusliides (`virsh`, `virt-manager`) |
| lighttpd | lighttpd | Väga kerge veebiserver |
| ligipääsetavus | accessibility | Võimalused, mis teevad süsteemi kasutatavaks erivajadusega inimestele (ekraanilugeja, luup, kleepuvad klahvid) |
| liides | interface | Võrguühenduse lõpp-punkt (nt `ens18`) |
| liitliides | bond, link aggregation | Mitu füüsilist võrguliidest ühe loogilise liidesena (rikkekindlus või läbilaskevõime) |
| liitmistaotlus | pull request, merge request | Ettepanek liita haru muudatused põhiharusse koos ülevaatusega |
| liitumisluba | join token | Saladus, millega uus sõlm klastriga liitub (k3s `K3S_TOKEN`) |
| liivakast | sandbox | Piiratud keskkond, kus programm näeb ja tohib teha ainult vähe (nt systemd turvaseaded) |
| link-local aadress | link-local address | Ainult kohtvõrgus kehtiv aadress (IPv6-s `fe80::/10`) |
| LIO | Linux-IO | Linuxi kerneli iSCSI sihtmärgi alamsüsteem (`targetcli`) |
| lisagrupp | supplementary group | Grupp, kuhu kasutaja kuulub lisaks põhigrupile |
| live-süsteem | live system | Andmekandjalt käivituv OS, mis ei vaja paigaldust |
| logide rotatsioon | log rotation | Logifailide regulaarne ümbernimetamine, pakkimine ja kustutamine |
| logrotate | logrotate | Tööriist, mis pöörab, pakib ja kustutab vanu logifaile |
| lokaat | locale | Keele, kuupäevade ja arvude vormingu seaded (nt `et_EE.UTF-8`) |
| Longhorn | Longhorn | Kubernetese hajus plokksalvestus, mis replikeerib andmeid sõlmede vahel |
| loogiline köide | logical volume, LV | LVM-is köitegrupist eraldatud kasutatav osa |
| LTS | Long Term Support | Pika toega väljalase (nt Ubuntu LTS - 5 aastat tavatuge) |
| lubav litsents | permissive licence | Litsents, mis lubab koodi kasutada ka kinnises tootes (MIT, BSD, Apache) |
| LUKS | Linux Unified Key Setup | Linuxi ketta krüpteerimise standard (`cryptsetup`) |
| LUN | Logical Unit Number | iSCSI sihtmärgi poolt jagatav üksik ketas |
| LVM-thin | LVM thin provisioning | LVM-i õhukeselt eraldatud kogum, millest ruumi võetakse alles kirjutamisel (Proxmoxi `local-lvm`) |
| lõhestunud aju | split brain | Olukord, kus kaks sõlme peavad end korraga põhisõlmeks ja andmed või aadressid lähevad lahku |
| lähtekood | source code | Programmi inimloetav kood |
| LXC | Linux Containers | Süsteemikonteinerid, mis käituvad nagu kerged virtuaalmasinad (Proxmox) |
| Lynis | Lynis | Süsteemi turvalisuse auditeerimise tööriist, mis annab karastamise soovitusi |
| Maildir | Maildir | Postkasti vorming, kus iga kiri on eraldi fail |
| mall (systemd) | template unit | Üksuse fail nimega `nimi@.service`, millest käivitatakse mitu eksemplari (`%i`) |
| manifest | manifest | YAML-fail, mis kirjeldab Kubernetese objektide soovitud olekut |
| manustatud andmebaas | embedded database | Andmebaas, mis on rakenduse sees ühe failina (SQLite) |
| MariaDB | MariaDB | MySQL-i haru, levinud avatud lähtekoodiga andmebaasiserver |
| marsruut | route | Reegel, kuhu pakette saata |
| masquerade | masquerade (SNAT) | NAT, mis asendab väljuva paketi lähteaadressi ruuteri aadressiga |
| massiiv | array | Mitut väärtust sisaldav muutuja |
| MDA | Mail Delivery Agent | Programm, mis paneb kirja postkasti (Dovecot) |
| mdadm | mdadm | Linuxi tarkvaralise RAID-i haldustööriist |
| metamärk | wildcard, glob | Mitmele failinimele sobiv muster (`*`, `?`) |
| mets | forest | Active Directory kõrgeim struktuur: üks või mitu ühise skeemiga domeeni |
| minikube | minikube | Ühe sõlme Kubernetese klaster arendaja arvutis |
| Molecule | Molecule | Ansible'i rollide testimise raamistik |
| MTA | Mail Transfer Agent | E-kirju edastav server (nt Postfix) |
| MUA | Mail User Agent | Kasutaja e-posti programm (Thunderbird, Outlook) |
| muudatuste logi | change log | Kirjed selle kohta, mis, millal ja miks süsteemis muudeti |
| muutuja | variable | Nimega väärtus |
| muutumatu distro | immutable / atomic distribution | Ainult lugemiseks süsteem, mida uuendatakse tervikuna (SteamOS, Silverblue) |
| mõõdik | metric | Arvuline näitaja ajas (nt protsessori kasutus) |
| mänguraamat | playbook | Ansible'i ülesannete kirjeldus YAML-failis |
| NAS | Network Attached Storage | Võrgu kaudu faile jagav salvestusseade või -süsteem (nt TrueNAS) |
| NAT | Network Address Translation | Aadresside teisendus, millega sisevõrgu masinad kasutavad ühist avalikku aadressi |
| NDP | Neighbor Discovery Protocol | IPv6 naabrite ja ruuterite leidmine (asendab ARP-i), kasutab ICMPv6-t |
| netfilter | netfilter | Linuxi kerneli pakettide filtreerimise raamistik, mida kasutavad nftables ja iptables |
| newsyslog | newsyslog | FreeBSD logide pööramise tööriist (Linuxi `logrotate` vaste) |
| NFS | Network File System | Linuxi/UNIX-i võrgufailisüsteem kataloogide jagamiseks |
| nftables | nftables | Linuxi tänapäevane tulemüüri tööriist (`nft`) |
| nginx | nginx | Kerge ja kiire veebiserver ning pöördpuhver |
| nimelahendus | name resolution | Nime teisendamine IP-aadressiks |
| nimeruum | namespace | Kerneli võimalus protsesside, võrgu jms isoleerimiseks |
| NoSQL | NoSQL | Mitterelatsioonilised andmebaasid (võti-väärtus, dokumendid jt) |
| NSS | Name Service Switch | Linuxi mehhanism, mis määrab, kust otsitakse kasutajaid, gruppe ja nimesid (`/etc/nsswitch.conf`) |
| NTP | Network Time Protocol | Kellaaja sünkroniseerimise protokoll (port 123/udp) |
| objektiklass | object class | LDAP-kirje tüüp, mis määrab kohustuslikud ja lubatud atribuudid |
| olekupõhine tulemüür | stateful firewall | Tulemüür, mis jätab ühendused meelde ja lubab automaatselt vastuspaketid |
| omanduslik tarkvara | proprietary software | Kinnise lähtekoodiga tarkvara, mille kasutusõigus ostetakse |
| OOM killer | out-of-memory killer | Kerneli mehhanism, mis mälu lõppemisel lõpetab protsessi |
| OpenLDAP | OpenLDAP | Avatud lähtekoodiga LDAP-kataloogiserver (`slapd`) |
| OpenZFS | OpenZFS | ZFS-i avatud lähtekoodiga arendus, mida kasutavad nii FreeBSD kui ka Linux |
| OpenTofu | OpenTofu | Terraformi vaba haru infrastruktuuri deklaratiivseks loomiseks koodi järgi |
| orkestreerimine | orchestration | Konteinerite automaatne paigutamine, käivitamine, skaleerimine ja taastamine mitme masina vahel |
| otsuste logi | decision log, ADR | Kirjed oluliste tehniliste valikute ja nende põhjuste kohta |
| OU | Organizational Unit | Kataloogi kaust kasutajate ja arvutite rühmitamiseks |
| paik | patch | Failide erinevuste kirjeldus, mida saab rakendada käsuga `patch` |
| pakett | package | Paigaldatav tarkvaraühik |
| pakihaldur | package manager | Tarkvara paigaldamise ja uuendamise vahend |
| pakkimine | compression | Faili mahu vähendamine (nt gzip) |
| pakkuja (OpenTofu) | provider | OpenTofu/Terraformi lisamoodul, mis suhtleb kindla platvormi API-ga (nt Proxmox) |
| PAM | Pluggable Authentication Modules | Linuxi moodulipõhine autentimise raamistik (`/etc/pam.d/`) |
| paroolifraas | passphrase | Parool, millega kaitstakse privaatvõtit (nt SSH-võti) |
| paroolipoliitika | password policy | Nõuded parooli pikkusele, keerukusele ja aegumisele (`pam_pwquality`, `chage`) |
| partitsioon | partition | Ketta osa |
| partitsioonitabel | partition table | Ketta partitsioonide kirjeldus (MBR, GPT) |
| Patroni | Patroni | PostgreSQL-i kõrge kättesaadavuse haldur automaatse ülevõtuga |
| peidetud fail | hidden file | Punktiga algava nimega fail |
| periodic | periodic | FreeBSD igapäevaste, -nädalaste ja -kuiste hooldusskriptide käivitaja |
| pesastatud virtualiseerimine | nested virtualization | Hüperviisori käitamine virtuaalmasinas |
| pesaüksus | socket unit | systemd `.socket` üksus, mis kuulab porti ja käivitab teenuse alles ühenduse saabumisel |
| pesa aktiveerimine | socket activation | systemd kuulab porti teenuse eest ja käivitab teenuse esimese ühenduse saabumisel |
| pf | Packet Filter | OpenBSD-st pärit tulemüür FreeBSD-s (`/etc/pf.conf`, `pfctl`); kehtib viimane sobiv reegel |
| pfSense | pfSense | FreeBSD-l põhinev tulemüüri- ja ruuterilahendus (OPNsense-i eelkäija) |
| PHP-FPM | PHP FastCGI Process Manager | Eraldi teenus, mis käivitab veebiserveri jaoks PHP-skripte |
| PID | process ID | Protsessi numbriline tunnus |
| pilet | ticket | Kerberose ajutine tõend autentimiseks (nt TGT) |
| pilvetõmmis | cloud image | Valmis paigaldatud kettatõmmis koos cloud-initiga, millest tehakse virtuaalmasina mall |
| pkgbase | pkgbase | FreeBSD baassüsteem pakettidena, mida uuendab `pkg` |
| plokkseade | block device | Seade, kust andmeid loetakse plokkide kaupa (ketas) |
| pod | pod | Kubernetese väikseim üksus: üks või mitu ühise võrgu ja kettaga konteinerit |
| Podman | Podman | Deemonita konteinerimootor, mis töötab ka ilma juurkasutajata |
| pool | pool, zpool | ZFS-i ketaste ühine salvestusruum |
| pordid | ports | FreeBSD retseptide kogum tarkvara kompileerimiseks lähtekoodist (`/usr/ports`) |
| pordisuunamine | port forwarding | Välise pordi liikluse suunamine sisevõrgu masinale |
| port | port | Teenust tähistav number (nt 22, 443) |
| portaal (iSCSI) | portal | iSCSI sihtmärgi IP-aadress ja port, mille kaudu initsiaator ühendub |
| POSIX | Portable Operating System Interface | Standard, mis kirjeldab Unixi-laadse süsteemi käske, kesta ja liideseid; POSIX-ile vastav skript töötab eri süsteemides |
| POSIX-ühilduvus | POSIX compliance | Kesta või tööriista vastavus POSIX-standardile, nii et standardse süntaksiga skriptid töötavad selles |
| PostgreSQL | PostgreSQL | Võimas avatud lähtekoodiga relatsiooniline andmebaas |
| PPA | Personal Package Archive | Ubuntu isiklik pakettide hoidla |
| preseed | preseed | Debiani automaatse paigalduse vastustefail |
| prindiserver | print server | Server, mis hoiab printerite järjekordi ja jagab printereid võrku |
| privaatvõti | private key | Võtmepaari salajane osa |
| PromQL | Prometheus Query Language | Prometheuse päringukeel |
| proovieksam | mock exam | Praktiline harjutuseksam ajapiiranguga |
| proovirežiim | dry run | Režiim, mis näitab, mida tehtaks, ilma tegemata |
| Proton | Proton | Valve'i ühilduvuskiht Windowsi mängude käitamiseks Linuxis |
| protsess | process | Töötav programm |
| Proxmox Backup Server | Proxmox Backup Server (PBS) | Proxmoxi deduplitseeriv ja inkrementaalne varundusserver |
| Puppet | Puppet | Agendipõhine seadistushaldur: serverid küsivad keskserverist ise oma seadistust (pull) |
| PVC | PersistentVolumeClaim | Kubernetese podi taotlus püsiketta järele |
| põhigrupp | primary group | Kasutaja vaikegrupp, millele kuuluvad tema loodud failid |
| päringute piirang | rate limit | Teenuse seatud piir, mitu päringut ajaühikus lubatakse (nt Let's Encrypt) |
| pöördpuhverserver | reverse proxy | Server, mis edastab päringud taustal töötavale rakendusele |
| pöördtsoon | reverse zone | DNS-tsoon, mis seob IP-aadressid nimedega (PTR-kirjed, `in-addr.arpa`) |
| püsivara | firmware | Emaplaadi programm, mis käivitub esimesena (BIOS, UEFI) |
| PXE | Preboot Execution Environment | Arvuti käivitamine võrgust |
| QEMU | Quick Emulator | Riistvara emulaator, mis koos KVM-iga käitab virtuaalmasinaid |
| Quadlet | Quadlet | Podmani viis kirjeldada konteinereid systemd üksustena (`.container` failid) |
| rc.conf | rc.conf | FreeBSD peamine seadistusfail: hostinimi, võrk ja lubatud teenused |
| RDN | Relative Distinguished Name | DN-i üks osa, nt `uid=mari` |
| RDP | Remote Desktop Protocol | Microsofti kaugtöölaua protokoll |
| realm | realm | Kerberose haldusala, kirjutatakse suurtähtedega (nt `AD.LAB.EXAMPLE`) |
| realmd | realmd | Tööriist (`realm join`), mis liidab Linuxi masina domeeniga ja seadistab SSSD |
| register | registry | Konteinerpiltide hoidla (nt docker.io) |
| regulaaravaldis | regular expression, regex | Muster teksti otsimiseks |
| rekursiivne | recursive | Kehtib ka kõigile alamkataloogidele |
| relee | relay, smarthost | SMTP-server, mille kaudu server oma kirjad edastab |
| rent | lease | DHCP-serveri poolt ajutiselt antud aadress |
| replikatsioon | replication | Andmete pidev kopeerimine teise serverisse |
| reserveering | reservation | DHCP-s kindlale MAC-aadressile seotud IP-aadress |
| ressursikogum | resource pool | Proxmoxi rühm VM-e ja salvestusi õiguste jagamiseks |
| ressursipiirang | resource limit | Protsessi või teenuse lubatud ressursside ülempiir (`ulimit`, `MemoryMax=`) |
| rikketest | failover test | Komponendi teadlik väljalülitamine, et kontrollida lahenduse töökindlust |
| roll (Ansible) | role | Korduvkasutatav Ansible'i ülesannete, mallide ja muutujate komplekt kindlas kataloogistruktuuris |
| roll (PostgreSQL) | role | PostgreSQL-i kasutaja või grupp |
| root_squash | root squash | NFS-i vaikevalik, mis muudab kliendi juurkasutaja serveris õigusteta kasutajaks |
| round robin | round robin | Koormuse jaotamine kordamööda kõigile serveritele |
| RPO | Recovery Point Objective | Kui palju andmeid (ajas mõõdetuna) tohib rikke korral kaotada |
| RSAT | Remote Server Administration Tools | Windowsi tööriistad AD ja serverite kaughalduseks |
| rsync | rsync | Failide sünkroonimise tööriist, mis kopeerib ainult muudatused |
| rsyslog | rsyslog | Traditsiooniline syslogi teenus, mis kirjutab logid `/var/log` failidesse ja saadab neid võrku |
| RTO | Recovery Time Objective | Kui kiiresti peab teenus pärast riket taastuma |
| räsi | hash | Andmetest (nt paroolist või failist) arvutatud lühike pöördumatu väärtus; vt ka kontrollsumma |
| saaleala | swap | Kettaruum, mida kasutatakse mälu laiendusena |
| SAN | Subject Alternative Name | Sertifikaadi väli, kus on loetletud kõik nimed, mille jaoks sertifikaat kehtib |
| scrub | scrub | ZFS-i kõigi andmete läbilugemine ja kontrollsummade kontroll |
| SDN | Software-Defined Networking | Tarkvaraliselt hallatav võrk (Proxmoxis tsoonid ja VNet-id kogu klastris) |
| seansi püsivus | sticky sessions | Koormusejaoturi seade, mis saadab sama kliendi alati samale taustserverile |
| seccomp | secure computing mode | Kerneli mehhanism, mis piirab protsessi lubatud süsteemikutseid |
| Secret | Secret | Kubernetese objekt saladuste (paroolid, võtmed) hoidmiseks; vaikimisi ainult base64-kodeeritud |
| sekundaarserver | secondary server | DNS-server, mis hoiab primaari tsoonist koopiat ja vastab samamoodi |
| sertifikaat | certificate | Allkirjastatud dokument, mis seob avaliku võtme serveri nimega |
| sertifitseerimiskeskus | certificate authority, CA | Asutus või süsteem, mis allkirjastab sertifikaate |
| SFTP | SSH File Transfer Protocol | Failiedastus SSH kaudu |
| SGID | set group ID | Kataloogil: uued failid saavad kataloogi grupi |
| shebang | shebang | Skripti esimene rida, mis määrab tõlgendaja (`#!/bin/bash`) |
| ShellCheck | ShellCheck | Shelliskriptide staatilise analüüsi tööriist, mis leiab levinud vigu |
| SIEM | Security Information and Event Management | Turvasündmuste keskne kogumine ja analüüs (nt Wazuh) |
| signaal | signal | Protsessile saadetav teade (nt SIGTERM) |
| sihtmärk | target | iSCSI server, mis jagab kettaid |
| silt | label | Võti-väärtus märgend, millega objekte valitakse (Kubernetes, konteinerid, Prometheus) |
| silumine | debugging | Vigade otsimine programmist |
| sisestusrežiim | insert mode | vim-i režiim teksti kirjutamiseks (`i`, väljumine `Esc`) |
| sissekanne | commit | Gitis salvestatud hetkeseis koos kirjeldusega |
| sisselogimishaldur | display manager | Graafiline sisselogimisekraan (GDM, SDDM, LightDM) |
| sisselogimiskest | login shell | Kasutaja vaikekest failis `/etc/passwd`, mis käivitub sisselogimisel; muudetakse käsuga `chsh` |
| skeem | schema | Reeglid, millised objektiklassid ja atribuudid kataloogis (LDAP, AD) lubatud on |
| skeletikataloog | skeleton directory | `/etc/skel` - failid, mis kopeeritakse uue kasutaja kodukataloogi |
| skript | script | Käskude jada sisaldav tekstifail |
| SLA | Service Level Agreement | Teenusetaseme leping: lubatud teenuse tase ja reageerimisaeg |
| SLAAC | Stateless Address Autoconfiguration | IPv6 aadressi automaatne seadistamine ruuteri teadaannete põhjal |
| SLO | Service Level Objective | Teenusetaseme eesmärk: sisemine sihtväärtus ühele näitajale |
| SMART | Self-Monitoring, Analysis and Reporting Technology | Ketaste enesediagnostika (`smartctl`) |
| SMB | Server Message Block | Windowsi failijagamise protokoll; Linuxis Samba |
| SOA | Start of Authority | Tsooni põhikirje: nimeserver, seerianumber ja ajad |
| SPF | Sender Policy Framework | DNS-kirje, mis loetleb domeeni nimel e-kirju saata lubatud serverid |
| SPICE | Simple Protocol for Independent Computing Environments | Virtuaalmasina graafilise konsooli protokoll (Proxmox, virt-manager) |
| SQL | Structured Query Language | Relatsiooniliste andmebaaside päringukeel |
| SQLite | SQLite | Failipõhine manustatud andmebaas |
| SRV-kirje | SRV record | DNS-kirje, mis näitab teenuse hosti ja porti |
| SSD | Solid State Drive | Pooljuhtketas, ilma liikuvate osadeta |
| `ssh-agent` | ssh-agent | Programm, mis hoiab lahtikrüpteeritud SSH võtmeid mälus, et parooli ei peaks iga kord sisestama |
| SSL | Secure Sockets Layer | TLS-i vananenud eelkäija; nimetust kasutatakse sageli TLS-i kohta |
| SSSD | System Security Services Daemon | Linuxi teenus, mis ühendab NSS-i ja PAM-i LDAP-i või AD-ga |
| staatiline marsruut | static route | Käsitsi seadistatud marsruut kindlasse võrku kindla ruuteri kaudu |
| standardsisend | standard input, stdin | Programmi sisendvoog (0) |
| standardveaväljund | standard error, stderr | Programmi veateadete voog (2) |
| standardväljund | standard output, stdout | Programmi väljundvoog (1) |
| StartTLS | STARTTLS | Tavalise ühenduse üleviimine krüpteeritud TLS-ühenduseks samas pordis |
| StatefulSet | StatefulSet | Kubernetese kontroller püsiva nime ja kettaga podidele (nt andmebaasid) |
| SteamOS | SteamOS | Valve'i Arch-põhine mängudistro |
| sticky bit | sticky bit | Kataloogil: faile saab kustutada ainult nende omanik |
| StorageClass | StorageClass | Kubernetese objekt, mis määrab, kuidas ja kust püsikettad luuakse (k3s-is `local-path`) |
| strace | strace | Tööriist programmi süsteemikutsete jälgimiseks |
| sudoers | sudoers | `sudo` õiguste seadistus (`/etc/sudoers`, `/etc/sudoers.d/`), muudetakse käsuga `visudo` |
| suhteline tee | relative path | Praegusest kataloogist algav tee |
| SUID | set user ID | Programm töötab faili omaniku õigustes |
| sõlm (klastris) | node | Klastri üks masin |
| sõltuvus | dependency | Pakett, mida teine pakett töötamiseks vajab |
| säilitusreegel | retention policy, prune | Reegel, mitu varukoopiat (päeva, nädala, kuu kaupa) alles hoida |
| süsteemikutse | system call | Programmi pöördumine kerneli poole (nt faili avamine) |
| systemd-resolved | systemd-resolved | systemd DNS-i lahendaja teenus (Ubuntu vaikimisi, `resolvectl`) |
| SYSVOL | SYSVOL | AD domeenikontrolleri jagatud kaust rühmapoliitikate ja sisselogimisskriptide jaoks |
| Zabbix | Zabbix | Agendipõhine monitooringusüsteem häirete ja töölaudadega |
| ZFS | ZFS | Failisüsteem ja köitehaldur ühes, kontrollsummade ja hetktõmmistega |
| zsh | Z shell | Bashi-sarnane, peaaegu POSIX-ühilduv kest täiustatud lõpetamise ja pluginatega (macOS-i vaikekest) |
| zvol | ZFS volume | ZFS-i pooli sees olev plokkseade |
| taastamisrežiim | rescue mode | Vähendatud režiim süsteemi hoolduseks |
| taastamistest | restore test | Päris taastamine testkeskkonda koos aja mõõtmisega, et kontrollida varukoopia kasutatavust |
| tagasipööramine | rollback, downgrade | Muudatuse tagasivõtmine või paketi viimine vanemale versioonile |
| tagasisidestus | loopback | Liides, mille kaudu masin räägib iseendaga (`lo`) |
| taimer | timer | systemd üksus ajastatud käivitamiseks |
| taust | background | Töö, mis töötab ilma kesta ootamata |
| taustserver | backend | Koormusejaoturi või pöördpuhvri taga töötav server |
| tavarežiim | normal mode | vim-i vaikerežiim, kus klahvid on käsud (liikumine, kustutamine, kopeerimine) |
| tee | path | Faili või kataloogi asukoht |
| teenus | service, daemon | Taustal töötav programm |
| teeüksus | path unit | systemd üksus, mis käivitab teenuse faili või kataloogi muutumisel |
| tekstiredaktor | text editor | Programm tekstifailide muutmiseks (nano, vim) |
| terminal | terminal (emulator) | Tekstiakent kuvav programm |
| Terraform | Terraform | HashiCorpi tööriist infrastruktuuri deklaratiivseks loomiseks koodi järgi (BSL-litsents) |
| tervisekontroll | health check | Taustserveri kättesaadavuse regulaarne kontroll |
| TFTP | Trivial File Transfer Protocol | Lihtne failiedastusprotokoll, mida kasutab PXE |
| TGT | Ticket Granting Ticket | Kerberose sisselogimispilet, millega küsitakse teenusepileteid |
| TLS | Transport Layer Security | Krüpteeritud ühenduse protokoll (HTTPS, LDAPS, SMTPS) |
| tmux | terminal multiplexer | Terminalijagur, mille seanss jääb SSH-ühenduse katkemisel alles |
| toru | pipe | Ühe käsu väljundi suunamine teise sisendiks (`\|`) |
| TOTP | Time-based One-Time Password | Ajapõhine ühekordne kood (telefonirakendus), mida kasutatakse kaheastmelisel autentimisel |
| TPM | Trusted Platform Module | Turvakiip (või virtuaalne vaste), mida nõuab nt Windows 11 |
| Traefik | Traefik | Konteineritele mõeldud pöördpuhver ja koormusejaotur |
| trunk-port | trunk port | Kommutaatori port, mis edastab mitme VLAN-i kaadreid märgistega |
| tsoon | zone | DNS-is ühe domeeni kirjete kogum |
| tsooniülekanne | zone transfer (AXFR/IXFR) | Tsooni kopeerimine primaarserverilt sekundaarserverile |
| tsükkel | loop | Korduvalt täidetav koodiplokk |
| tulemüür | firewall | Võrguliikluse filtreerimise süsteem |
| tuned | tuned | Teenus, mis rakendab süsteemile jõudlusprofiile (`tuned-adm`) |
| turvakontekst | security context | SELinuxi märgis failil, protsessil või pordil |
| turvauuendus | security update | Turvaauku parandav tarkvarauuendus |
| täisvarundus | full backup | Varundus, mis kopeerib kõik andmed |
| töölauakeskkond | desktop environment | Graafiline kasutajaliides (GNOME, KDE Plasma, Xfce) |
| udev | udev | Teenus, mis reageerib riistvara sündmustele: laadib moodulid, loob seadmefailid ja püsivad nimed, käivitab reeglid |
| UDP | User Datagram Protocol | Ühenduseta transpordiprotokoll (DNS, DHCP, NTP, WireGuard) |
| UEFI | Unified Extensible Firmware Interface | Tänapäevane püsivara liides, mis asendab BIOS-i; alglaadija on EFI süsteemipartitsioonil |
| UID | user ID | Kasutaja numbriline tunnus |
| ULA | Unique Local Address | IPv6 privaatvõrgu aadress (`fd00::/8`), IPv4 `10.0.0.0/8` vaste |
| umask | umask | Mask, mis määrab uute failide vaikimisi õigused |
| Unbound | Unbound | Rekursiivne ja vahemäluga DNS-lahendaja |
| UNIX | UNIX | 1969. aastal Bell Labsis loodud operatsioonisüsteem, Linuxi ja BSD eeskuju |
| UNIX-i filosoofia | Unix philosophy | Põhimõtted: iga programm teeb üht asja hästi, programmid töötavad koos, tekst on universaalne liides |
| Uptime Kuma | Uptime Kuma | Lihtne veebipõhine teenuste kättesaadavuse jälgija |
| URL | Uniform Resource Locator | Veebiressursi aadress, nt `https://example.com/leht` |
| USE meetod | Utilization, Saturation, Errors | Jõudlusanalüüsi meetod: iga ressursi kasutus, küllastus ja vead |
| USN | Ubuntu Security Notice | Ubuntu turvateade parandatud haavatavuse kohta |
| UTC | Coordinated Universal Time | Koordineeritud maailmaaeg; serverid hoiavad kella sageli UTC-s |
| util-linux | util-linux | Linuxi süsteemikäskude pakett (`mount`, `lsblk`, `fdisk` jt) |
| UUID | Universally Unique Identifier | Unikaalne identifikaator, millega nt failisüsteemi `/etc/fstab`-is tuvastatakse |
| vaikelüüs | default gateway | Ruuter, kuhu saadetakse kohalikust võrgust väljuv liiklus |
| Valkey | Valkey | Redisest tuletatud vaba võti-väärtus andmebaas |
| varundus | backup | Andmetest koopia tegemine taastamise jaoks |
| vastastikune litsents | copyleft licence | Litsents, mis nõuab muudetud versiooni levitamist sama litsentsiga (nt GPL) |
| vastustefail | answer file | Fail, mis vastab paigaldaja küsimustele ette (kickstart, preseed, autoinstall) |
| vdev | virtual device | ZFS-i ketaste rühm (üksik, peegel, raidz) |
| veth-paar | veth pair | Kaks omavahel ühendatud virtuaalset võrguliidest, millega ühendatakse konteiner sillaga |
| viip | prompt | Kesta ooteteade, nt `mari@debian:~$` |
| viit | symbolic link, symlink | Viide teisele failile või kataloogile |
| VirtIO | VirtIO | Paravirtualiseeritud kiired virtuaalseadmed (ketas, võrk) |
| virtuaalhost | virtual host, server block | Ühe veebiserveri sait, mis valitakse nime järgi |
| virtuaalne IP-aadress | virtual IP, VIP | Aadress, mis liigub rikke korral ühelt masinalt teisele (keepalived, VRRP) |
| VLAN | Virtual LAN | Loogiline kohtvõrk, mis eraldab liikluse sildiga (802.1Q) samas füüsilises võrgus |
| VNC | Virtual Network Computing | Graafilise töölaua kaugjuhtimise protokoll (nt Proxmoxi konsool) |
| vormindama | to format | Partitsioonile failisüsteemi looma |
| VPN | Virtual Private Network | Krüpteeritud tunnel võrkude või seadmete vahel |
| VRRP | Virtual Router Redundancy Protocol | Protokoll, millega masinad lepivad kokku, kes virtuaalset IP-aadressi hoiab |
| VT-x / AMD-V | hardware virtualization extensions | Protsessori riistvaraline virtualiseerimise tugi |
| võrgumask | netmask | Määrab, milline osa aadressist tähistab võrku (nt `/24`) |
| võrgunimeruum | network namespace | Kerneli eraldatud võrgukeskkond oma liideste, aadresside ja marsruutidega (konteinerite alus) |
| võti | option, flag | Käsu käitumist muutev parameeter, nt `-l` |
| võti-väärtus hoidla | key-value store | Andmebaas, mis hoiab väärtusi võtme järgi (Valkey, Redis) |
| vähima õiguse põhimõte | principle of least privilege | Igaüks saab ainult vajalikud õigused |
| väljakutse (ACME) | challenge | Test, millega CA kontrollib, et taotleja haldab domeeni (HTTP-01, DNS-01) |
| väljalase | release | Distro või programmi versioon |
| väljalaskemärkmed | release notes | Uue versiooni muudatuste ja teadaolevate probleemide kirjeldus |
| väljalaske uuendus | release upgrade | Distro üleminek uuele põhiversioonile (nt Debian 12 → 13) |
| väljumiskood | exit code, exit status | Käsu lõpetamise olek, 0 tähendab edu |
| VXLAN | Virtual Extensible LAN | Kihi 2 võrgu tunnel UDP kaudu (Flannel, Proxmoxi SDN) |
| WAN | Wide Area Network | Laivõrk; tulemüüri väline (interneti) võrk |
| Wayland | Wayland | Uus Linuxi kuvaprotokoll, X11 järglane |
| wheel | wheel | Administraatorite grupp (AlmaLinux, FreeBSD), mille liikmed võivad kasutada `sudo`/`su` |
| WireGuard | WireGuard | Linuxi kernelis sisalduv kaasaegne VPN |
| WSL | Windows Subsystem for Linux | Linuxi käitamine Windowsi sees |
| õigused | permissions | Lugemis-, kirjutus- ja käivitusõigus (`rwx`) |
| üksik rikkepunkt | single point of failure | Komponent, mille rikke korral lakkab kogu teenus töötamast |
| üksus | unit | systemd hallatav objekt (teenus, taimer jne) |
| ülevõtt | failover | Rikkis põhisüsteemi ülesannete üleviimine varusüsteemile |
| ümbersuunamine | redirection | Voo suunamine faili või failist (`>`, `<`) |
| X11 | X Window System | Vana Unixi graafiline kuvasüsteem |
| XAPI | XenAPI | XCP-ng haldusliides, mida kasutavad `xe` ja Xen Orchestra |
| `xargs` | xargs | Käsk, mis teeb sisendi ridadest teise käsu argumendid |
| Xen | Xen | Tüüp 1 hüperviisor, mida kasutab XCP-ng |
| Xen Orchestra | Xen Orchestra (XO) | XCP-ng veebipõhine haldus- ja varunduslahendus |
| XFS | XFS | AlmaLinuxi vaikimisi ajakirjaga failisüsteem; suurendada saab, vähendada mitte |

<!-- navigatsioon -->
---

[← UNIX-i ja Linuxi ajalugu](ajalugu.md) · [Sisukord](../../README.md#sisukord) · [Käskude loend →](kasud.md)
<!-- /navigatsioon -->
