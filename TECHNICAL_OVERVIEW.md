# CLN Static Site — Technical Overview

## 1. Purpose and Scope
- Objectif : site vitrine statique présentant l’offre “Connecter · Libérer · Normaliser (CLN)”.
- Cible : publication sur GitHub Pages ou tout hébergement statique.
- Périmètre : pages HTML statiques, feuille de styles CSS, interactions JavaScript pour un questionnaire de pré-diagnostic.

## 2. Structure Du Projet
```
PROJET_CLN/
├── index.html          # Page d'accueil
├── solutions.html      # Détails des offres
├── approche.html       # Mission, vision, méthodologie
├── realisations.html   # Cas d'usage + CTA questionnaire
├── diagnostic.html     # Questionnaire de pré-diagnostic (JS)
├── contact.html        # Formulaire de prise de contact
├── merci.html          # Page de confirmation après contact
├── styles.css          # Styles globaux et composants
├── LOGO_CLN.png        # Logo principal
├── *.jpg               # Visuels d'illustration
└── TECHNICAL_OVERVIEW.md (ce document)
```

## 3. Technologies Utilisées
- **HTML5** : pages statiques avec composant navigation commun.
- **CSS3** : feuille unique `styles.css` (variables CSS, grid, flexbox).
- **JavaScript Vanilla** : logique du questionnaire (`diagnostic.html`).
- **Aucune dépendance externe** ; polices système (`Montserrat` fallback websafe). Peut être enrichi via Google Fonts si nécessaire.

## 4. Design Système
- Palette : `#5a4fcf` (primaire), `#3e36a8`, accent `#00b894`, arrière-plan clair.
- Typographie : `Montserrat`, `Segoe UI`, `Helvetica Neue`, `Arial` (cascade).
- Composants réutilisables :
  - `header` + `.navbar` : navigation sticky, CTA “Être recontacté”.
  - `card`, `card-grid` : vitrines de services, valeurs, actions.
  - `timeline`, `projects-grid`, `contact-grid` : sections spécifiques.
  - Bouton `.cta-button` : style uniforme pour actions clés.
- Responsive : `grid-template-columns: repeat(auto-fit, minmax(...))` assure adaptation mobile. Menu compact (<720px) masque `.nav-links` (prévoir burger si croissance future).

## 5. Pages & Contenu
1. **index.html**
   - Hero avec slogan “Connecter · Libérer · Normaliser”.
   - Engagements CLN, valeurs différenciatrices, citation clé.
2. **solutions.html**
   - Modules `Connecter`, `Libérer`, `Normaliser`.
   - CTA orientés contact, méthodologie, réalisations.
3. **approche.html**
   - Mission, vision, valeurs.
   - Timeline en 4 étapes (Diagnostic → Accompagnement).
4. **realisations.html**
   - Trois cas d’usage illustrés, tags thématiques.
   - Invitation “Questionnaire de pré-diagnostic”.
5. **diagnostic.html**
   - Questionnaire multi-choix produisant synthèse dynamique.
   - Redirection vers `contact.html` pour prise de rendez-vous.
6. **contact.html**
   - Coordonnées directes, formulaire HTML.
   - Champs : nom, email, organisation, message, consentement.
   - `action` à personnaliser (Formspree, Netlify Forms, etc.).
7. **merci.html**
   - Confirmation visuelle post-contact.

## 6. Questionnaire De Pré-Diagnostic
- Formulaire géré côté client (`diagnostic.html`).
- Inputs :
  - `modules` (checkbox) : Connecter, Libérer, Normaliser.
  - `taille` (radio) : segments organisationnels.
  - `priorite` (select) : visibilité, efficacité, qualité, modernisation.
  - `delai` (radio) : court, moyen, long terme.
  - `mode` (radio) : diagnostic flash, pilotage complet, hybride.
- Traitement :
  - `buildModuleSummary()` : message selon modules sélectionnés.
  - `recommendationFromPriority()` : recommandation ciblée.
  - `rendezVousMessage()` : message d’appel à rendez-vous.
  - Résultat injecté via `innerHTML` dans `.result-card` + scroll automatique.
- Extension possible : persistance via `localStorage`, export PDF, envoi API.

## 7. Formulaire De Contact
- Champ hidden `_redirect` vers `merci.html`.
- Tout service de formulaire compatible POST peut être utilisé.
- Conformité RGPD : case à cocher obligatoire de consentement.
- Ajouts possibles :
  - reCAPTCHA v2/v3 (nécessite script externe).
  - Double opt-in via outil CRM / marketing automation.

## 8. Déploiement Recommandé (GitHub Pages)
1. Créer un dépôt GitHub et pousser l’intégralité du dossier.
2. Activer GitHub Pages sur la branche `main` (paramètres > Pages).
3. Choisir “root” ou dossier `/docs` selon organisation.
4. GitHub Pages générera `https://<utilisateur>.github.io/<dépôt>/`.
5. Option : ajouter `CNAME` pour domaine personnalisé.

## 9. Tests & Validation
- **Local** : `python -m http.server 8000` puis `http://localhost:8000/index.html`.
- Vérification manuelle :
  - Navigation barre haute (toutes les pages).
  - Questionnaire : scénarios multiples (aucun module, modules multiples).
  - Formulaire contact : champs requis, redirection `merci.html`.
- Accessibilité :
  - Vérifier contrastes (ok via palette présente).
  - Ajouter attributs `aria` / `role` si besoin d’amélioration.
- SEO de base :
  - Ajouter meta-description par page (TODO).
  - Titre par page déjà défini.

## 10. Conseils d’Évolution
- Intégrer un menu mobile hamburger et animation.
- Ajouter favicon, manifest et métadonnées Open Graph.
- Optimiser images (compression WebP, Lazy loading).
- Brancher un outil analytics (Matomo, Plausible, GA4).
- Envisager CMS headless (Contentful, Strapi) si besoin d’édition non-technique.
- Internationalisation : dupliquer gabarits avec attribut `lang`.

## 11. Maintenance
- Un seul fichier CSS : documenter les sections si croissance.
- Centraliser variables (couleurs, spacing) dans `:root`.
- Fichiers HTML modulaires : possibilité d’extraire header/footer via moteur templating (Jekyll, Eleventy) pour éviter duplications.
- Versionner les assets (nomenclature stable, dossier `assets/`).

## 12. Annexes
- Assets médias fournis : `LOGO_CLN.png`, photos Pexels, visuels blur hospital.
- Scripts Python présents (`ANIMATION_LOGO.py`) non utilisés par le site, à archiver ou documenter si animation future.

---
Document rédigé pour fournir une vision technique complète du site CLN. Mettre à jour à chaque évolution majeure.***
