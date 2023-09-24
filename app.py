from flask import Flask , render_template , send_from_directory , request, json
import json
import os 
app = Flask(__name__) 

global y_may_flu
global y_may_bgl
global y_aug_bgl
global y_aug_flu 
global y_jan_flu
global y_jan_bgl
global y_nov_flu
global y_nov_bgl 
global depth


@app.route("/") 
def hello_world():
    return(render_template("./index.html")) 

@app.route('/<string:page_name>')
def html_page(page_name):
	return render_template(page_name) 

@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'),'icon.ico')


@app.route('/test', methods=['POST','GET'])
def test():
    output = request.get_json()

    result = json.loads(output) 
    answer = list(result.values())
    print(answer[0])
    a= ""+answer[0]

    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    from sklearn.linear_model import LinearRegression

    data = pd.read_csv('./static/FinalData.csv')
    print(str(a))

    user_village_name = str(a)


    filtered_data = data[data['VILLAGE'] == user_village_name]


    if filtered_data.empty:
        print(f"No data found for village '{user_village_name}'.")
        return result
    else:


        label_encoder = LabelEncoder()


        filtered_data['FORMATION'] = label_encoder.fit_transform(filtered_data['FORMATION'])
        filtered_data['River Basin'] = label_encoder.fit_transform(filtered_data['River Basin'])


        X = filtered_data[['ELEVATION', 'Normal (1901-70)', 'Average rainfall (2012-21) (mm)',
                           'Rainfall (2021) (mm)', 'Departure (%) in 2021 from normal rainfall',
                           'Departure (%) in 2021 from Average rainfall', 'River Basin', 'FORMATION']]

        y_may_flu = filtered_data['MAY_flu']
        y_aug_flu = filtered_data['AUG_flu']
        y_nov_flu = filtered_data['NOV_flu']
        y_jan_flu = filtered_data['JAN_flu']

        depth = filtered_data['DEPTH']

        y_may_bgl = filtered_data['MAY_bgl']
        y_aug_bgl = filtered_data['AUG_bgl']
        y_nov_bgl = filtered_data['NOV_bgl']
        y_jan_bgl = filtered_data['JAN_bgl']    


        model = LinearRegression()

        model.fit(X, y_may_flu)
        model.fit(X, y_aug_flu)
        model.fit(X, y_nov_flu)
        model.fit(X, y_jan_flu)

        # Make predictions
        predictions_may_flu = model.predict(X)
        predictions_aug_flu = model.predict(X)
        predictions_nov_flu = model.predict(X)
        predictions_jan_flu = model.predict(X)

        avg_flu = ( predictions_may_flu + predictions_aug_flu + predictions_nov_flu + predictions_jan_flu ) / 4

        if ( avg_flu >= 0 ):
            print ( "Well can be constructed." )
            print ( "The fluctuation in Pre-Monsoon period (May) is " , y_may_flu[0] , " The water will be found " , y_may_bgl[0] , " meters below the ground water ( roughly ).")
            print ( "The fluctuation during Monsoon period (August) is " , y_aug_flu[0] , " The water will be found " , y_aug_bgl[0] , " meters below the ground water ( roughly ).")
            print ( "The fluctuation in Post-Monsoon period (November) is ", y_nov_flu[0] , " The water will be found " , y_nov_bgl[0] , " meters below the ground water ( roughly ).")
            print ( "The fluctuation in Irrigation period (January) is ", y_jan_flu[0] , " The water will be found " , y_jan_bgl[0] , " meters below the ground water ( roughly ).")
            print ( "Depth of the well should be ", depth[0] )
            return render_template("result.html",fluctuation_may = float(y_may_flu[0]), water_may = float(y_may_bgl[0]), fluctuation_aug = float(y_aug_flu[0]), water_aug = float(y_aug_bgl[0]), fluctuation_nov = float(y_nov_flu[0]), water_nov = float(y_nov_bgl[0]), fluctuation_jan = float(y_jan_flu[0]), water_jan = float(y_jan_bgl[0]), depth_fin = float(depth[0]),name="vijay")
        else:
            print ( "Well can't be constructed." )
            return render_template("result.html",depth_fin=float(depth[0]))
            
    
if __name__ =="__main__":
    app.run(debug=True)