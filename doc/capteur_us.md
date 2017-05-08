# Gestion des capteurs ultrasons

Pour le projet nous avons utiliser de capteurs utltrasons HC-SR04.
Si vous avez besoin d'aide au niveau de la compréhension du fonction d'un capteur
ultrasons, vous pourrez trouver des informations intéréssantes [ici](http://www.micropik.com/PDF/HCSR04.pdf) ou encore [ici](https://www.gotronic.fr/pj2-hc-sr04-utilisation-avec-picaxe-1343.pdf).

Les utltrasons son connecté et utilisé par une arduino ne servant que à la detection
d'objet, et cette arduino répond aux différentes questions que peut lui poser
la raspberry pi en I2C (voir fichier de desction des protocles utilisé).

La seule particularité théorique à prendre en considération c'est la convetion
temps/distance qui se fait à partir d'une simple formule :

343 * 100 / 10^6 [cm/µs] / 2 (aller-retour) = 58.3

ou 343 représente la vitesse du son en m/s, le 58,3 calculé sera la valeur par
laquelle il faudra diviser la valeur mesurée en seconde via la function pusleIn()
pour obtenir une distance en cm. (Et ainsi pouvoir renvoyer la rapsberry pi une
distance entre l'objet le plus proche dans le champ du capteur)

Pour plus d'info sur l'utilisation en elle même, voir [us_sensor.ino](https://github.com/Ecam-Eurobot-2017/main/blob/master/code/arduino/us_sensors/us_sensors.ino)
