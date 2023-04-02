import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import pickle

def load_data():
    return pd.read_csv('static/data/diabetes_data.csv')

def diabetes_prediction(gender, age, Polyuria, Polydipsia , sudden_weight_loss,weakness,Polyphagia,Genital_thrush,visual_blurring,Itching,Irritability,delayed_healing,partial_paresis,muscle_stiffness,Alopecia,Obesity):
    diabetes_data = load_data()
    diabetes_data = diabetes_data.drop(columns = 'class', axis = 1)
    X_category = diabetes_data[['Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss',
        'weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
        'Itching', 'Irritability', 'delayed healing', 'partial paresis',
        'muscle stiffness', 'Alopecia', 'Obesity']]
    age_column = diabetes_data['Age']   
    # Applying one-hot encoding to each column with categorical data
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    X_OH = pd.DataFrame(OH_encoder.fit_transform(X_category))
    X_OH.index = X_category.index #One-hot encoding removes the index so it's necessary to put them back
    X_OH.insert(0, 'Age', age_column.values)

    input = {'Age':age,'Gender':gender,'Polyuria':Polyuria,'Polydipsia':Polydipsia,'sudden weight loss':sudden_weight_loss,'weakness':weakness,'Polyphagia':Polyphagia,'Genital thrush':Genital_thrush,'visual blurring':visual_blurring,'Itching':Itching,'Irritability':Irritability,'delayed healing':delayed_healing,'partial paresis':partial_paresis,'muscle stiffness':muscle_stiffness,'Alopecia':Alopecia,'Obesity':Obesity}
    df_input = pd.DataFrame(input,index=[0])
    input_category = df_input[['Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss',
    'weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
    'Itching', 'Irritability', 'delayed healing', 'partial paresis',
    'muscle stiffness', 'Alopecia', 'Obesity']]

    input_age = df_input['Age']

    input_oh = OH_encoder.transform(input_category)
    input_oh = pd.DataFrame(input_oh)
    input_oh.insert(0, 'Age', input_age.values)
    input_oh = input_oh.values

    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open('static/data/'+filename, 'rb'))

    result = loaded_model.predict(input_oh)
    return result
