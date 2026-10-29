# Recette et livraison V5 — Pipelines en action

Date : 29 octobre 2026. Statut : livré et vérifié en production.

## Périmètre réalisé

- Nouveau bloc immédiatement après la présentation de l’accueil : définition des pipelines, cinq étapes et lien vers l’exemple.
- Nouvelle page pipelines.html : réception, contrôle, traitement, transmission et suivi d’une demande reçue par email ; quatre capacités, quatre cas de parcours et rôle humain explicite.
- Liens et explications dans Vos besoins, Comment nous travaillons et Exemples concrets. Articulation avec la mesure avant/après, l’autonomie et la rémunération liée aux bénéfices effectivement constatés.
- Menu de sept liens sur dix pages, quatre langues, métadonnées et sitemap actualisés. Nouvelle page éditoriale statique ; aucun pipeline réel exécuté ni nouvelle donnée collectée.
- Comportement du questionnaire V4 et du formulaire V3 conservé ; aucun redéploiement OVH nécessaire.

## Sources et contrôles

Documents préalables : commit 77bd27c165633e1f34f6480b53187c3f2a0de399.
Code candidat : 57a238e1d1ef8e0e67abee07a3c832b63f570dc2.
Exécution de vérification : https://github.com/timetogrowup/PROJET_CLN/actions/runs/40868321448.

| Contrôle | Résultat |
|---|---|
| Liens, ancres et métadonnées | Dix pages, 195 références locales ; cibles d’évitement et traductions visibles contrôlées |
| Structure V5 | Sept liens de menu, nouvelle page, cinq étapes, quatre capacités et quatre compléments, ancres et sitemap vérifiés |
| Catalogues | 443 textes statiques, 133 messages ; quatre langues et placeholders complets |
| Génération | Deux exécutions successives produisent les mêmes fichiers |
| Prévisualisation | Bloc d’accueil, menu, page dédiée et ouverture du complément sur l’incident observés dans le navigateur |
| Sécurité et HTTP V3 | 26 contrôles de sécurité, tests HTTP et dialogue humain sur deux moteurs réussis |
| Matrice responsive | 400 affichages réussis : dix pages × quatre langues × cinq largeurs × deux moteurs |
| Parcours V4 | 42 assertions réussies sur deux moteurs |
| Parcours V5 | 84 assertions réussies : étapes, capacités, clavier, langues, navigation, méthode, contact et absence de requêtes tierces |

## Anomalie corrigée

Les tests de structure ont détecté que les nouveaux blocs n’étaient pas réinjectés dans les pages existantes : le générateur attendait une balise main sans attribut, alors que les pages V4 avaient un identifiant. La substitution accepte maintenant les attributs de main. Les tests vérifient la présence effective des ancres et des blocs, et la stabilité de la régénération. Le défaut n’a pas été publié.

## Limites

Les scénarios sont illustratifs et les bénéfices sont à mesurer en mission. Pas de pipeline connecté à des logiciels clients, de données clients lues, de nouveau contrat ou de calcul automatique de rémunération. Aucun mail réel envoyé pendant la recette. Les essais sur téléphones physiques, lecteur d’écran et nouveaux lecteurs restent à réaliser ; une validation technique ne prouve pas la compréhension commerciale.

## Publication

Code livré sur main : [57a238e1d1ef8e0e67abee07a3c832b63f570dc2](https://github.com/timetogrowup/PROJET_CLN/commit/57a238e1d1ef8e0e67abee07a3c832b63f570dc2).

[Publication GitHub Pages 40868687159](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40868687159) réussie. Nouvelle page : https://cln-performance.com/pipelines.html.

Dix pages, trois scripts, une feuille de styles, deux catalogues et le sitemap, soit dix-sept ressources, ont été contrôlés en HTTPS normal avec paramètre de version et Cache-Control no-cache. Tous répondent HTTP 200 et correspondent octet par octet aux sources V5 testées.

Parcours public observé dans le navigateur : nouvelle page, cinq étapes, ouverture du complément sur un outil indisponible, puis lien vers la méthode et la rémunération. Aucune soumission de formulaire ni lecture de données client. Capture de la page publique conservée pour remise à Patrick.

Les documents de clôture sont versionnés après ce constat, sans changement des sources exécutables. La promotion de main utilise le commit précédent attendu, sans force ni réécriture d’historique.

La CI du commit 57a238e1d1ef8e0e67abee07a3c832b63f570dc2 est entièrement réussie. Aucune modification des sources exécutables ne sera ajoutée par la clôture documentaire.

## Critères d’acceptation

P01 à P10 : périmètre réalisé et vérifications techniques réussies. Les mesures de compréhension et de différenciation auprès de prospects ne sont pas déduites de ces résultats ; elles restent à mener avec de nouveaux lecteurs.
