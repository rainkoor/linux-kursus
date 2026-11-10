<!-- navigatsioon -->
[← Moodul 14. Andmebaasid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 14. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 14. Andmebaasid (kooli väikeserver, II osa)

| | |
|---|---|
| **Distrod** | Debian (`debian1`, laboritöö 13 server), AlmaLinux (`alma`, klient) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Laboritöö 13 server (nginx ja HTTPS töötavad), `alma` kaugühenduse testiks |
| **Eesmärk** | Paigaldada ja võrrelda MariaDB-d, PostgreSQL-i, SQLite'i ja Valkeyt, ühendada andmebaas veebirakendusega ning varundada ja taastada andmeid |

> **Aruanne:** vasta küsimustele **K1–K14**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

Kõigis osades kasutame sama andmestikku: tabel `opilased` (nimi, eriala).

---

## 1. osa. MariaDB ja PHP-rakendus

**1.0** Paigalda MariaDB ja PHP:

```bash
sudo apt install mariadb-server php-fpm php-mysql
```

**1.1** Loo andmebaas, kasutaja ja tabel:

```bash
sudo mariadb
```

```sql
CREATE DATABASE kool CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'kool'@'localhost' IDENTIFIED BY 'Tugev-Parool-123';
GRANT ALL PRIVILEGES ON kool.* TO 'kool'@'localhost';
FLUSH PRIVILEGES;
USE kool;
CREATE TABLE opilased (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nimi   VARCHAR(100) NOT NULL,
    eriala VARCHAR(100)
);
INSERT INTO opilased (nimi, eriala) VALUES
    ('Mari Maasikas', 'IT-süsteemid'),
    ('Jaan Tamm', 'IT-süsteemid'),
    ('Kati Kask', 'Tarkvaraarendus');
SELECT * FROM opilased;
EXIT;
```

**1.2** Kontrolli, et rakenduse kasutaja saab sisse logida ja näeb ainult oma andmebaasi:

```bash
mariadb -u kool -p -e "SHOW DATABASES; SELECT COUNT(*) FROM kool.opilased;"
sudo ss -tlpn | grep 3306
```

> **K1.** Milliseid andmebaase nägi kasutaja `kool`? Millisel aadressil MariaDB kuulab ja miks on see turvaline?

**1.3** Leia PHP-FPM pesa nimi ja lisa saidi `kool.lab.example` HTTPS-serveriplokki PHP tugi (vt teooria punkt 14.6). Muuda ka rida `index index.php index.html;`.

```bash
ls /run/php/
```

**1.4** Loo leht `/var/www/kool/opilased.php`:

```php
<?php
// Kooli õpilaste nimekiri andmebaasist
$dsn = 'mysql:host=localhost;dbname=kool;charset=utf8mb4';
try {
    $pdo = new PDO($dsn, 'kool', 'Tugev-Parool-123', [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    $read = $pdo->query('SELECT nimi, eriala FROM opilased ORDER BY nimi')->fetchAll();
} catch (PDOException $e) {
    http_response_code(500);
    exit('Andmebaasi viga: ' . htmlspecialchars($e->getMessage()));
}
?>
<!doctype html>
<html lang="et">
<head><meta charset="utf-8"><title>Õpilased</title></head>
<body>
<h1>Õpilased</h1>
<p>Server: <?= htmlspecialchars(gethostname()) ?>, PHP <?= PHP_VERSION ?></p>
<table border="1">
<tr><th>Nimi</th><th>Eriala</th></tr>
<?php foreach ($read as $r): ?>
<tr><td><?= htmlspecialchars($r['nimi']) ?></td><td><?= htmlspecialchars($r['eriala']) ?></td></tr>
<?php endforeach; ?>
</table>
</body>
</html>
```

**1.5** Testi:

```bash
sudo nginx -t && sudo systemctl reload nginx
curl https://kool.lab.example/opilased.php       # Ubuntu kliendist
```

Lisa andmebaasi veel üks õpilane ja laadi leht uuesti.

> **K2.** Miks kasutab PHP-kood funktsiooni `htmlspecialchars()`? Mis võiks juhtuda, kui andmebaasis oleks õpilase nimi `<script>alert(1)</script>`?

> **K3.** Parool on PHP-faili sisse kirjutatud. Millised on selle riskid ja kuidas saaks seda paremini teha?

**1.6** Peata MariaDB (`sudo systemctl stop mariadb`), laadi leht uuesti, vaata nginx-i ja PHP logisid ning käivita MariaDB uuesti.

> **K4.** Mida näitas leht? Millises logis oli viga näha (`/var/log/nginx/kool.error.log`, `journalctl -u php*-fpm`)?



---

## 2. osa. MariaDB varundus, kaugühendus ja parooli taastamine

**2.1** Varunda andmebaas, „kustuta kogemata“ tabel ja taasta:

```bash
sudo mariadb-dump --single-transaction kool > ~/kool.sql
sudo mariadb -e "DROP TABLE kool.opilased;"
curl -sk https://kool.lab.example/opilased.php | head -3
sudo mariadb kool < ~/kool.sql
curl -sk https://kool.lab.example/opilased.php | grep -c "<tr>"
```

**2.2** Luba `alma`-l lugeda andmebaasi `kool`: muuda `bind-address` (`/etc/mysql/mariadb.conf.d/50-server.cnf`) laborivõrgu aadressile `10.0.83.52`, loo kasutaja ainult lugemisõigusega ja ava tulemüür ainult `alma`-le:

```sql
CREATE USER 'aruanne'@'10.0.83.55' IDENTIFIED BY 'Aruande-Parool-1';
GRANT SELECT ON kool.* TO 'aruanne'@'10.0.83.55';
```

```bash
sudo systemctl restart mariadb
sudo ufw allow from 10.0.83.55 to any port 3306 proto tcp
```

`alma`-s:

```bash
sudo dnf install -y mariadb
mariadb -h 10.0.83.52 -u aruanne -p -e "SELECT * FROM kool.opilased;"
mariadb -h 10.0.83.52 -u aruanne -p -e "DELETE FROM kool.opilased;"
```

> **K5.** Kas lugemine õnnestus? Mis juhtus `DELETE`-iga? Miks on tulemüüri reegel lisaks kasutaja aadressipiirangule ikkagi vajalik?

**2.3** Sea MariaDB juurkasutajale parool (`ALTER USER 'root'@'localhost' IDENTIFIED BY '…';`), „unusta“ see ja taasta ligipääs meetodiga `--skip-grant-tables --skip-networking` (teooria punkt 14.2). Kontrolli taastamise ajal `sudo ss -tlpn | grep 3306`. Lõpuks taasta `unix_socket` autentimine.

> **K6.** Kas MariaDB kuulas taastamise ajal võrgus? Miks on see oluline?

---

## 3. osa. PostgreSQL

**3.1** Paigalda PostgreSQL ja loo sama andmebaas (teooria punkt 14.3):

```bash
sudo apt install -y postgresql
sudo -u postgres psql
```

```sql
CREATE ROLE kool LOGIN PASSWORD 'Tugev-Parool-123';
CREATE DATABASE kool OWNER kool;
\c kool kool
CREATE TABLE opilased (id SERIAL PRIMARY KEY, nimi VARCHAR(100) NOT NULL, eriala VARCHAR(100));
INSERT INTO opilased (nimi, eriala) VALUES ('Mari Maasikas','IT-süsteemid'), ('Jaan Tamm','IT-süsteemid'), ('Kati Kask','Tarkvaraarendus');
SELECT * FROM opilased;
\l
\du
\dt
\q
```

Kui `\c kool kool` annab vea `Peer authentication failed`, ühendu `psql -h localhost -U kool -d kool` (parooliga, TCP kaudu).

> **K7.** Miks ei lubanud `peer`-autentimine süsteemikasutajal `postgres` ühenduda andmebaasi kasutajana `kool`? Mis vahe on `peer` ja `scram-sha-256` meetodil?

**3.2** Luba `alma`-st ühendus: `listen_addresses = 'localhost,10.0.83.52'` failis `postgresql.conf` ja `pg_hba.conf`-i rida `host kool kool 10.0.83.55/32 scram-sha-256`. Taaskäivita ja ava tulemüür pordile 5432 ainult `alma`-le. `alma`-s:

```bash
sudo dnf install -y postgresql
psql -h 10.0.83.52 -U kool -d kool -c "SELECT COUNT(*) FROM opilased;"
```

**3.3** Varunda ja taasta:

```bash
sudo -u postgres pg_dump -Fc kool > ~/kool.dump
sudo -u postgres psql -d kool -c "TRUNCATE opilased;"
sudo -u postgres pg_restore -d kool --clean ~/kool.dump
sudo -u postgres psql -d kool -c "SELECT COUNT(*) FROM opilased;"
```

> **K8.** Võrdle MariaDB ja PostgreSQL-i: kuidas luuakse kasutaja, kus määratakse, kust võib ühenduda, ja kuidas varundatakse?

**3.4** (Valikuline) Muuda PHP-leht kasutama PostgreSQL-i: `sudo apt install php-pgsql`, DSN `pgsql:host=localhost;dbname=kool`, taaskäivita PHP-FPM.

---

## 4. osa. SQLite

**4.1** Loo sama tabel SQLite'is ja impordi andmed CSV-failist:

```bash
sudo apt install -y sqlite3
printf 'nimi,eriala\nMari Maasikas,IT-süsteemid\nJaan Tamm,IT-süsteemid\nKati Kask,Tarkvaraarendus\n' > opilased.csv
sqlite3 kool.db "CREATE TABLE opilased (nimi TEXT NOT NULL, eriala TEXT);"   # SQLite lisab ise varjatud veeru rowid
sqlite3 kool.db ".import --csv --skip 1 opilased.csv opilased"
sqlite3 -box kool.db "SELECT rowid, * FROM opilased;"
ls -l kool.db
file kool.db
```

**4.2** Varunda kahel viisil ja võrdle:

```bash
sqlite3 kool.db ".backup varu.db"
sqlite3 kool.db ".dump" > kool.sql
ls -l varu.db kool.sql
head kool.sql
```

**4.3** Leia süsteemist teisi SQLite'i andmebaase:

```bash
sudo find / -xdev \( -name "*.db" -o -name "*.sqlite" \) -size +1k 2>/dev/null | head
```

> **K9.** Kas leidsid süsteemist mõne SQLite'i faili? Milliste programmide omad? (Kui sul on laboritöö 15B Pi-hole või laboritöö 17 Uptime Kuma, uuri ka nende andmebaase.)

> **K10.** Miks ei ole SQLite'il kasutajaid ega porti? Mis on sellest tulenevad eelised ja puudused? Kuidas kaitsta SQLite'i andmeid?

---

## 5. osa. Valkey (Redis)

**5.1** Paigalda Valkey (või Redis) ja kasuta seda (teooria punkt 14.5):

```bash
sudo apt install -y valkey-server || sudo apt install -y redis-server
valkey-cli ping 2>/dev/null || redis-cli ping
```

```bash
valkey-cli SET tervitus "Tere, koolipäev!"
valkey-cli GET tervitus
valkey-cli SET seanss:mari "sisse logitud" EX 30
valkey-cli TTL seanss:mari
for i in $(seq 5); do valkey-cli INCR kylastused; done
sleep 31; valkey-cli GET seanss:mari
sudo ss -tlpn | grep 6379
```

(Kui paigaldasid Redise, asenda `valkey-cli` → `redis-cli`.)

**5.2** Mõõda kiirust:

```bash
valkey-benchmark -q -n 20000 -t set,get
```

> **K11.** Mis juhtus võtmega `seanss:mari` 31 sekundi pärast? Mitu operatsiooni sekundis Valkey tegi? Miks sobib see vahemäluks ja seansside hoidmiseks?

> **K12.** Millisel aadressil Valkey kuulab? Mis juhtuks, kui port 6379 oleks internetist ilma paroolita kättesaadav?

---

## 6. osa. Kokkuvõte

> **K13.** Täida tabel MariaDB, PostgreSQL, SQLite ja Valkey kohta: tüüp, port, klient, kasutajad ja õigused, varundus, sobiv kasutus.

> **K14.** Kooli uus rakendus vajab: kasutajate ja hinnete andmebaasi, kiiret seansside hoidlat kahe veebiserveri taga (laboritöö 13 HAProxy) ja väikest seadistuse hoidlat. Milliseid andmebaase kasutaksid ja miks?

---

## Lisaülesanne (valikuline)

1. **WordPress:** paigalda samasse serverisse WordPress oma andmebaasi ja kasutajaga (vt [lõpuprojekti](../lopuprojekt.md) teema E1 näide).
2. **Replikatsioon:** paigalda `debian2`-sse MariaDB ja seadista see `debian1` koopiaks (teooria punkt 14.2). Lisa põhiserverisse õpilane ja kontrolli, et ta ilmus koopiasse. Mis juhtub koopias `DROP TABLE`-i järel põhiserveris? Seejärel harjuta **ülevõttu** (teooria punkt 14.2): peata `debian1` MariaDB, tee `debian2` põhiserveriks, kirjuta sinna uus rida ja tee `debian1`-st uue põhiserveri koopia. Mõõda, kui kaua ülevõtt aega võttis.
3. **PHP seansid Valkeys:** paigalda `php-redis` ja sea PHP-FPM hoidma seansse Valkeys (`session.save_handler = redis`, `session.save_path = "tcp://127.0.0.1:6379"`).
4. **Adminer konteineris:** käivita Adminer konteinerina (moodul 12) ja halda sellega nii MariaDB-d kui ka PostgreSQL-i.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Milliseid andmebaase nägi kasutaja `kool`? Millisel aadressil MariaDB kuulab ja miks on see turvaline?
- **K2.** *(punkt 1.5)* Miks kasutab PHP-kood funktsiooni `htmlspecialchars()`? Mis võiks juhtuda, kui andmebaasis oleks õpilase nimi `<script>alert(1)</script>`?
- **K3.** *(punkt 1.5)* Parool on PHP-faili sisse kirjutatud. Millised on selle riskid ja kuidas saaks seda paremini teha?
- **K4.** *(punkt 1.6)* Mida näitas leht? Millises logis oli viga näha (`/var/log/nginx/kool.error.log`, `journalctl -u php*-fpm`)?
- **K5.** *(punkt 2.2)* Kas lugemine õnnestus? Mis juhtus `DELETE`-iga? Miks on tulemüüri reegel lisaks kasutaja aadressipiirangule ikkagi vajalik?
- **K6.** *(punkt 2.3)* Kas MariaDB kuulas taastamise ajal võrgus? Miks on see oluline?
- **K7.** *(punkt 3.1)* Miks ei lubanud `peer`-autentimine süsteemikasutajal `postgres` ühenduda andmebaasi kasutajana `kool`? Mis vahe on `peer` ja `scram-sha-256` meetodil?
- **K8.** *(punkt 3.3)* Võrdle MariaDB ja PostgreSQL-i: kuidas luuakse kasutaja, kus määratakse, kust võib ühenduda, ja kuidas varundatakse?
- **K9.** *(punkt 4.3)* Kas leidsid süsteemist mõne SQLite'i faili? Milliste programmide omad? (Kui sul on laboritöö 15B Pi-hole või laboritöö 17 Uptime Kuma, uuri ka nende andmebaase.)
- **K10.** *(punkt 4.3)* Miks ei ole SQLite'il kasutajaid ega porti? Mis on sellest tulenevad eelised ja puudused? Kuidas kaitsta SQLite'i andmeid?
- **K11.** *(punkt 5.2)* Mis juhtus võtmega `seanss:mari` 31 sekundi pärast? Mitu operatsiooni sekundis Valkey tegi? Miks sobib see vahemäluks ja seansside hoidmiseks?
- **K12.** *(punkt 5.2)* Millisel aadressil Valkey kuulab? Mis juhtuks, kui port 6379 oleks internetist ilma paroolita kättesaadav?
- **K13.** *(6. osa)* Täida tabel MariaDB, PostgreSQL, SQLite ja Valkey kohta: tüüp, port, klient, kasutajad ja õigused, varundus, sobiv kasutus.
- **K14.** *(6. osa)* Kooli uus rakendus vajab: kasutajate ja hinnete andmebaasi, kiiret seansside hoidlat kahe veebiserveri taga (laboritöö 13 HAProxy) ja väikest seadistuse hoidlat. Milliseid andmebaase kasutaksid ja miks?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 14. Andmebaasid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 14. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
