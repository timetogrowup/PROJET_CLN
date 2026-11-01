# Spécifications techniques — Audit de performance V1
1 novembre 2026.

## Architecture et fichiers
Architecture statique existante conservée. Module scripts/audit_performance.py appliqué après approach_diagnostic dans scripts/build_pedagogy.py : enrichissement ciblé de index.html, approche.html, pipelines.html et diagnostic.html ; traductions via i18n/static.json. Réutiliser sections, cartes et grilles CSS existantes sans nouvel effet. Métadonnées de méthode cohérentes avec audit autonome.

## Questionnaire et interfaces
Ajouter audit dans les options approach de scripts/case_journey.py et case-data.js. Réutiliser sélection radio, nettoyage, validation et synthèse actuels, messages case.choice.approach.audit dans les quatre langues. Pas de nouvelle persistance ni d’appel réseau. Les anciens transferts V11 restent valides. Renouveler URL de cache case-data sur diagnostic/contact. contact.html peut évoluer pour cette seule référence, sans changement de formulaire, contact.js, PHP ou secrets.

## Accessibilité, responsive et navigation
Un H1, H2/H3 hiérarchisés, labels radio natifs, pas de choix précoché, trois recommandations sans priorité visuelle. Réutiliser card-grid et CSS responsive. Préserver les ancres #diagnostic, #intervention, #pipeline, #remuneration et liens existants. Textes français lisibles sans JS ; traductions existantes côté navigateur, même propagation du paramètre lang.

## Données et confidentialité
Aucune note calculée, aucune donnée métier client stockée en plus. Réponses du prospect uniquement dans synthèse existante, contact éditable et consentement/envoi actuels. Aucun email réel pour la recette. API OVH inchangée.

## Vérification
Contrôles existants : catalogues complets, dix pages et ancres, génération idempotente, syntaxe JS/Python/PHP, tests V7–V11 et API avec simulations. Adapter assertions V12 devenues obsolètes. Ajouter couverture fonctionnelle du choix audit, nettoyage, résumé dans les quatre langues et absence de modification des données libres. Recette navigateur avec aperçu géré lorsque disponible : quatre langues, mobile/ordinateur, liens, radio audit, contact prérempli, médias, console ; consigner limites réelles.

## Publication et retour arrière
Commit cohérent sur main selon publication GitHub Pages existante. Pas de déploiement Hostinger/OVH. Vérifier exécution Pages, HTTP et empreintes des fichiers livrés sur domaine public. En cas de défaut, corriger ou revert du seul commit applicatif, sans reset forcé ni suppression des modifications tierces. Documenter SHA, exécution et résultats dans la recette et MINUTE.

## État de livraison — 1 novembre 2026
Réalisé conformément au périmètre : quatre pages éditoriales et cache du schéma sur contact, générateur et quatre langues conservés. Choix audit intégré au schéma V11 compatible et à la synthèse existante ; aucun moteur de note ni modification serveur. Référence applicative 4350db82ccad3e9dfc48ef03f06288eb471ea081 ; correctifs CI uniquement 179bf8b et e94cc74 ; fusion main b8641eeb399fc188cb8913f4d27f7ce680db5d02. CI 41311689535 réussie (400 dispositions, PHP et 26 contrôles sécurité, mails simulés). Pages 41311994659 réussie ; seize fichiers publics identiques, quatre langues et quatre parcours audit/contact vérifiés en production. Limites : appareils physiques et SMTP réel non testés. Rapport faisant foi : [recette](RECETTE_AUDIT_PERFORMANCE_V1.md).
