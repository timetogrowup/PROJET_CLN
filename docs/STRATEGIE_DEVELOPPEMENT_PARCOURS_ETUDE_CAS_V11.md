# Stratégie de développement — Étude de cas — V11

Date : 30 octobre 2026. Statut : préparation.

1. Synchroniser le dépôt avec main et lire les contrats du générateur, questionnaire, contact et email. Préserver les fichiers étrangers au travail.
2. Enregistrer besoin, spécifications et stratégie avant développement dans GitHub.
3. Définir le schéma des réponses et les textes dans les quatre langues. Créer la bibliothèque de synthèse partagée, sans dépendance réseau.
4. Générer le nouveau questionnaire, les cinq liens des menus et la confidentialité actualisée. Conserver les pages retirées du menu et les liens hors menu.
5. Implémenter validation/transfert puis préremplissage du contact ; sauvegarder le brouillon à chaque modification et conserver les protections de vérification/envoi existantes.
6. Ajouter les tests significatifs, mettre à jour les assertions historiques contredites par la décision V11. Tester le corps réel du mail avec un mailer simulé, sans contacter SMTP.
7. Régénérer, contrôler l'idempotence, catalogues, liens, syntaxe, sécurité et non-régressions. Recette Chrome quatre langues et petits écrans disponibles, corriger les anomalies.
8. Publier le frontend sur GitHub Pages via un commit atomique normal ; suivre le déploiement et vérifier fichiers et parcours publics sans envoyer de message réel.
9. Clôturer les trois documents, recette et MINUTE.md avec les résultats réellement exécutés, commits, adresse publique et limites.

## Dépendances et sortie
Schéma et traductions précèdent le transfert. Le contact dépend de la bibliothèque de synthèse ; son contrat message conserve l'API et l'hébergement existants. Publication après validation fonctionnelle et sécurité. Toute erreur de déploiement temporaire doit être diagnostiquée et seule l'étape en échec relancée si approprié.

## Retour arrière
Revert normal du commit applicatif, sans réécriture d'historique, puis republication. Les anciennes réponses ne sont jamais converties en nouveaux codes. Les documents tracent la livraison et ses limites.
