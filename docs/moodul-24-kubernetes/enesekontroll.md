# Moodul 24. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Milliseid probleeme lahendab konteinerite orkestreerimine võrreldes Quadleti või Compose'iga ühes masinas? Millal Kubernetest ei tasu kasutada?
2. Nimeta Kubernetese juhtkihi komponendid ja sõlme komponendid ning nende ülesanded.
3. Mida tähendab deklaratiivne haldus ja „soovitud olek“? Too näide.
4. Mis vahe on k3s-il, kubeadm-il ja minikube'il? Miks kasutatakse süsteemihalduse kursusel k3s-i?
5. Mis on pod ja miks ei käivitata rakendust tavaliselt otse podina, vaid Deploymentiga?
6. Mis on Service ja kuidas see teab, millistele podidele liiklust saata? Nimeta kolm teenuse tüüpi.
7. Mis vahe on `readinessProbe`-il ja `livenessProbe`-il?
8. Mis vahe on ressursside `requests` ja `limits` väärtustel? Mis juhtub, kui konteiner ületab mälupiirangu?
9. Kuidas toimub järkjärguline uuendus ja kuidas vigane uuendus tagasi võtta?
10. Mis vahe on ConfigMap'il ja Secret'il? Kas Secret on krüpteeritud?
11. Mis on Ingress ja Ingressi kontroller? Milline kontroller on k3s-is vaikimisi?
12. Mis on PVC ja StorageClass? Mis on `local-path` salvestuse puudus mitmesõlmelises klastris?
13. Mis on Helm, tabel (*chart*) ja väljalase (*release*)?
14. Kuidas viid sõlme hoolduseks klastrist välja ja tagasi? Mis juhtub podidega ootamatu sõlme rikke korral?
15. Miks on kõrge kättesaadavusega k3s-is kolm serverit, mitte kaks? Mis on GitOps?
16. Milliseid porte peab k3s klastri sõlmede vahel lubama ja milleks?

## Praktilised miniülesanded

1. Kirjuta käsud, mis näitavad kõigi nimeruumide podid koos sõlmedega ja viimased sündmused nimeruumis `kool`.
2. Kirjuta Deploymenti manifest `whoami` (pilt `docker.io/traefik/whoami`, 2 koopiat, port 80) ja sellele Service.
3. Deploymenti `kool` uus versioon ei käivitu. Kirjuta käsud, millega leiad põhjuse ja võtad uuenduse tagasi.
4. Kirjuta käsud, mis tühjendavad sõlme `k3s3` hoolduseks ja toovad selle pärast tagasi.

---

## Vastused

1. Mitme masina vahel ajastamine, konteinerite taaskäivitamine **teises masinas** sõlme rikke korral, skaleerimine, katkestuseta uuendused ja tagasivõtt, teenuste leidmine nime järgi, ühtne seadistuse ja saladuste haldus. Ei tasu, kui teenuseid ja servereid on vähe - Compose/Quadlet on lihtsam ja töökindlam ning Kubernetese hooldus nõuab aega ja oskusi.
2. Juhtkiht: kube-apiserver (ainus sissepääs, API), etcd (klastri olek), kube-scheduler (valib podile sõlme), kube-controller-manager (hoiab soovitud olekut). Sõlm: kubelet (käivitab konteinerid ja annab olekust teada), konteinerikäitur (containerd), kube-proxy (teenuste liikluse suunamine), CNI (podivõrk).
3. Kirjeldatakse lõpptulemust, mitte samme; kontrollerid võrdlevad pidevalt tegelikku olekut soovituga ja parandavad erinevused. Näide: Deployment `replicas: 3` - kui üks pod kustub, luuakse automaatselt uus.
4. kubeadm on ametlik tööriist „puhta“ Kubernetese paigaldamiseks komponent haaval (rohkem tööd); k3s on sertifitseeritud kerge distributsioon ühe binaarfailina koos vajalike lisadega ja paigaldub systemd teenusena tavalisse serverisse; minikube on ühe sõlme klaster arendaja arvutis. k3s-iga saab vähese ressursiga ehitada päris mitmesõlmelise klastri ja harjutada sõlmede lisamist, riket, hooldust ja varundust.
5. Pod on üks või mitu ühise võrgu ja kettaga konteinerit - väikseim käivitatav üksus. Pod on ajutine: kui see kustub või sõlm rikneb, ei looda seda ise uuesti. Deployment hoiab soovitud arvu koopiaid, loob kadunud podid uuesti ja haldab uuendusi.
6. Püsiv nimi ja IP-aadress podide hulgale; liiklus saadetakse kõigile valmis podidele, mille sildid vastavad teenuse `selector`-ile. Tüübid: ClusterIP (klastri sees), NodePort (iga sõlme pordil 30000–32767), LoadBalancer (väline aadress; k3s-is ServiceLB).
7. `readinessProbe` otsustab, kas pod saab liiklust (mittevalmis pod eemaldatakse teenusest); `livenessProbe` otsustab, kas konteiner on elus (ebaõnnestumisel taaskäivitatakse).
8. `requests` - garanteeritud osa, mille järgi ajastaja valib sõlme; `limits` - ülempiir (cgroup). Mälupiirangu ületamisel tapab kernel konteineri (`OOMKilled`) ja kubelet taaskäivitab selle.
9. Uued podid luuakse ükshaaval ja vanad eemaldatakse alles siis, kui uued on valmis, nii et teenus jätkub. Tagasi: `kubectl rollout undo deployment/<nimi>` (või eelmine manifest Gitist + `kubectl apply`).
10. ConfigMap - tavaline seadistus; Secret - saladused (paroolid, võtmed, sertifikaadid), mida saab eraldi õigustega kaitsta. Secret on vaikimisi ainult base64-kodeeritud, mitte krüpteeritud; krüpteerimine andmebaasis tuleb eraldi sisse lülitada ja Gitis kasutatakse Sealed Secrets'i, SOPS-i vms.
11. Ingress on reegel, mis suunab HTTP(S) päringu nime ja tee järgi teenusele; kontroller on pöördpuhver, mis reegleid täidab. k3s-is Traefik.
12. PVC on podi taotlus püsiketta järele (suurus, ligipääsuviis); StorageClass määrab, kuidas ja kust ketas luuakse. `local-path` hoiab andmeid ühe sõlme kohalikul kettal - pod on selle sõlmega seotud ja sõlme rikke korral pole andmed teistele kättesaadavad.
13. Helm on Kubernetese pakihaldur; tabel on pakett manifestide mallidest ja vaikeväärtustest; väljalase on tabeli konkreetne paigaldus klastris (oma nime, seadete ja revisjonidega).
14. `kubectl cordon <sõlm>`, `kubectl drain <sõlm> --ignore-daemonsets --delete-emptydir-data`, hooldus, `kubectl uncordon <sõlm>`. Ootamatul rikkel muutub sõlm `NotReady`-ks ja vaikimisi ~5 minuti pärast käivitatakse selle podid teistes sõlmedes (v.a podid, mis on seotud kohaliku kettaga).
15. etcd vajab otsuste tegemiseks häälteenamust: kolmest kaks on enamus, kahest üks ei ole - kahe serveriga klaster ei talu ühtegi riket paremini kui üks server. GitOps: klastri soovitud olek on Gitis ja kontroller (Argo CD, Flux) rakendab muudatused automaatselt.
16. 6443/tcp (API: agendid ja administraator → server), 8472/udp (Flannel VXLAN kõigi sõlmede vahel), 10250/tcp (kubelet), mitme serveri korral 2379–2380/tcp (etcd); klientidele 80/443 (Ingress). Hosti tulemüür peab lubama ka podi- ja teenusevõrgu (`10.42.0.0/16`, `10.43.0.0/16`).

### Miniülesannete lahendused

```bash
kubectl get pods -A -o wide
kubectl get events -n kool --sort-by=.lastTimestamp
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whoami
spec:
  replicas: 2
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
        - name: whoami
          image: docker.io/traefik/whoami
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: whoami
spec:
  selector:
    app: whoami
  ports:
    - port: 80
      targetPort: 80
```

```bash
kubectl rollout status deployment/kool -n kool
kubectl get pods -n kool
kubectl describe pod -n kool <uue-podi-nimi>      # sündmused: ImagePullBackOff, CrashLoopBackOff, OOMKilled…
kubectl logs -n kool <uue-podi-nimi> --previous   # kui konteiner käivitus ja kukkus
kubectl rollout undo deployment/kool -n kool
```

```bash
kubectl cordon k3s3
kubectl drain k3s3 --ignore-daemonsets --delete-emptydir-data
# … hooldus …
kubectl uncordon k3s3
```

<!-- navigatsioon -->
---

[← Laboritöö 24. k3s klaster](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 25. FreeBSD server →](../moodul-25-freebsd/index.md)
<!-- /navigatsioon -->
