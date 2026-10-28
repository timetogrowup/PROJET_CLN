# Expression de besoin détaillée V3
Date : 28 octobre 2026. Référence : [besoin](BESOIN_CONFIRMATION_HUMAINE_V3.md).

## Acteurs et résultat attendu
Visiteur sur ordinateur ou mobile, utilisant souris, clavier ou assistance vocale ; CLN destinataire des demandes. Réduire l'effort de saisie en retirant tout calcul, conserver la maîtrise des envois abusifs par les quotas existants.

## Exigences fonctionnelles
- F01 Retirer le bloc de calcul, champ numérique, bouton de changement de question et messages de calcul. Aucun contrôle humain visible pendant la saisie.
- F02 Valider les champs existants et confidentialité avant d'ouvrir une fenêtre modale ; champ invalide ciblé par le navigateur.
- F03 À chaque ouverture, case décochée et nouvelle autorisation temporaire, sans reprendre une confirmation antérieure.
- F04 Fenêtre avec titre, explication, case, confirmation désactivée avant cochage, annulation. Échap ferme ; aucune fermeture n'envoie.
- F05 Préparer la vérification seulement à l'ouverture. Si le service est indisponible, interdire l'envoi et offrir une nouvelle tentative explicite ou l'annulation.
- F06 Confirmer envoie une seule requête, ferme le parcours interactif et désactive les commandes d'envoi. Empêcher les doubles clics et vérifications périmées.
- F07 Expiration après dix minutes : informer, renouveler et demander de recocher ; ne pas envoyer automatiquement après renouvellement.
- F08 Conserver nom, email, organisation et message à l'annulation et lors d'un refus serveur. Brouillon de session trente minutes, suppression au succès, règles existantes conservées.
- F09 Ordinateur : position aléatoire bornée par la fenêtre visible, marge de sécurité. Mobile : centrage. Ne pas déplacer pendant l'interaction ; si rotation/réduction, adapter uniquement pour conserver la visibilité.
- F10 Modale native accessible : titre et description associés, focus initial dans la fenêtre, tabulation contenue, arrière-plan inactif, Échap et retour du focus.
- F11 Tous les textes, états de chargement et erreurs FR/EN/pt-BR/ES. Texte du visiteur inchangé.
- F12 Quotas email/IP et validation serveur inchangés. Aucun secret dans le navigateur. Aucun envoi si autorisation absente, expirée, falsifiée ou rejouée.

## Scénarios de recette
Nom/email/message/consentement manquant : aucune fenêtre. Données valides : fenêtre, case décochée, bouton bloqué. Annulation/Échap : saisie intacte et focus restitué. Cochage puis décochage : confirmation à nouveau bloquée. Confirmation : un POST. Erreur/expiration : message, renouvellement sans envoi automatique. Nouvelle ouverture : nouvelle confirmation. Réseau lent : annulation possible sans réouverture tardive. Rotation et formats étroits : aucune commande hors écran. Quota dépassé : délai explicite après confirmation sans second email.

## Hors périmètre et limites
Pas de service externe de détection automatisée, pas de preuve réelle d'humanité, pas de changement SMTP, DNS, destinataire ou secrets. La randomisation est ergonomique et ne remplace pas les protections serveur. Les exclusions légales antérieures restent respectées.
