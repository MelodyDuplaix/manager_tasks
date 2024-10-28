
# Manager de Tâches avec Points et Récompenses

Ce projet est un manager de tâches interactif, conçu avec Python et Streamlit, qui permet de suivre la réalisation de diverses tâches, organisées par catégories, en lien avec des objectifs spécifiques. Inspiré de logiciels tels qu'Habitica ou le plugin Gamified Tasks d’Obsidian, cet outil est personnalisé pour répondre aux besoins d’organisation et de productivité d’un business particulier.

## 🎯 Objectifs Généraux

L'objectif principal de ce manager est de fournir un système de suivi et de motivation pour :
- **Gérer diverses catégories de tâches** telles que l’administratif, les ventes, etc.
- **Suivre la progression des objectifs** avec des barres de progression quotidiennes, hebdomadaires et mensuelles.
- **Attribuer et déduire des points (pièces)** en fonction des tâches réalisées ou non.
- **Débloquer des récompenses** en échange des pièces accumulées pour maintenir la motivation.

## ⚙️ Fonctionnalités Principales

### Gestion des Tâches

- **Création de Tâches** : Permet de créer et d’organiser des tâches par catégories, chaque tâche contribuant aux objectifs globaux fixés. En fonction de la réalisation ou de l'absence de réalisation de certaines tâches, un solde positif ou négatif peut être généré pour garder une trace des progrès ou des aspects à améliorer.
  
- **Organisation par Objectifs** : Possibilité de structurer les tâches et de les associer à des objectifs spécifiques pour un suivi personnalisé, en créant un manager pour chaque objectif.

### Système de Points et Récompenses

- **Accumulation de Pièces** : Chaque tâche accomplie rapporte des pièces qui peuvent ensuite être échangées contre des récompenses.
- **Récompenses** : Les pièces gagnées permettent de débloquer des récompenses personnalisées, telles que :
  - Jour de repos
  - Cadeaux personnels (par exemple, repas préféré)
  - Vacances (ex. : une semaine de vacances)

### Suivi de la Progression des Objectifs

- **Barres de Progression** : Visualisation de la progression au quotidien, sur une base hebdomadaire et mensuelle, pour évaluer les progrès et ajuster les efforts en conséquence.
  
### Configurations Flexibles

- **Personnalisation des Tâches et Récompenses** : Des options sont disponibles pour ajuster les configurations des tâches et des récompenses selon les objectifs et besoins spécifiques, sans redémarrage de l’application.

## 🔄 Roadmap

- [x] ajouter des moyens de facilement / rapidement modifer les configs ✅ 2024-10-24
	- [x] configs de taches dispo ✅ 2024-10-24
	- [x] configs de récompenses dispo ✅ 2024-10-24
	- [x] configs d'objectifs ✅ 2024-10-24
- [x] ajouter une barre de progression mensuelle dans une page mensuelle ✅ 2024-10-24
- [x] ajouter une barre de progression hebdomadaire dans une page hebdo ✅ 2024-10-25
- [x] ajouter la possibilité d'avoir plusieurs sous managers ✅ 2024-10-28
- [x] ajouter un moyen de changer les configs des managers dispos ✅ 2024-10-28
- [x] ajouter des tâches ponctuelle ✅ 2024-10-28
- [ ] Avoir des pièces par sous types avec une possibilité d'avoir un nombre de pièce différente pour valider la journée (par exemple, il faut 10 pièces, dont 2 en sous type 1, 3 en sous type 2 et 2 en sous type 3) 
- [ ] avoir la possibilité de timers pour mesurer le temps sur les taches (bouton finir la journée, et enregistrement des heures quand on clique sur un bouton) 
- [ ] ajouter des stats sur les temps que l'on passe sur les taches 

## 🛠️ Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/MelodyDuplaix/manager_tasks.git
   cd manager_tasks
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez l’application :
   ```bash
   streamlit run app.py
   ```

