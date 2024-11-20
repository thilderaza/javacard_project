# Projet JavaCard 2024

## Partie 1 : Développment de l'applet JavaCard

## Partie 2 : Développment de l'application terminal

### Application de terminal :
    - Elle devra envoyer des données de transaction vers notre carte
    - Ainsi que les informations de la carte.
    - Transmettre les informations de la carte vers notre serveur de vérification.
  
   Pour envoyer des APDU à une carte, l'application doit d'abord se connecter à une carte via un lecteur de carte à puce. (https://pyscard.sourceforge.io/user-guide.html#smart-cards)

   Package à installer : 
   ```pip install pyscard```

La commande APDU est une structure utilisée pour échanger des données avec une carte à puce.

On choisit les articles qui nous intéresses (les prix sont indiqués), pusi on sauvegarde le total des articles, et le total sera transmis avec la date, l'heure et l'id de la carte.