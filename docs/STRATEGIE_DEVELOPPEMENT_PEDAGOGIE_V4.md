# Stratégie de développement V4 — Site orienté bénéfices

Date : 29 octobre 2026. Dépendance fonctionnelle : BESOIN_METIER_PEDAGOGIE_BENEFICES_V4.md. Dépendance technique : SPECIFICATIONS_TECHNIQUES_PEDAGOGIE_V4.md.

1. Lire la proposition V2, le dépôt actuel, MINUTE et les tests V3 ; identifier Pages, le backend OVH et les quatre langues. Préserver les fichiers non concernés.
2. Versionner les trois documents avant la réalisation. Définir les critères d’acceptation et les données V4 avant de coder le questionnaire.
3. Créer un générateur éditorial maintenable : contenus traduits, navigation commune, bénéfices, méthode commerciale et exemples illustratifs. Produire les pages en gardant les URL et l’identité graphique existantes.
4. Implémenter le questionnaire quotidien, puis sa synthèse et le transfert explicite. Adapter le contact sans toucher au contrat d’envoi V3. Expliquer le stockage dans Confidentialité.
5. Ajouter les styles responsives et les textes secondaires ; actualiser les métadonnées et les caches. Vérifier les liens et la couverture des traductions.
6. Exécuter syntaxe, catalogues, règles de sécurité et parcours navigateur isolés. Adapter les anciens tests du questionnaire au nouveau besoin ; conserver la régression du contrôle humain. Corriger les échecs et relancer les contrôles affectés.
7. Archiver un rapport de recette avec les résultats réellement observés. Publier la modification sur main par commit sans écraser un éventuel changement concurrent ; attendre la publication Pages.
8. Vérifier le domaine et le parcours de lecture/questionnaire sans envoyer de mail réel. Mettre à jour rapport, documents de référence et MINUTE avec commit, publication, limites et liens. Livrer les liens exacts.

## Dépendances et décisions

Les textes doivent être présents dans les quatre langues avant la publication. Le contact dépend des fonctions de synthèse initialisées par diagnostic.js. Le bouton d’ajout volontaire remplace le préremplissage automatique, donc ses tests doivent évoluer. Le backend OVH n’a pas besoin d’un nouveau déploiement. Aucun chiffre de résultat réel n’est inventé pour remplacer les références non justifiées.

## Sortie attendue

Documents et code versionnés ; tests pertinents verts ; publication Pages vérifiée ; journal reflétant le livré. Si un contrôle nécessite une infrastructure indisponible, le qualifier comme non effectué, sans assimiler cela à une réussite. Les tests humains de compréhension et la réception SMTP ne sont pas déduits de tests automatisés.

## Exécution et ajustements

Documents formalisés et enregistrés avant livraison. Développement et corrections sur feature/cln-v4-benefits, séparés de la production jusqu’à validation. Contrôles PHP et navigateur exécutés par GitHub Actions ; contrôles statiques et prévisualisation exécutés également dans l’environnement de travail. Trois anomalies de génération et de responsive ont été détectées et corrigées. La recette précise les commits, les résultats et la publication finale. Les outils de publication GitHub ont remplacé le push Git local, indisponible faute d’authentification locale ; aucun secret n’a été demandé ni stocké.

Étapes 1 à 8 terminées : recette finale 40863452204 réussie, promotion de main et publication Pages 40863813611 réussies, contrôle HTTP des quinze ressources et parcours public réalisés. Le rapport et MINUTE sont mis à jour après constat de la publication. Aucun changement de source n’a été introduit par la clôture documentaire.
