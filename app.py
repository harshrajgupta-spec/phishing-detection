from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("phishing.pkl", 'rb'))
xgb_model = pickle.load(open("xgb_model.pkl", 'rb'))
# rf_model = pickle.load(open("rf_model.pkl", 'rb'))

@app.route("/", methods=['GET', 'POST'])
def index():
 
    predict = None
    xgb_predict = None
    rf_predict = None
    active_tab = "model1"   # Default tab

    if request.method == 'POST':
        url = request.form.get('url')
        url2 = request.form.get('url2')
      #  url3 = request.form.get('url3')   # NEW FIELD

        # -------- MODEL 1 --------
        if url and url.strip():
            cleaned_url = re.sub(r'^https?://(www\.)?', '', url)
            pred = model.predict(vector.transform([cleaned_url]))[0]

            if pred == 'bad':
                predict = "UNSECURE!!"
            elif pred == 'good':
                predict = "SECURE!!"
            else:
                predict = "something went wrong!!"

            active_tab = "model1"
            return render_template("index.html", predict=predict, active_tab=active_tab)

        # -------- MODEL 2 --------
        if url2 and url2.strip():
            cleaned_url2 = re.sub(r'^https?://(www\.)?', '', url2)
            pred = xgb_model.predict(vector.transform([cleaned_url2]))[0]

            if pred == 1:
                xgb_predict = "SECURE!!"
            elif pred == 0:
                xgb_predict = "UNSECURE!!"
            else:
                xgb_predict = "something went wrong!!"

            active_tab = "model2"
            return render_template("index.html", xgb_predict=xgb_predict, active_tab=active_tab)

        # -------- MODEL 3 (RANDOM FOREST) --------
  
  #   if url3 and url3.strip():
   #         cleaned_url3 = re.sub(r'^https?://(www\.)?', '', url3)
    #        pred = rf_model.predict(vector.transform([cleaned_url3]))[0]
#
 #           if pred == 1:
  #              rf_predict = "SECURE!!"
   #         elif pred == 0:
      #          rf_predict = "UNSECURE!!"
       #     else:
        #        rf_predict = "something went wrong!!"
#
 #           active_tab = "model3"
  #          return render_template("index.html", rf_predict=rf_predict, active_tab=active_tab)
            

    # GET request
    return render_template("index.html", active_tab=active_tab)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
