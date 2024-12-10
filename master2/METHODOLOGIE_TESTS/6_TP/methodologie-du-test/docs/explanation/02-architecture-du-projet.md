# Architecture du projet

L'architecture du projet est la suivante :

```
.
├── docs
│                                    La documentation du projet
├── pyproject.toml
│                                    La configuration des différents outils
├── requirements.txt
│                                    Les dépendances du projet
├── src
│   └── calculatrice.py
│                                    Un exemple de classe en python
├── tests
│   ├── test_0_calculatrice.py
│   ├── test_1_1_km_a_pied.py
│   └── test_2_fizz_buzz.py
│                                    Les tests associés à la classe
└── venv
    └── bin
        └── activate
                                     L'executable à sourcer pour entrer dans le venv.
```

Pour démarrer, lancez les commandes suivantes :

```shell
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pytest
```
