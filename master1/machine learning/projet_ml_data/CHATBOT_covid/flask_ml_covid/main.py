from App.views import app

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True)
    app.secret_key = 'votre_clé_secrète'
    app.run(host='127.0.0.1', debug=True)