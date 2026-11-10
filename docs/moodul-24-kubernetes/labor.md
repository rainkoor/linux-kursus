<!-- navigatsioon -->
[← Moodul 24. Kubernetes: k3s](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 24. k3s klaster

| | |
|---|---|
| **Distro** | Debian 13 (kolm sõlme: `k3s1`, `k3s2`, `k3s3`) |
| **Kestus** | 4 × 90 minutit |
| **Vajalik** | Kolm Debiani VM-i (igaüks 2 vCPU, 2 GiB RAM, 20 GiB ketas; `k3s1`-le soovitatavalt 3 GiB). Kõige kiiremini saab need cloud-init mallist (moodul 23) või OpenTofuga (moodul 16). Laboritöö 13 labori CA (`debian1`, `/root/ca`). Ubuntu klient (`ubuntuklient`) |
| **Eesmärk** | Ehitada mitmesõlmeline Kubernetese klaster, käivitada sellel rakendus koos TLS-i ja püsiandmetega ning harjutada uuendamist ja hooldust |

**Aruanne:** vasta küsimustele **K1–K14**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

Tähised: `kasutaja` - sinu kasutajanimi. IP-aadressid on paigalduslisa plaanist (`10.0.83.61`–`63`); asenda `83` oma võrgu numbriga.

---

## 0. osa. Ettevalmistus

**0.1** Loo kolm masinat ja anna neile nimed ning staatilised aadressid:

| Masin | IP |
|---|---|
| `k3s1` | `10.0.83.61` |
| `k3s2` | `10.0.83.62` |
| `k3s3` | `10.0.83.63` |

**0.2** Lisa kõigi kolme masina ja Ubuntu kliendi faili `/etc/hosts`:

```text
10.0.83.61 k3s1.lab.example k3s1 kool.k8s.lab.example
10.0.83.62 k3s2.lab.example k3s2
10.0.83.63 k3s3.lab.example k3s3
```

**0.3** Igas sõlmes:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y curl
hostnamectl
timedatectl                     # kell peab olema sünkroonis (sertifikaadid!)
```

Tee kõigist masinatest **hetktõmmis** „enne k3s-i“.

---

## 1. osa. Server

**1.1** `k3s1`-s loo seadistusfail ja paigalda k3s (teooria punkt 24.4):

```bash
sudo mkdir -p /etc/rancher/k3s
sudo tee /etc/rancher/k3s/config.yaml <<'EOF'
node-ip: 10.0.83.61
tls-san:
  - k3s1.lab.example
write-kubeconfig-mode: "0600"
EOF
curl -sfL https://get.k3s.io -o k3s-install.sh
less k3s-install.sh
sudo INSTALL_K3S_CHANNEL=stable sh k3s-install.sh
```

**1.2** Kontrolli teenust ja seadista `kubectl` tavakasutajale:

```bash
systemctl status k3s
sudo ss -tlnp | grep -E '6443|10250'
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER: ~/.kube/config && chmod 600 ~/.kube/config
echo 'export KUBECONFIG=~/.kube/config' >> ~/.bashrc && source ~/.bashrc
kubectl version
kubectl get nodes -o wide
kubectl get pods -A
```

**K1.** Milline Kubernetese versioon paigaldati? Milliseid pode on nimeruumis `kube-system` ja mis on igaühe ülesanne (teooria punkt 24.4)? Milline protsess kuulab pordil 6443?

---

## 2. osa. Agendid

**2.1** `k3s1`-s vaata liitumisluba:

```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

**2.2** `k3s2`-s ja `k3s3`-s (asenda IP `node-ip` real vastavalt masinale):

```bash
sudo mkdir -p /etc/rancher/k3s
echo "node-ip: 10.0.83.62" | sudo tee /etc/rancher/k3s/config.yaml
curl -sfL https://get.k3s.io -o k3s-install.sh
sudo K3S_URL=https://10.0.83.61:6443 K3S_TOKEN='<token>' INSTALL_K3S_CHANNEL=stable sh k3s-install.sh
systemctl status k3s-agent
```

**2.3** `k3s1`-s:

```bash
kubectl get nodes -o wide
kubectl describe node k3s2 | grep -A6 -E "Capacity|Allocatable"
```

**K2.** Milline on iga sõlme roll (`ROLES`), sisemine IP ja konteinerikäitur (`CONTAINER-RUNTIME`)? Kui palju mälu ja protsessorit on sõlmel `k3s2` podide jaoks saadaval (`Allocatable`)? Miks on agendi liitumisluba saladus?

---

## 3. osa. Esimene rakendus

**3.1** Loo kataloog `~/k8s` ja sinna teooria punkti 24.5 manifest `kool.yaml` (Namespace, Deployment 3 koopiaga, Service). Rakenda:

```bash
mkdir -p ~/k8s && cd ~/k8s
kubectl apply -f kool.yaml
kubectl get all -n kool
kubectl get pods -n kool -o wide
```

**K3.** Millistes sõlmedes podid töötavad? Milline IP-aadress on igal podil ja milline teenusel `kool`? Millisest võrgust need aadressid on (teooria punkt 24.4)?

**3.2** Testi teenust klastri seest ajutise podiga:

```bash
kubectl run test -n kool --rm -it --image=docker.io/library/busybox:1.37 -- \
    wget -qO- http://kool.kool.svc.cluster.local | head -5
```

**3.3** Isetervenemine: kustuta üks pod ja jälgi teises terminalis:

```bash
kubectl get pods -n kool -w                       # teine terminal
kubectl delete pod -n kool <ühe-podi-nimi>
kubectl get events -n kool --sort-by=.lastTimestamp | tail -10
```

**K4.** Mis juhtus pärast podi kustutamist ja kui kiiresti? Milline Kubernetese komponent selle tegi ja miks (soovitud ja tegelik olek)?

---

## 4. osa. Skaleerimine, uuendus ja tagasivõtt

**4.1**

```bash
kubectl scale deployment kool -n kool --replicas=5
kubectl get pods -n kool -o wide
kubectl set image deployment/kool veeb=docker.io/library/nginx:1.28-alpine -n kool
kubectl rollout status deployment/kool -n kool
kubectl rollout history deployment/kool -n kool
kubectl describe deployment kool -n kool | grep Image
```

**4.2** Tee vigane uuendus olematu pildisildiga:

```bash
kubectl set image deployment/kool veeb=docker.io/library/nginx:9.99 -n kool
kubectl rollout status deployment/kool -n kool --timeout=60s
kubectl get pods -n kool
kubectl describe pod -n kool <uue-podi-nimi> | tail -15
```

Kontrolli, kas teenus vastab endiselt (punkt 3.2). Seejärel:

```bash
kubectl rollout undo deployment/kool -n kool
kubectl rollout status deployment/kool -n kool
```

**K5.** Mitu podi töötas vigase uuenduse ajal ja milline oli uue podi olek (`STATUS`) ning sündmus `describe` väljundis? Kas teenus katkes? Miks?

**4.3** Muuda failis `kool.yaml` koopiate arvuks 3 ja pildiks `nginx:1.28-alpine` ning tee `kubectl apply -f kool.yaml`.

**K6.** Miks tuleb muudatus lõpuks teha manifesti, kui sama tulemuse saab ka käsuga `kubectl scale` või `set image`?

---

## 5. osa. ConfigMap ja Secret

**5.1** Lisa faili `kool.yaml` teooria punkti 24.7 ConfigMap `kool-leht` (oma kooli nimega) ja haagi see Deploymentis kataloogi `/usr/share/nginx/html`. Rakenda ja kontrolli punkti 3.2 käsuga.

**5.2** Muuda ConfigMap'is lehe sisu, rakenda ja kontrolli mõne aja pärast uuesti (ilma podisid taaskäivitamata). Seejärel:

```bash
kubectl rollout restart deployment/kool -n kool
```

**5.3** Loo Secret ja vaata, kuidas see on salvestatud:

```bash
kubectl create secret generic db-parool -n kool --from-literal=parool='Väga-salajane-1'
kubectl get secret db-parool -n kool -o yaml
kubectl get secret db-parool -n kool -o jsonpath='{.data.parool}' | base64 -d; echo
```

**K7.** Kas lehe muudatus jõudis podidesse ilma taaskäivituseta (vihje: kulub kuni minut)? Milleks on `rollout restart`? Mida näitas Secret'i YAML ja miks ei tohi Secret'i manifesti Giti panna?

---

## 6. osa. Ingress ja TLS

**6.1** Loo `debian1`-s labori CA-ga sertifikaat nimele `kool.k8s.lab.example` (moodul 13):

```bash
sudo -i
cd /root/ca
openssl req -newkey rsa:2048 -nodes -keyout k8s.key -out k8s.csr -subj "/CN=kool.k8s.lab.example"
openssl x509 -req -in k8s.csr -CA labori-ca.crt -CAkey labori-ca.key -CAcreateserial \
    -out k8s.crt -days 365 -sha256 -extfile <(printf "subjectAltName=DNS:kool.k8s.lab.example")
openssl verify -CAfile labori-ca.crt k8s.crt
exit
```

Kopeeri `k8s.crt` ja `k8s.key` turvaliselt (`scp`) `k3s1`-sse ja kustuta seal võtmefail pärast Secret'i loomist.

**6.2** `k3s1`-s:

```bash
kubectl create secret tls kool-tls -n kool --cert=k8s.crt --key=k8s.key
shred -u k8s.key
```

Loo teooria punkti 24.8 Ingress failina `ingress.yaml` ja rakenda see.

**6.3** Ubuntu kliendis (labori CA on usaldatud laboritööst 13):

```bash
curl -I http://kool.k8s.lab.example
curl https://kool.k8s.lab.example
curl --resolve kool.k8s.lab.example:443:10.0.83.63 https://kool.k8s.lab.example
```

**K8.** Kas HTTPS töötas ilma hoiatuseta? Viimane käsk saatis päringu sõlmele `k3s3` - kas vastus tuli, isegi kui sellel sõlmel ei pruugi `kool` podi olla? Miks? Milline komponent päringu vastu võttis?

**6.4** Sõlme rike: vaata, millistes sõlmedes `kool` podid on, ja **lülita `k3s3` VM välja** (Proxmoxis *Shutdown*). Jälgi `k3s1`-s:

```bash
kubectl get nodes -w
kubectl get pods -n kool -o wide -w
```

Oota vähemalt 6 minutit, seejärel käivita `k3s3` uuesti.

**K9.** Kui kiiresti muutus `k3s3` olekuks `NotReady`? Millal käivitati selle podid teistes sõlmedes ja miks just siis? Kas veebileht vastas kogu aja jooksul aadressil `kool.k8s.lab.example` (kliendi `hosts` failis on `k3s1`)? Mis oleks juhtunud, kui välja oleks lülitatud `k3s1`?

---

## 7. osa. Püsiandmed

**7.1** Loo fail `andmed.yaml`: teooria punkti 24.9 PVC `andmed` ja Deployment `kirjutaja`, mis kirjutab iga 10 sekundi järel kellaaja püsikettale:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kirjutaja
  namespace: kool
spec:
  replicas: 1
  strategy:
    type: Recreate                # ReadWriteOnce ketas: vana pod enne uut maha
  selector:
    matchLabels:
      app: kirjutaja
  template:
    metadata:
      labels:
        app: kirjutaja
    spec:
      containers:
        - name: kirjutaja
          image: docker.io/library/busybox:1.37
          command: ["sh", "-c", "while true; do date >> /andmed/aeg.txt; sleep 10; done"]
          volumeMounts:
            - name: andmed
              mountPath: /andmed
      volumes:
        - name: andmed
          persistentVolumeClaim:
            claimName: andmed
```

```bash
kubectl apply -f andmed.yaml
kubectl get pvc,pv -n kool
kubectl get pods -n kool -l app=kirjutaja -o wide
```

**7.2** Oota minut, kustuta pod ja kontrolli, kas andmed säilisid:

```bash
kubectl exec -n kool deploy/kirjutaja -- wc -l /andmed/aeg.txt
kubectl delete pod -n kool -l app=kirjutaja
kubectl exec -n kool deploy/kirjutaja -- head -3 /andmed/aeg.txt
```

Leia andmed sõlmest, kus pod töötab: `sudo ls -R /var/lib/rancher/k3s/storage/`.

**K10.** Mis olekus oli PVC enne Deploymenti loomist ja pärast (vihje: `WaitForFirstConsumer`)? Kas andmed säilisid podi kustutamisel? Millises sõlmes ja kataloogis andmed asuvad ning mis juhtub selle sõlme rikke korral?

---

## 8. osa. Helm

**8.1** Paigalda `k3s1`-sse Helm (teooria punkt 24.10) ja podinfo:

```bash
helm repo add podinfo https://stefanprodan.github.io/podinfo
helm repo update
helm show values podinfo/podinfo | head -30
helm install demo podinfo/podinfo -n demo --create-namespace
kubectl get all -n demo
kubectl port-forward -n demo svc/demo-podinfo 9898:9898 &
curl -s http://localhost:9898 | head
kill %1
```

**8.2** Uuenda ja võta tagasi:

```bash
helm upgrade demo podinfo/podinfo -n demo --set replicaCount=3
kubectl get pods -n demo
helm history demo -n demo
helm rollback demo 1 -n demo
kubectl get pods -n demo
helm list -A
```

**K11.** Mitu Kubernetese objekti lõi üks `helm install` (`kubectl get all -n demo`)? Mis muutus pärast `upgrade` ja `rollback` käske? Kuidas hoiaksid Helmi paigalduse seadeid korratavana?

---

## 9. osa. Hooldus ja varundus

**9.1** Tühjenda sõlm hoolduseks:

```bash
kubectl cordon k3s2
kubectl drain k3s2 --ignore-daemonsets --delete-emptydir-data
kubectl get pods -A -o wide | grep k3s2
kubectl get nodes
```

Tee `k3s2`-s `sudo apt full-upgrade -y && sudo reboot`, seejärel `k3s1`-s `kubectl uncordon k3s2`.

**9.2** Ressursikasutus:

```bash
kubectl top nodes
kubectl top pods -A --sort-by=memory | head
```

**9.3** Varunda klastri olek `k3s1`-s:

```bash
sudo systemctl stop k3s
kubectl get pods -n kool 2>&1 | head -2         # API ei vasta
sudo crictl ps | head -5                        # konteinerid töötavad edasi?
sudo tar -czf /root/k3s-varu-$(date +%F).tar.gz \
    /var/lib/rancher/k3s/server/db /var/lib/rancher/k3s/server/token
sudo systemctl start k3s
ls -lh /root/k3s-varu-*.tar.gz
```

**K12.** Millised podid jäid `k3s2`-sse pärast `drain`-i ja miks (vihje: DaemonSet)? Kas veebileht vastas `k3s1` teenuse peatamise ajal? Mis on sinu varukoopias ja mida see **ei** sisalda?

**9.4** Kanna kõik manifestid (`~/k8s`) Git-hoidlasse (moodul 6). **Ära lisa** `k8s.key`, `kubeconfig`-faile ega Secret'ide väärtusi.

---

## 10. osa. Kokkuvõte

**K13.** Võrdle laboritöö 12 (Podman, Compose, Quadlet) ja selle laboritöö lahendust: mida Kubernetes juurde andis ja mis läks keerulisemaks? Millises olukorras soovitaksid kooli serverile Quadletti ja millises Kubernetest?

**K14.** Joonista (ASCII või Mermaid) oma klastri skeem: sõlmed ja IP-d, Traefik, teenus `kool`, podid, PVC ja klient. Märgi joonisele kõik üksikud rikkepunktid ja kirjuta iga juurde, kuidas selle kõrvaldaksid.

---

## Koristamine

Kui klastrit enam ei vaja: `sudo /usr/local/bin/k3s-agent-uninstall.sh` agentides ja `sudo /usr/local/bin/k3s-uninstall.sh` serveris - või taasta hetktõmmis „enne k3s-i“. Lülita masinad välja, kui sa nendega ei tööta.

---

## Lisaülesanne (valikuline)

1. **Kõrge kättesaadavus:** ehita kolmest serverist koosnev klaster sisseehitatud etcd-ga (teooria punkt 24.11; `cluster-init`) ja virtuaalse IP-ga `10.0.83.64` (keepalived, moodul 13). Lülita üks server välja: kas `kubectl` töötab edasi? Lülita teine välja: mis juhtub ja miks? Tee `sudo k3s etcd-snapshot save` ja leia tõmmis.
2. **GitOps Argo CD-ga:** paigalda Argo CD (`kubectl create namespace argocd` ja `kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`), loo Argo CD rakendus, mis jälgib sinu Git-hoidla kataloogi `k8s/`, ja muuda Gitis koopiate arvu. Kui kiiresti muudatus klastrisse jõudis? Mis juhtub, kui muudad koopiate arvu `kubectl scale`-iga?
3. **Seire:** paigalda Helmiga `kube-prometheus-stack` (hoidla `https://prometheus-community.github.io/helm-charts`) ja ava Grafana `kubectl port-forward`-iga. Leia töölaud, mis näitab podide mälukasutust nimeruumide kaupa.
4. **AlmaLinuxi sõlm:** lisa klastrisse agendiks AlmaLinuxi masin (SELinux `enforcing`, firewalld). Mida paigaldusskript lisaks paigaldas (`rpm -qa | grep -i selinux`)? Milliseid tulemüürireegleid oli vaja?
5. **minikube või kind oma arvutis:** paigalda oma arvutisse (või WSL-i) minikube ja käivita seal sama `kool.yaml`. Mis on teisiti (sõlmede arv, Ingress, salvestus)?
6. **Võrgupoliitika:** k3s sisaldab võrgupoliitikate kontrollerit. Kirjuta `NetworkPolicy`, mis lubab nimeruumi `kool` podidele liiklust ainult Traefikilt (nimeruum `kube-system`), ja kontrolli punkti 3.2 testiga teisest nimeruumist.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Milline Kubernetese versioon paigaldati? Milliseid pode on nimeruumis `kube-system` ja mis on igaühe ülesanne (teooria punkt 24.4)? Milline protsess kuulab pordil 6443?
- **K2.** *(punkt 2.3)* Milline on iga sõlme roll (`ROLES`), sisemine IP ja konteinerikäitur (`CONTAINER-RUNTIME`)? Kui palju mälu ja protsessorit on sõlmel `k3s2` podide jaoks saadaval (`Allocatable`)? Miks on agendi liitumisluba saladus?
- **K3.** *(punkt 3.1)* Millistes sõlmedes podid töötavad? Milline IP-aadress on igal podil ja milline teenusel `kool`? Millisest võrgust need aadressid on (teooria punkt 24.4)?
- **K4.** *(punkt 3.3)* Mis juhtus pärast podi kustutamist ja kui kiiresti? Milline Kubernetese komponent selle tegi ja miks (soovitud ja tegelik olek)?
- **K5.** *(punkt 4.2)* Mitu podi töötas vigase uuenduse ajal ja milline oli uue podi olek (`STATUS`) ning sündmus `describe` väljundis? Kas teenus katkes? Miks?
- **K6.** *(punkt 4.3)* Miks tuleb muudatus lõpuks teha manifesti, kui sama tulemuse saab ka käsuga `kubectl scale` või `set image`?
- **K7.** *(punkt 5.3)* Kas lehe muudatus jõudis podidesse ilma taaskäivituseta (vihje: kulub kuni minut)? Milleks on `rollout restart`? Mida näitas Secret'i YAML ja miks ei tohi Secret'i manifesti Giti panna?
- **K8.** *(punkt 6.3)* Kas HTTPS töötas ilma hoiatuseta? Viimane käsk saatis päringu sõlmele `k3s3` - kas vastus tuli, isegi kui sellel sõlmel ei pruugi `kool` podi olla? Miks? Milline komponent päringu vastu võttis?
- **K9.** *(punkt 6.4)* Kui kiiresti muutus `k3s3` olekuks `NotReady`? Millal käivitati selle podid teistes sõlmedes ja miks just siis? Kas veebileht vastas kogu aja jooksul aadressil `kool.k8s.lab.example` (kliendi `hosts` failis on `k3s1`)? Mis oleks juhtunud, kui välja oleks lülitatud `k3s1`?
- **K10.** *(punkt 7.2)* Mis olekus oli PVC enne Deploymenti loomist ja pärast (vihje: `WaitForFirstConsumer`)? Kas andmed säilisid podi kustutamisel? Millises sõlmes ja kataloogis andmed asuvad ning mis juhtub selle sõlme rikke korral?
- **K11.** *(punkt 8.2)* Mitu Kubernetese objekti lõi üks `helm install` (`kubectl get all -n demo`)? Mis muutus pärast `upgrade` ja `rollback` käske? Kuidas hoiaksid Helmi paigalduse seadeid korratavana?
- **K12.** *(punkt 9.3)* Millised podid jäid `k3s2`-sse pärast `drain`-i ja miks (vihje: DaemonSet)? Kas veebileht vastas `k3s1` teenuse peatamise ajal? Mis on sinu varukoopias ja mida see **ei** sisalda?
- **K13.** *(10. osa)* Võrdle laboritöö 12 (Podman, Compose, Quadlet) ja selle laboritöö lahendust: mida Kubernetes juurde andis ja mis läks keerulisemaks? Millises olukorras soovitaksid kooli serverile Quadletti ja millises Kubernetest?
- **K14.** *(10. osa)* Joonista (ASCII või Mermaid) oma klastri skeem: sõlmed ja IP-d, Traefik, teenus `kool`, podid, PVC ja klient. Märgi joonisele kõik üksikud rikkepunktid ja kirjuta iga juurde, kuidas selle kõrvaldaksid.
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 24. Kubernetes: k3s](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
