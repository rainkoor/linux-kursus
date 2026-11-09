# Sõnastik

Kursusel kasutatavad mõisted koos ingliskeelse vastega. Sõnastikku täiendatakse koos uute moodulitega.

| Eesti keeles | Inglise keeles | Selgitus |
|---|---|---|
| absoluutne tee | absolute path | Juurkataloogist `/` algav tee |
| ACL | Access Control List | Täpsem õiguste loend lisaks omanikule ja grupile |
| ajastaja | scheduler | Programm, mis käivitab töid kindlal ajal (cron) |
| ajavöönd | time zone | Piirkonna ajaarvestus, nt `Europe/Tallinn` |
| alglaadija | bootloader | Programm, mis laadib kerneli (nt GRUB) |
| alglaadimine | boot | Arvuti käivitamine kuni operatsioonisüsteemi töövalmiduseni |
| alias (tulemüüris) | alias | Nimega rühm aadresse või porte, mida kasutatakse tulemüürireeglites |
| andmebaas | database | Struktureeritud andmete kogum ja seda haldav server |
| Apache | Apache HTTP Server | Levinud moodulipõhine veebiserver (`apache2`, `httpd`) |
| ARC | Adaptive Replacement Cache | ZFS-i lugemisvahemälu RAM-is |
| argument | argument | Käsule antav sisend, nt failinimi |
| arhiiv | archive | Mitu faili ühes failis (nt `.tar`) |
| arvutikonto | computer account | Domeeniga liidetud masina konto Active Directorys |
| `at` | at | Käsk ühekordse töö käivitamiseks kindlal ajal |
| atribuut | attribute | LDAP-kirje väli, nt `uid` või `mail` |
| autofs | automounter | Teenus, mis haagib võrgukettad automaatselt esimesel kasutamisel ja lahutab jõudeolekus |
| avalik võti | public key | Võtmepaari jagatav osa |
| box | box | Vagranti valmis põhitõmmis virtuaalmasina loomiseks |
| Caddy | Caddy | Automaatse HTTPS-iga veebiserver |
| cgroup | control group | Kerneli mehhanism protsessirühmade ressursside (CPU, mälu, I/O) piiramiseks |
| chrony | chrony | Täielik NTP klient ja server |
| chroot | chroot | Protsessi juurkataloogi vahetamine, nt süsteemi parandamiseks taastemeedialt |
| cloud-init | cloud-init | Tööriist, mis seadistab virtuaalmasina esimesel käivitusel (nimi, IP, kasutaja, SSH-võti) |
| ConfigMap | ConfigMap | Kubernetese objekt seadistuse andmiseks podile failina või keskkonnamuutujana |
| copy-on-write | copy-on-write (CoW) | Andmeid ei kirjutata üle, vaid uude kohta (ZFS, Btrfs) |
| CoreDNS | CoreDNS | Pistikprogrammidega DNS-server, seadistus failis `Corefile` |
| CVE | Common Vulnerabilities and Exposures | Turvaaukude rahvusvaheline tunnus |
| dataset | dataset | ZFS-i pooli sees olev failisüsteem oma omadustega |
| Deployment | Deployment | Kubernetese objekt, mis hoiab rakenduse soovitud arvu pode ja haldab uuendusi |
| DHCP | Dynamic Host Configuration Protocol | Protokoll, millega võrguseadmed saavad automaatselt IP-aadressi ja võrguseaded |
| distributsioon, distro | distribution | Kernelist ja tarkvarast koosnev terviklik OS |
| DIT | Directory Information Tree | LDAP-kataloogi puukujuline struktuur |
| DN | Distinguished Name | LDAP-kirje täisnimi puus, nt `uid=mari,ou=People,dc=lab,dc=example` |
| DNS | Domain Name System | Nimede ja IP-aadresside teisendamise süsteem |
| dnsmasq | dnsmasq | Kerge DNS-, DHCP- ja TFTP-server |
| dom0, domU | domain 0, unprivileged domain | Xenis haldus-VM (dom0) ja tavalised külalismasinad (domU) |
| domeenikontroller | domain controller (DC) | Server, mis hoiab AD kataloogi ja autendib kasutajaid |
| domeen (AD) | domain | Ühise kataloogi ja turvapoliitikaga haldusala Active Directorys |
| eesmärk | target | systemd üksuste rühm, mis kirjeldab süsteemi olekut |
| eksportija | exporter | Programm, mis teeb mõõdikud Prometheusele kättesaadavaks (nt node_exporter) |
| EPEL | Extra Packages for Enterprise Linux | RHEL-i perekonna lisapakettide hoidla |
| esiplaan | foreground | Töö, mille lõppu kest ootab |
| etcd | etcd | Hajus võti-väärtus andmebaas, kus hoitakse Kubernetese klastri olekut |
| fail | file | Andmete kogum failisüsteemis |
| failisüsteem | filesystem | Viis andmete korraldamiseks andmekandjal |
| filtreeriv DNS | filtering DNS | DNS, mis blokeerib soovimatuid domeene (nt Pi-hole) |
| Flatpak | Flatpak | Distrost sõltumatu liivakastis rakenduste vorming (Flathub) |
| funktsioon | function | Nimega korduvkasutatav koodiplokk |
| füüsiline köide | physical volume, PV | LVM-i jaoks ettevalmistatud ketas või partitsioon |
| GID | group ID | Grupi numbriline tunnus |
| GitOps | GitOps | Töövõte, kus süsteemi soovitud olek on Gitis ja kontroller rakendab muudatused automaatselt |
| GPO, rühmapoliitika | Group Policy Object | Windowsi arvutite ja kasutajate tsentraalselt hallatav seadistus |
| grupp | group | Kasutajate kogum ühiste õiguste andmiseks |
| haakepunkt | mount point | Kataloog, kuhu failisüsteem haagitakse |
| haakima | to mount | Failisüsteemi lisamine kataloogipuusse |
| HAProxy | HAProxy | Kiire TCP/HTTP koormusejaotur |
| haru | branch | Gitis eraldi arendusliin |
| Helm | Helm | Kubernetese pakihaldur; pakett on tabel (*chart*) |
| hetktõmmis | snapshot | Köite või masina seisu jäädvustus kindlal hetkel |
| hoidla | repository | Tarkvarapakettide allikas |
| hoidla (Git) | repository | Projekti kataloog koos muudatuste ajalooga |
| hädaolukorra režiim | emergency mode | Minimaalne režiim süsteemi parandamiseks |
| hüperviisor | hypervisor | Tarkvara, mis käitab virtuaalmasinaid (KVM, Xen, ESXi, Hyper-V) |
| hüppeserver | jump host, bastion | Vahepealne server, mille kaudu ühendutakse sisevõrgu masinatesse (`ssh -J`, `ProxyJump`) |
| idempotentsus | idempotence | Korduv rakendamine annab sama tulemuse |
| infrastruktuur koodina | infrastructure as code, IaC | Infrastruktuuri kirjeldamine tekstifailides |
| Ingress | Ingress | Kubernetese reegel, mis suunab HTTP(S) päringud nime ja tee järgi teenustele |
| initsiaator | initiator | iSCSI klient, mis kasutab võrguketast |
| inventuur | inventory | Ansible'i hallatavate serverite loend |
| IOPS | Input/Output Operations Per Second | Ketta sisend-väljundoperatsioonide arv sekundis |
| IPv6 | Internet Protocol version 6 | 128-bitiste aadressidega IP-protokolli versioon |
| IQN | iSCSI Qualified Name | iSCSI seadme unikaalne nimi, nt `iqn.2026-11.example.lab:disk01` |
| iSCSI | Internet Small Computer Systems Interface | Protokoll plokkseadmete (ketaste) jagamiseks üle IP-võrgu |
| i-sõlm | inode | Failisüsteemi kirje, mis hoiab faili metaandmeid |
| juurkasutaja | root, superuser | Piiramatute õigustega kasutaja |
| juurkataloog | root directory | Kataloogipuu algus `/` |
| k3s | k3s | Kerge sertifitseeritud Kubernetese distributsioon ühe binaarfailina |
| karastamine | hardening | Süsteemi turvalisemaks muutmine seadistuse abil |
| kasutusjuhend | manual page, man page | Käsu dokumentatsioon (`man`) |
| kataloog | directory | Failide konteiner (Windowsis „kaust“) |
| kataloogiteenus | directory service | Kasutajate, gruppide ja muu info keskne andmebaas (LDAP, AD) |
| Kerberos | Kerberos | Piletitel põhinev võrguautentimise protokoll |
| kerneli moodul | kernel module | Töö ajal laaditav kerneli osa (nt draiver) |
| kernel, tuum | kernel | Operatsioonisüsteemi riistvara haldav osa |
| keskkonnamuutuja | environment variable | Muutuja, mis pärandatakse käivitatavatele programmidele |
| kest | shell | Käske tõlgendav programm, nt Bash |
| kickstart | kickstart | Red Hati perekonna automaatse paigalduse vastustefail (`inst.ks=`) |
| kihiline kaitse | defense in depth | Mitme teineteist täiendava kaitsekihi kasutamine |
| kodukataloog | home directory | Kasutaja isiklik kataloog, nt `/home/mari` |
| kohustuslik juurdepääsukontroll | mandatory access control, MAC | Süsteemne poliitika, mida ei saa mööda minna ka juurkasutaja (SELinux, AppArmor) |
| kompileerimine | compiling | Lähtekoodi tõlkimine käivitatavaks programmiks |
| konsool | console | Otse ühendatud ekraan ja klaviatuur või VM-i konsooliaken |
| konteiner | container | Isoleeritud protsess oma failisüsteemiga, jagab hosti kernelit |
| konteinerpilt | container image | Muutumatu mall, millest konteiner käivitatakse |
| koormus | load average | Protsessorit ootavate protsesside keskmine arv |
| koormusejaotur | load balancer | Jagab päringud mitme taustserveri vahel |
| koormustest | load test | Serveri jõudluse mõõtmine paljude samaaegsete päringutega (`ab`, `wrk`, k6) |
| kubectl | kubectl | Kubernetese klastri käsurea haldustööriist |
| Kubernetes | Kubernetes | Konteinerite orkestreerimise platvorm mitme serveri klastris |
| kuvaprotokoll | display protocol | Rakenduste ja ekraani suhtlusviis (Wayland, X11) |
| KVM | Kernel-based Virtual Machine | Linuxi kerneli virtualiseerimismoodul |
| kvoorum | quorum | Klastri sõlmede enamus, mis on vajalik otsuste tegemiseks |
| kõrge kättesaadavus | high availability (HA) | Lahendus, mis jätkab tööd ka ühe komponendi rikke korral |
| kõvaviit | hard link | Sama faili (i-sõlme) teine nimi |
| käsiraamat | runbook | Sammhaaval juhised tüüpiliste haldustoimingute ja rikete lahendamiseks |
| käsk | command | Programm või kesta sisekäsk |
| käskude asendus | command substitution | Käsu väljundi kasutamine väärtusena (`$( )`) |
| käsuajalugu | command history | Varem sisestatud käskude loend |
| käsurida | command line | Tekstipõhine töökeskkond |
| köide | volume | Püsiv andmehoidla konteineri jaoks |
| köitegrupp | volume group, VG | LVM-is füüsiliste köidete ühendatud ruum |
| LAN | Local Area Network | Kohtvõrk; tulemüüri sisemine võrk |
| LDAP | Lightweight Directory Access Protocol | Kataloogiteenuse päringuprotokoll |
| LDIF | LDAP Data Interchange Format | Tekstivorming LDAP-kirjete lisamiseks ja muutmiseks |
| lighttpd | lighttpd | Väga kerge veebiserver |
| liides | interface | Võrguühenduse lõpp-punkt (nt `ens18`) |
| liitliides | bond, link aggregation | Mitu füüsilist võrguliidest ühe loogilise liidesena (rikkekindlus või läbilaskevõime) |
| link-local aadress | link-local address | Ainult kohtvõrgus kehtiv aadress (IPv6-s `fe80::/10`) |
| lisagrupp | supplementary group | Grupp, kuhu kasutaja kuulub lisaks põhigrupile |
| live-süsteem | live system | Andmekandjalt käivituv OS, mis ei vaja paigaldust |
| logide rotatsioon | log rotation | Logifailide regulaarne ümbernimetamine, pakkimine ja kustutamine |
| lokaat | locale | Keele, kuupäevade ja arvude vormingu seaded (nt `et_EE.UTF-8`) |
| loogiline köide | logical volume, LV | LVM-is köitegrupist eraldatud kasutatav osa |
| LUKS | Linux Unified Key Setup | Linuxi ketta krüpteerimise standard (`cryptsetup`) |
| LUN | Logical Unit Number | iSCSI sihtmärgi poolt jagatav üksik ketas |
| lõhestunud aju | split brain | Olukord, kus kaks sõlme peavad end korraga põhisõlmeks ja andmed või aadressid lähevad lahku |
| lähtekood | source code | Programmi inimloetav kood |
| LXC | Linux Containers | Süsteemikonteinerid, mis käituvad nagu kerged virtuaalmasinad (Proxmox) |
| manifest | manifest | YAML-fail, mis kirjeldab Kubernetese objektide soovitud olekut |
| manustatud andmebaas | embedded database | Andmebaas, mis on rakenduse sees ühe failina (SQLite) |
| marsruut | route | Reegel, kuhu pakette saata |
| massiiv | array | Mitut väärtust sisaldav muutuja |
| mdadm | mdadm | Linuxi tarkvaralise RAID-i haldustööriist |
| metamärk | wildcard, glob | Mitmele failinimele sobiv muster (`*`, `?`) |
| Molecule | Molecule | Ansible'i rollide testimise raamistik |
| MTA | Mail Transfer Agent | E-kirju edastav server (nt Postfix) |
| muutuja | variable | Nimega väärtus |
| muutumatu distro | immutable / atomic distribution | Ainult lugemiseks süsteem, mida uuendatakse tervikuna (SteamOS, Silverblue) |
| mõõdik | metric | Arvuline näitaja ajas (nt protsessori kasutus) |
| mänguraamat | playbook | Ansible'i ülesannete kirjeldus YAML-failis |
| NAS | Network Attached Storage | Võrgu kaudu faile jagav salvestusseade või -süsteem (nt TrueNAS) |
| NAT | Network Address Translation | Aadresside teisendus, millega sisevõrgu masinad kasutavad ühist avalikku aadressi |
| nimelahendus | name resolution | Nime teisendamine IP-aadressiks |
| nimeruum | namespace | Kerneli võimalus protsesside, võrgu jms isoleerimiseks |
| NoSQL | NoSQL | Mitterelatsioonilised andmebaasid (võti-väärtus, dokumendid jt) |
| NTP | Network Time Protocol | Kellaaja sünkroniseerimise protokoll (port 123/udp) |
| objektiklass | object class | LDAP-kirje tüüp, mis määrab kohustuslikud ja lubatud atribuudid |
| OOM killer | out-of-memory killer | Kerneli mehhanism, mis mälu lõppemisel lõpetab protsessi |
| OpenTofu | OpenTofu | Terraformi vaba haru infrastruktuuri deklaratiivseks loomiseks koodi järgi |
| orkestreerimine | orchestration | Konteinerite automaatne paigutamine, käivitamine, skaleerimine ja taastamine mitme masina vahel |
| otsuste logi | decision log, ADR | Kirjed oluliste tehniliste valikute ja nende põhjuste kohta |
| OU | Organizational Unit | Kataloogi kaust kasutajate ja arvutite rühmitamiseks |
| paik | patch | Failide erinevuste kirjeldus, mida saab rakendada käsuga `patch` |
| pakett | package | Paigaldatav tarkvaraühik |
| pakihaldur | package manager | Tarkvara paigaldamise ja uuendamise vahend |
| pakkimine | compression | Faili mahu vähendamine (nt gzip) |
| PAM | Pluggable Authentication Modules | Linuxi moodulipõhine autentimise raamistik (`/etc/pam.d/`) |
| paroolipoliitika | password policy | Nõuded parooli pikkusele, keerukusele ja aegumisele (`pam_pwquality`, `chage`) |
| partitsioon | partition | Ketta osa |
| partitsioonitabel | partition table | Ketta partitsioonide kirjeldus (MBR, GPT) |
| peidetud fail | hidden file | Punktiga algava nimega fail |
| pesastatud virtualiseerimine | nested virtualization | Hüperviisori käitamine virtuaalmasinas |
| PID | process ID | Protsessi numbriline tunnus |
| pilet | ticket | Kerberose ajutine tõend autentimiseks (nt TGT) |
| plokkseade | block device | Seade, kust andmeid loetakse plokkide kaupa (ketas) |
| pod | pod | Kubernetese väikseim üksus: üks või mitu ühise võrgu ja kettaga konteinerit |
| pool | pool, zpool | ZFS-i ketaste ühine salvestusruum |
| pordisuunamine | port forwarding | Välise pordi liikluse suunamine sisevõrgu masinale |
| port | port | Teenust tähistav number (nt 22, 443) |
| PostgreSQL | PostgreSQL | Võimas avatud lähtekoodiga relatsiooniline andmebaas |
| PPA | Personal Package Archive | Ubuntu isiklik pakettide hoidla |
| preseed | preseed | Debiani automaatse paigalduse vastustefail |
| privaatvõti | private key | Võtmepaari salajane osa |
| PromQL | Prometheus Query Language | Prometheuse päringukeel |
| proovieksam | mock exam | Praktiline harjutuseksam ajapiiranguga |
| proovirežiim | dry run | Režiim, mis näitab, mida tehtaks, ilma tegemata |
| Proton | Proton | Valve'i ühilduvuskiht Windowsi mängude käitamiseks Linuxis |
| protsess | process | Töötav programm |
| PVC | PersistentVolumeClaim | Kubernetese podi taotlus püsiketta järele |
| põhigrupp | primary group | Kasutaja vaikegrupp, millele kuuluvad tema loodud failid |
| pöördpuhverserver | reverse proxy | Server, mis edastab päringud taustal töötavale rakendusele |
| püsivara | firmware | Emaplaadi programm, mis käivitub esimesena (BIOS, UEFI) |
| PXE | Preboot Execution Environment | Arvuti käivitamine võrgust |
| QEMU | Quick Emulator | Riistvara emulaator, mis koos KVM-iga käitab virtuaalmasinaid |
| realm | realm | Kerberose haldusala, kirjutatakse suurtähtedega (nt `AD.LAB.EXAMPLE`) |
| register | registry | Konteinerpiltide hoidla (nt docker.io) |
| regulaaravaldis | regular expression, regex | Muster teksti otsimiseks |
| rekursiivne | recursive | Kehtib ka kõigile alamkataloogidele |
| relee | relay, smarthost | SMTP-server, mille kaudu server oma kirjad edastab |
| rent | lease | DHCP-serveri poolt ajutiselt antud aadress |
| replikatsioon | replication | Andmete pidev kopeerimine teise serverisse |
| reserveering | reservation | DHCP-s kindlale MAC-aadressile seotud IP-aadress |
| ressursipiirang | resource limit | Protsessi või teenuse lubatud ressursside ülempiir (`ulimit`, `MemoryMax=`) |
| rikketest | failover test | Komponendi teadlik väljalülitamine, et kontrollida lahenduse töökindlust |
| roll (Ansible) | role | Korduvkasutatav Ansible'i ülesannete, mallide ja muutujate komplekt kindlas kataloogistruktuuris |
| roll (PostgreSQL) | role | PostgreSQL-i kasutaja või grupp |
| RPO | Recovery Point Objective | Kui palju andmeid (ajas mõõdetuna) tohib rikke korral kaotada |
| RTO | Recovery Time Objective | Kui kiiresti peab teenus pärast riket taastuma |
| räsi | hash | Paroolist arvutatud pöördumatu väärtus |
| saaleala | swap | Kettaruum, mida kasutatakse mälu laiendusena |
| scrub | scrub | ZFS-i kõigi andmete läbilugemine ja kontrollsummade kontroll |
| sertifikaat | certificate | Allkirjastatud dokument, mis seob avaliku võtme serveri nimega |
| sertifitseerimiskeskus | certificate authority, CA | Asutus või süsteem, mis allkirjastab sertifikaate |
| SGID | set group ID | Kataloogil: uued failid saavad kataloogi grupi |
| shebang | shebang | Skripti esimene rida, mis määrab tõlgendaja (`#!/bin/bash`) |
| SIEM | Security Information and Event Management | Turvasündmuste keskne kogumine ja analüüs (nt Wazuh) |
| signaal | signal | Protsessile saadetav teade (nt SIGTERM) |
| sihtmärk | target | iSCSI server, mis jagab kettaid |
| silumine | debugging | Vigade otsimine programmist |
| sissekanne | commit | Gitis salvestatud hetkeseis koos kirjeldusega |
| sisselogimishaldur | display manager | Graafiline sisselogimisekraan (GDM, SDDM, LightDM) |
| skeletikataloog | skeleton directory | `/etc/skel` - failid, mis kopeeritakse uue kasutaja kodukataloogi |
| skript | script | Käskude jada sisaldav tekstifail |
| SLAAC | Stateless Address Autoconfiguration | IPv6 aadressi automaatne seadistamine ruuteri teadaannete põhjal |
| SMART | Self-Monitoring, Analysis and Reporting Technology | Ketaste enesediagnostika (`smartctl`) |
| SQL | Structured Query Language | Relatsiooniliste andmebaaside päringukeel |
| SQLite | SQLite | Failipõhine manustatud andmebaas |
| SRV-kirje | SRV record | DNS-kirje, mis näitab teenuse hosti ja porti |
| SSSD | System Security Services Daemon | Linuxi teenus, mis ühendab NSS-i ja PAM-i LDAP-i või AD-ga |
| standardsisend | standard input, stdin | Programmi sisendvoog (0) |
| standardveaväljund | standard error, stderr | Programmi veateadete voog (2) |
| standardväljund | standard output, stdout | Programmi väljundvoog (1) |
| SteamOS | SteamOS | Valve'i Arch-põhine mängudistro |
| sticky bit | sticky bit | Kataloogil: faile saab kustutada ainult nende omanik |
| strace | strace | Tööriist programmi süsteemikutsete jälgimiseks |
| suhteline tee | relative path | Praegusest kataloogist algav tee |
| SUID | set user ID | Programm töötab faili omaniku õigustes |
| sõlm (klastris) | node | Klastri üks masin |
| sõltuvus | dependency | Pakett, mida teine pakett töötamiseks vajab |
| süsteemikutse | system call | Programmi pöördumine kerneli poole (nt faili avamine) |
| ZFS | ZFS | Failisüsteem ja köitehaldur ühes, kontrollsummade ja hetktõmmistega |
| zvol | ZFS volume | ZFS-i pooli sees olev plokkseade |
| taastamisrežiim | rescue mode | Vähendatud režiim süsteemi hoolduseks |
| tagasisidestus | loopback | Liides, mille kaudu masin räägib iseendaga (`lo`) |
| taimer | timer | systemd üksus ajastatud käivitamiseks |
| taust | background | Töö, mis töötab ilma kesta ootamata |
| taustserver | backend | Koormusejaoturi või pöördpuhvri taga töötav server |
| tee | path | Faili või kataloogi asukoht |
| teenus | service, daemon | Taustal töötav programm |
| tekstiredaktor | text editor | Programm tekstifailide muutmiseks (nano, vim) |
| terminal | terminal (emulator) | Tekstiakent kuvav programm |
| Terraform | Terraform | HashiCorpi tööriist infrastruktuuri deklaratiivseks loomiseks koodi järgi (BSL-litsents) |
| tervisekontroll | health check | Taustserveri kättesaadavuse regulaarne kontroll |
| TFTP | Trivial File Transfer Protocol | Lihtne failiedastusprotokoll, mida kasutab PXE |
| TGT | Ticket Granting Ticket | Kerberose sisselogimispilet, millega küsitakse teenusepileteid |
| toru | pipe | Ühe käsu väljundi suunamine teise sisendiks (`\|`) |
| Traefik | Traefik | Konteineritele mõeldud pöördpuhver ja koormusejaotur |
| tsoon | zone | DNS-is ühe domeeni kirjete kogum |
| tsükkel | loop | Korduvalt täidetav koodiplokk |
| tulemüür | firewall | Võrguliikluse filtreerimise süsteem |
| tuned | tuned | Teenus, mis rakendab süsteemile jõudlusprofiile (`tuned-adm`) |
| turvakontekst | security context | SELinuxi märgis failil, protsessil või pordil |
| turvauuendus | security update | Turvaauku parandav tarkvarauuendus |
| töölauakeskkond | desktop environment | Graafiline kasutajaliides (GNOME, KDE Plasma, Xfce) |
| UID | user ID | Kasutaja numbriline tunnus |
| umask | umask | Mask, mis määrab uute failide vaikimisi õigused |
| vaikelüüs | default gateway | Ruuter, kuhu saadetakse kohalikust võrgust väljuv liiklus |
| Valkey | Valkey | Redisest tuletatud vaba võti-väärtus andmebaas |
| varundus | backup | Andmetest koopia tegemine taastamise jaoks |
| vastustefail | answer file | Fail, mis vastab paigaldaja küsimustele ette (kickstart, preseed, autoinstall) |
| vdev | virtual device | ZFS-i ketaste rühm (üksik, peegel, raidz) |
| viip | prompt | Kesta ooteteade, nt `mari@debian:~$` |
| viit | symbolic link, symlink | Viide teisele failile või kataloogile |
| VirtIO | VirtIO | Paravirtualiseeritud kiired virtuaalseadmed (ketas, võrk) |
| virtuaalhost | virtual host, server block | Ühe veebiserveri sait, mis valitakse nime järgi |
| virtuaalne IP-aadress | virtual IP, VIP | Aadress, mis liigub rikke korral ühelt masinalt teisele (keepalived, VRRP) |
| VLAN | Virtual LAN | Loogiline kohtvõrk, mis eraldab liikluse sildiga (802.1Q) samas füüsilises võrgus |
| vormindama | to format | Partitsioonile failisüsteemi looma |
| VPN | Virtual Private Network | Krüpteeritud tunnel võrkude või seadmete vahel |
| VRRP | Virtual Router Redundancy Protocol | Protokoll, millega masinad lepivad kokku, kes virtuaalset IP-aadressi hoiab |
| võrgumask | netmask | Määrab, milline osa aadressist tähistab võrku (nt `/24`) |
| võti | option, flag | Käsu käitumist muutev parameeter, nt `-l` |
| võti-väärtus hoidla | key-value store | Andmebaas, mis hoiab väärtusi võtme järgi (Valkey, Redis) |
| vähima õiguse põhimõte | principle of least privilege | Igaüks saab ainult vajalikud õigused |
| väljalase | release | Distro või programmi versioon |
| väljalaske uuendus | release upgrade | Distro üleminek uuele põhiversioonile (nt Debian 12 → 13) |
| väljumiskood | exit code, exit status | Käsu lõpetamise olek, 0 tähendab edu |
| WAN | Wide Area Network | Laivõrk; tulemüüri väline (interneti) võrk |
| Wayland | Wayland | Uus Linuxi kuvaprotokoll, X11 järglane |
| WireGuard | WireGuard | Linuxi kernelis sisalduv kaasaegne VPN |
| WSL | Windows Subsystem for Linux | Linuxi käitamine Windowsi sees |
| õigused | permissions | Lugemis-, kirjutus- ja käivitusõigus (`rwx`) |
| üksik rikkepunkt | single point of failure | Komponent, mille rikke korral lakkab kogu teenus töötamast |
| üksus | unit | systemd hallatav objekt (teenus, taimer jne) |
| ülevõtt | failover | Rikkis põhisüsteemi ülesannete üleviimine varusüsteemile |
| ümbersuunamine | redirection | Voo suunamine faili või failist (`>`, `<`) |
| X11 | X Window System | Vana Unixi graafiline kuvasüsteem |
| `xargs` | xargs | Käsk, mis teeb sisendi ridadest teise käsu argumendid |
| Xen | Xen | Tüüp 1 hüperviisor, mida kasutab XCP-ng |
| .htaccess | .htaccess | Apache'i kataloogipõhine seadistusfail |
