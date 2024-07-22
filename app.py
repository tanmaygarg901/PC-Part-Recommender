from flask import Flask, render_template, request, jsonify
from recommender import recommend_build

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    budget = data.get('budget')
    cpu_pref = data.get('cpu_pref', [])
    gpu_pref = data.get('gpu_pref', []) 
    if isinstance(cpu_pref, str):
        cpu_pref = [cpu_pref]
    if isinstance(gpu_pref, str):
        gpu_pref = [gpu_pref]
    
    recommendations = recommend_build(budget, cpu_pref, gpu_pref)
    
    if isinstance(recommendations, str):
        return jsonify({"error": recommendations})
    
    return jsonify(recommendations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)