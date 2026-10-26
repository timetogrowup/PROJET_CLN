# MINUTE — CLN Performance
**Photographie métier et technique du projet**  
**Date : 26 octobre 2026**  
**Version : 1.0**  
**Référentiel :** dépôt `timetogrowup/PROJET_CLN`, branche `main`  
**Site :** https://cln-performance.com

> Document de reprise du projet. Les états sont distingués entre **confirmé**, **observé dans le code**, **à vérifier** et **à faire**. Toute nouvelle MINUTE doit dater les faits, les décisions et les changements.

## 1. Synthèse exécutive
CLN Performance dispose d'un site vitrine opérationnel, publié sur **GitHub Pages** sous le domaine **cln-performance.com**, avec navigation, pages métier, formulaire de contact et questionnaire de pré-diagnostic. Le parcours de consultation a été testé manuellement avec succès le 26/10/2026 : Solutions, Notre approche, Réalisations (images comprises), Diagnostic (recommandation calculée), Contact (formulaire affiché).

**Point bloquant pour la mise en relation commerciale :** l'envoi du formulaire renvoie **405 Not Allowed**. Le site est servi par GitHub Pages (hébergement statique) alors que l'action du formulaire pointe vers `contact.php` : GitHub Pages n'exécute pas PHP.

Une offre d'hébergement **OVHcloud Starter** est désormais affichée **active**, avec **PHP 8.4** et **1 Go** d'espace. Le pack de messagerie inclus n'est pas encore actif (statut **« Adresses e-mails : Inactif »** observé lors de la dernière vérification). La prochaine étape est son activation et la création de la boîte officielle **contact@cln-performance.com**.

**Décision d'architecture provisoire :** ne pas interrompre GitHub Pages, préparer le traitement PHP sur OVHcloud, idéalement sur un sous-domaine technique dédié après configuration et tests. Aucun basculement DNS de la partie web n'est autorisé tant que l'environnement de réception n'est pas testé.

## 2. Objectifs métier
- Présenter CLN, sa proposition de valeur « Ciblé · Libéré · Normé », ses solutions, son approche et ses réalisations.
- Susciter des contacts commerciaux et des demandes de rendez-vous.
- Qualifier le besoin d'un prospect avec un questionnaire de pré-diagnostic, produire une recommandation synthétique et la reprendre dans le parcours Contact.
- Fournir un point d'entrée professionnel crédible, accessible sur le nouveau nom de domaine.

### Parcours utilisateur cible
Visite → consultation des offres → diagnostic facultatif → recommandation personnalisée → formulaire → confirmation réelle de l'envoi → notification reçue par CLN → prise de contact commerciale.

### Réalisé et validé côté métier
| Fonction | État au 26/10/2026 | Preuve / limite |
| --- | --- | --- |
| Page d'accueil et identité visuelle | Confirmé | Capture de la page de production |
| Page Solutions | Confirmé | Test manuel utilisateur : OK |
| Page Notre approche | Confirmé | Test manuel utilisateur : OK |
| Page Réalisations et images | Confirmé | Test manuel utilisateur : OK |
| Questionnaire / recommandation | Confirmé pour scénario essayé | Test manuel utilisateur : OK ; cas limites non testés |
| Affichage page Contact | Confirmé | Test manuel utilisateur : OK |
| Transmission de la demande | **Bloqué** | Erreur 405 constatée sur capture |
| Réception d'email / prise en charge commerciale | Non validé | Impossible tant que l'envoi échoue |

## 3. Inventaire technique et déploiement
- **GitHub :** `https://github.com/timetogrowup/PROJET_CLN`, branche `main`.
- **Source :** pages `index.html`, `solutions.html`, `approche.html`, `realisations.html`, `diagnostic.html`, `contact.html`, `merci.html`, styles `styles.css`, images et logo.
- **Domaine public :** `cln-performance.com`. Domaine personnalisé renseigné dans les paramètres GitHub Pages ; capture « DNS check successful » et déploiement GitHub Pages.
- **Fichier `CNAME` :** contient `cln-performance.com`.
- **Site en production actuellement :** GitHub Pages ; HTTPS visible dans le navigateur, mais renouvellement, www, redirections et politique de sécurité non audités.
- **Traitement de formulaire existant dans le dépôt :** `contact.html` soumet en POST vers `contact.php`; script PHP vérifie les champs puis utilise `mail()`. Une page `merci.html` existe.
- **Diagnostic :** logique en JavaScript côté navigateur ; conservation temporaire de la recommandation dans `localStorage` (`clnRecommendation`), puis reprise sur la page Contact. Aucun stockage serveur de diagnostic établi.
- **OVHcloud Starter :** service « Actif » vu en console ; PHP global 8.4 ; 1 000 Mo annoncés ; hôte technique affiché `nkzkafh.cluster129.hosting.ovh.net`. Hébergement distinct du GitHub Pages en production.
- **Messagerie OVHcloud :** entrée MX Plan pour `cln-performance.com` visible mais impossibilité initiale de créer un compte. Assistant d'activation du pack email accessible depuis l'hébergement ; retour à « Adresses e-mails : Inactif » à la dernière capture. Activation non confirmée.
- **Documents historiques :** `README.md` décrit encore Hostinger / `cln-solutions.fr` et un ancien processus de déploiement. **Obsolète pour l'architecture actuellement observée** : à réviser sans effacer l'historique utile.

## 4. Anomalies et risques
| ID | Priorité | État | Description / conséquence |
| --- | --- | --- | --- |
| A01 | Critique | Confirmé | Formulaire POST → `contact.php` sur GitHub Pages : 405, aucune demande transmise |
| A02 | Haute | Confirmé | Messagerie officielle `contact@cln-performance.com` pas encore créée / validée |
| A03 | Haute | Observé dans le code | Adresse destinataire et affichée encore en `@cln-solutions.fr` ; textes PHP mentionnent l'ancien domaine |
| A04 | Haute | Observé dans le code | Numéro `+33 7 00 00 00 00` à confirmer ou retirer ; identifiant LinkedIn également à vérifier |
| A05 | Haute | Observé dans le code | Lien « Mentions légales » = `#` ; page dédiée non trouvée au chemin habituel |
| A06 | Haute | À tester | Sécurité du formulaire : antispam, abus, rate limiting, CSRF selon architecture, consentement, protection des données, configuration serveur |
| A07 | Moyenne | À tester | Tests mobile, accessibilité, SEO, vitesse, liens morts, 404, www/HTTPS, configuration DNS et MX/SPF/DKIM/DMARC |
| A08 | Moyenne | Observé | Documentation README et éventuelle automatisation Hostinger à rationaliser ; éviter tout déploiement vers l'ancien prestataire |

## 5. Décisions actées
1. Conserver **GitHub** comme référentiel du code et de la documentation.
2. Domaine public **cln-performance.com**.
3. Garder le site **GitHub Pages** en ligne durant la préparation de la solution OVHcloud.
4. Choisir **OVHcloud** plutôt qu'un prestataire tiers de formulaires (ex. Formspree) pour le traitement des demandes.
5. Utiliser **contact@cln-performance.com** comme adresse officielle souhaitée.
6. Reporter toute intervention réseau en production jusqu'à validation du schéma technique, des certificats et des essais.

## 6. Plan d'action priorisé
### P0 — Réparer la chaîne de contact (bloquant)
- [ ] Attendre / vérifier l'activation effective du pack d'emails associé au Starter ; ouvrir la rubrique Emails, vérifier disponibilité des comptes.
- [ ] Créer `contact@cln-performance.com`, définir les accès de manière sécurisée et tester réception + émission.
- [ ] Relever l'état des enregistrements DNS actuels avant tout changement (web et mail), notamment MX, SPF, DKIM, DMARC.
- [ ] Concevoir le point de terminaison OVHcloud (ex. `api.cln-performance.com/contact.php`) : sous-domaine, configuration multisite OVH, DNS spécifique, certificat TLS et validation du fonctionnement PHP. **Le sous-domaine n'est pas encore créé.**
- [ ] Corriger le formulaire HTML pour viser le service OVHcloud : validation, redirections et réponse appropriées entre origines ; anticiper CORS si requête JavaScript, ou utiliser une soumission HTML classique avec une page de confirmation compatible.
- [ ] Implémenter le traitement serveur sécurisé : filtrage, protection antispam, limites de taille, journalisation minimale, envoi fiable avec en-têtes appropriés ; privilégier SMTP authentifié si disponible/approprié plutôt que supposer `mail()` opérationnel.
- [ ] Faire tests de bout en bout : succès reçu, erreur de champs, indisponibilité, spam, confirmation affichée seulement lorsque l'envoi est réellement accepté, contrôle en boîte destinataire.
- [ ] Déployer de façon réversible sans changer les entrées A/CNAME du site public tant qu'elles servent GitHub Pages.

### P1 — Fiabilisation / conformité
- [ ] Mettre à jour tous les emails et mentions `cln-solutions.fr`, et confirmer les coordonnées de contact.
- [ ] Rédiger mentions légales + politique de confidentialité : identité de l'éditeur, hébergeurs, finalités et durées de conservation des contacts, droits RGPD, consentement.
- [ ] Tester affichages mobile/tablette, navigation clavier, contrastes, formulaires et messages d'erreur.
- [ ] Auditer DNS/SSL, redirections, accessibilité des pages, erreurs 404, référencement (titres, descriptions, robots/sitemap selon besoin).
- [ ] Contrôler le stockage `localStorage` du diagnostic, la minimisation des données et la sécurité des contenus injectés dans le DOM.
- [ ] Actualiser `README.md` et les workflows pour refléter la production GitHub Pages et le service OVHcloud ; neutraliser la dépendance documentaire à Hostinger.

### P2 — Évolutions métier
- [ ] Mesurer les conversions visite → diagnostic → contact sans collecter de données non nécessaires.
- [ ] Formaliser les étapes de prise en charge d'une demande, délai de réponse et suivi commercial.
- [ ] Étudier prise de rendez-vous, suivi des prospects et amélioration de la recommandation, après fiabilisation du formulaire.

## 7. Vérifications restant ouvertes / critères d'acceptation
**Go pour le formulaire seulement si :** l'email officiel existe, les DNS mail sont cohérents, l'endpoint OVHcloud est accessible en HTTPS, le POST fonctionne, l'email parvient à la boîte (et ses réponses reviennent au prospect), les erreurs sont compréhensibles, l'antispam est en place et le site actuel reste accessible.

**Go pour une migration intégrale éventuelle seulement si :** décision métier explicite, copie de sauvegarde, tests du site sur OVHcloud, plan de retour arrière, DNS maîtrisés. Cette migration n'est **pas décidée**.

## 8. Situation administrative connue
- Une commande Starter de **22,90 € TTC** a initialement été observée « Validation » le 26/10/2026 ; une capture ultérieure confirme le service Starter « Actif ». 
- Le pack email est encore montré « Inactif » à la dernière capture ; son statut réel est à revérifier après propagation/provisionnement.
- Ne pas conserver ici d'identifiants secrets, mots de passe SMTP/FTP ou données personnelles saisies lors des essais.

## 9. Instructions de reprise
À la prochaine session :
1. Ouvrir cette MINUTE avant toute modification.
2. Vérifier l'activation des emails et la boîte `contact@cln-performance.com`.
3. Inspecter la configuration OVHcloud et choisir l'endpoint PHP isolé.
4. Mettre au point les tests, déployer la correction, vérifier la réception réelle.
5. Mettre à jour la présente MINUTE : nouvelle date, résultats factuels, décisions, anomalies résolues, points ouverts et liens vers commits.

**Statut global : site vitrine consultable ; fonction commerciale de contact non opérationnelle ; infrastructure OVHcloud de remplacement partiellement disponible.**
