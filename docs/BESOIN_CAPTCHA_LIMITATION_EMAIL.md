# Expression du besoin — Protection du formulaire CLN Performance

Statut : proposition fonctionnelle à valider avant développement. Aucun changement du formulaire dans ce document.

## Objectif

Réduire les soumissions automatisées et les envois répétés avec une même adresse email, tout en conservant un formulaire simple, accessible et utilisable sur mobile.

Ces protections complètent le champ piège et la limitation par adresse IP déjà présents.

## 1. Vérification simple avant envoi

Le visiteur doit répondre à une question de calcul élémentaire, par exemple « Combien font 3 + 4 ? », avant de pouvoir envoyer sa demande.

- Question en texte, lisible par les lecteurs d'écran et utilisable au clavier.
- Calcul court, sans ambiguïté, sans image à déchiffrer ni création de compte.
- Possibilité de demander une autre question sans effacer les autres champs.
- Validité proposée : 10 minutes. Une question expirée est remplacée et une explication est affichée.
- Vérification obligatoire côté serveur : modifier la page ou envoyer une requête directe ne permet pas de contourner le contrôle.
- Une réponse validée ne peut servir qu'à un seul envoi.
- Une réponse absente, incorrecte ou expirée n'entraîne aucun envoi de mail.

Message proposé : « La réponse au contrôle de sécurité est incorrecte ou a expiré. Veuillez répondre à la nouvelle question. »

Ce contrôle simple constitue une protection complémentaire ; il n'est pas présenté comme une garantie d'identification humaine.

## 2. Limitation des demandes par adresse email

La fréquence est contrôlée pour l'adresse email de contact renseignée dans le formulaire.

Paramètres proposés, ajustables ultérieurement :
- Un délai minimum de **10 minutes entre deux demandes prises en charge** pour une même adresse.
- Un maximum de **3 demandes prises en charge sur toute période glissante de 60 minutes** pour cette adresse.
- Si plusieurs limites s'appliquent, la date du prochain envoi autorisé tient compte de toutes les limites.

Le contrôle s'applique même si le visiteur change de navigateur, efface son stockage local ou utilise un autre réseau.

Les espaces en début et fin sont ignorés et les différences de majuscules/minuscules ne créent pas une nouvelle adresse pour le contrôle. Les points et les suffixes « + » ne sont pas supprimés arbitrairement. Cette règle limite une adresse saisie, sans prétendre identifier une personne ni empêcher l'utilisation de plusieurs adresses.

Message proposé : « Veuillez patienter avant un nouvel envoi avec cette adresse email. Vous pourrez réessayer dans environ X minutes. »

Le délai affiché correspond au temps réellement restant, arrondi à la minute supérieure.

## 3. Comportement attendu

- Les contrôles s'effectuent avant l'envoi de l'email.
- Un captcha incorrect ou un formulaire invalide ne consomme pas le quota des demandes prises en charge.
- Une demande est comptabilisée lorsque le serveur SMTP accepte le message. Une panne certaine avant cette acceptation ne consomme pas ce quota.
- L'acceptation SMTP n'est pas présentée comme une preuve de livraison dans la boîte destinataire.
- Un double clic, une actualisation ou deux soumissions simultanées ne doivent pas permettre un doublon ou le contournement du délai.
- Les données saisies restent disponibles pour correction en cas d'échec, sans les placer dans l'URL ni dans des journaux.
- Un succès affiche la confirmation existante. Un refus ou une panne affiche un message clair, jamais un faux succès.
- Aucun renvoi automatique d'une demande refusée n'est réalisé.

## 4. Données et exploitation

- Les compteurs sont gérés côté serveur et restent efficaces sans stockage local du navigateur.
- Le dispositif de limitation évite de conserver une copie en clair de l'adresse email uniquement pour ce contrôle ; il conserve un identifiant protégé et le minimum d'horodatages nécessaires.
- Les traces propres à cette limitation sont supprimées automatiquement à l'expiration de leur utilité.
- Aucun contenu du message ni mot de passe n'est conservé dans les compteurs.
- La politique de confidentialité est actualisée pour expliquer cette protection.
- Les protections existantes par IP et champ piège restent actives. Les limites par IP peuvent également s'appliquer même si l'adresse email n'a pas atteint son quota.
- Le captcha ne nécessite pas de service tiers ni de nouvelle collecte publicitaire.

## 5. Critères de validation

1. Réponse correcte et adresse autorisée : une seule demande est prise en charge.
2. Réponse absente, fausse, expirée ou déjà utilisée : aucun email envoyé.
3. Nouvelle demande avant 10 minutes avec la même adresse : refus et délai restant correct.
4. Nouvelle demande après 10 minutes, sous le plafond horaire : acceptation.
5. Quatrième demande dans une fenêtre glissante de 60 minutes : refus, même si 10 minutes se sont écoulées.
6. Une variation de casse ou des espaces périphériques ne contournent pas la limite.
7. Changer de navigateur ou de réseau ne contourne pas la limite par email.
8. Deux soumissions simultanées avec la même adresse ne produisent pas deux messages.
9. Une erreur de validation ne pénalise pas le quota des demandes réussies.
10. Le formulaire conserve les saisies utiles après un refus ; la question peut être renouvelée.
11. Les scénarios sont vérifiés sur mobile, au clavier et avec les attributs nécessaires aux technologies d'assistance.
12. Les erreurs du transport mail et les délais d'expiration n'entraînent pas de faux succès ni de renvoi en double.

## Périmètre de cette étape

Formalisation du besoin uniquement. La conception technique et la modification du code feront l'objet de l'étape suivante, après validation des règles proposées.
