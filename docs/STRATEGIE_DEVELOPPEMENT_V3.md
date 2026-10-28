# Stratégie de développement V3
Date : 28 octobre 2026.

1. Stocker le besoin, expression détaillée et spécification technique dans GitHub avant le développement ; relever main et conserver le retour arrière V2.
2. Remplacer le mécanisme de calcul par autorisation opaque signée pour confirmation déclarative. Adapter les tests de sécurité et HTTP, garder tous les quotas.
3. Développer dialog et cycle de vie différé, traductions, focus, conservation de saisie, annulation réseau et positions bornées.
4. Mettre à jour les tests navigateur : cas fonctionnels de la fenêtre, erreurs et double soumission simulée, plus couverture responsive multilingue existante. Faire exécuter la CI sur branche isolée et corriger avant publication.
5. Publier main, déployer API OVH par workflow SFTP existant avec host key épinglée et secrets privés. Vérifier les deux hébergements, la modale publique et refus d'un POST sans confirmation ; ne pas automatiser le cochage en production.
6. Enregistrer résultats, commits, pipelines, limites et état réel de publication dans MINUTE et le rapport V3. Mettre à jour README/confidentialité pour retirer les mentions de calcul.

## Critères de sortie
Ancien contrôle retiré du code actif, dialog au clic après validation, quatre langues, mobile/clavier/position bornée, saisie intacte à l'annulation, jetons signés à usage unique, limites et tests de concurrence conservés, CI verte, production observée et MINUTE actualisée.

## Garde-fous
Pas de nouveau prestataire, coût, clé tierce ni modification DNS/SMTP. La case n'est pas présentée comme preuve d'humanité. Tests de soumission mockés hors production. Garder les autorisations et informations légales existantes.
