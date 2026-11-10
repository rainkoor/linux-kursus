<!-- navigatsioon -->
[← Laboritöö 14. Andmebaasid (kooli väikeserver, II osa)](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 15. Võrguteenused: DNS, failijagamine, e-post ja varundus →](../moodul-15-vorguteenused/index.md)
<!-- /navigatsioon -->

# Moodul 14. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Miks peab veebirakendusel olema oma andmebaasikasutaja?

<details>
<summary>Vastus</summary>

Vähima õiguse põhimõte: kui rakendus häkitakse, pääseb ründaja ligi ainult selle rakenduse andmebaasile, mitte kõigile andmebaasidele ega serveri haldusele.

</details>

**2.** Miks ei ole töötava andmebaasi failide kopeerimine usaldusväärne varukoopia?

<details>
<summary>Vastus</summary>

Failid võivad olla poolelioleva muudatuse keskel ja omavahel ebajärjepidevad. Kasutada tuleb `mariadb-dump`/`pg_dump`-i või peatada teenus.

</details>

**3.** Kuidas taastada MariaDB juurkasutaja unustatud parool? Miks peab sel ajal kasutama valikut `--skip-networking`?

<details>
<summary>Vastus</summary>

Peata teenus, käivita see valikutega `--skip-grant-tables --skip-networking` (nt `systemctl set-environment MYSQLD_OPTS=…`), logi sisse ilma paroolita, `FLUSH PRIVILEGES;` ja `ALTER USER … IDENTIFIED BY …`, seejärel käivita teenus tavapäraselt. Ilma õiguste kontrollita saaks muidu igaüks võrgust andmebaasi ilma paroolita kasutada.

</details>

**4.** Mis vahe on relatsioonilisel andmebaasiserveril, manustatud andmebaasil ja võti-väärtus hoidlal? Too igaühe kohta näide.

<details>
<summary>Vastus</summary>

Server: eraldi teenus võrgus, mitu klienti (MariaDB, PostgreSQL); manustatud: andmebaas on fail, mida rakendus otse kasutab (SQLite); võti-väärtus: mälupõhine kiire hoidla (Valkey, Redis).

</details>

**5.** Mis on PostgreSQL-is roll? Kuidas erineb see MariaDB kasutajast `'nimi'@'host'`?

<details>
<summary>Vastus</summary>

Roll on kasutaja või grupp (sama mõiste); õigused antakse rollidele. MariaDB-s on kasutaja seotud aadressiga, kust ta ühendub; PostgreSQL-is määrab ühenduse lubamise eraldi fail `pg_hba.conf`.

</details>

**6.** Mida määrab fail `pg_hba.conf`? Mis on `peer`-autentimine?

<details>
<summary>Vastus</summary>

Kes (kasutaja), millisesse andmebaasi, kust (aadress) ja millise meetodiga tohib ühenduda. `peer` - kohalik ühendus, kus operatsioonisüsteemi kasutajanimi peab ühtima andmebaasi kasutajanimega.

</details>

**7.** Millal sobib SQLite ja millal mitte? Kuidas varundada SQLite'i andmebaasi?

<details>
<summary>Vastus</summary>

Sobib üks rakendus, väike/keskmine andmemaht, seadistus ja olek; ei sobi palju samaaegseid kirjutajaid, mitu serverit, NFS. Varundus: `sqlite3 fail.db ".backup varu.db"` või `.dump`, või failikoopia peatatud rakendusega.

</details>

**8.** Milleks kasutatakse Valkeyt/Redist? Miks tekkis Valkey?

<details>
<summary>Vastus</summary>

Vahemälu, seansid, järjekorrad, loendurid. Valkey tekkis 2024, kui Redis muutis litsentsi mittevabaks - kogukond jätkas viimase vaba versiooni põhjal.

</details>

**9.** Miks ei tohi Redise/Valkey porti avada võrku ilma paroolita?

<details>
<summary>Vastus</summary>

See on mälupõhine ja vaikimisi ilma autentimiseta; ründaja saab lugeda ja kirjutada kõiki andmeid ning võib serveri üle võtta (nt failide kirjutamise kaudu).

</details>

**10.** Mis on replikatsioon ja miks see ei asenda varukoopiat?

<details>
<summary>Vastus</summary>

Teise serverisse pidevalt uuendatav koopia. Vead ja kustutamised (`DROP TABLE`) replitseeritakse samuti kohe - varukoopia on ajaline koopia, millest saab taastada varasema seisu.

</details>

**11.** Miks peab PHP-leht kasutama `htmlspecialchars()`-i andmebaasist tulnud teksti väljastamisel?

<details>
<summary>Vastus</summary>

Andmebaasis võib olla HTML-i või JavaScripti (nt kasutaja sisestatud nimi); ilma kodeerimiseta käivitaks brauser selle (XSS).

</details>

**12.** Mis on ülevõtt (*failover*)? Milliseid samme teed MariaDB-s, et koopiast saaks põhiserver, ja miks ei tohi vana põhiserverit pärast parandamist lihtsalt uuesti käivitada?

<details>
<summary>Vastus</summary>

Rikkis põhiserveri asendamine koopiaga. Koopias: kontrolli replikatsiooni olekut, `STOP REPLICA`, `RESET REPLICA ALL`, `read_only = OFF` (ka seadistusfailis) ning suuna rakendus uuele serverile (nimi või virtuaalne IP). Vana server võtaks vastu kirjutusi ja andmed läheksid lahku (*split brain*) - sellest tehakse uue põhiserveri koopia.

</details>

## Praktilised miniülesanded

**1.** Kirjuta SQL-käsud, mis loovad andmebaasi `moodle` ja kasutaja `moodle`, kellel on sellele andmebaasile kõik õigused ning kes saab ühenduda ainult aadressilt `10.0.83.55`.

<details>
<summary>Lahendus</summary>

```sql
CREATE DATABASE moodle CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'moodle'@'10.0.83.55' IDENTIFIED BY 'Tugev-Parool-456';
GRANT ALL PRIVILEGES ON moodle.* TO 'moodle'@'10.0.83.55';
```

</details>

**2.** Loo PostgreSQL-is roll `moodle` parooliga ja andmebaas `moodle`, mille omanik see roll on.

<details>
<summary>Lahendus</summary>

```sql
CREATE ROLE moodle LOGIN PASSWORD 'Tugev-Parool-456';
CREATE DATABASE moodle OWNER moodle;
```

</details>

**3.** Kirjuta `pg_hba.conf` rida, mis lubab rollil `moodle` ühenduda andmebaasi `moodle` ainult aadressilt `10.0.83.55` paroolitõendusega.

<details>
<summary>Lahendus</summary>

```text
host  moodle  moodle  10.0.83.55/32  scram-sha-256
```

</details>

**4.** Ekspordi SQLite'i andmebaasist `kool.db` tabel `opilased` CSV-failiks.

<details>
<summary>Lahendus</summary>

```bash
sqlite3 -csv -header kool.db "SELECT * FROM opilased;" > opilased.csv
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 14. Andmebaasid (kooli väikeserver, II osa)](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 15. Võrguteenused: DNS, failijagamine, e-post ja varundus →](../moodul-15-vorguteenused/index.md)
<!-- /navigatsioon -->
