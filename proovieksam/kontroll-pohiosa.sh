#!/bin/bash
# Põhiosa proovieksami automaatne kontroll (Debian 13).
# Kasutus: sudo bash kontroll-pohiosa.sh
# Väljund: iga ülesande kohta OK/VIGA ja lõpus punktisumma.
set -uo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "Käivita juurkasutajana: sudo bash $0" >&2
    exit 2
fi

punkte=0
kokku=0

kontroll() {
    # kontroll PUNKTID "kirjeldus" käsk [argumendid...]
    local p="$1" kirjeldus="$2"
    shift 2
    kokku=$((kokku + p))
    if "$@" &>/dev/null; then
        printf '  OK    (%d p) %s\n' "$p" "$kirjeldus"
        punkte=$((punkte + p))
    else
        printf '  VIGA  (0/%d) %s\n' "$p" "$kirjeldus"
    fi
}

pealkiri() { printf '\n%s\n' "$1"; }

# --- abifunktsioonid -------------------------------------------------------
on_grupis()  { id -nG "$1" | tr ' ' '\n' | grep -qx "$2"; }
kest_on()    { [[ "$(getent passwd "$1" | cut -d: -f7)" == "$2" ]]; }
omanik_on()  { [[ "$(stat -c '%U:%G' "$1")" == "$2" ]]; }
oigused_on() { [[ "$(stat -c '%a' "$1")" == "$2" ]]; }
pakett_on()  { dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q "install ok installed"; }
sshd_seade() { sshd -T 2>/dev/null | grep -qix "$1"; }
lubatud_ja_aktiivne() { systemctl is-enabled "$1" && systemctl is-active "$1"; }
lv_suurus_vahemikus() {
    # lv_suurus_vahemikus VG/LV MIN_MiB MAX_MiB
    local s
    s=$(lvs --noheadings --units m --nosuffix -o lv_size "$1" 2>/dev/null | tr -d ' ' | cut -d. -f1)
    [[ -n "$s" ]] && (( s >= $2 && s <= $3 ))
}
veebileht_sisaldab() {
    # loeb http://127.0.0.1/ ilma curl-ita (Bashi /dev/tcp), alamkestas
    (
        exec 3<>/dev/tcp/127.0.0.1/80 || exit 1
        printf 'GET / HTTP/1.0\r\nHost: localhost\r\n\r\n' >&3
        timeout 5 cat <&3 | grep -q "$1"
    )
}
ufw_lubab() { ufw status | grep -Eq "^($1)(/tcp)?[[:space:]]+ALLOW"; }

echo "Põhiosa proovieksami kontroll: $(hostname) $(date '+%F %T')"

pealkiri "1. Süsteem"
kontroll 2 "Hostinimi on pohi.lab.example" bash -c '[[ "$(hostnamectl --static)" == pohi.lab.example ]]'
kontroll 2 "Ajavöönd on Europe/Tallinn" bash -c '[[ "$(timedatectl show -p Timezone --value)" == Europe/Tallinn ]]'

pealkiri "2. Kasutajad ja grupid"
kontroll 1 "Grupp 'opetajad' on olemas (GID 4000)" bash -c '[[ "$(getent group opetajad | cut -d: -f3)" == 4000 ]]'
kontroll 1 "Kasutaja 'anna' kuulub gruppi opetajad" on_grupis anna opetajad
kontroll 1 "Kasutaja 'peeter' kuulub gruppi opetajad" on_grupis peeter opetajad
kontroll 1 "Kasutajate anna ja peeter kest on /bin/bash" bash -c '[[ "$(getent passwd anna | cut -d: -f7)" == /bin/bash && "$(getent passwd peeter | cut -d: -f7)" == /bin/bash ]]'
kontroll 1 "Kasutaja 'anna' saab kasutada sudo't (grupp sudo)" on_grupis anna sudo
kontroll 1 "Kasutajal 'varundus' on kest /usr/sbin/nologin" kest_on varundus /usr/sbin/nologin
kontroll 1 "Kasutaja peeter parool aegub iga 60 päeva järel" bash -c "chage -l peeter | grep -Eq 'Maximum.*: 60$'"

pealkiri "3. Failid, õigused ja tekst"
kontroll 1 "/srv/opetajad omanik on root:opetajad" omanik_on /srv/opetajad root:opetajad
kontroll 2 "/srv/opetajad õigused on 2770 (SGID)" oigused_on /srv/opetajad 2770
kontroll 2 "/srv/avalik õigused on 1777 (sticky bit)" oigused_on /srv/avalik 1777
kontroll 2 "/root/hosts-viit on sümbolviit failile /etc/hosts" bash -c '[[ -L /root/hosts-viit && "$(readlink /root/hosts-viit)" == /etc/hosts ]]'
kontroll 2 "/root/bash-kasutajad.txt: bash-kestaga kasutajad tähestiku järjekorras" \
    bash -c "diff <(cat /root/bash-kasutajad.txt) <(grep 'bash\$' /etc/passwd | cut -d: -f1 | sort)"
kontroll 1 "/root/tcp-arv.txt sisaldab /etc/services TCP-ridade arvu" \
    bash -c '[[ "$(tr -d "[:space:]" < /root/tcp-arv.txt)" == "$(grep -c "/tcp" /etc/services)" ]]'

pealkiri "4. Tarkvara, teenused ja ajastamine"
kontroll 1 "Paketid tree ja htop on paigaldatud" bash -c 'dpkg-query -W -f="\${Status}" tree htop | grep -c "install ok installed" | grep -qx 2'
kontroll 1 "Pakett nginx on paigaldatud" pakett_on nginx
kontroll 2 "nginx töötab ja käivitub alglaadimisel" lubatud_ja_aktiivne nginx
kontroll 2 "Veebiserveri avaleht sisaldab sõna 'Põhiosa'" veebileht_sisaldab "Põhiosa"
kontroll 2 "systemd taimer kettaaruanne.timer on lubatud ja aktiivne" lubatud_ja_aktiivne kettaaruanne.timer
kontroll 1 "Taimer käivitub iga päev kell 06:00" bash -c "systemctl cat kettaaruanne.timer | grep -Eq '^OnCalendar=.*06:00'"

pealkiri "5. Võrk, SSH ja tulemüür"
kontroll 2 "SSH: juurkasutaja sisselogimine keelatud" sshd_seade "permitrootlogin no"
kontroll 2 "ufw on aktiivne" bash -c "ufw status | grep -q 'Status: active'"
kontroll 1 "ufw lubab SSH (22)" ufw_lubab "22|OpenSSH"
kontroll 1 "ufw lubab HTTP (80)" ufw_lubab "80|Nginx HTTP|Nginx Full|WWW"

pealkiri "6. Kettad ja LVM"
kontroll 1 "Köitegrupp vg_pohi on olemas" vgs vg_pohi
kontroll 2 "Köide lv_kodu on suurendatud ~600 MiB-ni (580–640)" lv_suurus_vahemikus vg_pohi/lv_kodu 580 640
kontroll 2 "lv_kodu on ext4 ja haagitud /mnt/kodu" bash -c "findmnt -n -o FSTYPE /mnt/kodu | grep -qx ext4"
kontroll 2 "Failisüsteem on koos köitega suurendatud (üle 500 MiB)" bash -c '(( $(df -BM --output=size /mnt/kodu | tail -1 | tr -dc 0-9) > 500 ))'
kontroll 2 "/mnt/kodu haagitakse püsivalt (fstab, UUID)" \
    bash -c "grep -Eq '^UUID=[^ ]+[[:space:]]+/mnt/kodu[[:space:]]' /etc/fstab"

pealkiri "7. Skript"
kontroll 1 "/usr/local/bin/tervitus on olemas ja käivitatav" test -x /usr/local/bin/tervitus
kontroll 2 "'tervitus Mari' väljastab 'Tere, Mari!'" bash -c '[[ "$(/usr/local/bin/tervitus Mari)" == "Tere, Mari!" ]]'
kontroll 2 "Ilma argumendita: veateade standardveaväljundisse ja väljumiskood 1" \
    bash -c 'out=$(/usr/local/bin/tervitus 2>/dev/null); kood=$?; [[ $kood -eq 1 && -z "$out" ]]'

pealkiri "8. Varundus ja taastamine"
kontroll 2 "/var/backups/etc-AAAA-KK-PP.tar.gz on olemas ja sisaldab kataloogi /etc" \
    bash -c 'f=$(ls -1 /var/backups/etc-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].tar.gz | tail -1) && tar -tzf "$f" | grep -Eq "^/?etc/passwd$"'
kontroll 2 "Arhiivist on taastatud ainult /root/taaste/etc/hostname" \
    bash -c '[[ -s /root/taaste/etc/hostname && ! -e /root/taaste/etc/passwd ]]'
kontroll 2 "/home on kopeeritud kataloogi /var/backups/home koos omanikega" \
    bash -c '[[ -d /var/backups/home/anna && "$(stat -c %U /var/backups/home/anna)" == anna && "$(stat -c %U /var/backups/home/peeter)" == peeter ]]'

printf '\nKokku: %d / %d punkti (%d%%)\n' "$punkte" "$kokku" $(( punkte * 100 / kokku ))
if (( punkte * 100 / kokku >= 70 )); then
    echo "Tulemus: SOORITATUD (vähemalt 70%)"
else
    echo "Tulemus: MITTE SOORITATUD (alla 70%)"
fi
