# Livraison V3 — confirmation humaine avant envoi
Date : 28 octobre 2026 (Europe/Paris).

## Documents de référence
- [Besoin initial](BESOIN_CONFIRMATION_HUMAINE_V3.md)
- [Expression de besoin détaillée](EXPRESSION_BESOIN_DETAILLEE_V3.md)
- [Spécification technique détaillée](SPECIFICATION_TECHNIQUE_V3.md)
- [Stratégie appliquée](STRATEGIE_DEVELOPPEMENT_V3.md)

## Changements
Le calcul, le champ numérique, le changement de question et les textes associés ont été retirés du code actif. Le clic sur « Envoyer la demande » valide d'abord les champs, puis ouvre une fenêtre native accessible avec case « Je suis un humain », confirmation et annulation. Aucun contrôle humain affiché et aucune requête de vérification pendant la saisie initiale.

Sur ordinateur la position varie à chaque ouverture dans les limites de l'écran ; sur petit écran la fenêtre est centrée. Les saisies sont conservées à l'annulation, Échap est pris en charge, le focus revient au bouton d'envoi. Le bouton de confirmation est bloqué avant cochage et pendant l'envoi. Les quatre langues sont conservées.

Autorisation opaque signée HMAC, purpose human-v3, expiration dix minutes, consommation unique sous verrou. Ancien protocole refusé. Limites email (dix minutes entre demandes, trois par heure), IP (une minute, cinq par heure, trente tentatives par heure), validation, honeypot et SMTP inchangés. La clé persistante et les mots de passe restent privés.

## Recette automatisée
[CI vérifiée](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40770221773), commit 4666b7492d79efdbd3f6bfb5a48e3b7df8cb183f : succès.

| Contrôle | Résultat |
| --- | --- |
| Syntaxe PHP et JS | Réussie |
| Sécurité PHP | 26 contrôles, dont absence de confirmation, ancien jeton, expiration, falsification, rejeu, quotas et concurrence |
| HTTP en environnement isolé | Origines CORS, retrait ancien endpoint, champs/types/taille, redirections traduites, refus sans confirmation ou jeton valide |
| Catalogues | 236 textes statiques et 73 messages dynamiques complets dans les langues attendues |
| Fenêtre Chromium et WebKit | Ouverture différée, champs invalides, erreur et nouvelle tentative, annulation pendant chargement, focus et clavier, position variable, expiration puis nouveau cochage, un seul POST simulé malgré double clic |
| Affichages | 360 combinaisons : neuf pages, quatre langues, cinq largeurs, deux moteurs ; diagnostic et saisies libres conservés |

Les tests d'envoi de la fenêtre sont interceptés en environnement isolé. Aucun email de test V3 n'est envoyé. Un défaut de focus après « Réessayer » détecté pendant la recette a été corrigé avant publication ; la CI finale est verte.

## Publication
- Backend : fce91fc67ec937cb4e4558e23925c8c6023ad165.
- Frontend : 46bf1b44d060bcc131af0d980550f0c0f07faf00.
- Workflow API : https://github.com/timetogrowup/PROJET_CLN/actions/runs/40770896678.
- API : workflow terminé avec succès.
- [Publication GitHub Pages](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40771310253) : succès.
- Arbre source publié identique à celui de la CI : 1f9db61d79e8d60b1878c20f6068df3bfefb8495.

## Contrôles publics après publication
- GET op=human : 200, JSON token/expires sans opérandes, CORS exact à l’origine autorisée.
- Ancien GET op=challenge : 405 ; origine étrangère sur op=human : 403.
- POST sans confirmation : 303 human_required avec langue espagnole conservée.
- POST avec jeton falsifié : 303 human_invalid. Aucun SMTP déclenché par ces refus.
- Navigateur public en français : aucun bloc de calcul dans le formulaire ; ouverture de la fenêtre après validation ; case décochée, confirmation désactivée ; autorisation chargée ; fenêtre intégralement visible.
- Annuler ferme, conserve les valeurs et restitue le focus au bouton d’envoi. Aucune confirmation humaine cochée et aucun envoi réel effectué pendant le contrôle public. Les champs de démonstration ont ensuite été vidés.
- Capture de la fenêtre enregistrée pour le compte rendu utilisateur.

## Retour arrière coordonné
Restaurer les fichiers frontend ET contact.php/contact_security.php du commit V2 ed6fb95c753a9ab0b0492b1e087ed477128d7327, puis déployer l'API par le workflow SFTP existant et publier Pages. Conserver clé privée et état des quotas. Le helper privé doit être restauré avec l'API ; une restauration du seul fichier public est insuffisante. Vérifier GET 405/Allow POST, le protocole de la version restaurée et le parcours complet. Ne pas exposer la configuration privée ni désactiver la vérification de clé SFTP.

## Limites
La case et sa position variable ne prouvent pas l'humanité d'un visiteur ; il s'agit d'une confirmation déclarative, complétée par les quotas serveur. Pas de prestataire tiers ni coût ajouté. Recette responsive simulée et deux moteurs ; contrôle sur téléphone physique et lecteur d'écran réel restant à réaliser. SMTP inchangé et vérifié dans les livraisons précédentes ; la réception d'un nouvel email V3 n'est pas revendiquée. Les points antérieurs de MINUTE et les exclusions légales restent suivis.
