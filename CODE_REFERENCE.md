# CLN Static Site — Code Reference

Ce document décrit précisément la structure du code, fichier par fichier, afin de faciliter la maintenance et l’évolution du site.

## 1. `styles.css`
- **Variables et base (l.1-48)** : palette de couleurs (`--primary`, `--accent`), police principale (`--font-sans`). Réinitialisation légère avec `box-sizing: border-box`.
- **Typographie et éléments globaux (l.16-67)** : styles de base pour `body`, `a`, `img`.
- **En-tête et navigation (l.34-103)** :
  - `header` sticky avec bordure basse.
  - `.navbar` : conteneur flex, largeur max 1100px.
  - `.brand` : logo + nom, image 42px.
  - `.nav-links` : liens horizontaux, classe `.active` surlignée par bordure verte.
  - `.cta-button` : bouton arrondi commun (couleur accent, hover).
- **Layouts principaux (l.106-188)** :
  - `main` : padding homogène.
  - `.hero` : grid responsive pour sections hero.
  - `.section-title`, `.section-lead` pour titres et accroches.
  - `.card-grid`, `.card`, `.quote-block` : modules de présentation.
- **Composants spécifiques (l.190-263)** :
  - `.timeline`, `.timeline-step` : frise verticale.
  - `.projects-grid`, `.project-card`, `.project-tags` : cartes réalisations.
  - `.tag` : puce thématique.
- **Contact & formulaire (l.265-312)** :
  - `.contact-grid` : grid deux colonnes.
  - `.checkbox` : style consentement.
  - `input`, `textarea` : focus accentué.
- **Pied de page (l.314-336)** : fond sombre, liens blancs atténués.
- **Questionnaire (l.338-356)** :
  - `fieldset`, `legend`, `.helper-text`.
  - `.pill-group`, `.pill` : boutons multi-sélection.
  - `.radio-list` pour radios empilés.
  - `.questionnaire` et `.result-card` : mise en forme du formulaire et de la synthèse.
- **Responsive (l.338-350)** : sous 720px, nav masquée pour laisser place au bouton (menu burger à prévoir si besoin).

## 2. Gabarit HTML commun
Chaque page suit la même structure :
```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>…</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header>…</header>
    <main>…</main>
    <footer>…</footer>
  </body>
</html>
```

- **`header`** : navigation identique sur toutes les pages avec lien actif (`class="active"`). CTA « Être recontacté » pointant vers `contact.html`.
- **`footer`** : bloc commun avec email, lien contact, placeholder mentions légales.

## 3. Pages HTML

### `index.html`
- **Hero** : slogan, titre principal, description et CTA vers `solutions.html`, image illustrative.
- **Section “CLN en trois engagements”** : trois `.card` orientant vers ancres `solutions.html#connecter|#liberer|#normaliser`.
- **Citation** : `.quote-block` reprenant la vision CLN.
- **Section “Pourquoi CLN ?”** : cartes mettant en avant vision alignée, solutions prêtes, accompagnement durable.

### `solutions.html`
- Page axée sur le détail des offres.
- Trois sections distinguées (`id` `connecter`, `liberer`, `normaliser`) chacune emballée dans `.card` avec listes à puces et CTA.
- Titles `h2` explicites pour SEO.

### `approche.html`
- Section “Mission et vision” avec `card-grid`.
- Timeline `div.timeline` listant les quatre étapes (Diagnostic → Accompagnement).
- Citation finale rappelant l’importance des standards.

### `realisations.html`
- `projects-grid` : trois `article.project-card` combinant visuel, résumé et tags.
- Section CTA :
  - Carte “Un projet à partager ?” -> `contact.html`.
  - Carte “Questionnaire de pré-diagnostic” -> `diagnostic.html` (remplace ancien téléchargement).

### `diagnostic.html`
- Formulaire de pré-diagnostic (`form#diagnostic-form`).
- `fieldset` successifs :
  - Sélection multi-choix `modules` (checkbox).
  - Radios `taille`, `delai`, `mode`.
  - `select` `priorite`.
- Bouton “Obtenir ma recommandation”.
- Conteneur `div#diagnostic-resultat` caché (`hidden`) affichant la synthèse.
- Scripts inline :
  - `buildModuleSummary(modules)` : message selon modules cochés.
  - `recommendationFromPriority(priority)` : recommandation par priorité déclarée.
  - `rendezVousMessage(delai, mode)` : message invitant au rendez-vous.
  - Listener `form.addEventListener('submit', …)` : empêche le POST, construit le bloc de synthèse, le rend visible, effectue un scroll doux vers la carte.
- Aucune dépendance externe ; code ES6 simple.

### `contact.html`
- Bloc de coordonnées directes + formulaire.
- Formulaire `POST` vers `contact.php` (traitement PHP local). Champs :
  - `name`, `_replyto` (email), `company`, `message`.
  - Case à cocher `consent` obligatoire pour l’accord RGPD.
- Message d’alerte affiché selon le paramètre de requête `status` (`success`, `invalid`, `error`).

### `merci.html`
- Hero de remerciement + bouton retour accueil.
- Pas de logique supplémentaire.

## 4. Fichiers Média
- `LOGO_CLN.png` : utilisé dans la navigation (42px). 
- `pexels-*.jpg`, `blur-hospital-clinic-interior.jpg` : placés dans les sections hero ou réalisations.
- `ANIMATION_LOGO.py`, `Etude_*`, `TEST.html` etc. : présents mais non utilisés dans les pages principales du site (possible héritage / travail futur).

## 5. Identifiants & Classes Réutilisées
- `.cta-button` : tous les appels à l’action (pensez à mettre à jour si nouvelle couleur).
- `.card` et `.card-grid` : cartes modulaires, utilisées sur plusieurs pages.
- `.section-title`, `.section-lead` : titres et chapeaux cohérents.
- `.nav-links .active` : doit être mis à jour selon la page courante (actuellement géré manuellement dans chaque fichier).
- `.questionnaire` + `.result-card` : spécifiques à `diagnostic.html`, mais peuvent servir de base pour d’autres formulaires.

## 6. Points D’attention Pour Évolutions
- Navigation mobile : actuellement simple masquage des liens. Pour un menu burger, prévoir JS supplémentaire ou injection d’un menu latéral.
- Duplication du header/footer : un moteur de templates (Jekyll, Eleventy) ou includes HTML standard pourraient éviter les mises à jour multiples.
- SEO : penser à ajouter balises `meta name="description"` et attributs `alt` détaillés pour les images restantes.
- Formulaire contact : personnaliser l’action et prévoir un traitement côté service (auto-réponse, CRM).
- Accessibilité : vérifier l’ordre de tabulation, utiliser des `aria-label` si des icônes sont ajoutées.

## 7. Dépendances & Compatibilité
- Aucune bibliothèque externe. Compatible avec navigateurs modernes (supporte `grid`, `flex`, `clamp`).
- Les couleurs utilisent CSS vars, compatibles Edge/Chrome/Firefox/Safari récents.
- Aucun build nécessaire pour déployer.

## 8. Tests Rapides
- Ouvrir `index.html` dans un navigateur ; vérifier navigation, boutons, images.
- Pour le questionnaire :
  1. Soumettre sans modules → vérifier message par défaut.
  2. Soumettre avec plusieurs modules → concaténation des messages.
  3. Changer priorité/délai → confirmer modifications de la synthèse.
- Pour le formulaire contact : test manuel en environnement PHP/Hostinger, vérifier la redirection `merci.html` et la réception de l’email sur `patrick.lyonnet@cln-solutions.fr`.

---
Mettre à jour ce référentiel dès qu’une modification de structure ou de composant est effectuée dans le code.***
