# Projet JavaCard 2024

A installer pour faire fonctionner la carte : 
```sudo apt-get install libusb-dev libusb++-0.1-4c2 libusb-1.0-0-dev libccid pcscd libpcsclite1 libpcsclite-dev libpcsc-perl pcsc-tools```

Dépendance python : 
```pip install cryptography pyscard flask requests```

Scan pour trouver la carte JavaCard : 
```pcsc_scan ```

Lancer le serveur : 
```python server.py```

Lancer l'application : 
```python main.py```
