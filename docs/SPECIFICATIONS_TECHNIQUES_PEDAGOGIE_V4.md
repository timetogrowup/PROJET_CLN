# Spécifications techniques V4 — Parcours pédagogique CLN

Date : 29 octobre 2026. Statut initial : à implémenter puis compléter par le rapport de recette V4.

## Architecture et déploiement

Conserver HTML/CSS/JavaScript sans compilation, à la racine de main, CNAME cln-performance.com et publication GitHub Pages existante. API contact.php sur api.cln-performance.com chez OVHcloud inchangée. Les documents Markdown et les tests sont versionnés dans le même dépôt ; ils ne nécessitent pas d’exécution serveur.

## Composants

Neuf pages publiques : six principales, deux légales et merci. Le générateur Python scripts/build_pedagogy.py produit les blocs éditoriaux des six pages, leur en-tête/pied commun et les ajouts au catalogue. Les pages restent complètes en français sans rendu JavaScript des contenus éditoriaux. site.js conserve la sélection de langue, la traduction des textes statiques et les liens internes. Styles additionnels responsive et focus, liens d’évitement, sections ancrées et details/summary natifs.

diagnostic.js fournit l’orientation V4 et son affichage ; il initialise ses fonctions de synthèse même sur contact.html. contact.js garde la machine d’état et les protections V3. Son adaptation limite l’import de synthèse aux actions explicites et ajoute la prise en compte d’un paramètre de besoin autorisé. Pas de changement des noms, types, limites et action du formulaire serveur.

## Données et interfaces

Réponse V4 : {version:4, generatedAt:date ISO, answers:{problems:string[], frequency:string, people:string, impacts:string[], tools:string[], goal:string, horizon:string}}. Les valeurs sont des codes fermés ; pas de HTML issu de saisie utilisateur. La sélection « inconnu » ou « aucun outil précisé » reste possible. Affichage avec textContent et création d’éléments, pas d’innerHTML utilisateur.

Clé clnRecommendation : enregistrement uniquement au clic « transmettre ma synthèse » ; expiration existante de trente jours, lecture protégée contre JSON/date invalides et stockage indisponible. La synthèse n’est lue par contact que si summary=1 ; elle n’est pas ajoutée automatiquement au message. Le bouton d’ajout est désactivé après utilisation et n’écrase jamais un message existant. Effacer retire seulement le texte prérempli s’il n’a pas été modifié. Le brouillon sessionStorage existant reste conservé trente minutes selon V3. Les formats anciens sont reconnus et renvoyés au questionnaire sans recalcul V4.

Paramètre need : ressaisies, repetitif, chiffres ou suivi ; toute autre valeur ignorée. Liste modifiable sur contact. Changer la liste ne modifie pas le message ; ajouter le contexte est une action distincte. Aucune donnée libre dans l’URL. Les langues fr, en, pt-BR et es restent portées par lang et le catalogue ; les chaînes V4 sont traduites dans les quatre langues. Les réponses sont des codes, la synthèse est régénérée dans la langue choisie.

Le questionnaire n’envoie rien au serveur. Seule la validation finale du formulaire entraîne le POST serveur existant, précédé du contrôle humain V3. Les essais de formulaire isolent l’API et interceptent l’envoi pour ne pas transmettre de message.

## Contraintes et sécurité

Préserver API, jeton à usage unique, durée, anti-rejeu, limitation de débit, CORS et consentement existants. Aucun secret ajouté au dépôt. Pas de dépendance de production nouvelle. Liens relatifs compatibles racine et Pages. Versionner CSS et JS pour limiter les anciens fichiers en cache. Ne pas transformer des coûts récurrents tiers en promesse d’absence totale de coût. Pages légales : décrire le stockage effectif, sans prétendre à une nouvelle certification de conformité.

## Modalités de test

- Syntaxe JavaScript, PHP existant et catalogues complets ; vérifier les placeholders et la couverture des chaînes nouvelles.
- Liens HTML, fichiers et ancres ; un seul h1 par page ; libellés et descriptions.
- Tests d’orientation : problème unique, multiples, inconnus, données invalides ; labels lisibles ; pas d’exécution HTML.
- Parcours navigateur : questionnaire, affichage sans coordonnées, absence de sauvegarde avant choix, transfert choisi, ajout puis effacement, préservation du brouillon et changement de langue.
- Matrice quatre langues, neuf pages, largeurs 320, 390, 768, 1024 et 1280 px sur Chromium et WebKit ; contrôler menu et détails.
- Régression fenêtre humaine V3 et sécurité PHP/API locale ; pas de mail réel ni résolution d’un CAPTCHA en production.
- Après publication : statut Pages du commit et GET des pages/JS/CSS ; vérification du discours et du questionnaire sur le domaine. Enregistrer les limites et résultats exacts dans RECETTE_PEDAGOGIE_V4.md.

## Retour arrière

Créer un commit correctif rétablissant uniquement les fichiers V4 depuis le parent de livraison, sans réinitialiser la branche ni écraser d’autres travaux. Une panne d’API externe n’est pas une preuve de régression éditoriale ; documenter séparément.
