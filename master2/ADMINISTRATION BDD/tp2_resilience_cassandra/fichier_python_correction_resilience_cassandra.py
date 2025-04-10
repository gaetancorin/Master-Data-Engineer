import os
import uuid
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import (
    DowngradingConsistencyRetryPolicy,
    TokenAwarePolicy,
    DCAwareRoundRobinPolicy,
    ExponentialReconnectionPolicy,
)
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

# Définition du profil d'exécution avec paramètres avancés
profile_default = ExecutionProfile(
    load_balancing_policy=TokenAwarePolicy(
        DCAwareRoundRobinPolicy(local_dc="DC1", used_hosts_per_remote_dc=3)
    ),
    retry_policy=DowngradingConsistencyRetryPolicy(),  # Permet de rétrograder la consistance à ONE en cas d'indisponibilité
    consistency_level=ConsistencyLevel.LOCAL_QUORUM,
    serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
    request_timeout=15,
)

# Connexion au cluster avec deux machines (remplacez par vos adresses IP)
cluster = Cluster(
    contact_points=['localhost'],
    port=9042,
    execution_profiles={EXEC_PROFILE_DEFAULT: profile_default},
    protocol_version=4,
    connect_timeout=20,
    reconnection_policy=ExponentialReconnectionPolicy(1.0, 10.0),
)

# Connexion initiale sans keyspace
session = cluster.connect()

# Création du keyspace s'il n'existe pas
create_ks_query = """
CREATE KEYSPACE IF NOT EXISTS test_retry
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '2'}
"""
session.execute(create_ks_query)

# Affecter le keyspace à la session
session.set_keyspace("test_retry")

# Optionnel : création de la table 'users' si elle n'existe pas
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY,
    name text,
    age int
)
"""
session.execute(create_table_query)

def test_retry_policy():
    print("\nTest de la politique de retry avec downgrade à ONE en cas d'indisponibilité")
    query = SimpleStatement("INSERT INTO users (id, name, age) VALUES (%s, %s, %s)")
    try:
        session.execute(query, (uuid.uuid4(), "Alice", 30))
        print("Insertion réussie avec rétrogradation à ONE si nécessaire")
    except Exception as e:
        print(f"Erreur : {e}")

test_retry_policy()
cluster.shutdown()
