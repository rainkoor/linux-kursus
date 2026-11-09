# Moodul 8. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mida tähendavad seadmenimed `/dev/sdb2`, `/dev/vda1` ja `/dev/nvme0n1p3`?
2. Millised on GPT eelised MBR-i ees?
3. Mis vahe on partitsioonil ja failisüsteemil?
4. Millist failisüsteemi kasutab AlmaLinux vaikimisi? Millist piirangut tuleb sellega arvestada?
5. Mis juhtub failidega, mis olid haakepunkti kataloogis enne haakimist?
6. Mida tähendab veateade `target is busy` ja kuidas leida põhjus?
7. Selgita `/etc/fstab` rea `UUID=1234-abcd /srv/andmed ext4 defaults,nofail 0 2` kõiki välju.
8. Miks kasutada fstab-is UUID-d, mitte seadme nime?
9. Mida tuleks teha pärast fstab-i muutmist enne taaskäivitust?
10. Mis on saaleala ja millal seda kasutatakse?
11. Selgita LVM-i kolme kihti: PV, VG ja LV.
12. Nimeta kolm LVM-i eelist tavaliste partitsioonide ees.
13. Mida teeb võti `-r` käsus `lvextend`?
14. Mis kaitseb LUKS ja mille eest see ei kaitse?
15. Ketas on `df -h` järgi täis, kuid `du` ei leia suuri faile. Mis võib olla põhjus?
16. Millised failid on vaja muuta, et LUKS-iga krüpteeritud ketas avataks ja haagitaks alglaadimisel?

## Praktilised miniülesanded

Tee ülesanded laborimasinas, kus on vaba lisaketas (siin `/dev/sdd`).

1. Loo kettale `/dev/sdd` GPT-tabel ja üks partitsioon, mis võtab kogu ketta.
2. Loo partitsioonile ext4 failisüsteem sildiga `varu` ja haagi see püsivalt kataloogi `/varu`, kasutades fstab-is sildi (`LABEL=`) viidet.
3. Leia kataloogis `/usr` viis suurimat alamkataloogi.
4. Köitegrupis `vg_andmed` on 2 GiB vaba. Loo sinna 500 MiB köide `lv_logid` XFS-failisüsteemiga.
5. Suurenda köidet `lv_logid` nii, et see kasutab kogu köitegrupi vaba ruumi.
6. Kontrolli, mitu i-sõlme on juurfailisüsteemis kasutusel.

---

## Vastused

1. `/dev/sdb2` - teise SATA/SCSI-ketta teine partitsioon; `/dev/vda1` - esimese VirtIO Block ketta esimene partitsioon; `/dev/nvme0n1p3` - esimese NVMe-ketta kolmas partitsioon.
2. Toetab üle 2 TiB kettaid, kuni 128 partitsiooni ja hoiab partitsioonitabeli koopiat ketta lõpus.
3. Partitsioon on ketta osa (ruum). Failisüsteem on selle ruumi korraldus, mis võimaldab sinna faile salvestada. Partitsioon tuleb enne kasutamist vormindada.
4. XFS. XFS-i saab ainult suurendada, mitte vähendada.
5. Need ei ole haakimise ajal nähtavad, kuid ei kao - need tulevad lahtihaakimisel tagasi.
6. Mõni protsess kasutab failisüsteemi (nt avatud fail või kest selles kataloogis). Põhjuse leiab käsuga `fuser -vm haakepunkt` või `lsof`.
7. `UUID=1234-abcd` - failisüsteemi unikaalne tunnus; `/srv/andmed` - haakepunkt; `ext4` - failisüsteemi tüüp; `defaults,nofail` - tavalised valikud ja alglaadimine jätkub, kui seadet pole; `0` - dump (ei kasutata); `2` - kontrollitakse alglaadimisel pärast juurfailisüsteemi.
8. Seadmenimed võivad ketaste lisamisel või eemaldamisel muutuda, UUID on failisüsteemi püsiv tunnus.
9. `findmnt --verify`, `systemctl daemon-reload` ja `mount -a` ning kontrollida tulemust (`df -h`).
10. Kettaruum, kuhu kernel tõstab vähe kasutatud mälu, kui RAM saab otsa. See hoiab ära mälupuudusest tingitud kokkujooksmise, kuid on RAM-ist palju aeglasem.
11. **PV** - LVM-i jaoks ettevalmistatud ketas või partitsioon; **VG** - ühe või mitme PV ühendatud ruum; **LV** - VG-st eraldatud osa, mida kasutatakse nagu partitsiooni.
12. Näiteks: köiteid saab suurendada töö ajal; köitegruppi saab lisada uusi kettaid; köide võib ulatuda üle mitme ketta; hetktõmmised.
13. Suurendab koos köitega ka failisüsteemi.
14. LUKS kaitseb seisvaid andmeid: varastatud või äravisatud kettalt ei saa andmeid lugeda ilma paroolita. See ei kaitse töötavat süsteemi - kui ketas on avatud, näevad seda kõik, kellel on failiõigused, ja ründaja, kes saab süsteemi ligi.
15. Näiteks kustutatud fail, mida mõni protsess veel avatuna hoiab (`lsof +L1`); i-sõlmed on otsas (`df -i`); andmed on peidus haakepunkti all; `du` ei näe faile, millele kasutajal pole lugemisõigust.
16. `/etc/crypttab` (LUKS-seadme avamine: nimi, UUID, võti või `none`) ja `/etc/fstab` (avatud seadme `/dev/mapper/nimi` haakimine).

### Miniülesannete lahendused

```bash
# 1
sudo parted -s /dev/sdd mklabel gpt
sudo parted -s /dev/sdd mkpart varu ext4 1MiB 100%
# 2
sudo mkfs.ext4 -L varu /dev/sdd1
sudo mkdir -p /varu
echo "LABEL=varu  /varu  ext4  defaults,nofail  0  2" | sudo tee -a /etc/fstab
sudo findmnt --verify && sudo systemctl daemon-reload && sudo mount -a
# 3
sudo du -h --max-depth=1 /usr 2>/dev/null | sort -h | tail -6
# 4
sudo lvcreate -n lv_logid -L 500M vg_andmed
sudo mkfs.xfs /dev/vg_andmed/lv_logid
# 5 (failisüsteem peab olema haagitud, et XFS-i saaks suurendada)
sudo mkdir -p /srv/logid && sudo mount /dev/vg_andmed/lv_logid /srv/logid
sudo lvextend -r -l +100%FREE /dev/vg_andmed/lv_logid
# 6
df -i /
```

Ülesandes 3 näitab `tail -6` kuut rida, sest viimane rida on kataloog `/usr` ise koos kogusummaga.

<!-- navigatsioon -->
---

[← Laboritöö 8. Kettad, failisüsteemid ja LVM](labor.md) · [Sisukord](../../README.md#sisukord) · [Proovieksam: põhiosa →](../proovieksam-pohiosa.md)
<!-- /navigatsioon -->
