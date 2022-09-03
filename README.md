# LE PROJET TRIVIA-API

Le projet Trivia est une plate-forme de jeux pour les étudiants et les employers d'Udacity, afin de favoriser la creation des liens sociaux entre ces derniers. Les utilisateurs de la plate-forme peuvent afficher toutes les questions par catégorie, ajouter de nouvelles questions en exigeant qu'elles comprennent le texte de la question et de la réponse, supprimer les question, rechercher des questions à partir d'une chaîne de texte de requête et enfin jouer le questionnaire en randomisant toutes les questions ou dans une catégorie spécifique. Dans le cadre du Nanodegré Fullstack, il sert de projet pratique de fin de  module  pour les leçons du Cours 2 : Développement et documentation des API. En réalisant ce projet, j'apprends et applique mes compétences en conception et en mise en œuvre des points de terminaison d'API bien formatés qui tirent parti des connaissances de HTTP et des meilleures pratiques de développement d'API.

Tout le code backend suit [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Pour Commencer

### Pré-requis et Développement local
Les développeurs qui utilisent ce projet doivent déjà avoir Python3, pip et node installés sur leurs machines locales.

### Configuration du backend

Depuis le dossier backend, exécutez `pip install requirements.txt`. Tous les paquets requis sont inclus dans le fichier d'exigences. 

Pour lancer l'application, exécutez les commandes suivantes : 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Ces commandes mettent l'application en mode développement et dirigent notre application à utiliser le fichier `__init__.py` dans notre dossier flaskr. Le travail en mode développement affiche un débogueur interactif dans la console et redémarre le serveur à chaque fois que des modifications sont apportées. Si vous exécutez localement sous Windows, recherchez les commandes dans la [documentation Flask] (http://flask.pocoo.org/docs/1.0/tutorial/factory/).

L'application est exécutée sur `http://127.0.0.1:5000/` par défaut et est un proxy dans la configuration du frontend. 

### Configuration du Frontend

Depuis le dossier du frontend, exécutez les commandes suivantes pour démarrer le client : 
```
npm install // une seule fois pour installer les dépendances
npm start 
```

Par défaut, le frontend sera exécuté sur localhost:3000.

### Tests
Afin d'exécuter les tests, naviguez dans le dossier backend et exécutez les commandes suivantes : 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

La première fois que vous exécutez les tests, omettez la commande dropdb. 

Tous les tests sont conservés dans ce fichier et doivent être maintenus au fur et à mesure des mises à jour des fonctionnalités de l'application. 

## Référence API

### Pour Commencer
- URL de base : Actuellement, cette application ne peut être exécutée que localement et n'est pas hébergée en tant qu'URL de base. L'application backend est hébergée à l'adresse par défaut, `http://127.0.0.1:5000/`, qui est définie comme un proxy dans la configuration du frontend. 
- Authentification : Cette version de l'application ne nécessite pas d'authentification ou de clés API. 

### Gestion des erreurs
Les erreurs sont renvoyées sous forme d'objets JSON au format suivant :
```
{
    "success" : False, 
    "error" : 404,
    "message" : "resource not found"
}
```
L'API renvoie deux types d'erreur lorsque les demandes échouent :
- 404 : resource not found
- 422 : unprocessable

### Points de Terminaisons  et Comportements

#### GET /categories

`GET '/categories'`

- Général :
    - Renvoie un objet avec une seule clé, « categories », qui contient un objet « id : category_string » : paires de valeurs.
    - Récupère un dictionnaire de catégories dans lequel les clés sont les ID, et la valeur est la chaîne correspondante de la catégorie
    - Arguments de la requête : aucun
- Exemple : `curl http://127.0.0.1:5000/categories`

```json 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

---
### GET /categories/${id}/questions

`GET '/questions?page=${integer}'`

-General :
    - Récupère un ensemble paginé de questions, un nombre total de questions, toutes les catégories et la chaîne de catégorie actuelle.
    - Arguments de la requête : `page` - nombre entier
    - Retourne : Un objet contenant 10 questions paginées, le nombre total de questions, l'objet comprenant toutes les catégories et la chaîne de la catégorie actuelle.
-Exemple : `curl http://127.0.0.1:5000/questions?page=1`

```json
{
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "total_questions": 21,
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Science", 
}
```

---
### GET /categories/${id}/questions

`GET '/categories/${id}/questions'`

-Generale : 
    - Récupère les questions d'une catégorie spécifiée par l'argument de requête id.
    - Arguments de la requête : `id` - nombre entier
    - Retourne : Un objet contenant les questions de la catégorie spécifiée, le nombre total de questions et la chaîne de la catégorie actuelle.
-Exemple : `curl http://127.0.0.1:5000/categories/2/questions`
```json
{
  "current_category": "Geography", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "54", 
      "category": 3, 
      "difficulty": 4, 
      "id": 25, 
      "question": "le continent Africain compte combien de pays?"
    }
  ], 
  "total_questions": 2
}
```

---
### DELETE /questions/${id}

`DELETE '/questions/${id}'`
    
-Generale : 
    - Supprime une question spécifiée en utilisant l'identifiant de la question.
    - Arguments de la requête : `id` - nombre entier
    - Retourne : l'identifiant de l'objet supprimé
-Exemple : `curl -X DELETE http://127.0.0.1:5000/questions/10`
```json
{
  "deleted": 10
}
```

---

### POST /quizzes

`POST '/quizzes'`

-Generale : 
    - Envoie une requête post afin d'obtenir la question suivante pendent une session de jeux
    - Retourne un objet unique contenant une question (la prochaine question du jeux)
    
    
-Exemple : `curl -H "Content-Type: application/json" -X POST -d '{"previous_questions":[1,3], "quiz_category" : {"type": "Science", "id": "3" }}' http://localhost:5000/quizzes`

```json
{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }
}
```
---
### POST /questions

`POST '/questions'`

-Generale : 
    - Dans le cas ou le coprs de la requête contient `Un objet question` Envoie une requête de post afin d'ajouter une nouvelle question
    - retourne : Aucune nouvelle donnée
    -Corps de la requête : 
```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```
-Exemple : `curl -H "Content-Type: application/json" -X POST -d '{"question": "Heres a new question string","answer": "Heres a new answer string","difficulty": 1, "category": 3}' http://localhost:5000/questions`

```json
{

}
```
----
`POST '/questions'`

-Generale : 
    - Dans le cas ou le corps de la requête contien `searchTerm`, envoi d'une requête de poste afin de rechercher une question spécifique par terme de recherche
    - Corps de la requête :
```json
{
  "searchTerm": "this is the term the user is looking for"
}
```
    -Retourne : un tableau de questions, un nombre de totalQuestions correspondant au terme de recherche et la chaîne de catégorie actuelle.

-Exemple : `curl -H "Content-Type: application/json" -X POST -d '{"searchTerm": "title"}' http://localhost:5000/questions`

```json
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "total_questions": 2
}
```
## Deployment N/A

## Authors
CHEDJOU SOFFO Rocelin

## Acknowledgements 
L'équipe formidable d'Udacity et tous les étudiants. Particulierement à mon session lead BADIOU OURO-BANG'NA