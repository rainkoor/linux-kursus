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

## Praktilised miniülesanded

1. Kirjuta Ansible'i ülesanne, mis loob kasutaja `abi` (kest `/bin/bash`, lisagrupp `sudo`).
2. Kirjuta Ansible'i ad-hoc käsk, mis näitab kõigi serverite vaba kettaruumi juurfailisüsteemis.

---

## Vastused

1. Serverite ja infrastruktuuri seadistus kirjeldatakse tekstifailides (kood), mida hoitakse versioonihalduses, vaadatakse üle ja rakendatakse automaatselt.
2. **Inventuur** - hallatavate serverite loend; **moodul** - üks tegevus (nt `package`); **ülesanne** - mooduli kasutamine parameetritega; **mänguraamat** - ülesannete kogum serverigruppidele; **käsitleja** - ülesanne, mis käivitub ainult muudatuse korral.
3. Sama tegevuse korduv rakendamine annab alati sama tulemuse - kui olek on juba õige, ei muudeta midagi. Mänguraamatut võib turvaliselt korduvalt käivitada ja see parandab seadistuse triivi.
4. Vagrant loob virtuaalmasinaid tekstifaili (Vagrantfile) järgi; box on valmis põhitõmmis. Vagrant sobib arendus- ja laborikeskkonnaks oma arvutis (VirtualBox); Terraform/OpenTofu sobib püsiva infrastruktuuri (nt Proxmoxi, pilve) loomiseks ja haldamiseks.
5. Korduvkasutatav ülesannete komplekt kindlas kataloogistruktuuris: `tasks/`, `handlers/`, `templates/`, `files/`, `defaults/`, `vars/`, `meta/`. `defaults/` on madalaima prioriteediga vaikeväärtused; `group_vars/` (ja `host_vars/`) kirjutavad need keskkonna järgi üle.
6. `--syntax-check` → `ansible-lint` → `--check --diff` → kaks järjestikust käivitust (`changed=0`) → Molecule (ajutine masin, rakendus, korduvrakendus, kontroll, kustutamine). `idempotence` käivitab rolli teist korda ja ebaõnnestub, kui midagi muudeti.
7. OpenTofu loob masinad deklaratiivse koodi järgi (pakkuja kaudu, nt Proxmoxi API); cloud-init seadistab masina esimesel käivitusel (nimi, IP, kasutaja, SSH-võti), misjärel Ansible seadistab teenused. Olekufailis võivad olla saladused ja see muutub iga käivitusega; seda hoitakse turvalises jagatud salvestuses, mitte Gitis.

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

<!-- navigatsioon -->
---

[← Laboritöö 16. Ansible ja Vagrant](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 17. Seire ja jõudlus →](../moodul-17-seire/index.md)
<!-- /navigatsioon -->
