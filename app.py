from flask import Flask, request, render_template_string

app = Flask(__name__)

def calculate_food_waste_co2(weight_kg, food_type):
    co2_emission_factors = {
        'rice': 2.75,  # kg CO2/kg
        'vegetables': 1.5,
        'meat': 17.5,
        'udon': 2.0,
        'ごはん': 2.75,
        'ご飯': 2.75,  # ご飯を追加
        'ピザ': 5.0,
        'そば': 3.0,
        'チキン': 6.5
    }
    co2_emission_factor = co2_emission_factors.get(food_type, 0)
    co2_emission = weight_kg * co2_emission_factor
    return co2_emission

def calculate_clothing_waste_co2(weight_kg, material_type):
    co2_emission_factors = {
        'silk': 10.0,  # kg CO2/kg
        'polyester': 7.0,
        'cotton': 5.5,
        'シルク': 10.0,
        'コットン': 5.5,
        'ポリエステル': 7.0
    }
    co2_emission_factor = co2_emission_factors.get(material_type, 0)
    co2_emission = weight_kg * co2_emission_factor
    return co2_emission

@app.route('/')
def index():
    form_html = '''
    <form action="/calculate" method="post">
        <label for="item_type">アイテムの種類:</label>
        <select name="item_type" id="item_type">
            <option value="food">食品</option>
            <option value="clothing">衣類</option>
        </select>
        <br>
        <label for="weight">重量(kg):</label>
        <input type="number" step="0.01" name="weight" id="weight" required>
        <button type="button" onclick="decreaseWeight()">-</button>
        <button type="button" onclick="increaseWeight()">+</button>
        <br>
        <label for="item_subtype">詳細:</label>
        <input type="text" name="item_subtype" id="item_subtype" required>
        <br>
        <button type="submit">計算</button>
    </form>
    <script>
        function increaseWeight() {
            var weightInput = document.getElementById("weight");
            weightInput.value = (parseFloat(weightInput.value) + 0.1).toFixed(2);
        }

        function decreaseWeight() {
            var weightInput = document.getElementById("weight");
            if (weightInput.value > 0.1) {
                weightInput.value = (parseFloat(weightInput.value) - 0.1).toFixed(2);
            }
        }
    </script>
    '''
    return render_template_string(form_html)

@app.route('/calculate', methods=['POST'])
def calculate():
    item_type = request.form['item_type']
    weight_kg = float(request.form['weight'])
    item_subtype = request.form['item_subtype']
    
    if item_type == 'food':
        co2_emission = calculate_food_waste_co2(weight_kg, item_subtype)
        if co2_emission == 0:
            return f'{item_subtype}のCO2排出係数が見つかりませんでした。'
    elif item_type == 'clothing':
        co2_emission = calculate_clothing_waste_co2(weight_kg, item_subtype)
        if co2_emission == 0:
            return f'{item_subtype}のCO2排出係数が見つかりませんでした。'
    else:
        co2_emission = 0
    
    return f'CO2排出量: {co2_emission} kg'

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # ポートを5002に設定
