# Laboritöö 16. Ansible ja Vagrant

| | |
|---|---|
| **Distro** | AlmaLinux (juhtmasin), Debian ja Ubuntu (hallatavad sõlmed) |
| **Kestus** | 4 × 90 minutit |
| **Vajalik** | Laboritöö 12 AlmaLinuxi masin koos Git-hoidlaga `~/infra`, varasemate laboritööde Debiani ja Ubuntu masinad. 2. osa jaoks oma arvuti VirtualBoxi ja Vagrantiga |
| **Eesmärk** | Seadistada mitu serverit korraga Ansible'iga, jagada kood rollideks, testida seda ja luua korratav laborikeskkond |

**Aruanne:** vasta küsimustele **K1–K11**. Esita ka oma Git-hoidla (`git log --oneline --graph` väljund).

Tähised: `DEBIAN_IP`, `UBUNTU_IP`, `ALMA_IP`, `kasutaja` - asenda oma väärtustega.

---

## 1. osa. Ansible

Seadistad Ansible'iga korraga Debiani ja Ubuntu masina: lisad ühised tööriistad, sisselogimisteate ja nginx-i saidi pordil 8090.

**1.1** Paigalda Ansible ja kontrolli SSH-ühendust hallatavatega. Kopeeri vajadusel oma AlmaLinuxi kasutaja SSH-võti:

```bash
sudo dnf install ansible-core
ansible --version
ssh-keygen -t ed25519            # kui võtit veel pole
ssh-copy-id kasutaja@DEBIAN_IP
ssh-copy-id kasutaja@UBUNTU_IP
```

**1.2** Loo projekt ja inventuur:

```bash
mkdir -p ~/infra/ansible/{templates,files} && cd ~/infra/ansible
```

`inventuur.ini`:

```ini
[veebiserverid]
debian1 ansible_host=DEBIAN_IP
ubuntusrv ansible_host=UBUNTU_IP

[all:vars]
ansible_user=kasutaja
```

`ansible.cfg`:

```ini
[defaults]
inventory = inventuur.ini
```

**1.3** Ad-hoc käsud:

```bash
ansible all -m ansible.builtin.ping
ansible all -a "uptime"
ansible all -m ansible.builtin.setup -a "filter=ansible_distribution*"
ansible all -b -K -a "whoami"
```

**K1.** Mida vastas `ping`? Milliseid distro fakte Ansible kogus? Mida tegi `-b -K`?

**1.4** Loo mall `templates/motd.j2`:

```jinja
====================================================
  {{ ansible_hostname }} - {{ ansible_distribution }} {{ ansible_distribution_version }}
  Seda serverit haldab Ansible. Käsitsi muudatused
  võidakse üle kirjutada!
  Vastutaja: {{ vastutaja }}
====================================================
```

mall `templates/index.html.j2`:

```jinja
<!doctype html>
<html lang="et"><head><meta charset="utf-8"><title>{{ ansible_hostname }}</title></head>
<body>
<h1>{{ kooli_nimi }}</h1>
<p>Server: {{ ansible_hostname }} ({{ ansible_distribution }} {{ ansible_distribution_version }})</p>
<p>IP: {{ ansible_default_ipv4.address }}</p>
</body></html>
```

ja nginx-i saidi seadistus `files/ansible-sait.conf`:

```nginx
server {
    listen 8090;
    root /var/www/ansible;
    index index.html;
}
```

**1.5** Loo mänguraamat `veebiserverid.yml`:

```yaml
- name: Ühine seadistus ja veebisait
  hosts: veebiserverid
  become: true

  vars:
    kooli_nimi: Haapsalu õppekool
    vastutaja: "{{ lookup('env', 'USER') }}"
    tooriistad:
      - htop
      - tree
      - curl

  tasks:
    - name: Paigalda ühised tööriistad
      ansible.builtin.package:
        name: "{{ tooriistad }}"
        state: present

    - name: Sisselogimisteade
      ansible.builtin.template:
        src: templates/motd.j2
        dest: /etc/motd
        mode: "0644"

    - name: Paigalda nginx
      ansible.builtin.package:
        name: nginx
        state: present

    - name: Saidi kataloog
      ansible.builtin.file:
        path: /var/www/ansible
        state: directory
        mode: "0755"

    - name: Saidi avaleht
      ansible.builtin.template:
        src: templates/index.html.j2
        dest: /var/www/ansible/index.html
        mode: "0644"

    - name: Saidi seadistus
      ansible.builtin.copy:
        src: files/ansible-sait.conf
        dest: /etc/nginx/sites-available/ansible-sait
        mode: "0644"
      notify: Laadi nginx uuesti

    - name: Luba sait
      ansible.builtin.file:
        src: /etc/nginx/sites-available/ansible-sait
        dest: /etc/nginx/sites-enabled/ansible-sait
        state: link
      notify: Laadi nginx uuesti

    - name: nginx töötab
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Laadi nginx uuesti
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

**1.6** Kontrolli ja käivita kõigepealt proovirežiimis:

```bash
ansible-playbook veebiserverid.yml --syntax-check
ansible-playbook veebiserverid.yml -K --check --diff
```

**1.7** Käivita päriselt - **kaks korda järjest**:

```bash
ansible-playbook veebiserverid.yml -K
ansible-playbook veebiserverid.yml -K
```

**K2.** Kopeeri mõlema käivituse lõpukokkuvõte (`PLAY RECAP`) aruandesse. Mille poolest need erinevad? Mida tähendab idempotentsus?

**1.8** Kontrolli tulemust:

```bash
ansible veebiserverid -a "curl -s http://localhost:8090"
ssh kasutaja@DEBIAN_IP
```

**K3.** Mida näitas veebileht kummaski serveris? Kas sisselogimisel ilmus teade? Kuidas sai sama mall eri serverites eri sisu?

**1.9** **Seadistuse triiv:** logi Ubuntu masinasse ja muuda faili `/var/www/ansible/index.html` käsitsi. Kustuta Debianis pakett `tree`. Käivita mänguraamat uuesti.

**K4.** Mida Ansible tegi? Mis on „seadistuse triiv“ (*configuration drift*) ja kuidas Ansible seda lahendab?

**1.10** Lisa kolmas server: lisa inventuuri AlmaLinuxi masin ise (`alma ansible_host=localhost ansible_connection=local`) gruppi `veebiserverid` ja käivita mänguraamat.

**K5.** Mis juhtus AlmaLinuxis? Milline ülesanne ebaõnnestus ja miks? (Vihje: kas AlmaLinuxi nginx kasutab kataloogi `sites-available`?) Kuidas peaks mänguraamatut muutma, et see töötaks ka AlmaLinuxis? (Vihje: `when: ansible_os_family == "Debian"` ja `/etc/nginx/conf.d/`.)

Paranda mänguraamat või eemalda AlmaLinux inventuurist.

**1.11** Lisa Ansible'i projekt Giti ja saada kaughoidlasse:

```bash
cd ~/infra
git add ansible
git commit -m "Lisa veebiserverite Ansible'i mänguraamat"
git push
```


---

## 2. osa. Vagrant (valikuline, oma arvutis)

**2.1** Paigalda oma arvutisse VirtualBox ja Vagrant ning loo teooria punkti 16.3 Vagrantfile'iga kolm masinat:

```bash
vagrant up
vagrant status
vagrant ssh debian -c "hostnamectl"
```

**2.2** Käivita nende vastu 1. osa mänguraamat (`config.vm.provision "ansible"` või eraldi inventuuriga, kus `ansible_host` on Vagrantfile'i IP-aadressid ja kasutaja `vagrant`).

**2.3** Kustuta masinad (`vagrant destroy -f`), loo uuesti ja veendu, et tulemus on sama.

---

## 3. osa. Rollid ja testimine

Teed 1. osa mänguraamatust rolli, viid muutujad õigetesse failidesse ja testid koodi (teooria punkt 16.4).

**3.1** Loo roll ja tõsta failid sinna:

```bash
cd ~/infra/ansible
ansible-galaxy role init --init-path roles veebiserver
mv templates/motd.j2 templates/index.html.j2 roles/veebiserver/templates/
mv files/ansible-sait.conf roles/veebiserver/files/
```

**3.2** Kirjuta `roles/veebiserver/defaults/main.yml`:

```yaml
kooli_nimi: Kool
vastutaja: administraator
tooriistad:
  - htop
  - tree
  - curl
```

ja `group_vars/veebiserverid.yml`:

```yaml
kooli_nimi: Haapsalu õppekool
vastutaja: "{{ lookup('env', 'USER') }}"
```

**3.3** Tõsta 1. osa mänguraamatu `tasks:` ülesanded faili `roles/veebiserver/tasks/main.yml` ja `handlers:` faili `roles/veebiserver/handlers/main.yml` (ilma `- name: … hosts:` päiseta, ainult ülesannete loend). Rollis viidatakse mallidele ja failidele ilma kataloogita: `src: motd.j2`, `src: ansible-sait.conf`. Loo uus mänguraamat `site.yml`:

```yaml
- name: Veebiserverid rolliga
  hosts: veebiserverid
  become: true
  roles:
    - veebiserver
```

**3.4** Kontrolli ja käivita:

```bash
ansible-playbook site.yml --syntax-check
ansible-playbook site.yml -K --check --diff
ansible-playbook site.yml -K
ansible-playbook site.yml -K | tee /tmp/teine.txt
grep -E 'changed=[1-9]' /tmp/teine.txt && echo "EI OLE IDEMPOTENTNE" || echo "OK"
```

**K6.** Mida näitab veebileht nüüd kooli nimena - rolli vaikeväärtust või `group_vars` väärtust? Miks? Mis juhtub, kui käivitad `ansible-playbook site.yml -K -e kooli_nimi=Test`?

**3.5** Paigalda `ansible-lint` ja kontrolli projekti:

```bash
sudo dnf install -y python3-pip
python3 -m pip install --user ansible-lint
ansible-lint
```

Paranda leiud (või põhjenda, miks mõnda ei paranda) ja käivita uuesti, kuni leide pole.

**K7.** Milliseid leide `ansible-lint` andis (reegli nimed)? Kas mõni neist oleks võinud põhjustada päris vea?

**3.6** Tee lõpuks muudatus, mis rikub idempotentsuse: lisa rolli ülesanne

```yaml
- name: Kirjuta paigaldusaeg
  ansible.builtin.shell: date > /var/www/ansible/aeg.txt
```

ja käivita idempotentsuse kontroll uuesti. Seejärel paranda ülesanne nii, et see muudaks faili ainult esimesel korral (vihje: `creates: /var/www/ansible/aeg.txt`).

**K8.** Mida näitas idempotentsuse kontroll enne ja pärast parandust? Miks loeb Ansible `shell`-ülesande alati muutunuks?

**3.7** Kanna muudatused Giti: `git add -A && git commit -m "Veebiserveri roll, group_vars ja ansible-lint"` ja `git push`.

---

## 4. osa. Kokkuvõte

**K9.** Võrdle laboritöid 13–15 (käsitsi seadistatud server) ja selle laboritöö 1. osa (Ansible). Kui kaua kuluks kummalgi viisil 20 ühesuguse serveri seadistamiseks? Millised on automatiseerimise eelised ja puudused?

**K10.** Kirjelda, kuidas kasutaksid Giti, konteinereid ja Ansible'it koos, et laboritööde 13–15 server oleks võimalik ühe tunniga nullist uuesti üles ehitada.

**K11.** Koosta `git log --oneline --graph` väljund oma hoidlast. Mitu sissekannet tegid? Kas sissekannete kirjeldused on arusaadavad ka kellelegi teisele?


---

## Lisaülesanne (valikuline)

1. **Molecule:** loo rollile `veebiserver` Molecule'i stsenaarium, mis testib rolli Podmani konteineris (Debian 13 ja AlmaLinux 10 pildiga). Lisa `verify.yml`, mis kontrollib, et fail `/var/www/ansible/index.html` on olemas ja sisaldab kooli nime. Käivita `molecule test`. Millised sammud (create, converge, idempotence, verify, destroy) läbiti? Miks ei saa konteineris nginx-i teenust tavapäraselt testida (teooria punkt 16.4)?
2. **Kasutajad:** lisa mänguraamatusse ülesanne, mis loob kõigisse serveritesse laboritöö 6 CSV-faili põhjal kasutajad (`ansible.builtin.read_csv` ja `ansible.builtin.user` koos `loop`-iga).
3. **Ansible + konteinerid:** kirjuta mänguraamat, mis paigaldab hallatavatele masinatele Podmani ja käivitab seal laboritöö 12 kooli saidi konteineri Quadleti abil.
4. **Laboritöö 13 automaatselt:** kirjuta mänguraamat, mis ehitab tühjast Debiani masinast laboritöö 13 veebiserveri (nginx, saidid, sertifikaat, MariaDB).

---

## Õpetajale: kontrollvastused

| Küsimus | Vastus |
|---|---|
| K2 | Esimene `changed>0`, teine `changed=0` |
| K3 | Mall täidetakse iga serveri faktidega (`ansible_hostname`, `ansible_distribution`) |
| K4 | Ansible taastas avalehe ja paigaldas `tree` uuesti (`changed`); triiv - serveri tegelik olek erineb kirjeldatust |
| K5 | Ülesanne „Saidi seadistus“ ebaõnnestub (`/etc/nginx/sites-available` puudub). Lahendus: AlmaLinuxis `conf.d` + `when`-tingimused; lisaks firewalld ja SELinux |
| K6 | `group_vars` väärtus (Haapsalu õppekool), sest `group_vars` on kõrgema prioriteediga kui rolli `defaults`; `-e` on kõige kõrgema prioriteediga, leht näitab „Test“ |
| K7 | Sõltub koodist; tavalised: `fqcn` (täielik moodulinimi), `name` (ülesande nimi), `yaml`, `risky-file-permissions` (puuduv `mode`). Puuduv `mode` võib päriselt jätta faili valede õigustega |
| K8 | Enne: teine käivitus `changed=1` (EI OLE IDEMPOTENTNE); pärast `creates:`-i `changed=0`. Ansible ei tea, mida käsk teeb, nii et `shell`/`command` on alati „changed“, kui ei kasuta `creates`/`removes` või `changed_when` |

> **Märkus õpetajale:** Ansible'i mänguraamatu ja mallide YAML/Jinja2 süntaks on testitud, käivitamist päris masinates mitte. Kui `ansible.builtin.package` ei leia Debianis paketti, käivita enne `apt update` (lisa ülesanne `ansible.builtin.apt: update_cache: true` koos `when`-iga).
