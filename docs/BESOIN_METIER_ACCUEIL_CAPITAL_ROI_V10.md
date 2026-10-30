# Besoin métier — Accueil, capital existant et retour sur investissement — V10

Date : 30 octobre 2026. Statut : livré et vérifié en ligne.

## Objectifs
Présenter CLN Performance comme une petite structure spécialisée qui intervient de façon ciblée et chirurgicale dans l'écosystème applicatif du client. Valoriser les applications, les données et les compétences existantes ; montrer comment des automatisations ciblées permettent de rechercher des premiers gains plus tôt avec un investissement initial limité.

## Utilisateurs et bénéfices
Dirigeants, responsables opérationnels, responsables de transformation et des systèmes d'information. Leur permettre de comprendre la proposition, d'évaluer l'intérêt d'un premier périmètre, de consulter des exemples puis de contacter CLN ou de faire le point sur leur situation.

## Périmètre
Refonte de l'accueil et de ses métadonnées, quatre langues dès livraison (français, anglais, portugais du Brésil, espagnol). Conservation à côté du texte introductif de l'animation existante de la flèche. Intégration du comparatif ROI validé sous les verbatim. Réemploi des parcours Faire le point, Contact et Nos pipelines en action. Aucun changement du formulaire, de son traitement ni des autres pages éditoriales.

## Parcours éditorial
1. Présentation : « Une petite structure. Des interventions ciblées. Des gains concrets. » Texte expliquant la précision, le périmètre maîtrisé, la connexion des applications et l'automatisation. CTA « Identifier vos premiers gains » vers diagnostic.html. Flèche conservée, à côté sur grand écran.
2. Capital : « Votre écosystème applicatif et le savoir-faire de vos collaborateurs sont un capital. Faites-le fructifier. » Évoquer les coûts de migration, interfaces, formation et réorganisation.
3. Productivité : « La meilleure interface, c'est parfois celle dont vous n'avez plus besoin pour accomplir une tâche. » Relier cette idée aux tâches supprimées, ressaisies évitées, données enrichies et décisions humaines.
4. Investissement : « Investir là où le gain se crée, pour un retour sur investissement rapide. » Comparatif animé, explication et CTA vers le contact.
5. Engagements Ciblé / Libéré / Normé, lien vers les pipelines en action ; interlocuteur Patrick, autonomie et modalités de rémunération existantes préservées dans une présentation sobre.

## Comparatif illustratif
CLN à gauche : trois étapes sur neuf mois (cibler et connecter ; automatiser et mettre en service ; étendre et stabiliser). Faible investissement initial et gains qui continuent de s'accumuler jusqu'à 36 mois. À droite : neuf étapes sur 36 mois (cadrer, choisir, concevoir, paramétrer, développer les interfaces, migrer, tester, former, déployer). Chaque étape apparaît avec la position de la courbe correspondante. Deux graphiques indépendants sous les blocs, échelles identiques. Chronologie commune ; arrêt de lecture au mois 9. La courbe représente le solde cumulé gains moins coûts, pas un taux de ROI. Le remplacement reste négatif au mois 36 dans cet exemple et commence seulement à produire des gains.

## Règles de gestion
RG01. Langage accessible et bénéfices avant détails techniques. « Chirurgicale » signifie précision et perturbations limitées.
RG02. Les calendriers 9/36 mois et les courbes sont illustratifs : aucun délai, économie ni rentabilité garanti.
RG03. Le remplacement d'une application peut être pertinent ; il se décide au regard du contexte. Aucun dénigrement universel des logiciels modernes.
RG04. Le temps libéré n'est pas automatiquement une économie financière ; les indicateurs, coûts et période de mesure sont définis avec le client.
RG05. Pas de données client, chiffre financier inventé, client de référence ou témoignage fabriqué.
RG06. Vidéos sans son, pause/reprise, image de synthèse agrandissable, transcription textuelle. Sans JavaScript ou avec réduction du mouvement : synthèse statique lisible.
RG07. Seul le média de langue sélectionnée se charge ; les animations se mettent en pause hors écran ou lorsque l'onglet est masqué. Une pause choisie reste respectée.
RG08. Conserver les destinations commerciales existantes et l'hébergement actuel.

## Critères d'acceptation
CA01. Une seule H1 présente la petite structure et les gains ; flèche conservée à côté du texte sur ordinateur, disposition adaptée au téléphone.
CA02. Ordre des cinq blocs respecté et verbatim visibles, sans répétition des anciens blocs génériques.
CA03. Comparatif identique au scénario approuvé, dans les quatre langues, avec même chronologie et mêmes échelles.
CA04. Légende illustrative, portée de la comparaison et distinction temps/économie explicites.
CA05. Contrôles au clavier, fermeture par Échap, retour de focus, alternative textuelle et statique ; absence de débordement de page.
CA06. Liens valides vers diagnostic, contact, méthode et pipelines ; aucun changement d'envoi de message.
CA07. Tests de non-régression, génération reproductible, publication et contrôle de la version publique ; rapport et journal à jour.

## Livraison effective — 30 octobre 2026
Accueil livré en quatre langues, flèche conservée, cinq blocs éditoriaux, comparatif 36 secondes avec 3/9 étapes et deux graphiques indépendants. Médias optimisés (huit vidéos et quatre posters), transcription, pause/reprise et synthèse statique agrandissable. Aucun changement du traitement du contact.

Version applicative initiale : `c6445f1b97eb152c4c0013920ff164162dcb7239`. Correction du mouvement de la flèche : `26e939b35f4276d98e38d1add82b03e5cf29cd5c`. Cette correction empêche un événement de lecture tardif de relancer la flèche hors écran ; elle est couverte par un test supplémentaire.

GitHub Pages : publication de la correction réussie, exécution [41068286785](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41068286785), tentative 2 après un échec temporaire du service de déploiement. Accueil : https://cln-performance.com/ . Dix-sept fichiers publics HTTP 200 et SHA-256 identiques ; quatre langues et contrôles validés sur le domaine. Tests détaillés et limites dans [le rapport de recette](RECETTE_ACCUEIL_CAPITAL_ROI_V10.md). Safari et appareils physiques non testés ; les seize fenêtres de recette sont des vérifications CSS dans Chrome.
