<!-- navigatsioon -->
[← Laboritöö 21. Seire ja jõudlus](labor.md) · [Sisukord](../../README.md#sisukord) · [Proovieksam: süvendusosa →](../proovieksam.md)
<!-- /navigatsioon -->

# Moodul 21. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Millised on seire kolm alustala ja milleks igaüks on?

<details>
<summary>Vastus</summary>

Mõõdikud (arvud ajas: trendid, jõudlus), logid (sündmused: mis juhtus), häired (teade inimesele, kui on vaja tegutseda).

</details>

**2.** Selgita USE meetodit. Too iga ressursi jaoks üks käsk, millega seda kontrollida.

<details>
<summary>Vastus</summary>

Iga ressursi (CPU, mälu, ketas, võrk) kohta: kasutus (*Utilization*), küllastus ehk järjekord (*Saturation*), vead (*Errors*). Nt CPU - `mpstat`, `vmstat` `r`; mälu - `free`, `vmstat si/so`; ketas - `iostat -x` (`%util`, `aqu-sz`); võrk - `sar -n DEV`, `ip -s link`.

</details>

**3.** Mida tähendab koormus (*load average*) `4.00, 2.50, 1.20` 2 tuumaga masinas?

<details>
<summary>Vastus</summary>

Viimase minuti jooksul oli keskmiselt 4 protsessi, mis töötasid või ootasid - 2 tuuma jaoks kaks korda rohkem kui jõuab; koormus on kasvanud (15 min tagasi 1,2).

</details>

**4.** Miks on `free -h` väljundis veerg `free` väike, kuigi server töötab hästi? Millist veergu tuleb vaadata?

<details>
<summary>Vastus</summary>

Linux kasutab vaba mälu failide vahemäluna, mille saab vajadusel kohe vabastada. Vaadata tuleb veergu `available`.

</details>

**5.** Mida näitavad `top` väljundis `wa` ja `st`?

<details>
<summary>Vastus</summary>

`wa` - protsessor ootab kettaoperatsioone; `st` - hüperviisor andis protsessoriaja teistele virtuaalmasinatele.

</details>

**6.** Mis vahe on `vmstat`-il ja `sar`-il?

<details>
<summary>Vastus</summary>

`vmstat` näitab praegust olekut reaalajas; `sar` kogub ja säilitab ajalugu, millest saab vaadata ka möödunud aega.

</details>

**7.** Milleks on `strace` ja millal seda kasutada?

<details>
<summary>Vastus</summary>

Näitab programmi süsteemikutseid (failide avamine, võrk, protsessid). Kasuta, kui programm ei tööta ja veateade ei ütle, miks - nt leiad, millist faili see otsib.

</details>

**8.** Kuidas leiad, milline protsess hoiab faili avatuna või kuulab kindlal pordil?

<details>
<summary>Vastus</summary>

`lsof /tee/failini`, `lsof -i :port`, `ss -tlpn`, `fuser`.

</details>

**9.** Kuidas töötab Prometheus (*pull*) ja mis on eksportija?

<details>
<summary>Vastus</summary>

Prometheus küsib ise kindla intervalliga sihtmärkidelt HTTP kaudu (`/metrics`) mõõdikuid ja salvestab need. Eksportija on programm, mis teeb süsteemi või teenuse mõõdikud selles vormingus kättesaadavaks (nt node_exporter).

</details>

**10.** Mille poolest erinevad Prometheus ja Zabbix?

<details>
<summary>Vastus</summary>

Prometheus: *pull*, mõõdikud ja PromQL, konteinerimaailma standard, seadistus failides. Zabbix: agendid, valmis mallid, kõik veebiliideses, levinud klassikalises taristus ja võrguseadmete seires.

</details>

**11.** Mida mõõdab Uptime Kuma ja mille poolest erineb see Prometheusest?

<details>
<summary>Vastus</summary>

Kättesaadavust väljastpoolt: kas teenus vastab ja kui kiiresti, sertifikaadi kehtivus. Prometheus mõõdab masina ja teenuste sisemisi näitajaid.

</details>

**12.** Mis on häirete väsimus ja kuidas seda vältida?

<details>
<summary>Vastus</summary>

Kui häireid on liiga palju ja enamik ei vaja tegutsemist, hakatakse neid ignoreerima. Häire ainult siis, kui inimene peab midagi tegema; ooteaeg (`for`); ülejäänu armatuurlauale.

</details>

**13.** Miks peab seiresüsteemi port (nt 9100) olema tulemüüris lubatud ainult seireserverile?

<details>
<summary>Vastus</summary>

Mõõdikud avaldavad infot süsteemi kohta (tarkvara, kasutus, failisüsteemid) ja eksportijat võib rünnata - vähima õiguse põhimõte.

</details>

**14.** Mis on OOM killer ja kust selle tegevust näha?

<details>
<summary>Vastus</summary>

Kerneli mehhanism, mis mälu otsasaamisel tapab protsessi. `journalctl -k | grep -i "out of memory"` või `dmesg`.

</details>

**15.** Miks on Proxmoxi VM-is kõrge `st` väärtus probleem, mida VM-i sees lahendada ei saa?

<details>
<summary>Vastus</summary>

`st` tähendab, et hüperviisori sõlm on ülekoormatud ja VM ei saa protsessoriaega; põhjus on väljaspool VM-i - lahendus on sõlme koormuse vähendamine või VM-i teisele sõlmele viimine.

</details>

**16.** Mis on tuned ja millise profiili soovitab see virtuaalmasinale?

<details>
<summary>Vastus</summary>

Teenus, mis rakendab terve komplekti jõudlusseadeid profiilina (`tuned-adm profile …`); virtuaalmasinale `virtual-guest`.

</details>

**17.** Milleks on serveris vaja MTA-d (nt Postfix), kui see ei ole e-posti server? Mis on relee (*smarthost*)?

<details>
<summary>Vastus</summary>

Et serveri enda programmid (cron, systemd, `smartd`, skriptid) saaksid teateid saata. Relee on teine SMTP-server (asutuse või pakkuja oma), mille kaudu server kirjad edastab, selle asemel et neid ise otse adressaatide serveritesse saata.

</details>

**18.** Miks peab Postfixi `inet_interfaces` olema laborserveris `loopback-only`?

<details>
<summary>Vastus</summary>

Server ei tohi võtta võrgust kirju vastu ega edastada neid - avatud releed kasutatakse rämpsposti saatmiseks ja server satub mustadesse nimekirjadesse.

</details>

**19.** Mis on KPI ja mis on SLA? Too kummagi kohta näide.

<details>
<summary>Vastus</summary>

KPI on mõõdetav tulemusnäitaja, mille järgi hinnatakse, kas teenus täidab eesmärki (nt kättesaadavus kuus, vastamisaeg, varunduse õnnestumise osakaal). SLA on teenusetaseme leping teenuse osutaja ja kliendi vahel: lubatud tase ja reageerimisaeg (nt „kättesaadavus 99,5%, rikkele reageeritakse 1 tunni jooksul“).

</details>

**20.** Kui palju seisakut lubab kuus 99% ja kui palju 99,9% kättesaadavus?

<details>
<summary>Vastus</summary>

99% lubab umbes 7,3 tundi kuus, 99,9% umbes 44 minutit kuus.

</details>

**21.** Millised kolm omadust on heal KPI-l?

<details>
<summary>Vastus</summary>

See on mõõdetav (arv ja ühik), kokku lepitud (kasutaja ja haldur ootavad sama) ja jälgitav (seiresüsteem mõõdab seda ise ja annab häire enne piiri ületamist).

</details>

## Praktilised miniülesanded

**1.** Kuva iga 5 sekundi järel ketaste laiendatud statistika ilma jõudeolevate seadmeteta.

<details>
<summary>Lahendus</summary>

```bash
iostat -xz 5
```

</details>

**2.** Leia, millised protsessid kasutavad praegu kõige rohkem kettakirjutust.

<details>
<summary>Lahendus</summary>

```bash
pidstat -d 2 3            # või: sudo iotop -o
```

</details>

**3.** Näita eilse päeva (nt kuu 7. päev) protsessori kasutust Debianis.

<details>
<summary>Lahendus</summary>

```bash
sar -u -f /var/log/sysstat/sa07
```

</details>

**4.** Kirjuta PromQL-päring, mis näitab masinaid, kus juurfailisüsteemis on vaba ruumi alla 10%.

<details>
<summary>Lahendus</summary>

```text
node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} < 0.10
```

</details>

**5.** Jälgi, milliseid faile käsk `ls /etc` avab.

<details>
<summary>Lahendus</summary>

```bash
strace -e trace=openat ls /etc
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 21. Seire ja jõudlus](labor.md) · [Sisukord](../../README.md#sisukord) · [Proovieksam: süvendusosa →](../proovieksam.md)
<!-- /navigatsioon -->
