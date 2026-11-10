<!-- navigatsioon -->
[← Moodul 20. Seire ja jõudlus](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 20. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 20. Seire ja jõudlus

| | |
|---|---|
| **Distrod** | Debian (`debian1` - koormuse analüüs ja jälgitav), Ubuntu (`ubuntusrv` - seireserver Dockeriga), AlmaLinux (`alma` - jälgitav) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Varasemate laboritööde masinad, `ubuntusrv`-s Docker (või Podman) ja vähemalt 2 GiB mälu |
| **Eesmärk** | Õppida leidma jõudlusprobleeme käsurealt ja ehitada laborivõrgule seiresüsteem |

> **Aruanne:** vasta küsimustele **K1–K14**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

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

> **K1.** Mitu tuuma masinal on ja mis on koormus? Kui palju mälu on tegelikult vaba (`available`) ja kui palju on failide vahemälus? Kas `top` päises on `st` väärtus suurem kui 0 - mida see Proxmoxi VM-is tähendab?

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

> **K2.** Täida tabel: iga koormuse jaoks - milline tööriist ja milline veerg näitas probleemi kõige selgemini (nt `vmstat` `r`, `wa`, `si/so`, `iostat` `%util`, `await`)?

> **K3.** Kas mälukoormusel hakkas süsteem kasutama saaleala (`si`/`so`)? Mis juhtub, kui mälu ja saaleala saavad otsa (vaata `journalctl -k | grep -i oom`)?

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

> **K4.** Kas sar-i ajaloost on näha, millal koormust tekitasid? Mitme minuti järel sysstat andmeid kogub?

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

> **K5.** Millist faili programm otsis ja mis oli tulemus (`ENOENT`, `EACCES`)? Kuidas probleemi parandaksid?

**4.2** Kes hoiab faili avatuna:

```bash
tail -f /var/log/dpkg.log &
sudo lsof /var/log/dpkg.log
sudo lsof -i -P -n | grep LISTEN
kill %1
```

> **K6.** Milline protsess hoidis logifaili avatuna? Millised protsessid kuulavad võrgus (võrdle `ss -tlpn` väljundiga)?

## 5. osa. Prometheus ja Grafana

**5.1** Paigalda node_exporter masinatesse `debian1` ja `ubuntusrv` (`sudo apt install prometheus-node-exporter`) ning `alma`-sse konteinerina (teooria punkt 20.5). Ava tulemüüris port 9100 ainult seireserverile. Kontrolli seireserverist:

```bash
curl -s http://10.0.83.52:9100/metrics | grep -c ^node_
```

**5.2** Loo `ubuntusrv`-s kataloog `~/seire`, failid `compose.yaml` ja `prometheus.yml` (teooria punkt 20.5) ning käivita. Lisa kataloog oma Git-hoidlasse.

```bash
cd ~/seire
docker compose up -d
docker compose ps
```

Ava `http://10.0.83.54:9090/targets`.

> **K7.** Kas kõik sihtmärgid olid **UP**? Kui mõni oli **DOWN**, mis oli põhjus (tulemüür, vale IP, eksportija ei tööta)?

**5.3** Proovi Prometheuse veebiliideses (*Graph*/*Query*) päringuid teooria tabelist. Käivita `debian1`-s uuesti `stress-ng --cpu $(nproc) --timeout 120s` ja vaata protsessori kasutuse graafikut.

> **K8.** Kirjuta PromQL-päring, mis näitab iga masina vaba mälu protsentides. Mis oli tulemus?

**5.4** Ava Grafana (`http://10.0.83.54:3000`), muuda administraatori parool, lisa andmeallikas Prometheus (`http://prometheus:9090`) ja impordi armatuurlaud ID **1860**.

> **K9.** Miks on Grafanas andmeallika aadress `http://prometheus:9090`, mitte `http://localhost:9090`? (Vihje: moodul 14, Compose'i võrk.)

**5.5** Loo Grafanas häire (*Alerting* → *Alert rules*), mis käivitub, kui mõne masina juurfailisüsteemis on vaba ruumi alla 20%. Testi seda: täida `alma`-s ketast (`fallocate -l <suurus> /var/tmp/suur.fail`) ja kustuta fail pärast testi.

> **K10.** Kas häire käivitus? Mida tähendab häire olek *Pending* ja *Firing*? Miks on reeglis `for: 10m` (või *Pending period*)?

## 6. osa. Kättesaadavus: Uptime Kuma

**6.1** Käivita `ubuntusrv`-s Uptime Kuma (teooria punkt 20.6) ja lisa jälgimised:

- HTTPS: `https://kool.lab.example` (laboritöö 15) - lisa `ubuntusrv`-le labori CA või lülita sertifikaadikontroll välja ja põhjenda;
- DNS: `kool.lab.example` serveris `10.0.83.52` (laboritöö 17);
- TCP-port: `10.0.83.53:445` (Samba).

**6.2** Peata `debian1`-s nginx (`sudo systemctl stop nginx`), oota ja vaata, millal Uptime Kuma probleemi märkas. Käivita nginx uuesti.

> **K11.** Kui kaua kulus probleemi märkamiseks? Millest see sõltub? Kas Uptime Kuma näitab ka sertifikaadi aegumist?

## 7. osa. Kokkuvõte

> **K12.** Kasutaja kaebab, et veebileht on kell 9–10 aeglane. Kirjelda samm-sammult, kuidas põhjust otsiksid (USE meetod, käsud, sar, Grafana).

> **K13.** Millised häired seadistaksid kooli laborivõrgule? Too 5 häiret ja põhjenda, miks just need (ja mitte rohkem).

> **K14.** Võrdle Prometheust ja Zabbixit: millal valiksid kumma?

---

## Koristamine

```bash
cd ~/seire && docker compose down          # andmed jäävad köidetesse; -v kustutaks ka need
docker rm -f uptime-kuma
rm ~/katkine.sh
```

---

## Lisaülesanne (valikuline)

1. **Alertmanager:** lisa Compose'i faili Alertmanager, kirjuta Prometheuse reegel `KetasTaitub` (teooria punkt 20.5) ja suuna häired e-posti (Postfix, teooria punkt 20.8, või Mailpit, laboritöö 14).
2. **Loki:** lisa logide kogumiseks Grafana Loki ja Alloy (või Promtail) ning vaata `debian1` journali logisid Grafanas.
3. **Zabbix:** paigalda Zabbixi server (konteineritena: `zabbix/zabbix-server-pgsql`, `zabbix/zabbix-web-nginx-pgsql`, `postgres`) ja agent `debian1`-sse, seo host malliga *Linux by Zabbix agent*.
4. **Netdata:** paigalda Netdata ühte masinasse ja võrdle selle reaalajagraafikuid Grafanaga.
5. **Võrgu läbilaskevõime:** paigalda `iperf3` masinatesse `debian1` ja `ubuntusrv` (ava tulemüüris ajutiselt port 5201/tcp) ning mõõda kiirus mõlemas suunas. Käivita mõõtmise ajal teises masinas `stress-ng --cpu 0` ja vaata, kas tulemus muutub. Mida näitab `ethtool ens18`?
6. **tuned:** vaata AlmaLinuxis `tuned-adm active` ja `tuned-adm recommend`. Vaheta profiil `throughput-performance`-ks ja tagasi ning võrdle `sysctl vm.dirty_ratio` väärtusi.
7. **E-posti teavitused:** paigalda Debiani Postfix kohaliku kohaletoimetamisega (*Local only*; kui õpetaja annab SMTP-relee andmed, vali *Satellite system*, teooria punkt 20.8). Suuna `root`-i kirjad oma kasutajale (`/etc/aliases`, `newaliases`), saada testkiri (`echo test | mail -s test root`) ja loe seda käsuga `mail`. Seadista moodulis 9 loodud `varundus-viga.service` saatma e-kirja ja kontrolli seda, rikkudes varundusskripti meelega. Miks peab `inet_interfaces` olema `loopback-only`?

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.1)* Mitu tuuma masinal on ja mis on koormus? Kui palju mälu on tegelikult vaba (`available`) ja kui palju on failide vahemälus? Kas `top` päises on `st` väärtus suurem kui 0 - mida see Proxmoxi VM-is tähendab?
- **K2.** *(punkt 2.3)* Täida tabel: iga koormuse jaoks - milline tööriist ja milline veerg näitas probleemi kõige selgemini (nt `vmstat` `r`, `wa`, `si/so`, `iostat` `%util`, `await`)?
- **K3.** *(punkt 2.3)* Kas mälukoormusel hakkas süsteem kasutama saaleala (`si`/`so`)? Mis juhtub, kui mälu ja saaleala saavad otsa (vaata `journalctl -k | grep -i oom`)?
- **K4.** *(punkt 3.1)* Kas sar-i ajaloost on näha, millal koormust tekitasid? Mitme minuti järel sysstat andmeid kogub?
- **K5.** *(punkt 4.1)* Millist faili programm otsis ja mis oli tulemus (`ENOENT`, `EACCES`)? Kuidas probleemi parandaksid?
- **K6.** *(punkt 4.2)* Milline protsess hoidis logifaili avatuna? Millised protsessid kuulavad võrgus (võrdle `ss -tlpn` väljundiga)?
- **K7.** *(punkt 5.2)* Kas kõik sihtmärgid olid **UP**? Kui mõni oli **DOWN**, mis oli põhjus (tulemüür, vale IP, eksportija ei tööta)?
- **K8.** *(punkt 5.3)* Kirjuta PromQL-päring, mis näitab iga masina vaba mälu protsentides. Mis oli tulemus?
- **K9.** *(punkt 5.4)* Miks on Grafanas andmeallika aadress `http://prometheus:9090`, mitte `http://localhost:9090`? (Vihje: moodul 14, Compose'i võrk.)
- **K10.** *(punkt 5.5)* Kas häire käivitus? Mida tähendab häire olek *Pending* ja *Firing*? Miks on reeglis `for: 10m` (või *Pending period*)?
- **K11.** *(punkt 6.2)* Kui kaua kulus probleemi märkamiseks? Millest see sõltub? Kas Uptime Kuma näitab ka sertifikaadi aegumist?
- **K12.** *(7. osa)* Kasutaja kaebab, et veebileht on kell 9–10 aeglane. Kirjelda samm-sammult, kuidas põhjust otsiksid (USE meetod, käsud, sar, Grafana).
- **K13.** *(7. osa)* Millised häired seadistaksid kooli laborivõrgule? Too 5 häiret ja põhjenda, miks just need (ja mitte rohkem).
- **K14.** *(7. osa)* Võrdle Prometheust ja Zabbixit: millal valiksid kumma?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 20. Seire ja jõudlus](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 20. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
