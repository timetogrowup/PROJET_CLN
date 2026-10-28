# Expression du besoin — Site CLN Performance multilingue

Statut : besoin fonctionnel, à décliner en spécification technique avant développement. Aucun code modifié à cette étape.

## 1. Objectif

Permettre au visiteur de consulter l'ensemble du site CLN Performance dans la langue de son choix, avec une présentation cohérente et sans mélange de langues.

## 2. Langues disponibles

| Langue | Libellé dans le sélecteur | Identifiant de référence |
| --- | --- | --- |
| Français | Français | fr |
| Anglais | English | en |
| Portugais du Brésil | Português (Brasil) | pt-BR |
| Espagnol | Español | es |

Le français est la langue par défaut. Lors d'une première visite sans choix explicite, le site s'affiche en français, quelle que soit la langue du navigateur. Une langue non reconnue conduit à un affichage en français.

Le portugais doit employer le vocabulaire et les usages du Brésil, et non ceux du Portugal.

## 3. Sélecteur de langue

- Un petit sélecteur de langue est placé en haut de la page d'accueil, dès le premier écran.
- Il est identifiable, compact, lisible sur ordinateur et mobile, et ne masque ni le logo ni la navigation.
- Chaque langue porte son nom dans sa propre langue, sans dépendre uniquement de drapeaux ou d'abréviations.
- Le français est sélectionné initialement.
- Le sélecteur est utilisable au clavier et avec un lecteur d'écran ; la langue active est identifiable.
- Le changement s'applique à la page courante sans demander de confirmation.

Proposition de cohérence pour les autres pages : reprendre ce même petit sélecteur dans l'en-tête commun, afin de permettre un changement sans retour obligatoire à l'accueil. Le besoin minimal impératif reste sa présence en haut de l'accueil.

## 4. Continuité de navigation

- Après un choix, toutes les pages ouvertes dans le parcours du visiteur utilisent cette langue.
- Les liens de navigation, le retour à l'accueil, les liens légaux et la page de confirmation conservent ce choix.
- Un rechargement de page ne remet pas arbitrairement le site en français.
- Le dernier choix est mémorisé dans le navigateur pour les visites suivantes ; en l'absence de préférence disponible, le français s'applique.
- Si la mémorisation locale est indisponible, le changement reste utilisable et le choix est conservé autant que possible pendant la navigation.
- Le dispositif et la durée de mémorisation sont précisés dans la conception technique et l'information de confidentialité.
- Le changement de langue conserve les champs déjà saisis, les réponses au diagnostic et leur ordre de priorité. Il ne déclenche aucun envoi de formulaire.

## 5. Périmètre des traductions

Tous les textes destinés au visiteur doivent être disponibles dans les quatre langues :

- Accueil, solutions, approche et réalisations.
- Navigation, titres, sous-titres, paragraphes, cartes, boutons et pied de page.
- Questionnaire : questions, réponses proposées, aides, classement des priorités et compteurs de sélection.
- Résultats du diagnostic : profils, recommandations, priorités, horizons, étapes suivantes et synthèse transférée vers Contact.
- Formulaire : libellés, exemples, caractère obligatoire/facultatif, case de confidentialité et explications.
- Captcha simple : consigne, renouvellement, réponse absente ou incorrecte et expiration.
- Messages liés aux limitations par IP ou email, temps d'attente et nombre d'unités.
- Erreurs de validation, indisponibilités du service et échecs d'envoi, y compris ceux provenant du serveur.
- Page de confirmation et textes d'erreur accessibles dans le parcours.
- Mentions légales et politique de confidentialité, avec le même périmètre d'informations publiées que la version française.
- Textes alternatifs des images, noms accessibles, titres de page et descriptions utilisées pour le référencement.

Les adresses email, liens de contact, numéros d'identification, montants du capital, coordonnées et noms propres restent exacts dans toutes les langues. Ils ne sont pas remplacés par des exemples fictifs.

Les textes saisis librement par le visiteur ne sont pas traduits automatiquement. Une demande en langue étrangère n'est pas reformulée à son insu.

Les chiffres, pluriels, dates et durées sont présentés de manière adaptée à la langue choisie, sans modifier leur valeur.

## 6. Diagnostic et contact

- Les règles de calcul et les résultats métier du diagnostic sont identiques dans toutes les langues ; seul leur affichage change.
- Une recommandation déjà calculée peut être affichée dans une autre langue sans refaire le questionnaire.
- Le transfert vers Contact respecte la langue courante.
- Les parties libres saisies ou modifiées par l'utilisateur sont préservées lors d'un changement de langue.
- Une ancienne synthèse conservée dans le navigateur ne provoque pas un mélange de langues ; une compatibilité ou une invitation claire à recalculer est prévue.
- La langue choisie est transmise avec la demande afin que CLN identifie la langue souhaitée pour la réponse.
- Les confirmations et erreurs du serveur reviennent dans la langue utilisée pour l'envoi.
- Les contrôles de sécurité, quotas, destinataire et transport SMTP restent les mêmes quelle que soit la langue ; changer de langue ne réinitialise pas les limites d'envoi.

## 7. Qualité et exploitation

- Une base complète de traductions est préparée et relue pour les quatre langues avant mise en service.
- Les formulations sont adaptées au contexte professionnel et aux usages locaux, sans traduction mot à mot maladroite.
- Toute modification ultérieure d'un texte doit entraîner la mise à jour de ses quatre versions.
- Une traduction manquante est détectée lors des vérifications avant publication ; le français sert de repli contrôlé en cas d'anomalie imprévue.
- Les textes plus longs ne provoquent ni troncature, ni débordement, ni bouton inutilisable.
- La langue du document est correctement déclarée pour les technologies d'assistance.
- Les traductions légales doivent être fidèles au périmètre du français ; la traduction ne constitue pas une validation de conformité juridique.

## 8. Critères de validation

1. Première visite sans préférence : site en français.
2. Le sélecteur de l'accueil propose exactement Français, English, Português (Brasil), Español.
3. Chaque sélection traduit l'ensemble des textes affichés, y compris les textes d'accessibilité.
4. La langue est conservée lors de la navigation et du rechargement.
5. La préférence est reprise lors d'une visite suivante dans le même navigateur, si sa mémorisation est disponible.
6. Changer de langue pendant un diagnostic conserve les réponses et ne modifie pas la recommandation métier.
7. Changer de langue dans Contact conserve le message et les autres champs sans envoyer la demande.
8. Les erreurs, le captcha, les délais de blocage et la confirmation utilisent la langue courante.
9. La langue est identifiable dans la demande reçue par CLN ; le message libre reste inchangé.
10. Les limitations de fréquence et les protections serveur ne peuvent pas être contournées en changeant de langue.
11. Aucune clé de traduction ni variable technique n'est affichée au visiteur.
12. Le parcours est vérifié dans les quatre langues sur ordinateur, mobile et tablette.

## 9. Articulation avec le besoin de protection

Ce besoin complète docs/BESOIN_CAPTCHA_LIMITATION_EMAIL.md. La conception technique doit prévoir dès le départ la traduction du captcha et des messages de limitation par email, afin d'éviter une interface multilingue partielle.

## Étape suivante

Préparer la spécification technique du multilingue, la liste exhaustive des textes et le référentiel des traductions. Le présent document n'autorise pas à présenter les traductions comme réalisées ou le sélecteur comme déjà déployé.
