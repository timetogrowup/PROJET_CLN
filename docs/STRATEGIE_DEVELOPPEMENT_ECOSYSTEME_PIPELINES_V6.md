# Stratégie de développement V6 — Écosystème et pipelines

Date : 29 octobre 2026. Statut : exécutée et clôturée.

1. Examiner le dépôt main, l’accueil V5, les générateurs et les tests. Constat : pipeline présent après le premier écran, mais promesse principale encore centrée sur les ressaisies et le temps.
2. Enregistrer besoin, spécifications et stratégie avant développement.
3. Réécrire en quatre langues les sources éditoriales : accueil puis besoins, pipeline, méthode, exemples, questionnaire, contact, confirmation et message commun. Mettre à jour recommandations et métadonnées sans changer les codes de stockage.
4. Générer les pages, vérifier la couverture des traductions, relire la progression source → enrichissement → application destinataire. Réviser les contrôles qui vérifient des textes V5 devenus obsolètes, en conservant leur exigence fonctionnelle.
5. Exécuter génération répétée, contrôles statiques et tests disponibles ; publier le candidat sur une branche et exécuter la CI complète avant main. Corriger les anomalies.
6. Promouvoir le candidat validé sans réécriture d’historique. Attendre la publication GitHub Pages ; vérifier la version publique et les ressources livrées.
7. Actualiser les trois documents et MINUTE avec le périmètre réel, le rapport de recette, les SHA, liens et limites. Aucun envoi de mail de production.

Dépendances : sources avant fichiers générés ; libellés et recommandations ensemble ; CI réussie avant promotion ; publication avant bilan de production. Les tests techniques ne remplacent pas un retour de compréhension des prospects.

## Exécution réelle
Étapes 1 à 7 réalisées. Documents enregistrés dans 978648be88378a70e4825122ae20979ee8707ef7 avant le code. PHP absent localement : sécurité et tests HTTP exécutés avec succès en CI. Prévention ajoutée pendant la revue : version 6 des synthèses pour ne pas réinterpréter les réponses anciennes. Tests complets réussis avant promotion de main ; publication et contenu public vérifiés. Le rapport de recette et MINUTE consignent les résultats et les limites.
