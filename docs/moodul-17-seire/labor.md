# Laboritöö 17. Seire ja jõudlus

| | |
|---|---|
| **Distrod** | Debian (`debian1` - koormuse analüüs ja jälgitav), Ubuntu (`ubuntusrv` - seireserver Dockeriga), AlmaLinux (`alma` - jälgitav) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Varasemate laboritööde masinad, `ubuntusrv`-s Docker (või Podman) ja vähemalt 2 GiB mälu |
| **Eesmärk** | Õppida leidma jõudlusprobleeme käsurealt ja ehitada laborivõrgule seiresüsteem |

**Aruanne:** vasta küsimustele **K1–K14**.

---

## 1. osa. Süsteemi ülevaade (Debian)

**1.1** Paigalda tööriistad ja vaata masina ülevaadet:

```bash
sudo apt install sysstat stress-ng htop strace lsof
nproc
uptime
free -h
vmstat 1 5
iostat -xz 1 3
```

**K1.** Mitu tuuma masinal on ja mis on koormus? Kui palju mälu on tegelikult vaba (`available`) ja kui palju on failide vahemälus? Kas `top` päises on `st` väärtus suurem kui 0 - mida see Proxmoxi VM-is tähendab?

## 2. osa. Koormuse tekitamine ja tuvastamine

Ava kaks terminali. Ühes tekitad koormuse, teises uurid.

**2.1** Protsessori koormus:

```bash
stress-ng --cpu $(nproc) --timeout 60s
```

Teises terminalis:

```bash
uptime
vmstat 2
mpstat -P ALL 2 3
pidstat 2 3
```

**2.2** Mälukoormus:

```bash
stress-ng --vm 1 --vm-bytes 80% --timeout 60s
```

```bash
free -h
vmstat 2
```

**2.3** Kettakoormus:

```bash
stress-ng --hdd 2 --hdd-bytes 512M --timeout 60s
```

```bash
iostat -xz 2
pidstat -d 2 3
```

**K2.** Täida tabel: iga koormuse jaoks - milline tööriist ja milline veerg näitas probleemi kõige selgemini (nt `vmstat` `r`, `wa`, `si/so`, `iostat` `%util`, `await`)?

**K3.** Kas mälukoormusel hakkas süsteem kasutama saaleala (`si`/`so`)? Mis juhtub, kui mälu ja saaleala saavad otsa (vaata `journalctl -k | grep -i oom`)?

## 3. osa. Ajalugu sar-iga

**3.1** Lülita sysstat'i ajaloo kogumine sisse ja tee 10 minuti pärast uuesti mõni koormustest:

```bash
sudo systemctl enable --now sysstat
systemctl list-timers | grep sysstat
```

Hiljem (või järgmises tunnis):

```bash
sar -u
sar -q
sar -r
```

**K4.** Kas sar-i ajaloost on näha, millal koormust tekitasid? Mitme minuti järel sysstat andmeid kogub?

## 4. osa. Tõrkeotsing strace'i ja lsof-iga

**4.1** Loo „katkine“ programm:

```bash
cat > ~/katkine.sh <<'EOF'
#!/bin/bash
seadistus=/etc/minu-rakendus/seaded.conf
[ -r "$seadistus" ] || { echo "Viga: midagi läks valesti" >&2; exit 1; }
echo "Töötab"
EOF
chmod +x ~/katkine.sh
~/katkine.sh
```

Oletame, et sa ei näe skripti sisu. Leia `strace`-iga, mida programm otsib:

```bash
strace -f -e trace=file ~/katkine.sh 2>&1 | tail -15
```

**K5.** Millist faili programm otsis ja mis oli tulemus (`ENOENT`, `EACCES`)? Kuidas probleemi parandaksid?

**4.2** Kes hoiab faili avatuna:

```bash
tail -f /var/log/dpkg.log &
sudo lsof /var/log/dpkg.log
sudo lsof -i -P -n | grep LISTEN
kill %1
```

**K6.** Milline protsess hoidis logifaili avatuna? Millised protsessid kuulavad võrgus (võrdle `ss -tlpn` väljundiga)?

## 5. osa. Prometheus ja Grafana

**5.1** Paigalda node_exporter masinatesse `debian1` ja `ubuntusrv` (`sudo apt install prometheus-node-exporter`) ning `alma`-sse konteinerina (teooria punkt 17.5). Ava tulemüüris port 9100 ainult seireserverile. Kontrolli seireserverist:

```bash
curl -s http://10.0.83.52:9100/metrics | grep -c ^node_
```

**5.2** Loo `ubuntusrv`-s kataloog `~/seire`, failid `compose.yaml` ja `prometheus.yml` (teooria punkt 17.5) ning käivita. Lisa kataloog oma Git-hoidlasse.

```bash
cd ~/seire
docker compose up -d
docker compose ps
```

Ava `http://10.0.83.54:9090/targets`.

**K7.** Kas kõik sihtmärgid olid **UP**? Kui mõni oli **DOWN**, mis oli põhjus (tulemüür, vale IP, eksportija ei tööta)?

**5.3** Proovi Prometheuse veebiliideses (*Graph*/*Query*) päringuid teooria tabelist. Käivita `debian1`-s uuesti `stress-ng --cpu $(nproc) --timeout 120s` ja vaata protsessori kasutuse graafikut.

**K8.** Kirjuta PromQL-päring, mis näitab iga masina vaba mälu protsentides. Mis oli tulemus?

**5.4** Ava Grafana (`http://10.0.83.54:3000`), muuda administraatori parool, lisa andmeallikas Prometheus (`http://prometheus:9090`) ja impordi armatuurlaud ID **1860**.

**K9.** Miks on Grafanas andmeallika aadress `http://prometheus:9090`, mitte `http://localhost:9090`? (Vihje: moodul 12, Compose'i võrk.)

**5.5** Loo Grafanas häire (*Alerting* → *Alert rules*), mis käivitub, kui mõne masina juurfailisüsteemis on vaba ruumi alla 20%. Testi seda: täida `alma`-s ketast (`fallocate -l <suurus> /var/tmp/suur.fail`) ja kustuta fail pärast testi.

**K10.** Kas häire käivitus? Mida tähendab häire olek *Pending* ja *Firing*? Miks on reeglis `for: 10m` (või *Pending period*)?

## 6. osa. Kättesaadavus: Uptime Kuma

**6.1** Käivita `ubuntusrv`-s Uptime Kuma (teooria punkt 17.6) ja lisa jälgimised:

- HTTPS: `https://kool.lab.example` (laboritöö 13) - lisa `ubuntusrv`-le labori CA või lülita sertifikaadikontroll välja ja põhjenda;
- DNS: `kool.lab.example` serveris `10.0.83.52` (laboritöö 15);
- TCP-port: `10.0.83.53:445` (Samba).

**6.2** Peata `debian1`-s nginx (`sudo systemctl stop nginx`), oota ja vaata, millal Uptime Kuma probleemi märkas. Käivita nginx uuesti.

**K11.** Kui kaua kulus probleemi märkamiseks? Millest see sõltub? Kas Uptime Kuma näitab ka sertifikaadi aegumist?

## 7. osa. Kokkuvõte

**K12.** Kasutaja kaebab, et veebileht on kell 9–10 aeglane. Kirjelda samm-sammult, kuidas põhjust otsiksid (USE meetod, käsud, sar, Grafana).

**K13.** Millised häired seadistaksid kooli laborivõrgule? Too 5 häiret ja põhjenda, miks just need (ja mitte rohkem).

**K14.** Võrdle Prometheust ja Zabbixit: millal valiksid kumma?

---

## Koristamine

```bash
cd ~/seire && docker compose down          # andmed jäävad köidetesse; -v kustutaks ka need
docker rm -f uptime-kuma
rm ~/katkine.sh
```

---

## Lisaülesanne (valikuline)

1. **Alertmanager:** lisa Compose'i faili Alertmanager, kirjuta Prometheuse reegel `KetasTaitub` (teooria punkt 17.5) ja suuna häired e-posti (laboritöö 15 Postfix või Mailpit, laboritöö 12).
2. **Loki:** lisa logide kogumiseks Grafana Loki ja Alloy (või Promtail) ning vaata `debian1` journali logisid Grafanas.
3. **Zabbix:** paigalda Zabbixi server (konteineritena: `zabbix/zabbix-server-pgsql`, `zabbix/zabbix-web-nginx-pgsql`, `postgres`) ja agent `debian1`-sse, seo host malliga *Linux by Zabbix agent*.
4. **Netdata:** paigalda Netdata ühte masinasse ja võrdle selle reaalajagraafikuid Grafanaga.
5. **tuned:** vaata AlmaLinuxis `tuned-adm active` ja `tuned-adm recommend`. Vaheta profiil `throughput-performance`-ks ja tagasi ning võrdle `sysctl vm.dirty_ratio` väärtusi.

---

## Õpetajale: kontrollvastused

| Küsimus | Vastus |
|---|---|
| K1 | Sõltub VM-ist; `available` ≫ `free`, sest vahemälu vabastatakse vajadusel; `st` > 0 - hüperviisori sõlm on ülekoormatud ja VM ootab protsessorit |
| K2 | CPU: `vmstat r` > tuumade arv, `us` ~100, `mpstat` kõik tuumad; mälu: `free` `available` väheneb, `vmstat si/so`; ketas: `vmstat wa`, `b`, `iostat %util` ~100 ja kasvav `w_await`, `pidstat -d` näitab `stress-ng-hdd` |
| K3 | Kui saaleala on, siis `so` > 0; kui kõik otsas, tapab OOM killer protsessi (`Out of memory: Killed process …`) |
| K4 | Jah, kui test oli pärast kogumise algust; vaikimisi iga 10 minuti järel (`sysstat-collect.timer`) |
| K5 | `/etc/minu-rakendus/seaded.conf`, `ENOENT`; loo fail (või kataloog) või muuda skripti seadistust |
| K6 | `tail`; kuulajad nt `sshd`, `nginx`, `named`, `mariadbd`, `prometheus-node`, `smbd` - sama mis `ss -tlpn` |
| K7 | Tavaliselt DOWN põhjused: tulemüür (`ufw`/`firewalld`) blokeerib 9100, vale IP või eksportija ei tööta |
| K8 | `node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100` |
| K9 | Grafana konteineris on `localhost` Grafana konteiner ise; Compose'i võrgus leitakse teine konteiner teenuse nime järgi |
| K10 | *Pending* - tingimus kehtib, kuid ooteaeg pole täis; *Firing* - häire aktiivne; ooteaeg väldib lühiajaliste hüpete pärast valehäireid |
| K11 | Sõltub kontrolli intervallist (vaikimisi 60 s) ja korduskatsete arvust; jah, HTTPS-jälgimisel näitab sertifikaadi kehtivust ja võib selle kohta teavitada |
| K14 | Prometheus: konteinerid, dünaamiline taristu, PromQL, palju eksportijaid; Zabbix: klassikalised serverid ja võrguseadmed, valmis mallid, kõik veebiliideses |

> **Märkus õpetajale:** laboritööd ei ole terviklikult testitud. Kontrolli enne tundi Prometheuse ja Grafana konteinerpiltide versioonid ning Grafana menüüde nimed (sõltuvad versioonist). `stress-ng --vm 1 --vm-bytes 80%` võib väikese mäluga VM-is käivitada OOM killeri - see on õppimise mõttes hea, kuid hoiata õppijaid.
