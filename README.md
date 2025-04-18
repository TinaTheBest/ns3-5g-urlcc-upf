# ns3-5g-urlcc-upf

#  NS-3.43 - Simulation de l’emplacement et du nombre optimal de UPFs dans un réseau 5G URLLC

Ce projet utilise **NS-3.43** pour simuler un scénario de communication **5G URLLC (Ultra-Reliable Low-Latency Communication)** avec plusieurs **UPFs (User Plane Functions)**.  
L’objectif est de déterminer **l’emplacement optimal** et le **nombre minimal de UPFs** dans un réseau 5G pour garantir **une latence minimale** et **une fiabilité maximale**.

---

##  Environnement de travail

- Système : WSL (Ubuntu sous Windows) ou Linux natif
- NS-3 version : 3.43
- Python : avec environnement virtuel (`venv`)

---

##  Prérequis

### Installer les paquets système nécessaires

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git g++ make
sudo apt install python-is-python3
```

---

##  Étapes d’installation

### 1. Aller dans le dossier NS-3

```bash
cd ~/ns-allinone-3.43/ns-3.43/
```

### 5. Compiler NS-3

```bash
cd ~/ns-allinone-3.43/ns-3.43/
./ns3 configure --enable-examples --enable-tests --enable-python-bindings
./ns3 build
```

---

## Lancer la simulation
---

### Créer et activer l’environnement virtuel Python

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Cloner le projet dans le dossier `scratch`

```bash
cd scratch
git clone https://github.com/<ton-nom-utilisateur>/ns3-5g-urlcc-upf.git
cd ns3-5g-urlcc-upf/
python main.py
```

---

##  Objectif du projet

- Simuler différents **emplacements de UPFs** dans un réseau 5G URLLC
- Tester **plusieurs topologies** et scénarios pour identifier :
  - le **nombre optimal de UPFs**
  - l'**emplacement stratégique** pour minimiser la latence et maximiser la fiabilite

---

## 📚 Ressources utiles

- [Documentation NS-3 et Python]([https://www.nsnam.org/documentation/](https://www.nsnam.org/docs/manual/html/python.html))



