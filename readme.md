TP Electromob
=======================

Présentation
------------

Ce TP a été réalisé dans le cadre d’une UV projet à l’IMT Nord Europe. Il consitre à programmer les mouvements du robot pour recréer une ligne de production de batterie

Les cellules arrive sur le convoyeur et viennent se heurter à la barrière, puis le robot viens recuperer cette cellule et la place dans l'emplacement d'injection. Il prend l'outil d'injection et mime l'injection d'electrolyte dans la cellule. Puis le robot viens placer la cellule dans la boites qui fait office de batterie.

Installation
------------

Pour ce TP, il vous est fourni:

-Le materiel à installer
-Les codes pour les cartes EPS32
-Le code pour la connectivité entre le PC et les ESP32
-Un template pour les TPs

Un video du resultat et de l'installation sont disponibles.


TP1
---
Dans cette première partie, vous allez manipuler le robot et coder ses déplacements pour récupérer la cellule depuis le convoyeur, simuler l’injection de l’électrolyte puis la déposer dans la boîte. 

Ouvrez le fichier BatteryBoxConnection_EN_BLANK_TP1.

Votre objectif est de réaliser les fonctions suivantes:
•”get_cell_conv() “ 
qui récupère la cellule du convoyeur et la dépose sur le support d’injection
•”inject()” 
qui simule le processus d’injection de l'électrolyte dans la cellule
•”place_into_box(n)”
qui déplace la cellule du support d’injection jusqu’à la n-ième position dans la boîte

Pour cela, il faut d’abord effectuer la tâche manuellement, en relevant à chaque étape la position du robot (“Visualiser”, “Position actuelle”, “Cartésien”). Ensuite, utiliser ces positions ainsi que les fonctions détaillées dans l’annexe pour compléter les trois fonctions.


TP2
---
Nous allons ensuite complexifier le problème en ajoutant des contraintes. 

Ouvrir le fichier BatteryBoxConnection_EN_BLANK_TP2.

On décide d’automatiser le processus de détection de la cellule par le robot, qui lance alors votre script pour déplacer la cellule jusqu’à la boîte. Arrivé à celle-ci, on souhaite que la boite transmette les informations relatives aux emplacements disponibles à l’ordinateur, et que votre script soit adapté pour déposer la cellule dans un emplacement libre.
Pour cela, on va utiliser des cartes ESP32.


Pour cela on créer une boucle d'action qu'il faut completer.
Des instructions indiquant une possible solution sont donnée en commentaire du programme.


Connexion PC2ESP32
------------------

On retrouve dans le GITHUB. le code des ESP32 pour la boite et la table.

La boite correspond à la batterie qui contient les 5 emplacements de cellules.
La table correspond au controle de la porte et l'emplacement pour l'injection.

Ces codes peuvent être televerser via l'Arduino IDE, avec l'ajout de l'extension pour carte EPS32 :

Ces codes dialoguent avec le port Serie d'un PC lorsqu'il est disponible. Fournissant ainsi leur adresse IP lors de la connexion à un réseau, ainsi que d'autres informations pratiques.

Le script de dialogue est pc2esp32.py
Les fonctions sont :

    -pin_value=get_pin_try(pin:int,s:socket.socket,nb_try:int,pr=True): 
        permet de demander l’état du capteur “i” relié au ESP32 connecté par le socket “s”

    -s=begin_one_connection(TCP_IP,TCP_PORT): 
        permet de se connecter à l’ESP32 d’adresse IP “IP” et au port “PORT”. Renvoie le socket de connection “s” 

    -end_one_connection(s:socket.socket): 
        met fin à la connection de socket “s”

    -open_gate_try(s:socket.socket,nb_try:int) : 
        demande à ouvrir la porte

    -close_gate_try(s:socket.socket,nb_try:int)
        demande à fermer la porte

Démarche pour l'adresse IP :
    -Créer un hotspot WiFi à l'aide d'un portable ou d'un PC.
    -Modifier les codes pour les ESP32 en notant le SSID et le MDP du réseau WiFi.
    -Connecter les ESP32s au PC et televerse ce programme.
    -Ouvre le "Serial Monitor" qui permet de lire les messages envoyer par l'ESP32
    -Recuper l'adresse IP obtenu lors de la connexion.
    -Noter cette adresse IP dans le code python du TP
    
Si le PC et l'ESP32 sont connecté au même réseau WiFi avec les bon paramètres de connexion, vous devriez être capable de recuperer des informations.

Cette connexion est néanmoins très lente et des pertes de paquets sont fréquentes.
Je recommande d'utiliser les timeout pour renvoyer des paquets à intervalles régulier jusqu'a réponse.

ProgrammeTest
-------------

Il est fourni : 

    testwifi.py: code simple qui permet de tester si la connexion se fait bien entre les ESP32 et le PC

    testmotor: code simple qui permet de tester si la configuration du portail est correct


Matériel plastique
------------------ 

En cas de casse: Tous les objets imprimés en 3D ont leus modèles disponible.

Instruction utilisation de l'IDE Arduino pour la carte ESP32 Wrover IE
----------------------------------------------------------------------

-Installer IDE Arduino sur https://www.arduino.cc/en/software

-Connecter l'ESP32 Wrover IE avec un cable micro-usb

-Le pc doit détecter la carte 

-Sur l'IDE Arduino: 
Fichier/Préférences
Dans <URL de gestionnaire de carte supplémentaires> 

Ajouter https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

-Dans la fenetre principal cliquer sur les choix des cartes, autres cartes, utiliser ESP32 Wrover Module ou ESP32 Dev Board

-Dans outils: 
Upload Speed : 115200
Flash frequency : 80MHz
Sélectionner le port de la carte : (COM3 ou 5 dans mon cas)

-La carte devrait être détectée et programmable


Lien tutoriel:
http://emery.claude.free.fr/esp32-idearduino.html
https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html