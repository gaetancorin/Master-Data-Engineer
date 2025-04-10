from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import RetryPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
import uuid

class CustomRetryPolicy(RetryPolicy):
    def on_read_timeout(self,*args,**kwargs):
        print("Timeout en lecture, ressai force")
        return self.RETRY

    def on_write_timeout(self,*args,**kwargs):
        print("Timeout en écriture , ressai force")
        return self.RETRY

    def on_unavailable(self,*args,**kwargs):
        print("Noeud indisponible, ressai avec coherence reduite")
        return self.RETRY
  

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('test_retry')
session.default_retry_policy = CustomRetryPolicy()

def test_retry_policy () :
    print("\n Test de la politique personnalise")
    # query = SimpleStatement(
    #     "INSERT INTO users (id, name, age) VALUES (%s,%s, %s)")
    query = SimpleStatement(
        "INSERT INTO users (id, name, age) VALUES (%s, %s, %s)",
        consistency_level=ConsistencyLevel.QUORUM  # Exige au moins 2 nœuds
    )
    try :
        session.execute(query, (uuid.uuid4(), "Alice", 30))
        print("Insertion reussie avec la politique personnalisee")
    except Exception as e :
        print(f"Erreur: {e}")

test_retry_policy()
cluster.shutdown()