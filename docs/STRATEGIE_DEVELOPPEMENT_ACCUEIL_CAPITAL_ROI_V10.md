# Stratégie de développement — Accueil capital et ROI — V10

Date : 30 octobre 2026. Statut : stratégie exécutée et livraison vérifiée.

## Séquence
1. Lire le dépôt courant, les générations V6–V9, contrôleurs, styles et tests. Vérifier le HEAD distant et préserver les changements étrangers à la livraison.
2. Enregistrer besoin, spécifications et stratégie dans GitHub avant l'implémentation ; ne pas déployer de contenu incomplet de page.
3. Réutiliser le scénario animé approuvé et produire les huit vidéos et quatre posters. Vérifier dimensions, durée, codecs et contenus dans chaque langue. Ne pas ajouter les GIFs lourds au site.
4. Écrire la transformation finale de l'accueil et ses traductions. Conserver la flèche, les messages commerciaux existants utiles, les parcours et l'ancre #pipelines. Ajouter transcription, limites du scénario et CTA.
5. Ajouter les styles dédiés et réutiliser le lecteur paramétrable ; ne modifier son comportement partagé que si un besoin réel ou un défaut le justifie.
6. Mettre à jour les tests historiques devenus contradictoires et ajouter les vérifications utiles au nouveau scénario. Exécuter syntaxe, catalogues, liens, régressions média/mouvement et vérification de génération idempotente.
7. Faire la recette visuelle et fonctionnelle de l'accueil dans les quatre langues ; corriger les anomalies constatées. Captures de travail uniquement, pas de publication des captures.
8. Commiter les fichiers nécessaires et publier sur main via GitHub, sans force. Suivre le déploiement existant et vérifier les fichiers publics et l'accueil.
9. Finaliser le rapport de recette, actualiser les trois documents et MINUTE.md avec la portée réellement livrée, la référence du commit et les limites de vérification.

## Dépendances
Les traductions éditoriales et les médias doivent être prêts avant recette quatre langues. La génération dépend du pipeline éditorial existant. La publication dépend des tests statiques/unitaires et de la validation visuelle disponible. Les performances dépendent des vidéos compressées et du chargement à la visibilité.

## Vérifications et sortie
Tests significatifs : parcours éditorial, absence de contenu non traduit, fidélité 3/9 étapes et 9/36 mois, lecteur au clavier, charge initiale statique, conservation flèche et cas V8/V9, ancres/destinations. Une limite de navigateur est documentée avec les contrôles de remplacement réellement effectués. Aucun email de test envoyé. Les données saisies et le traitement du contact sont hors périmètre.

## Retour arrière
La livraison est isolée dans un commit applicatif. En cas de régression publique, revenir par un commit de revert normal sur ce commit, sans réécriture d'historique, puis redéployer et contrôler. Conserver les documents pour tracer l'incident.

## Livraison effective — 30 octobre 2026
Accueil livré en quatre langues, flèche conservée, cinq blocs éditoriaux, comparatif 36 secondes avec 3/9 étapes et deux graphiques indépendants. Médias optimisés (huit vidéos et quatre posters), transcription, pause/reprise et synthèse statique agrandissable. Aucun changement du traitement du contact.

Version applicative initiale : `c6445f1b97eb152c4c0013920ff164162dcb7239`. Correction du mouvement de la flèche : `26e939b35f4276d98e38d1add82b03e5cf29cd5c`. Cette correction empêche un événement de lecture tardif de relancer la flèche hors écran ; elle est couverte par un test supplémentaire.

GitHub Pages : publication de la correction réussie, exécution [41068286785](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41068286785), tentative 2 après un échec temporaire du service de déploiement. Accueil : https://cln-performance.com/ . Dix-sept fichiers publics HTTP 200 et SHA-256 identiques ; quatre langues et contrôles validés sur le domaine. Tests détaillés et limites dans [le rapport de recette](RECETTE_ACCUEIL_CAPITAL_ROI_V10.md). Safari et appareils physiques non testés ; les seize fenêtres de recette sont des vérifications CSS dans Chrome.
