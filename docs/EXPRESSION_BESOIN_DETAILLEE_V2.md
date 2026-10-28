# Expression de besoin détaillée V2 — Formulaire protégé et site multilingue
Date : 28 octobre 2026. Références : BESOIN_CAPTCHA_LIMITATION_EMAIL.md et BESOIN_SITE_MULTILINGUE.md.

## Objectif et périmètre
Offrir les neuf pages du site en français, anglais, portugais brésilien et espagnol ; protéger chaque demande par un calcul simple et des limites serveur communes à toutes les langues. Conserver l'hébergement GitHub Pages, l'API PHP 8.4 et le SMTP OVHcloud existants. Les informations légales exclues à la demande de Patrick restent exclues ; aucune nouvelle identité n'est inventée.

## Parcours et règles métier
FR est le défaut, sans détection automatique de la langue du navigateur. Le visiteur choisit Français / English / Português (Brasil) / Español dans un sélecteur compact en haut de l'accueil, repris sur toutes les pages. Priorité : choix explicite dans l'URL, préférence du navigateur conservée 365 jours, puis FR. Le choix se transmet aux liens et aux retours de l'API. Il reste utilisable si le stockage navigateur est bloqué.

Les textes visibles, métadonnées, aides, attributs accessibles et messages dynamiques sont traduits. Les données factuelles restent inchangées. Le texte libre du visiteur n'est ni traduit ni effacé. Changer de langue ne déclenche aucun envoi, ne réinitialise pas le diagnostic ou ses priorités et ne remet aucun quota à zéro.

Le diagnostic conserve ses règles métier ; sa synthèse est reconstruite dans la langue courante depuis des réponses structurées. Les anciennes synthèses sans données structurées ne sont pas injectées comme HTML : le visiteur est invité à recalculer. Une synthèse expire après 30 jours. Les champs modifiés manuellement ne sont pas réécrits lors d'un changement de langue.

## Captcha
Calcul aléatoire d'addition, opérandes de 1 à 9, question textuelle accessible au clavier et aux lecteurs d'écran. Durée 10 minutes. Renouvellement indépendant des autres champs. Réponse vérifiée côté serveur et jeton authentifié, non réutilisable. Un contrôle purement JavaScript ne suffit pas. Le calcul simple est un frein complémentaire, pas une preuve certaine d'humanité.

## Limites d'envoi
Même adresse email normalisée : délai minimum 600 secondes et plafond de 3 acceptations SMTP sur 3600 secondes glissantes. La normalisation ignore espaces périphériques et casse, sans supprimer points ou suffixes +. Contrôle indépendant du navigateur, du réseau et de la langue. Maintien des protections par IP (60 secondes et 5 acceptations/heure) et du champ piège. Les tentatives abusives ont un compteur séparé ; les erreurs de saisie/captcha ne consomment pas le quota des envois acceptés.

Deux demandes simultanées ou deux clics ne créent pas deux mails. Seule l'acceptation SMTP compte comme envoi pris en charge ; elle ne prouve pas la réception finale. Une panne n'affiche jamais un faux succès. Le refus de fréquence affiche le temps restant en minutes arrondies vers le haut, dans la langue courante.

## Protection des saisies et des données
Lors d'un rejet serveur, les données nécessaires à la correction restent disponibles dans l'onglet courant ; elles sont supprimées du brouillon après succès ou à l'expiration du brouillon (30 minutes). Elles ne figurent ni dans l'URL ni dans les logs. Les compteurs contiennent des empreintes protégées et des dates, pas d'email ni d'IP en clair. Nettoyage des traces expirées à chaque accès au fichier d'état. La notice de confidentialité décrit les usages et durées réellement implémentés. Aucun service de captcha tiers.

## Messages et accessibilité
Question, renouvellement, chargement, absence de connexion, captcha incorrect/expiré, refus de fréquence, champs invalides et confirmation sont disponibles dans les quatre langues. Les champs sont étiquetés, les erreurs annoncées et les actions accessibles au clavier. Le formulaire est indisponible tant qu'aucun défi valide n'a été chargé ; une panne du contrôle n'autorise pas un envoi non protégé.

## Recette obligatoire
Vérifier les quatre langues, leurs métadonnées et les neuf pages ; absence de clé technique visible ; conservation des réponses et textes libres ; ancienne synthèse et stockage bloqué ; captcha faux/absent/expiré/rejoué ; délais 10 min, plafond glissant 3/h, simultanéité et panne SMTP ; variantes de casse ; CORS et origine ; interface sur mobile/tablette. Les tests de quotas utilisent une horloge contrôlée et un transport simulé, sans attendre une heure ni envoyer de mails inutiles. Recette de production : un seul envoi explicitement identifié vers la boîte officielle.

## Livraison
Spécifications et stratégie versionnées, tests vérifiables, sauvegarde du backend et de sa configuration privée, déploiement API avant frontend, vérification publique et compte rendu dans MINUTE. Aucune promesse de conformité juridique complète.
