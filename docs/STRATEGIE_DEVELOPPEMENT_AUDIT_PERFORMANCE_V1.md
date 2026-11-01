# Stratégie de développement — Audit de performance V1
1 novembre 2026.

1. Contrôles préalables : main propre, SHA de référence, README/MINUTE, chaîne de génération et schéma questionnaire ; comparer les quatre pages et catalogue publics au dépôt, consulter Unrealists. Documenter dans DIAGNOSTIC_PREALABLE_AUDIT_PERFORMANCE_V1.md.
2. Enregistrer les trois documents de cadrage avant développement.
3. Implémenter le module éditorial final ; enrichir accueil/méthode/pipelines/questionnaire sans toucher médias ni styles existants.
4. Ajouter option audit dans source questionnaire et schéma partagé, traductions générées ; cache du schéma sur ses deux pages consommatrices. Dépendance : source, validation et messages livrés ensemble.
5. Régénérer ; inspecter diff ; contrôler qu’aucun autre contenu ou ressource n’a évolué. Adapter tests éditoriaux V12 selon nouvelles décisions.
6. Exécuter catalogues/liens, syntaxe, tests statiques, parcours questionnaire/contact et médias ; génération idempotente. Corriger avant publication. Effectuer recette navigateur si aperçu géré disponible ; documenter les contrôles non exécutés.
7. Conditions de publication : diff limité, contrôles pertinents réussis, pas d’email réel, API inchangée. Commit sur main puis push ; suivre exécution Pages jusqu’à statut terminal.
8. Contrôler domaine public : pages et catalogue, schéma partagé, empreintes identiques, langues et parcours avec navigateur si disponible. Ne pas assimiler HTTP 200 à un parcours interactif réussi.
9. Repli : revert du commit applicatif sur main, déploiement Pages, vérification publique de la version restaurée. Aucun reset force ni modification de secrets.
10. Actualiser README, MINUTE et rapport RECETTE_AUDIT_PERFORMANCE_V1.md avec fichiers, tests réellement exécutés, limites, SHA et URL déploiement ; distinguer prévu/réalisé/testé/publié/vérifié.

## État de livraison — 1 novembre 2026
Réalisé conformément au périmètre : quatre pages éditoriales et cache du schéma sur contact, générateur et quatre langues conservés. Choix audit intégré au schéma V11 compatible et à la synthèse existante ; aucun moteur de note ni modification serveur. Référence applicative 4350db82ccad3e9dfc48ef03f06288eb471ea081 ; correctifs CI uniquement 179bf8b et e94cc74 ; fusion main b8641eeb399fc188cb8913f4d27f7ce680db5d02. CI 41311689535 réussie (400 dispositions, PHP et 26 contrôles sécurité, mails simulés). Pages 41311994659 réussie ; seize fichiers publics identiques, quatre langues et quatre parcours audit/contact vérifiés en production. Limites : appareils physiques et SMTP réel non testés. Rapport faisant foi : [recette](RECETTE_AUDIT_PERFORMANCE_V1.md).

## Dernier ajustement livré — Multisélection, 1 novembre 2026
La question « Où en êtes-vous dans votre réflexion sur les applications ? » utilise des cases à cocher et accepte plusieurs réponses sans plafond. « Nous ne savons pas encore » reste exclusif. Toutes les réponses sélectionnées sont reprises dans le message de contact ; les anciens transferts V11 à choix unique restent compatibles. Les quatre langues sont conservées.

Réalisation : passer approach en multisélection dans la source de génération et le schéma partagé ; normaliser les anciens codes simples ; conserver validation et exclusivité génériques ; adapter tests et versions de cache sur les deux pages et la redirection. Après tests locaux, publier sur main, attendre Pages et contrôler plusieurs choix puis leur transfert sur le domaine public. Ces étapes ont été réalisées ; détails dans la recette actualisée.
