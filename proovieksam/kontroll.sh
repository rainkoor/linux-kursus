#!/bin/bash
# Proovieksami automaatne kontroll (AlmaLinux 10).
# Kasutus: sudo bash kontroll.sh
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
on_grupis()      { id -nG "$1" | tr ' ' '\n' | grep -qx "$2"; }
kest_on()        { [[ "$(getent passwd "$1" | cut -d: -f7)" == "$2" ]]; }
omanik_on()      { [[ "$(stat -c '%U:%G' "$1")" == "$2" ]]; }
oigused_on()     { [[ "$(stat -c '%a' "$1")" == "$2" ]]; }
acl_sisaldab()   { getfacl -p "$1" 2>/dev/null | grep -q "$2"; }
teenus_avatud()  { firewall-cmd --list-services | tr ' ' '\n' | grep -qx "$1"; }
sshd_seade()     { sshd -T 2>/dev/null | grep -qix "$1"; }
selinux_tyyp()   { ls -Zd "$1" 2>/dev/null | grep -q "$2"; }
lv_suurus_vahemikus() {
    # lv_suurus_vahemikus VG/LV MIN_MiB MAX_MiB
    local s
    s=$(lvs --noheadings --units m --nosuffix -o lv_size "$1" 2>/dev/null | tr -d ' ' | cut -d. -f1)
    [[ -n "$s" ]] && (( s >= $2 && s <= $3 ))
}
lubatud_ja_aktiivne() { systemctl is-enabled "$1" && systemctl is-active "$1"; }

echo "Proovieksami kontroll: $(hostname) $(date '+%F %T')"

pealkiri "1. Süsteem ja võrk"
kontroll 2 "Hostinimi on eksam.lab.example" bash -c '[[ "$(hostnamectl --static)" == eksam.lab.example ]]'
kontroll 2 "Ajavöönd on Europe/Tallinn" bash -c '[[ "$(timedatectl show -p Timezone --value)" == Europe/Tallinn ]]'
kontroll 2 "Kell on sünkroonis (chronyd töötab ja on lubatud)" lubatud_ja_aktiivne chronyd

pealkiri "2. Kasutajad ja grupid"
kontroll 1 "Grupp 'arendajad' on olemas (GID 3000)" bash -c '[[ "$(getent group arendajad | cut -d: -f3)" == 3000 ]]'
kontroll 1 "Kasutaja 'liis' kuulub gruppi arendajad" on_grupis liis arendajad
kontroll 1 "Kasutaja 'tom' kuulub gruppi arendajad" on_grupis tom arendajad
kontroll 1 "Kasutajal 'robot' on kest /sbin/nologin" kest_on robot /sbin/nologin
kontroll 2 "Grupp arendajad saab käivitada sudo-ga 'systemctl restart httpd' (sudoers.d)" \
    bash -c "grep -rqs '^%arendajad.*systemctl restart httpd' /etc/sudoers.d/ && visudo -c"
kontroll 1 "Kasutaja liis parool aegub iga 90 päeva järel" bash -c "chage -l liis | grep -Eq 'Maximum.*: 90$'"

pealkiri "3. Failid ja õigused"
kontroll 1 "Kataloog /srv/projekt on olemas, omanik root:arendajad" omanik_on /srv/projekt root:arendajad
kontroll 2 "/srv/projekt õigused on 2770 (SGID)" oigused_on /srv/projekt 2770
kontroll 2 "Kasutajal 'robot' on /srv/projekt-le lugemisõigus ACL-iga" acl_sisaldab /srv/projekt "user:robot:r-x"
kontroll 2 "Arhiiv /root/etc-varu.tar.gz on olemas ja sisaldab faili etc/ssh/sshd_config" \
    bash -c "tar -tzf /root/etc-varu.tar.gz | grep -q 'etc/ssh/sshd_config'"
kontroll 2 "Fail /root/suured.txt sisaldab /usr all olevaid üle 50 MiB faile" \
    bash -c "test -s /root/suured.txt && diff <(sort /root/suured.txt) <(find /usr -type f -size +50M | sort)"

pealkiri "4. Tarkvara ja teenused"
kontroll 1 "Pakett httpd on paigaldatud" rpm -q httpd
kontroll 2 "httpd töötab ja käivitub alglaadimisel" lubatud_ja_aktiivne httpd
kontroll 2 "Veebiserver vastab lehega, mis sisaldab sõna 'Eksam'" bash -c "curl -s http://localhost/ | grep -q Eksam"
kontroll 2 "Tulemüüris on lubatud teenus http" teenus_avatud http

pealkiri "5. Kettad ja LVM"
kontroll 2 "Köitegrupp vg_eksam on olemas" vgs vg_eksam
kontroll 2 "Köide lv_andmed suurusega ~500 MiB (480–560)" lv_suurus_vahemikus vg_eksam/lv_andmed 480 560
kontroll 2 "lv_andmed on XFS ja haagitud /mnt/andmed" bash -c "findmnt -n -o FSTYPE /mnt/andmed | grep -qx xfs"
kontroll 2 "/mnt/andmed haagitakse püsivalt (fstab, UUID)" \
    bash -c "grep -Eq '^UUID=[^ ]+[[:space:]]+/mnt/andmed[[:space:]]' /etc/fstab"
kontroll 2 "Lisasaaleala 256 MiB on aktiivne ja fstab-is" \
    bash -c "swapon --show=NAME,SIZE --noheadings | grep -q '256M' && grep -Eq '^[^#].*[[:space:]]swap[[:space:]]' /etc/fstab"

pealkiri "6. Turvalisus"
kontroll 2 "SSH: juurkasutaja sisselogimine keelatud" sshd_seade "permitrootlogin no"
kontroll 2 "SSH kuulab pordil 2222 ja tulemüür lubab selle" bash -c "sshd -T | grep -qix 'port 2222' && firewall-cmd --list-ports | grep -qw 2222/tcp"
kontroll 2 "SELinux on enforcing" bash -c '[[ "$(getenforce)" == Enforcing ]]'
kontroll 3 "Veebisisu kataloogil /srv/veeb on SELinuxi tüüp httpd_sys_content_t" selinux_tyyp /srv/veeb httpd_sys_content_t
kontroll 2 "Journal on püsiv (/var/log/journal olemas)" test -d /var/log/journal

pealkiri "7. Ajastamine ja kernel"
kontroll 3 "systemd taimer varunda-etc.timer on lubatud ja aktiivne" lubatud_ja_aktiivne varunda-etc.timer
kontroll 2 "Kerneli parameeter vm.swappiness = 10 püsivalt (/etc/sysctl.d/)" \
    bash -c "sysctl -n vm.swappiness | grep -qx 10 && grep -rqs 'vm.swappiness *= *10' /etc/sysctl.d/"

pealkiri "8. Konteiner"
kontroll 3 "Quadlet-teenus 'eksamiveeb' töötab ja vastab pordil 8080" \
    bash -c "systemctl is-active eksamiveeb.service && curl -s http://localhost:8080/ >/dev/null"

printf '\nKokku: %d / %d punkti (%d%%)\n' "$punkte" "$kokku" $(( punkte * 100 / kokku ))
if (( punkte * 100 / kokku >= 70 )); then
    echo "Tulemus: SOORITATUD (vähemalt 70%)"
else
    echo "Tulemus: MITTE SOORITATUD (alla 70%)"
fi
