<!-- navigatsioon -->
[← Laboritöö 16. Ansible ja Vagrant](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 17. Seire ja jõudlus →](../moodul-17-seire/index.md)
<!-- /navigatsioon -->

# Moodul 16. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis on infrastruktuur koodina (IaC)?
2. Mis on Ansible'i inventuur, moodul, ülesanne, mänguraamat ja käsitleja?
3. Mida tähendab idempotentsus? Miks on see oluline?
4. Mis on Vagrant, box ja Vagrantfile? Millal kasutada Vagranti ja millal Terraformi/OpenTofut?
5. Mis on Ansible'i roll ja millistest kataloogidest see koosneb? Mis vahe on rolli `defaults/main.yml` ja `group_vars/` muutujatel?
6. Nimeta Ansible'i koodi testimise tasemed alates süntaksikontrollist kuni Molecule'ini. Mida kontrollib Molecule'i samm `idempotence`?
7. Mis on cloud-init ja OpenTofu roll virtuaalmasinate loomisel? Miks ei panda olekufaili `terraform.tfstate` Giti?
8. Millal on Bashi skript koos systemd taimeriga parem valik kui Ansible ja millal vastupidi?
9. Miks on Ansible'is parem kasutada moodulit (nt `ansible.builtin.lineinfile`, `template`) kui `shell`- või `command`-moodulit?
10. Kuidas teeb üks mänguraamat sama tööd Debianis ja AlmaLinuxis, kuigi paketi nimi ja pakihaldur erinevad?
11. Mis on Ansible Vault ja kuidas hoiad paroole Gitis turvaliselt?
12. Mida näitab `ansible-playbook --check --diff` ja miks tasub seda enne päris käivitust kasutada?

## Praktilised miniülesanded

1. Kirjuta Ansible'i ülesanne, mis loob kasutaja `abi` (kest `/bin/bash`, lisagrupp `sudo`).
2. Kirjuta Ansible'i ad-hoc käsk, mis näitab kõigi serverite vaba kettaruumi juurfailisüsteemis.
3. Kirjuta ülesanne, mis loob mallist `motd.j2` faili `/etc/motd`, ja käsitleja, mis taaskäivitab `nginx`-i ainult siis, kui mallist loodud fail `/etc/nginx/conf.d/kool.conf` muutus.
4. Kirjuta kaks ülesannet, mis paigaldavad veebiserveri nii Debiani (`apache2`) kui ka AlmaLinuxi (`httpd`) masinatesse.

---

## Vastused

1. Serverite ja infrastruktuuri seadistus kirjeldatakse tekstifailides (kood), mida hoitakse versioonihalduses, vaadatakse üle ja rakendatakse automaatselt.
2. **Inventuur** - hallatavate serverite loend; **moodul** - üks tegevus (nt `package`); **ülesanne** - mooduli kasutamine parameetritega; **mänguraamat** - ülesannete kogum serverigruppidele; **käsitleja** - ülesanne, mis käivitub ainult muudatuse korral.
3. Sama tegevuse korduv rakendamine annab alati sama tulemuse - kui olek on juba õige, ei muudeta midagi. Mänguraamatut võib turvaliselt korduvalt käivitada ja see parandab seadistuse triivi.
4. Vagrant loob virtuaalmasinaid tekstifaili (Vagrantfile) järgi; box on valmis põhitõmmis. Vagrant sobib arendus- ja laborikeskkonnaks oma arvutis (VirtualBox); Terraform/OpenTofu sobib püsiva infrastruktuuri (nt Proxmoxi, pilve) loomiseks ja haldamiseks.
5. Korduvkasutatav ülesannete komplekt kindlas kataloogistruktuuris: `tasks/`, `handlers/`, `templates/`, `files/`, `defaults/`, `vars/`, `meta/`. `defaults/` on madalaima prioriteediga vaikeväärtused; `group_vars/` (ja `host_vars/`) kirjutavad need keskkonna järgi üle.
6. `--syntax-check` → `ansible-lint` → `--check --diff` → kaks järjestikust käivitust (`changed=0`) → Molecule (ajutine masin, rakendus, korduvrakendus, kontroll, kustutamine). `idempotence` käivitab rolli teist korda ja ebaõnnestub, kui midagi muudeti.
7. OpenTofu loob masinad deklaratiivse koodi järgi (pakkuja kaudu, nt Proxmoxi API); cloud-init seadistab masina esimesel käivitusel (nimi, IP, kasutaja, SSH-võti), misjärel Ansible seadistab teenused. Olekufailis võivad olla saladused ja see muutub iga käivitusega; seda hoitakse turvalises jagatud salvestuses, mitte Gitis.
8. Skript ja taimer sobivad ühe masina lihtsaks korduvaks tööks (varundus, koristamine), kus pole vaja mitut masinat ühesuguseks hoida. Ansible on parem, kui servereid on mitu, seadistus peab olema kõigis sama, korduval käivitamisel ei tohi midagi katki minna (idempotentsus) ja kogu serveri olek peab olema koodina kirjeldatud.
9. Moodul on idempotentne ja teab olekut: muudab ainult siis, kui vaja, ja annab õige `changed`/`ok` tulemuse, mis käivitab käsitlejaid õigesti. `shell` käivitab käsu iga kord ja Ansible ei tea, kas midagi muutus; korduvkäivitus võib anda erineva tulemuse.
10. Tingimustega (`when: ansible_os_family == "Debian"` / `"RedHat"`) või muutujatega, mille väärtus sõltub distrost (nt `group_vars/` või `vars/Debian.yml`); osa mooduleid (`package`, `service`) töötab mõlemas ühtemoodi.
11. Ansible Vault krüpteerib muutujafailid (`ansible-vault create`/`encrypt`); Gitis on krüpteeritud fail ja parool antakse käivitamisel (`--ask-vault-pass`) või parooli failist, mis ei ole Gitis.
12. Kuivkäivitus: näitab, mida muudetaks (`changed`) ja failide muudatuste erinevust, ilma midagi muutmata. Nii näed enne päris käivitust, kas mänguraamat teeb seda, mida ootad.

### Miniülesannete lahendused

```yaml
- name: Loo kasutaja abi
  ansible.builtin.user:
    name: abi
    shell: /bin/bash
    groups: sudo
    append: true
```

```bash
ansible all -a "df -h /"
```

```yaml
# tasks
- name: Teadaanne sisselogimisel
  ansible.builtin.template:
    src: motd.j2
    dest: /etc/motd
    mode: "0644"

- name: Kooli saidi seadistus
  ansible.builtin.template:
    src: kool.conf.j2
    dest: /etc/nginx/conf.d/kool.conf
  notify: Taaskäivita nginx

# handlers
- name: Taaskäivita nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
```

```yaml
- name: Paigalda Apache (Debian)
  ansible.builtin.apt:
    name: apache2
    update_cache: true
  when: ansible_os_family == "Debian"

- name: Paigalda Apache (AlmaLinux)
  ansible.builtin.dnf:
    name: httpd
  when: ansible_os_family == "RedHat"
```

<!-- navigatsioon -->
---

[← Laboritöö 16. Ansible ja Vagrant](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 17. Seire ja jõudlus →](../moodul-17-seire/index.md)
<!-- /navigatsioon -->
