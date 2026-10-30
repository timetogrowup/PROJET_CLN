# Besoin métier — Navigation et étude de cas — V11

Date : 30 octobre 2026. Statut : livré et vérifié en ligne.

## Objectifs et utilisateurs
Simplifier la navigation et permettre à un prospect (dirigeant, responsable opérationnel, SI ou transformation) de préparer un échange avec CLN en décrivant son environnement applicatif, ses équipes, difficultés, objectifs et calendrier. Réduire les ressaisies : la validation ouvre le contact et préremplit le message réellement transmis par email.

## Périmètre
Les dix pages du site et leurs quatre langues. Retirer du menu « Vos besoins » et « Exemples concrets », conserver leurs pages, adresses et liens existants. Renommer « Faire le point » en « Et si on étudiait votre cas ? » et harmoniser les CTA vers diagnostic.html. Cinq entrées : Accueil ; Nos pipelines en action ; Comment nous travaillons ; Et si on étudiait votre cas ? ; Contact. Garder l'hébergement et les protections du formulaire.

## Questions et progression
Les estimations portent sur le périmètre à étudier, pas nécessairement l'entreprise entière. Aucune expertise technique requise.
1. Applications concernées : 1–3 / 4–10 / 11–20 / plus de 20 / inconnu.
2. Collaborateurs utilisateurs : 1–10 / 11–50 / 51–200 / plus de 200 / inconnu.
3. Échanges : largement interconnectées / certaines automatiquement / surtout fichiers ou ressaisies / principalement séparées / inconnu.
4. Difficultés (plusieurs) : ressaisies / tâches répétitives / données dispersées ou incohérentes / informations difficiles à réunir / passages de relais / suivi difficile / autre / à préciser ensemble.
5. Objectifs (deux maximum) : productivité / modernisation SI / connexion / fiabilité / pilotage / travail des équipes / à préciser ensemble.
6. Réflexion : améliorer l'existant / envisager des remplacements / projet engagé / comparer / inconnu.
7. Premiers résultats : moins de 3 mois / 3–6 / 6–12 / au-delà / à définir.
8. Situation concrète : texte libre facultatif, 2 000 caractères maximum.

## Parcours
Bouton « Continuer pour étudier mon cas ». Contrôler les réponses, constituer une synthèse factuelle, ouvrir automatiquement contact.html et remplir le pavé « Votre situation ». Annoncer avant validation que ce transfert ne constitue pas un envoi. Le visiteur peut corriger et compléter ce pavé sans bouton d'ajout supplémentaire. L'envoi du formulaire de contact transmet automatiquement le contenu final de ce pavé avec les coordonnées. Un accès direct au contact reste possible.

## Règles de gestion
RG01. Les questions fermées sont requises avec une option d'incertitude ; celle-ci est exclusive des autres choix du groupe. Au moins une difficulté et un objectif, deux objectifs maximum.
RG02. Aucune estimation de ROI, diagnostic ou recommandation inventée dans la synthèse.
RG03. Seule une validation explicite du nouveau questionnaire remplace la situation préremplie. Un rechargement/retour au contact préserve le brouillon modifié.
RG04. Aucun email n'est envoyé par le questionnaire. L'envoi intervient après validation du formulaire et vérification humaine existante.
RG05. Le champ éditable final est celui utilisé dans le corps du mail, pas une copie ou un aperçu distinct.
RG06. Les anciennes réponses ne sont pas interprétées avec les nouveaux codes. Expliquer un transfert expiré/ancien et proposer de refaire le questionnaire.
RG07. Pas de réponses dans l'URL. Transfert dans l'onglet, durée maximale trente minutes ; brouillon de contact trente minutes après sa dernière modification. Stockage local bloqué : synthèse visible à copier et accès contact, sans perte silencieuse.
RG08. Texte libre conservé tel que saisi. Traduire une synthèse automatique lors d'un changement de langue seulement si elle n'a pas été modifiée par le visiteur.
RG09. Langues FR/EN/PT-BR/ES, clavier, téléphone, gestion des erreurs et consentement/protections existants.

## Critères d'acceptation
CA01. Cinq liens sur les dix menus, aucune suppression de pages ni de leurs liens hors menu.
CA02. Questionnaire cohérent, options complètes, validation et limites explicites.
CA03. La validation ouvre directement le contact, situation complète préremplie et modifiable.
CA04. Reload, retour et erreur d'envoi préservent les modifications ; nouvelle validation remplace la situation précédente.
CA05. Contenu final inclus dans l'email dans les quatre langues, sans copie manuelle ni ajout supplémentaire.
CA06. Aucun envoi automatique ni donnée dans l'URL ; ancienne version/expiration/stockage indisponible traités.
CA07. Tests utiles, publication et vérification du domaine, documents et journal conformes à la livraison.

## Livraison effective — 30 octobre 2026
Version `24279fb679521ad72f193608e5245b4aa5a17cb5`, déployée avec succès sur GitHub Pages ([exécution 41083532813](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41083532813), première tentative). Nouveau parcours : https://cln-performance.com/diagnostic.html?lang=fr .

Dix menus à cinq liens, pages retirées du menu conservées avec les liens hors menu. Sept questions fermées et une situation facultative, quatre langues. Contact automatiquement prérempli dans le champ message, texte éditable conservé sur reload/erreur. Validation finale du contact seule responsable de l'envoi ; traitement PHP/SMTP conservé. Transfert et brouillon de session d'onglet à trente minutes, sans réponses dans l'URL.

Tests JS, structure/catalogues (665/200), dix pages/185 références, régressions V7 à V10 et PHP réussis. Les quatre corps d'emails ont été contrôlés avec le véritable contact.php et un mailer simulé, sans SMTP réel. Recette Chrome : quatre parcours complets, 32 dispositions, limite des objectifs et inconnus exclusifs. Dix-sept fichiers publics HTTP 200 et SHA-256 identiques ; transfert et conservation des modifications revérifiés en ligne dans les quatre langues.

Détails et limites : [rapport de recette](RECETTE_PARCOURS_ETUDE_CAS_V11.md). Pas de test Safari/WebKit, d'appareil physique ni de réception SMTP réelle. Un stockage bloqué donne une synthèse copiable au lieu d'un transfert automatique.
