import flask
from flask import render_template
import pickle
import sklearn

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def main():
    if flask.request.method == 'GET':
        return render_template('main.html')
    if flask.request.method == 'POST':
        # Загрузка модели
        with open('model_GBR1_app.pkl', 'rb') as f:
            loaded_model = pickle.load(f)
        
        # Получение параметров
        matrix_filler_ratio = float(flask.request.form['Соотношение матрица-наполнитель'])
        density = float(flask.request.form['Плотность, кг/м3'])
        elasticity_modulus = float(flask.request.form['модуль упругости, ГПа'])
        hardener_content = float(flask.request.form['Количество отвердителя, м.%'])
        epoxy_group_content = float(flask.request.form['Содержание эпоксидных групп,%_2'])
        flash_point = float(flask.request.form['Температура вспышки, С_2'])
        surface_density = float(flask.request.form['Поверхностная плотность, г/м2'])
        tensile_strength = float(flask.request.form['Прочность при растяжении, МПа'])
        resin_consumption = float(flask.request.form['Потребление смолы, г/м2'])
        stitching_angle = float(flask.request.form['Угол нашивки, град'])
        stitch_step = float(flask.request.form['Шаг нашивки'])
        stitch_density = float(flask.request.form['Плотность нашивки'])

        # Предсказание
        y_pred = loaded_model.predict([[matrix_filler_ratio, density, elasticity_modulus, hardener_content, epoxy_group_content,
                                         flash_point, surface_density, tensile_strength, resin_consumption,
                                         stitching_angle, stitch_step, stitch_density]])
        
        return render_template('main.html', result=y_pred[0])  # Предполагается, что y_pred - это массив

if __name__ == '__main__':
    app.run()
    