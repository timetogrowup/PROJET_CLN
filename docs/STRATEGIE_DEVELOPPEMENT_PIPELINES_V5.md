# Stratégie de développement V5 — Pipelines en action

Date : 29 octobre 2026. Références : BESOIN_METIER_PIPELINES_V5.md et SPECIFICATIONS_TECHNIQUES_PIPELINES_V5.md.

1. Vérifier le dépôt, le générateur V4, les tests, la publication existante et l’absence de changements locaux. Conserver l’architecture et le formulaire.
2. Formaliser et enregistrer les trois documents dans GitHub avant les développements.
3. Définir les contenus traduits du scénario et des exceptions dans un module dédié. Construire d’abord la page pipelines.html, qui sera la cible des nouveaux liens.
4. Intégrer le bloc Accueil après le premier écran, la section Besoins, le lien dans Exemples et l’explication dans la Méthode. Étendre le menu sur toutes les pages, les métadonnées, le cache et le sitemap.
5. Adapter les styles des cinq étapes et des exceptions aux petits écrans. Réutiliser les composants natifs et l’identité V4.
6. Étendre les tests de structure, de traduction et les parcours ; exécuter la génération deux fois pour vérifier sa stabilité. Détecter et corriger les anomalies avant publication.
7. Exécuter la CI sur branche dédiée : sécurité V3, questionnaire V4, parcours V5 et matrice 400 affichages. Publier sur main uniquement après réussite des contrôles du code final.
8. Vérifier Pages et les fichiers servis sur le domaine ; parcourir la nouvelle page sans envoi de formulaire. Mettre à jour les documents, les références de code, le rapport et MINUTE avec les résultats réels.

## Dépendances

La page dédiée et ses traductions précèdent les liens. Le menu commun doit être généré avant la matrice responsive. Le module éditorial est appelé avant la sauvegarde du catalogue. Les tests existants qui supposent six liens ou neuf pages évoluent explicitement ; les tests de protection et de transfert ne changent pas de sens.

## Conditions de clôture

P01 à P10 documentés, tests techniques réussis, code et documentation versionnés, publication vérifiée. Pas de nouveau moteur métier ni de déploiement OVH. Toute vérification non réalisée est indiquée comme telle. Les retours utilisateurs et les bénéfices réels d’une mission ne se déduisent pas de la réussite de la CI.
