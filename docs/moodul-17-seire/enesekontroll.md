<!-- navigatsioon -->
[← Laboritöö 17. Seire ja jõudlus](labor.md) · [Sisukord](../../README.md#sisukord) · [Proovieksam: süvendusosa →](../proovieksam.md)
<!-- /navigatsioon -->

# Moodul 17. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Millised on seire kolm alustala ja milleks igaüks on?
2. Selgita USE meetodit. Too iga ressursi jaoks üks käsk, millega seda kontrollida.
3. Mida tähendab koormus (*load average*) `4.00, 2.50, 1.20` 2 tuumaga masinas?
4. Miks on `free -h` väljundis veerg `free` väike, kuigi server töötab hästi? Millist veergu tuleb vaadata?
5. Mida näitavad `top` väljundis `wa` ja `st`?
6. Mis vahe on `vmstat`-il ja `sar`-il?
7. Milleks on `strace` ja millal seda kasutada?
8. Kuidas leiad, milline protsess hoiab faili avatuna või kuulab kindlal pordil?
9. Kuidas töötab Prometheus (*pull*) ja mis on eksportija?
10. Mille poolest erinevad Prometheus ja Zabbix?
11. Mida mõõdab Uptime Kuma ja mille poolest erineb see Prometheusest?
12. Mis on häirete väsimus ja kuidas seda vältida?
13. Miks peab seiresüsteemi port (nt 9100) olema tulemüüris lubatud ainult seireserverile?
14. Mis on OOM killer ja kust selle tegevust näha?
15. Miks on Proxmoxi VM-is kõrge `st` väärtus probleem, mida VM-i sees lahendada ei saa?
16. Mis on tuned ja millise profiili soovitab see virtuaalmasinale?

## Praktilised miniülesanded

1. Kuva iga 5 sekundi järel ketaste laiendatud statistika ilma jõudeolevate seadmeteta.
2. Leia, millised protsessid kasutavad praegu kõige rohkem kettakirjutust.
3. Näita eilse päeva (nt kuu 7. päev) protsessori kasutust Debianis.
4. Kirjuta PromQL-päring, mis näitab masinaid, kus juurfailisüsteemis on vaba ruumi alla 10%.
5. Jälgi, milliseid faile käsk `ls /etc` avab.

---

## Vastused

1. Mõõdikud (arvud ajas: trendid, jõudlus), logid (sündmused: mis juhtus), häired (teade inimesele, kui on vaja tegutseda).
2. Iga ressursi (CPU, mälu, ketas, võrk) kohta: kasutus (*Utilization*), küllastus ehk järjekord (*Saturation*), vead (*Errors*). Nt CPU - `mpstat`, `vmstat` `r`; mälu - `free`, `vmstat si/so`; ketas - `iostat -x` (`%util`, `aqu-sz`); võrk - `sar -n DEV`, `ip -s link`.
3. Viimase minuti jooksul oli keskmiselt 4 protsessi, mis töötasid või ootasid - 2 tuuma jaoks kaks korda rohkem kui jõuab; koormus on kasvanud (15 min tagasi 1,2).
4. Linux kasutab vaba mälu failide vahemäluna, mille saab vajadusel kohe vabastada. Vaadata tuleb veergu `available`.
5. `wa` - protsessor ootab kettaoperatsioone; `st` - hüperviisor andis protsessoriaja teistele virtuaalmasinatele.
6. `vmstat` näitab praegust olekut reaalajas; `sar` kogub ja säilitab ajalugu, millest saab vaadata ka möödunud aega.
7. Näitab programmi süsteemikutseid (failide avamine, võrk, protsessid). Kasuta, kui programm ei tööta ja veateade ei ütle, miks - nt leiad, millist faili see otsib.
8. `lsof /tee/failini`, `lsof -i :port`, `ss -tlpn`, `fuser`.
9. Prometheus küsib ise kindla intervalliga sihtmärkidelt HTTP kaudu (`/metrics`) mõõdikuid ja salvestab need. Eksportija on programm, mis teeb süsteemi või teenuse mõõdikud selles vormingus kättesaadavaks (nt node_exporter).
10. Prometheus: *pull*, mõõdikud ja PromQL, konteinerimaailma standard, seadistus failides. Zabbix: agendid, valmis mallid, kõik veebiliideses, levinud klassikalises taristus ja võrguseadmete seires.
11. Kättesaadavust väljastpoolt: kas teenus vastab ja kui kiiresti, sertifikaadi kehtivus. Prometheus mõõdab masina ja teenuste sisemisi näitajaid.
12. Kui häireid on liiga palju ja enamik ei vaja tegutsemist, hakatakse neid ignoreerima. Häire ainult siis, kui inimene peab midagi tegema; ooteaeg (`for`); ülejäänu armatuurlauale.
13. Mõõdikud avaldavad infot süsteemi kohta (tarkvara, kasutus, failisüsteemid) ja eksportijat võib rünnata - vähima õiguse põhimõte.
14. Kerneli mehhanism, mis mälu otsasaamisel tapab protsessi. `journalctl -k | grep -i "out of memory"` või `dmesg`.
15. `st` tähendab, et hüperviisori sõlm on ülekoormatud ja VM ei saa protsessoriaega; põhjus on väljaspool VM-i - lahendus on sõlme koormuse vähendamine või VM-i teisele sõlmele viimine.
16. Teenus, mis rakendab terve komplekti jõudlusseadeid profiilina (`tuned-adm profile …`); virtuaalmasinale `virtual-guest`.

### Miniülesannete lahendused

```bash
iostat -xz 5
pidstat -d 2 3            # või: sudo iotop -o
sar -u -f /var/log/sysstat/sa07
```

```text
node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} < 0.10
```

```bash
strace -e trace=openat ls /etc
```

<!-- navigatsioon -->
---

[← Laboritöö 17. Seire ja jõudlus](labor.md) · [Sisukord](../../README.md#sisukord) · [Proovieksam: süvendusosa →](../proovieksam.md)
<!-- /navigatsioon -->
