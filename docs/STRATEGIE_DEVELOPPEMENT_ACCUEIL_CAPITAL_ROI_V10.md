# Stratégie de développement — Accueil capital et ROI — V10

Date : 30 octobre 2026. Statut : préparation.

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
