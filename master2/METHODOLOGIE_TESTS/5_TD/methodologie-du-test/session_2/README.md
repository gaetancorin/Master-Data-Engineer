
# Librarie

Lancer le serveur : 

Avec compose (recommandé)

```shell
docker compose up
```

Sans compose

```shell
.\start.ps1
# Vous pouvez avoir besoin de désactiver la protection admin :
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# ou
./start.sh
```

Ajouter un livre
```shell
curl -X POST http://localhost:5000/books -H 'Content-Type: application/json' -d '{"title": "1984", "author": "George Orwell", "year": 1949, "stock": 8}'
```

Récupérer un livre
```shell
curl -X GET http://localhost:5000/books/1
```

Modifier un livre
```shell
curl -X PUT http://localhost:5000/books/1 -H 'Content-Type: application/json' -d '{"title": "Animal Farm", "author": "George Orwell", "stock": 3}'
```

Supprimer un livre
```shell
curl -X DELETE http://localhost:5000/books/1
```

Chercher un livre
```shell
curl http://localhost:5000/books/search/george
```

Emprunter un livre
```shell
curl -X POST http://localhost:5000/books/1/borrow
```

Rendre un livre
```shell
curl -X POST http://localhost:5000/books/1/return
```

