from flask import Flask, render_template
from routes import house_routes
import pickle
import sqlite3
import os

app = Flask(__name__)
app.register_blueprint(house_routes.bp)
cur_dir = os.path.join(__file__)


DATABASE_PATH = os.path.join(cur_dir, 'house.db')

# conn = sqlite3.connect(DATABASE_PATH)
def Regression(X_train, y_train, X_test):
  # rd_forest, xgboost
  score = []
  y_test = []
  clf = clf_from_pickle = pickle.load(open("rdforest_regressor.pkl", 'rb'))(X_train, y_train)
  score.append(clf_from_pickle[1])
  pred = clf.predict(X_test)
  y_test.append(pred)

  clf = pickle.load(open("xgb_regressor.pkl", 'rb'))(X_train, y_train)
  score.append(clf_from_pickle[1])
  pred = clf.predict(X_test)
  y_test.append(pred)


  return y_test, score


@app.route('/')
def index():
  return render_template('index.html'), 200

@app.route('/', methods=['POST'])
def select_data() :
  form = request.form
  if request.method == 'POST' :

    result = request.form
    
    y, proba = Regression(x_train, y_train, x_test)
    return render_template('index.html', content=selected, 
                        prediction=y, 
                        probability=round(proba*100, 2)) 
    
  return render_template('index.html', form=form), 200, 
if __name__ == '__main__':
  app.run(debug=True)