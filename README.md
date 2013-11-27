Groupe5
=======

Travail d'analyse syntaxique. Groupe 5

Contributeurs :

  Augustin
  Sarah
  Maximin


Ont cloné :
  Sarah
  Augustin

Idee:
    Virer les règles de proba trop petites ( ça sert à rien et ça encombre).
    
    Pour chaque LH :
        calculer m = max( P(RH) )
        virer toutes les règles qui réécrivent LH avec une proba < m * un petit nombre.

TODO
  X Finir la binarisation
  X Mail aux groupes
  - Creer input pour groupe 4
  X Installer parseur
  - Brancher avec parseur:
    * Mail Sagot
  - Train/test
  - Faire un lecteur de texte au format du groupe 4 qui réécrit les infos après.

   {....1}token1 {....2}token2

   parse: token1 token2

   resultat: (token1 (token2))

   remet: ({...}token ({...}token))

  - stade plus avancé :
   
   {....1}token1 {....2}token2

   parse: token1_cat token2_cat

   lexique non-ambigu:
      token1_catx : catx : proba

   resultat: (token1 (token2))

   remet: ({...}token ({...}token))
