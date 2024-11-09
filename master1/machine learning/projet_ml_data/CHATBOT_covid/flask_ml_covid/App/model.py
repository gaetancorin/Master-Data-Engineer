import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

def create_model_and_fit():
    # loading df
    df = pd.read_csv("./datas/CovidDataset.csv")

    # replace Yes,No values by 0,1
    for column in df.columns:
        le = preprocessing.LabelEncoder()
        le.fit(df[column])
        df[column] = le.transform(df[column])

    #définition du train et du test suivant les colonnes ayant un impact
    X = df[['Sore throat', 'Dry Cough', 'Abroad travel', 'Breathing Problem',
           'Attended Large Gathering', 'Contact with COVID Patient', 'Fever',
           'Family working in Public Exposed Places',
           'Visited Public Exposed Places', 'Hyper Tension', 'Asthma', 'Diabetes']]
    y = df['COVID-19']

    #creation du modèle avec les hyperparamètres finetuner, puis entrainement du modèle
    RFC = RandomForestClassifier(n_estimators = 20, criterion = 'gini', random_state = 0)
    RFC.fit(X, y)
    return RFC

def get_target_by_model(model, data):
    RFC = model
    data_user = pd.DataFrame({k: [v] for k, v in data.items()})

    confiance = RFC.predict_proba(data_user)

    prediction = RFC.predict(data_user)
    print("prediction : ", prediction, 'confiance :', confiance)

    return prediction, confiance
