<!-- navigatsioon -->
[← Moodul 23. E-posti server](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 23. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 23. E-posti server

| | |
|---|---|
| **Distro** | Ubuntu 24.04 (`ubuntusrv` - e-posti server `mail.lab.example`), Debian (`debian1` - laboritöö 17 DNS-server), klient: Debian või Ubuntu töölaud |
| **Kestus** | 4 × 90 minutit |
| **Vajalik** | Laboritöö 17 BIND9 DNS-server tsooniga `lab.example`, laboritöö 15 oma CA (`debian1:/root/ca`) või isesigneeritud sertifikaat |
| **Eesmärk** | Ehitada sisevõrgu e-posti server: Postfix, Dovecot, autenditud saatmine, DKIM ja DNS-kirjed ning testida ja varundada seda |

> **Aruanne:** vasta küsimustele **K1–K12**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

Laboris kasutatavad tähised: `MAIL_IP` - Ubuntu masina aadress (`10.0.83.54`), `DNS_IP` - `debian1` aadress.

---

## 0. osa. DNS-kirjed

**0.1** Lisa `debian1` tsooni `lab.example` (teooria punkt 23.2):

```text
@       IN  MX   10 mail.lab.example.
mail    IN  A    MAIL_IP
@       IN  TXT  "v=spf1 mx -all"
_dmarc  IN  TXT  "v=DMARC1; p=none; rua=mailto:postmaster@lab.example"
```

ja pöördtsooni `MAIL_IP` PTR-kirjeks `mail.lab.example.`. Suurenda seerianumbreid ja laadi tsoonid uuesti.

**0.2** Seadista Ubuntu kasutama DNS-ina `debian1`-t (Netplanis `nameservers`, laboritöö 17) ja kontrolli:

```bash
dig MX lab.example +short
dig mail.lab.example +short
dig -x MAIL_IP +short
dig TXT lab.example +short
```

> **K1.** Miks peab MX-kirje osutama nimele, millel on A-kirje, mitte IP-aadressile ega CNAME-ile? Mida tähendab SPF-kirjes `-all` ja mida `~all`?

---

## 1. osa. Postfix: kirjade vastuvõtt

**1.1** Muuda Ubuntu masina nimi ja paigalda Postfix (vali **Internet Site**, *System mail name* `lab.example`):

```bash
sudo hostnamectl set-hostname mail.lab.example
sudo apt install postfix bsd-mailx swaks
```

**1.2** Seadista `main.cf` teooria punkti 23.3 järgi (`myhostname`, `mydomain`, `myorigin`, `mydestination`, `mynetworks`, `home_mailbox = Maildir/`, `smtpd_relay_restrictions`). Kontrolli ja rakenda:

```bash
sudo postfix check
sudo postconf -n
sudo systemctl reload postfix
sudo ufw allow 25/tcp
```

**1.3** Loo kaks kasutajat (`mari`, `jaan`) ja saada kiri kohalikult ning teisest masinast:

```bash
sudo adduser mari; sudo adduser jaan
echo "Tere Mari" | mail -s "Esimene kiri" mari
swaks --to jaan@lab.example --from test@lab.example --server mail.lab.example     # debian1-st (sudo apt install swaks)
sudo ls /home/jaan/Maildir/new/
sudo cat /home/jaan/Maildir/new/*
sudo grep -E "jaan|status=" /var/log/mail.log | tail
```

> **K2.** Leia logist ühe kirja järjekorra ID ja kirjelda selle järgi kirja teekonda (`smtpd`, `cleanup`, `qmgr`, `local`). Mis oli lõplik `status=`?

> **K3.** Millised päised lisas Postfix kirjale (`Received:`, `Return-Path:`, `Message-Id:`)? Mida näitab `Received:` rida?

**1.4** Proovi kasutada serverit **avatud releena**: saada `debian1`-st kiri võõrasse domeeni ilma autentimiseta:

```bash
swaks --to keegi@example.org --from mari@lab.example --server mail.lab.example
```

> **K4.** Mis vastuse said? Milline seade selle põhjustas ja miks on see e-posti serveri kõige olulisem turvaseade?

---

## 2. osa. Dovecot ja TLS

**2.1** Loo serverile sertifikaat nimega `mail.lab.example` (laboritöö 15 CA-ga või isesigneeritud) ja kopeeri see kohtadesse `/etc/ssl/certs/mail.lab.example.crt` ning `/etc/ssl/private/mail.lab.example.key` (võtme õigused `600`).

**2.2** Paigalda Dovecot ja seadista postkasti asukoht, TLS ja Postfixi autentimise pesa (teooria punkt 23.4):

```bash
sudo apt install dovecot-imapd dovecot-lmtpd
sudo nano /etc/dovecot/conf.d/10-mail.conf
sudo nano /etc/dovecot/conf.d/10-ssl.conf
sudo nano /etc/dovecot/conf.d/10-master.conf
sudo systemctl restart dovecot
sudo doveconf -n | head -30
sudo ufw allow 993/tcp
```

**2.3** Loe Mari postkasti IMAP-i kaudu teisest masinast:

```bash
curl -k --user mari:PAROOL "imaps://mail.lab.example/INBOX"
curl -k --user mari:PAROOL "imaps://mail.lab.example/INBOX;UID=1"
curl --user mari:PAROOL "imap://mail.lab.example/INBOX"      # ilma TLS-ita
```

> **K5.** Mida vastas server ilma TLS-ita (port 143) ühendusele? Miks on `disable_plaintext_auth = yes` oluline? Kus asuvad kirjad serveris ja mis juhtub failiga `Maildir/new/…` pärast lugemist?

---

## 3. osa. Autenditud saatmine (submission)

**3.1** Lülita `master.cf`-is sisse `submission` teenus ja lisa `main.cf`-i TLS- ja SASL-seaded (teooria punkt 23.5):

```bash
sudo postfix check && sudo systemctl restart postfix
sudo ss -tlpn | grep -E ':(25|587|993) '
sudo ufw allow 587/tcp
openssl s_client -connect mail.lab.example:587 -starttls smtp -quiet </dev/null | head -5
```

**3.2** Saada `debian1`-st Mari nimel kiri Jaanile ja kiri võõrasse domeeni - mõlemad autentimisega:

```bash
swaks --to jaan@lab.example --from mari@lab.example --server mail.lab.example:587 \
      --tls --auth-user mari --auth-password 'PAROOL'
swaks --to keegi@example.org --from mari@lab.example --server mail.lab.example:587 \
      --tls --auth-user mari --auth-password 'PAROOL'
mailq                              # serveris
```

> **K6.** Kas võõrasse domeeni saatmine õnnestus nüüd (vaata `mailq` ja logi)? Miks kiri tegelikult kohale ei jõua? Mis vahe on portidel 25 ja 587?

**3.3** Proovi vale parooliga ja vaata logi (`sudo grep -i sasl /var/log/mail.log | tail -3`).

**3.4** (Valikuline, kui sul on töölaud) Seadista Thunderbirdis konto `mari@lab.example`: IMAP `mail.lab.example:993` SSL/TLS, SMTP `mail.lab.example:587` STARTTLS, mõlemal tavaline parool. Saada kiri Jaanile ja loe see Jaani kontoga.

---

## 4. osa. DKIM ja DMARC

**4.1** Paigalda OpenDKIM, loo võti valijaga `kool` ja seadista OpenDKIM ning Postfixi *milter* (teooria punkt 23.6).

**4.2** Lisa `debian1` tsooni faili `kool.txt` sisu (TXT-kirje `kool._domainkey`) - pane tähele, et pikk võti on jagatud mitmeks jutumärkides osaks; see on lubatud. Suurenda seerianumbrit.

```bash
dig TXT kool._domainkey.lab.example +short
sudo opendkim-testkey -d lab.example -s kool -vvv
```

**4.3** Saada Mari nimel kiri Jaanile (3.2 käsuga) ja vaata Jaani postkastis kirja päiseid:

```bash
sudo grep -A3 "DKIM-Signature" /home/jaan/Maildir/new/* | tail -5
sudo grep -i opendkim /var/log/mail.log | tail -5
```

> **K7.** Mida näitas `opendkim-testkey` ja milliseid välju sisaldab `DKIM-Signature` päis (`d=`, `s=`, `h=`, `b=`)? Mida teeks saaja server, kui keegi muudaks kirja teemat teel?

> **K8.** Miks alustatakse DMARC-poliitikaga `p=none` ja mida saadetakse `rua` aadressile? Millal võiks minna üle `p=reject`-ile?

---

## 5. osa. Turvalisus ja rämpspost

**5.1** Seadista fail2ban (moodul 12) kaitsma Postfixi autentimist ja Dovecoti:

```text
# /etc/fail2ban/jail.d/post.local
[postfix-sasl]
enabled = true

[dovecot]
enabled = true
```

```bash
sudo apt install fail2ban
sudo systemctl restart fail2ban
sudo fail2ban-client status postfix-sasl
```

Ubuntu kirjutab e-posti logi faili `/var/log/mail.log` (rsyslog), mida fail2ban vaikimisi loeb.

Proovi `debian1`-st mitu korda vale parooliga (3.3) ja kontrolli, kas aadress blokeeriti. Eemalda blokeering: `sudo fail2ban-client set postfix-sasl unbanip DNS_IP`.

> **K9.** Mitme vale katse järel aadress blokeeriti? Miks rünnatakse e-posti servereid paroolide arvamisega eriti palju?

**5.2** Lisa `main.cf`-i `smtpd_recipient_restrictions` hulka DNS-põhine must nimekiri ja kontrolli logist, et seadistus laaditi:

```text
smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination, reject_rbl_client zen.spamhaus.org
```

> **K10.** Mida teeb `reject_rbl_client` ja milline on selle risk (vihje: avalikud DNS-resolverid ja Spamhausi kasutustingimused)?

---

## 6. osa. Teavitused ja varundus

**6.1** Suuna `root`-i, `postmaster`-i ja `abuse` kirjad Marile (`/etc/aliases`, `sudo newaliases`) ja testi: `echo test | mail -s "root-ile" root`.

**6.2** Varunda postkastid ja seadistus restic'uga (moodul 9) ning taasta Jaani üks kustutatud kiri:

```bash
export RESTIC_REPOSITORY=/varu/restic-mail RESTIC_PASSWORD_FILE=/root/.restic-parool
sudo -E restic init
sudo -E restic backup /home/*/Maildir /etc/postfix /etc/dovecot /etc/opendkim /etc/aliases
sudo rm /home/jaan/Maildir/cur/* /home/jaan/Maildir/new/* 2>/dev/null
sudo -E restic restore latest --target / --include /home/jaan/Maildir
curl -k --user jaan:PAROOL "imaps://mail.lab.example/INBOX"
```

> **K11.** Kas Jaani kirjad on IMAP-is jälle näha? Miks on DKIM-i privaatvõti varunduses oluline? Miks on Maildiri vorming varundamiseks mugavam kui üks suur postkastifail?

> **K12.** Kool kaalub, kas pidada oma e-posti serverit või kasutada pilveposti. Too kummagi poolt vähemalt kolm argumenti, arvestades selle laboritöö kogemust (töö, turvalisus, kättetoimetavus, andmete asukoht, hind).

---

## Lisaülesanne (valikuline)

1. **Virtuaalsed postkastid:** seadista Postfix ja Dovecot nii, et domeeni `teine.example` kasutajad ei ole süsteemi kasutajad (`virtual_mailbox_domains`, Dovecoti `passwd-file`).
2. **Rspamd:** paigalda Rspamd, ühenda see Postfixiga milterina ja vaata veebiliidesest kirjade hindeid. Asenda OpenDKIM Rspamdi DKIM-allkirjaga.
3. **Roundcube:** paigalda veebipost (Roundcube) nginx-i ja PHP-ga (moodul 15) ning loe kirju brauseris.
4. **Teine server:** paigalda AlmaLinuxi masinasse teine Postfix domeenile `teine.example` (DNS-is oma MX) ja saada kirju kahe serveri vahel. Kontrolli saaja poolel SPF-i ja DKIM-i tulemust (`Authentication-Results:` päis, vajab OpenDKIM-i `Mode sv` ja SPF-i kontrollijat, nt `postfix-policyd-spf-python`).

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 0.2)* Miks peab MX-kirje osutama nimele, millel on A-kirje, mitte IP-aadressile ega CNAME-ile? Mida tähendab SPF-kirjes `-all` ja mida `~all`?
- **K2.** *(punkt 1.3)* Leia logist ühe kirja järjekorra ID ja kirjelda selle järgi kirja teekonda (`smtpd`, `cleanup`, `qmgr`, `local`). Mis oli lõplik `status=`?
- **K3.** *(punkt 1.3)* Millised päised lisas Postfix kirjale (`Received:`, `Return-Path:`, `Message-Id:`)? Mida näitab `Received:` rida?
- **K4.** *(punkt 1.4)* Mis vastuse said? Milline seade selle põhjustas ja miks on see e-posti serveri kõige olulisem turvaseade?
- **K5.** *(punkt 2.3)* Mida vastas server ilma TLS-ita (port 143) ühendusele? Miks on `disable_plaintext_auth = yes` oluline? Kus asuvad kirjad serveris ja mis juhtub failiga `Maildir/new/…` pärast lugemist?
- **K6.** *(punkt 3.2)* Kas võõrasse domeeni saatmine õnnestus nüüd (vaata `mailq` ja logi)? Miks kiri tegelikult kohale ei jõua? Mis vahe on portidel 25 ja 587?
- **K7.** *(punkt 4.3)* Mida näitas `opendkim-testkey` ja milliseid välju sisaldab `DKIM-Signature` päis (`d=`, `s=`, `h=`, `b=`)? Mida teeks saaja server, kui keegi muudaks kirja teemat teel?
- **K8.** *(punkt 4.3)* Miks alustatakse DMARC-poliitikaga `p=none` ja mida saadetakse `rua` aadressile? Millal võiks minna üle `p=reject`-ile?
- **K9.** *(punkt 5.1)* Mitme vale katse järel aadress blokeeriti? Miks rünnatakse e-posti servereid paroolide arvamisega eriti palju?
- **K10.** *(punkt 5.2)* Mida teeb `reject_rbl_client` ja milline on selle risk (vihje: avalikud DNS-resolverid ja Spamhausi kasutustingimused)?
- **K11.** *(punkt 6.2)* Kas Jaani kirjad on IMAP-is jälle näha? Miks on DKIM-i privaatvõti varunduses oluline? Miks on Maildiri vorming varundamiseks mugavam kui üks suur postkastifail?
- **K12.** *(punkt 6.2)* Kool kaalub, kas pidada oma e-posti serverit või kasutada pilveposti. Too kummagi poolt vähemalt kolm argumenti, arvestades selle laboritöö kogemust (töö, turvalisus, kättetoimetavus, andmete asukoht, hind).
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 23. E-posti server](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 23. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
