# Stratégie de développement — animation pipeline V8
29 octobre 2026.

1. Relire le dépôt et les générateurs ; garder l'hébergement et les développements V7. Enregistrer les documents de cadrage dans GitHub avant la réalisation.
2. Versionner le dessin procédural, traduire toutes les chaînes, adapter les tailles de police aux cadres et générer les quatre variantes en vidéo et posters. Vérifier durées, tailles et rendu.
3. Étendre le générateur : déplacer le bloc bout-en-bout après l'introduction, ajouter vidéo, commandes, explication et dialogue. Ajouter les catalogues puis générer les pages.
4. Développer le lecteur progressif : langue, pause, visibilité, repli, réduction de mouvement ; ajouter la vue agrandie accessible. Garder les scripts de l'API inchangés.
5. Exécuter les contrôles automatiques puis l'aperçu navigateur ; tester notamment changements de langue rapides, pause conservée et retour du focus. Corriger les anomalies et vérifier l'idempotence du générateur.
6. Commit applicatif sur le dépôt, déploiement GitHub Pages existant, vérification du SHA et de la page publique ainsi que des médias.
7. Mettre à jour le rapport de recette et MINUTE avec les résultats et limites réels. Retour arrière par commit inverse, sans réécriture de l'historique ni changement DNS.

## Bilan de réalisation
Étapes 1 à 7 exécutées. Déploiement Pages 40894964249 réussi pour 66be840326187a7422851aeda1c50bb90ba03c7a ; commandes et quatre langues vérifiées sur la page publique. Les tests d’appareils physiques et Safari restent une limite de recette, pas un résultat acquis.
