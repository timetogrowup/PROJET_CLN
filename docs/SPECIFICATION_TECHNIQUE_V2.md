# Spécification technique V2
Date : 28 octobre 2026. Source : EXPRESSION_BESOIN_DETAILLEE_V2.md.

## Architecture
Conserver les pages HTML françaises comme source lisible et repli sans JavaScript. Ajouter un catalogue exhaustif de traductions statiques et de messages dynamiques, un module site.js commun, diagnostic.js et contact.js. Pas de framework ni de service externe. URL ?lang=fr|en|pt-BR|es ; whitelist stricte. Traduction des noeuds texte et attributs depuis leur valeur originale, jamais depuis une traduction précédente. Exclure les valeurs saisies et les scripts. document.lang, titre, description et liens de navigation suivent le choix. Identifiants stables des réponses, indépendants de leur libellé.

Le sélecteur est commun aux neuf en-têtes. Préférence stockée avec date d'expiration (365 jours) ; URL prioritaire. Dégradation si localStorage inaccessible. Les nouveaux textes doivent figurer dans les trois langues étrangères et le français ; contrôle automatique de complétude.

## Diagnostic
Schéma versionné 2 : réponses canoniques, ordre des priorités, texte libre, generatedAt. Génération de la synthèse par fonctions pures à partir de ces données et du catalogue. Rendu via textContent, jamais réinjection d'HTML provenant du stockage. TTL 30 jours. Reprise vers Contact et effacement. La réécriture de préremplissage au changement de langue n'a lieu que si le champ correspond encore au dernier préremplissage automatique.

## API
GET contact.php?op=challenge : JSON contenant opérandes et jeton opaque signé. CORS limité aux deux origines de production (ou refus d'une origine étrangère) ; Vary: Origin, Cache-Control: no-store. Pas de cookie tiers ni de session interorigine. Le jeton porte un nonce et une expiration, avec HMAC de l'identifiant, date et réponse attendue ; aucune clé dans le navigateur.
POST existant enrichi de lang, captcha_token et captcha_answer. Validation stricte types/tailles/consentement, piège et origine avant SMTP. Succès ou refus renvoie une redirection 303 vers contact/merci avec statut, langue et délai entier borné. Aucun champ libre dans l'URL. Les états sont traduits côté page.
Les GET sans opération restent rejetés 405/Allow: POST pour conserver le contrôle de santé du déploiement.

## Stockage serveur et atomicité
Clé aléatoire persistante dans ~/.cln-secrets/mail.json, ajoutée lors du déploiement sans changer les secrets existants. Fichier d'état privé 0600 hors www, verrou flock exclusif partagé entre processus PHP. Empreintes HMAC séparées pour email/IP. Tables JSON pour horodatages SMTP acceptés, défis consommés et essais invalides. Purge des éléments expirés à chaque requête POST. Le verrou couvre la réservation et l'appel SMTP (timeout court, faible volume du site), ce qui sérialise les envois et empêche les doubles acceptations concurrentes. Écrire la consommation du captcha avant l'appel SMTP. Ajouter les compteurs d'envoi après acceptation ; en cas d'exception, ne pas ajouter de succès et ne pas autoriser la réutilisation du même captcha.
Le délai est le maximum des limites email/IP ; un plafond horaire renvoie l'échéance de la plus ancienne acceptation encore comptée. Aucune remise à zéro en changeant de langue. Une limitation distincte des essais incorrects évite les boucles de devinettes sans pénaliser le quota d'envoi réussi.

## Frontend contact
Chargement du défi par fetch sans cookies ; fermeture de l'envoi en cas d'indisponibilité. Expiration client informative, expiration serveur impérative. Bouton de renouvellement, réponse effacée au changement de question uniquement. Soumission HTML classique cross-origin conservée. Brouillon dans sessionStorage pendant 30 minutes pour retour après erreur ; purge au succès. La désactivation du bouton évite les doubles clics côté UX, mais le verrou et le jeton restent l'autorité serveur. Messages invalid natifs surchargés par des messages localisés.

## Déploiement et réversibilité
Réutiliser SFTP à clé serveur épinglée et SMTP secret existant. Sauvegarder mail.json hors www avant ajout de clé ; ne jamais afficher ni commiter de secret. PHPMailer 7.1.1 inchangé. Nouveau backend compatible avec les anciennes pages : elles reçoivent captcha_required au lieu d'un envoi non protégé, pendant la courte transition. Déployer backend puis activer les nouveaux assets frontend dans un commit atomique. Rollback : sauvegarde PHP précédente et commit frontend précédent ; ne pas effacer les compteurs ni la clé lors d'un simple déploiement.

## Tests
Tests unitaires PHP du coeur de sécurité avec horloge et transport factices, tests HTTP sur serveur PHP local en CI, tests de concurrence multi-processus, faux tokens/expiration/types et origines. Tests Playwright des quatre langues, textes, sélecteur, stockage bloqué, saisies, diagnostic, messages et tailles. Tests SMTP de production limités à la boîte officielle. Absence de secrets et brouillons dans sortie des tests et dépôt.
