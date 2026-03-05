import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Define a pasta de destino para as imagens
output_dir = os.path.join(os.path.dirname(__file__), "graficos_neurobiologia")
os.makedirs(output_dir, exist_ok=True)

# Dataset expandido
data = {
    "Animal": [
        "Humano", "Cachalote", "Elefante", "Chimpanzé", "Macaco-Prego", 
        "Cachorro", "Gato", "Corvo", "Arara", "Rato", 
        "Musaranho", "Mosca-das-Frutas", "Aranha-Saltadora", "C. elegans"
    ],
    "Cerebro_Massa_g": [
        1350, 7800, 4600, 400, 52, 
        72, 30, 15, 14, 2, 
        0.1, 0.00001, 0.000005, 0.0000001
    ],
    "Neuronio_Total_Bilh": [
        86.0, 200.0, 257.0, 28.0, 3.7,
        2.2, 1.2, 1.5, 1.4, 0.07,
        0.004, 0.00025, 0.0001, 0.000000302
    ],
    "Neuronio_Cortical_Bilh": [
        16.3, 10.5, 5.6, 6.2, 1.1,
        0.53, 0.25, 1.2, 1.1, 0.02,
        0.001, 0, 0, 0
    ],
    "FPS_Biologico_Hz": [
        60, 20, 15, 60, 80,
        75, 55, 100, 120, 100,
        150, 250, 200, 50
    ]
}

df = pd.DataFrame(data)

# Configurando o estilo Seaborn para ficar "Dark/Sci-Fi" combinando com Melanora
sns.set_theme(style="darkgrid")
plt.style.use("dark_background")

def create_scatter_neurons_vs_mass():
    plt.figure(figsize=(10, 6))
    
    # Vamos usar log scale por conta da disparidade absurda (Elefante vs Mosca)
    # Apenas removermos quem tem massa extremíssima para focar nos vertebrados se quisermos,
    # mas log-log abraça todos.
    
    ax = sns.scatterplot(
        data=df, 
        x="Cerebro_Massa_g", 
        y="Neuronio_Total_Bilh", 
        size="FPS_Biologico_Hz", 
        sizes=(50, 500), 
        hue="FPS_Biologico_Hz",
        palette="cool",
        alpha=0.8
    )
    
    # Anotar nome dos animais
    for i in range(df.shape[0]):
        plt.text(
            df.Cerebro_Massa_g[i] * 1.1, 
            df.Neuronio_Total_Bilh[i], 
            df.Animal[i], 
            fontsize=9,
            color='white'
        )

    plt.xscale('log')
    plt.yscale('log')
    plt.title("Relação Absoluta: Massa do Cérebro vs Total de Neurônios (Escala Log)", fontsize=14, pad=15)
    plt.xlabel("Massa do Cérebro (gramas)", fontsize=12)
    plt.ylabel("Total de Neurônios (Bilhões)", fontsize=12)
    
    path = os.path.join(output_dir, "01_relacao_massa_neuronios.png")
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Gráfico salvo: {path}")

def create_bar_fps():
    plt.figure(figsize=(12, 7))
    
    # Ordenar por FPS Biologico
    df_sorted = df.sort_values(by="FPS_Biologico_Hz", ascending=False)
    
    ax = sns.barplot(
        data=df_sorted, 
        x="FPS_Biologico_Hz", 
        y="Animal", 
        hue="FPS_Biologico_Hz",
        palette="plasma",
        legend=False
    )
    
    plt.title("Percepção Temporal: FPS Biológico (Frequência Média em Hz)", fontsize=14, pad=15)
    plt.xlabel("Frequência Visual Crítica (Flicker Fusion - Hz)", fontsize=12)
    plt.ylabel("")
    
    # Adicionar anotações de quão mais rápido que humanos é
    human_fps = df[df["Animal"] == "Humano"]["FPS_Biologico_Hz"].values[0]
    for i, p in enumerate(ax.patches):
        width = p.get_width()
        ratio = width / human_fps
        if ratio > 1.2:
            ax.text(width + 2, p.get_y() + p.get_height()/2, f"{ratio:.1f}x Humano", va='center', fontsize=9, color='lightgreen')
            
    path = os.path.join(output_dir, "02_fps_biologico.png")
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Gráfico salvo: {path}")
    
def create_scatter_cortical():
    # Remover insetos que não tem córtex igual a mamiferos/aves para esse gráfico
    df_cortex = df[df["Neuronio_Cortical_Bilh"] > 0]
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=df_cortex.sort_values("Neuronio_Cortical_Bilh", ascending=False),
        x="Neuronio_Cortical_Bilh",
        y="Animal",
        color="cyan"
    )
    plt.title("Densidade da Consciência: Estima-se Neurônios no Córtex/Pálio (Bilhões)", fontsize=14)
    plt.xlabel("Bilhão de Neurônios")
    plt.ylabel("")
    
    path = os.path.join(output_dir, "03_densidade_cortical.png")
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Gráfico salvo: {path}")

if __name__ == "__main__":
    print("Gerando gráficos de visualização (Matplotlib + Seaborn)...")
    create_scatter_neurons_vs_mass()
    create_bar_fps()
    create_scatter_cortical()
    print("Concluído!")
