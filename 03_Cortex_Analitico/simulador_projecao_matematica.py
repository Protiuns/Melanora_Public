import os
import json

# Parâmetros Basais
NODE_COUNT = 200
BASE_W_SURVIVE = 0.5
BASE_W_EXPLORE = 0.5
BASE_W_MAINTAIN = 0.5
ALPHA_ADRENALINE_SURVIVE = 3.0
ALPHA_DOPAMINE_EXPLORE = 2.0
ALPHA_SEROTONIN_MAINTAIN = 2.0
DECAY_RATE = 0.02

def calculate_projection(ticks: int, initial_adrenaline: float, initial_dopamine: float, initial_serotonin: float):
    # Arrays de dados
    adren_arr = []
    dopa_arr = []
    sero_arr = []
    
    surv_arr = []
    expl_arr = []
    main_arr = []
    
    energy_arr = []
    
    adren = initial_adrenaline
    dopa = initial_dopamine
    sero = initial_serotonin
    
    for t in range(ticks):
        adren_arr.append(round(adren, 3))
        dopa_arr.append(round(dopa, 3))
        sero_arr.append(round(sero, 3))
        
        w_surv = NODE_COUNT * (BASE_W_SURVIVE * (1.0 + (adren * ALPHA_ADRENALINE_SURVIVE)))
        w_expl = NODE_COUNT * (BASE_W_EXPLORE * (1.0 + (dopa * ALPHA_DOPAMINE_EXPLORE)))
        w_main = NODE_COUNT * (BASE_W_MAINTAIN * (sero * ALPHA_SEROTONIN_MAINTAIN))
        
        surv_arr.append(round(w_surv, 2))
        expl_arr.append(round(w_expl, 2))
        main_arr.append(round(w_main, 2))
        
        heat = (adren * 1.5) + (dopa * 1.2) + abs(0.5 - sero)
        energy_arr.append(round(heat * 100, 2))
        
        adren = max(0.0, adren - DECAY_RATE)
        dopa = max(0.0, dopa - DECAY_RATE)
        if sero > 0.5:
            sero = max(0.5, sero - DECAY_RATE)
        elif sero < 0.5:
            sero = min(0.5, sero + DECAY_RATE)

    return {
        "ticks": list(range(ticks)),
        "fluids": {"adren": adren_arr, "dopa": dopa_arr, "sero": sero_arr},
        "weights": {"surv": surv_arr, "expl": expl_arr, "main": main_arr},
        "energy": energy_arr
    }

def build_dashboard():
    # Calcular 80 ticks
    ticks = 80
    data_attack = calculate_projection(ticks, 1.0, 0.0, 0.0)
    data_explore = calculate_projection(ticks, 0.0, 0.9, 0.4)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Motor Analítico - Projeções Matemáticas</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background-color: #121212; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }}
        h1 {{ text-align: center; color: #4dc9f6; font-size: 2em; margin-bottom: 30px; letter-spacing: 2px; }}
        .dashboard {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 1400px; margin: 0 auto; }}
        .card {{ background-color: #1e1e1e; border-radius: 12px; padding: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }}
        .card h2 {{ font-size: 1.2em; color: #fff; margin-bottom: 15px; text-align: center; border-bottom: 1px solid #333; padding-bottom: 10px; }}
        canvas {{ max-height: 350px; }}
        .footer {{ text-align: center; margin-top: 40px; padding: 20px; color: #888; border-top: 1px solid #333; }}
    </style>
</head>
<body>
    <h1>SIMULAÇÃO MATEMÁTICA: FLUTUAÇÃO DE REDE INSETÓIDE (200 NÓS)</h1>
    <div class="dashboard">
        <div class="card">
            <h2>PÂNICO (Adrenalina 100%) - Pesos Gravitacionais</h2>
            <canvas id="chartPanic"></canvas>
        </div>
        <div class="card">
            <h2>CURIOSIDADE (Dopamina 90%) - Pesos Gravitacionais</h2>
            <canvas id="chartExplore"></canvas>
        </div>
        <div class="card">
            <h2>DECAIMENTO METABÓLICO (Fluídos via Tempo)</h2>
            <canvas id="chartFluids"></canvas>
        </div>
        <div class="card">
            <h2>GASTO CALORÍFICO (Trabalho Energético da CPU)</h2>
            <canvas id="chartEnergy"></canvas>
        </div>
    </div>

    <script>
        Chart.defaults.color = '#b0b0b0';
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";

        const ticks = {json.dumps(data_attack['ticks'])};

        // Gráfico Pânico
        new Chart(document.getElementById('chartPanic'), {{
            type: 'line',
            data: {{
                labels: ticks,
                datasets: [
                    {{ label: 'Fuga/Sobrevivência', data: {json.dumps(data_attack['weights']['surv'])}, borderColor: '#ff4444', borderWidth: 3, tension: 0.1 }},
                    {{ label: 'Explorar', data: {json.dumps(data_attack['weights']['expl'])}, borderColor: '#4cc9f0', borderDash: [5, 5], tension: 0.1 }},
                    {{ label: 'Manter Padrão', data: {json.dumps(data_attack['weights']['main'])}, borderColor: '#44ff44', borderDash: [2, 2], tension: 0.1 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});

        // Gráfico Explorar
        new Chart(document.getElementById('chartExplore'), {{
            type: 'line',
            data: {{
                labels: ticks,
                datasets: [
                    {{ label: 'Explorar', data: {json.dumps(data_explore['weights']['expl'])}, borderColor: '#4cc9f0', borderWidth: 3, tension: 0.1 }},
                    {{ label: 'Fuga/Sobrevivência', data: {json.dumps(data_explore['weights']['surv'])}, borderColor: '#ff4444', borderDash: [5, 5], tension: 0.1 }},
                    {{ label: 'Manter Padrão', data: {json.dumps(data_explore['weights']['main'])}, borderColor: '#44ff44', borderDash: [2, 2], tension: 0.1 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});

        // Gráfico de Decaimento de Fluídos (Combinado)
        new Chart(document.getElementById('chartFluids'), {{
            type: 'line',
            data: {{
                labels: ticks,
                datasets: [
                    {{ label: 'Adrenalina (Ataque)', data: {json.dumps(data_attack['fluids']['adren'])}, borderColor: '#ff4444', backgroundColor: 'rgba(255, 68, 68, 0.1)', fill: true, tension: 0.1 }},
                    {{ label: 'Dopamina (Curiosidade)', data: {json.dumps(data_explore['fluids']['dopa'])}, borderColor: '#4cc9f0', backgroundColor: 'rgba(76, 201, 240, 0.1)', fill: true, tension: 0.1 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});

        // Gráfico de Energia
        new Chart(document.getElementById('chartEnergy'), {{
            type: 'line',
            data: {{
                labels: ticks,
                datasets: [
                    {{ label: 'Gasto em Pânico', data: {json.dumps(data_attack['energy'])}, borderColor: '#ffb703', backgroundColor: 'rgba(255, 183, 3, 0.2)', fill: true, tension: 0.4 }},
                    {{ label: 'Gasto em Curiosidade', data: {json.dumps(data_explore['energy'])}, borderColor: '#fb8500', backgroundColor: 'rgba(251, 133, 0, 0.1)', fill: true, tension: 0.4 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});
    </script>
</body>
</html>
"""
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dash_projecao.html')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard HTML com os dados pre-calculados da projeção foi gerado: {save_path}")

if __name__ == "__main__":
    build_dashboard()
