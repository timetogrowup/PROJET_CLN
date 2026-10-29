# Spécifications techniques V5 — Présentation des pipelines

Date : 29 octobre 2026. Statut : conception avant réalisation. Complément des spécifications V4, sans changement de l’architecture de production.

## Architecture et composants

HTML/CSS/JavaScript statiques sur GitHub Pages, domaine cln-performance.com et branche main ; API contact.php OVHcloud V3 inchangée. Nouvelle page pipelines.html avec canonique propre et métadonnées traduites. Aucun nouveau script de production ni dépendance externe.

scripts/build_pedagogy.py reste le point de génération commun. Un module scripts/pipeline_content.py contient les blocs éditoriaux V5, en quatre langues, et retourne le corps de la page dédiée ainsi que les blocs Accueil, Besoins, Méthode et Exemples. Il utilise les fonctions de titres, paragraphes et liens existantes. Le générateur inclut le septième lien de menu, appelle le module, produit la nouvelle page et sauvegarde le catalogue enrichi. Un squelette HTML complet est créé si la nouvelle page est absente ; les pages historiques ne sont pas dupliquées.

styles.css reçoit des classes limitées au bloc et aux étapes de pipeline. Une liste ordonnée de cinq étapes constitue la représentation visuelle ; elle s’empile sur petit écran et porte un sens sans CSS. Les exceptions sont présentées dans des éléments details/summary natifs, utilisables au clavier. Tous les contenus essentiels restent lisibles sans ouverture des compléments.

## Données et interfaces

Les données ajoutées sont uniquement éditoriales : tuples de textes français, anglais, portugais brésilien et espagnol. Les clés statiques suivent le mécanisme V4 ; aucun texte utilisateur et aucune donnée métier réelle. Pas de nouvelle clé de stockage local ni de POST, fetch ou interface serveur pour le pipeline illustratif.

Liens : index.html#pipelines vers pipelines.html ; solutions.html#bout-en-bout vers la même page ; approche.html#pipeline vers la méthode de mesure et approche.html#remuneration ; realisations.html vers la page dédiée ; CTA final vers contact.html. Les liens internes conservent la langue via site.js. Le sitemap inclut pipelines.html.

Les scripts partagés reçoivent une version de cache V5 dans le HTML, sans changement de leur logique. Les neuf pages antérieures gardent leurs URL et données. Aucun changement du format de synthèse V4, du préremplissage volontaire, des protections anti-rejeu ou du transport SMTP.

## Contraintes

La reprise est expliquée comme conditionnelle aux contrôles et aux règles définies, avec validation humaine pour les cas sensibles. Ne pas confondre capacités proposées et fonctionnalités d’un produit déjà connecté au client. Aucun indicateur illustratif chiffré ne devient une mesure commerciale réelle.

Conserver navigation et identité visuelle V4 ; sept liens peuvent se répartir sur plusieurs lignes. Pas de bandeau envahissant ni d’animation obligatoire. Lisibilité à 320 px, focus visible, cibles tactiles et titres hiérarchisés. Préserver les mentions légales et la politique actuelle, sans nouvelle revendication juridique.

## Tests

- Syntaxe, quatre langues et placeholders ; traduction de tous les nouveaux textes visibles, titres, descriptions et libellés.
- Dix pages, menu cohérent à sept liens et bon état actif ; liens locaux, ancres et sitemap ; unicité des scripts et génération déterministe.
- Tests de structure et de contenu : définition accessible, cinq étapes, capacités, exceptions, rôle humain et mesure ; nouveau parcours accueil → pipelines → méthode/contact dans les quatre langues.
- Matrice existante étendue : dix pages × quatre langues × cinq largeurs × Chromium/WebKit = 400 affichages. Régression questionnaire V4 et dialogue V3.
- Sécurité PHP et tests HTTP existants, toujours sans mail réel. Aucun test ne doit récupérer de données d’un vrai client.
- Après publication : succès Pages du commit, comparaison des fichiers servis avec les sources, lecture de la page publique, ouverture d’un complément et navigation. Distinguer tests simulés et validation par prospects.

## Livraison et retour arrière

Documents préalables enregistrés avant développement ; code et tests sur feature/cln-v5-pipelines ; promotion de main après contrôles réussis avec vérification du parent. Retour arrière par commit correctif limité aux fichiers V5, sans réinitialisation de l’historique ni retrait des travaux concurrents. Résultats et limites dans RECETTE_PIPELINES_V5.md et MINUTE.md.
