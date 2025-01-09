# Projet JavaCard 2024

## Part 1: JavaCard applet development

## Part 2: Terminal application development

### Terminal application :
    - It should send the transaction data to our card
    - As well as the card information.
    - Transmit card information to the verification server.
  
   To send the APDU to a card, the application must firstly connect to a card via a smart card reader.
   (https://pyscard.sourceforge.io/user-guide.html#smart-cards)

   Package to install : 
   ```pip install pyscard```

The command APDU is a structure used to exchange data with a smart card.

We select the articles that we're interested in (the prices are indicated), then we save the amount of the price of the articles, and the amount will be transmitted with the date, time and card id.