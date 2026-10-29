# Stratégie de développement — logo CLN — V7
Date : 29 octobre 2026.

1. Lire le dépôt actuel et identifier le générateur, les styles communs, les langues et l'hébergement. Préserver les travaux V6 et les formulaires.
2. Formaliser le besoin, les spécifications et cette stratégie ; consigner les résultats dans RECETTE_LOGO_V7.md.
3. Partir du GIF validé ; produire le poster, WebM et MP4 recadrés. Dépendance : médias prêts avant intégration HTML.
4. Ajouter une transformation dédiée au générateur : en-têtes, figure d'accueil, déplacement de l'exemple, traductions et cache V7. Conserver toutes les pages et leurs liens.
5. Ajouter les styles puis le cycle de vie JS : poster par défaut, chargement conditionnel, lecture/pause, réduction du mouvement et visibilité. Dépendance : clés traduites disponibles via CLN.ready.
6. Régénérer, exécuter les contrôles syntaxiques, statiques, catalogues et tests ciblés du mouvement. Vérifier l'idempotence puis l'aperçu navigateur. Corriger toute anomalie avant publication.
7. Enregistrer les documents et le code dans GitHub, en commit cohérent ; publier via l'hébergement existant, sans déplacer le projet vers un autre service. Vérifier le déploiement associé au commit et les ressources publiques.
8. Mettre à jour la recette et MINUTE avec les résultats réellement obtenus et les limites. En cas d'échec de déploiement, conserver le commit et documenter la cause ; ne pas annoncer une publication réussie.

## Retour arrière
Revenir au commit précédent de la livraison via un nouveau commit inverse ; ne pas réécrire l'historique partagé. Les médias et le logo antérieur restent disponibles dans l'historique.
