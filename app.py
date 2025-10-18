# app.py
# Flask Web Interface for V15 Engine
# Commit: 9fbbb9e01f1b2932fdda1f7573f7dacbbe9d1149
# Preservation on GitHub: https://github.com/UIngarsoe/SSISM-V15-PYINNYASHI-

from flask import Flask, request, render_template
from SSISM_V15_Engine import V15_SSISM_Predict

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        query_time = request.form['query_time']
        location = request.form['location']
        v0 = float(request.form['v0'])
        result = V15_SSISM_Predict(name, dob, query_time, location, v0)
        return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
