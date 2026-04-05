# 🎵 MakeMeAPlaylist

> Application web qui analyse les habitudes musicales d'un utilisateur Spotify et génère automatiquement une playlist personnalisée grâce au Machine Learning.

---

## Présentation

MakeMeAPlaylist est un projet personnel développé de A à Z de manière autonome.

L'utilisateur se connecte avec son compte Spotify. L'application récupère ses 1000 dernières chansons likées, entraîne un modèle de Machine Learning sur son profil musical, puis parcourt un catalogue de millions de titres pour identifier ceux qui correspondent à ses goûts. Une playlist est ensuite créée automatiquement directement dans son compte Spotify.

---

## Fonctionnement

**1. Connexion sécurisée**
L'authentification passe par le protocole OAuth 2.0 de Spotify. L'utilisateur se connecte via la page officielle Spotify, sans que l'application n'ait accès à son mot de passe.

**2. Collecte et analyse des données**
L'application récupère les 1000 dernières chansons likées de l'utilisateur. Pour chaque titre, elle extrait 12 caractéristiques audio fournies par Spotify : le caractère dansant, l'énergie, le tempo, le niveau acoustique, etc.

**3. Entraînement du modèle**
Un algorithme de Machine Learning est entraîné pour distinguer les chansons que l'utilisateur aime de celles qu'il ne connaît pas. Il apprend ainsi à modéliser précisément son profil musical.

**4. Génération des recommandations**
Le modèle analyse un dataset d'environ 100000 titres du catalogue Spotify et sélectionne uniquement les titres pour lesquels il estime à 99% ou plus que l'utilisateur les appréciera.

**5. Création de la playlist**
Les titres sélectionnés sont automatiquement ajoutés dans une nouvelle playlist sur le compte Spotify de l'utilisateur.

---

## Technologies utilisées

| Rôle | Technologie |
|---|---|
| Application web | Python / Flask |
| Authentification | OAuth 2.0 / Spotipy |
| Traitement des données | Pandas |
| Modèle de recommandation | Scikit-learn |
| Conteneurisation | Docker |

---

## Compétences mobilisées

- Conception de l'architecture complète d'une application web full-stack de ML
- Mise en place d'une authentification OAuth 2.0
- Construction d'un pipeline de données complet : collecte via API, nettoyage et transformation en dataset exploitable
- Conception et entraînement d'un modèle de Machine Learning supervisé sur des données réelles
- Intégration d'une API tierce (Spotify Web API) dans une application web
- Conteneurisation de l'application avec Docker

---

## Auteur

Ayman FITOURI
Projet personnel développé entièrement de manière autonome.

> ⚠️ Depuis novembre 2024, Spotify a retiré l'accès aux audio features de son API publique. 
> L'application ne peut donc plus fonctionner en production. Ce projet a vocation à illustrer 
> les compétences techniques mobilisées plutôt qu'à être utilisé en conditions réelles.