# ECAM - Eurobot 2017

## Git Utilisation

### Inclure les changements d'un repository forker
Lorsque des modifications ont été réalisées sur le repository principal, vous devez intégrer ces changements à votre repository local (**fork**)

Voici les étapes à suivre:

1.  **Remote.**
  ```
  git remote add <name> <url>
  ```
  Le **name** correspond à l'alias de l'url suivant et **l'url** correspond à l'url de clone du repository git principal (repository que  vous forker).

  * Exemple:
  ```
  git remote add eurobot https://github.com/Ecam-Eurobot-2017/main.git
  ```

2.  **Fetch.**
  ```
  git fetch <name>
  ```
  Le **name** est l'alias choisit dans le **git remote** présenté plus haut. Celui-ci permet de récupérer les données. Git créera   automatiquement une nouvelle branche.

  * Exemple:
  ```
  git fetch eurobot
  ```

3. **Merge.**
  ```
  git merge <branch>
  ```

  Nous allons inclure les changements de la branche créé plus haut dans notre branche principal **master**.

  * Exemple:
  ```
  git merge eurobot/master
  ```

**Pour finir** lorsque vous voudrez la prochaine fois inclure les modifications du repository principal dans votre repository local. Vous ne devrez plus qu'utiliser:
```
git pull <name> master
```
Ceci incluera donc tous les changements directement dans votre branche principal **master**.

* Exemple:
```
git pull eurobot master
```

Afin d'inclure les changements sur votre repository en ligne sur GitHub par exemple il suffit de faire un ```git push``` vu que les
changements n'étaient présents que sur votre machine local.
