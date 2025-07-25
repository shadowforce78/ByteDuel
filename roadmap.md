---

# 🚀 Roadmap & Todo List Dev — Byte Duel

---

## 🔹 Phase 1 — Prototype Core (1-2 semaines)

### Objectif : Avoir un prototype jouable localement avec la mécanique de base

* [ ] Créer la structure du projet (HTML/CSS/JS vanilla)
* [ ] Implémenter la grille de jeu (3x4 ou 4x5), interface basique de placement
* [ ] Définir une classe `Unit` avec stats de base (PV, ATK, vitesse d’attaque, type)
* [ ] Implémenter le draft simple : tirage aléatoire de X unités + choix limité
* [ ] Implémenter le système de combat “Synchro Strike” : toutes unités attaquent en même temps par “tick”
* [ ] Gérer le déplacement des unités melee vers la prochaine cible après kill
* [ ] Afficher les résultats de la partie (victoire/défaite)
* [ ] Système simple de scoring et gain de monnaie local (stocké en localStorage)

---

## 🔹 Phase 2 — Interface & UX (1-2 semaines)

### Objectif : Rendre le jeu agréable et intuitif à jouer

* [ ] UI claire et responsive : grille, draft, stats, placements
* [ ] Drag & drop (ou click) pour placer les unités
* [ ] Animation simple des attaques, déplacements, morts
* [ ] Affichage des buffs/débuffs avec icônes claires
* [ ] Sons brefs (clic, attaque, victoire)
* [ ] Ajout d’un écran de fin avec stats détaillées
* [ ] Intégration d’une intro/splash screen basique

---

## 🔹 Phase 3 — Progression & Compétition (2-3 semaines)

### Objectif : Ajouter la progression joueur et un système de classement local

* [ ] Implémenter système de level/XP joueur
* [ ] Créer un système de ranking simple (Bronze, Argent, Or) basé sur le score local
* [ ] Stocker les données progression + monnaie en localStorage
* [ ] Ajouter un leaderboard local (top scores du joueur)
* [ ] Intégrer une monnaie “ByteCoins” pour récompenses
* [ ] Permettre achat de skins cosmétiques (visuels uniquement)

---

## 🔹 Phase 4 — Contenu & Équilibrage (2-4 semaines)

### Objectif : Ajouter variété, synergies, missions et peaufinage

* [ ] Ajouter 10-15 unités variées avec effets/buffs simples
* [ ] Implémenter synergies de base (ex : 2 archers = +10% attaque)
* [ ] Ajouter un système simple de missions/journalières
* [ ] Améliorer l’IA adverse (si mode solo)
* [ ] Rééquilibrer les unités et synergies selon tests

---

## 🔹 Phase 5 — Multiplayer & Backend (optionnel / futur)

### Objectif : Permettre le PvP en ligne et gestion serveur

* [ ] Développer backend Node.js pour matchmaking et stockage
* [ ] Implémenter WebSocket pour échanges en temps réel
* [ ] Système d’authentification joueur (email/mot de passe)
* [ ] Héberger leaderboard global
* [ ] Déployer une version bêta multijoueur

---

## 🔹 Phase 6 — Packaging & Publication

* [ ] Préparer version desktop via Tauri
* [ ] Préparer version mobile via Capacitor (APK, PWA)
* [ ] Tests multi-plateformes
* [ ] Préparation documentation / tutoriels
* [ ] Lancement Early Access / Playtests
