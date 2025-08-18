import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def entrenar_clustering(csv_path: str, n_clusters: int = 3):
    """
    Entrena un modelo K-Means no supervisado usando el CSV de lecturas.
    - Escala los datos
    - Aplica clustering
    - Guarda el modelo en datos/modelos/kmeans_model.pkl
    - Devuelve DataFrame con columna 'Cluster'
    """

    # Crear carpeta para guardar modelos
    os.makedirs("datos/modelos", exist_ok=True)

    # Cargar CSV
    df = pd.read_csv(csv_path)

    # Transformar DiaSemana a número
    dias_semana = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3,
                   "Friday":4, "Saturday":5, "Sunday":6}
    df["DiaSemana_num"] = df["DiaSemana"].map(dias_semana)

    features = ["Valor", "Hora", "DiaSemana_num"]
    X = df[features]

    # Escalar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Entrenar K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    df["Cluster"] = clusters

    # Guardar modelo
    joblib.dump(kmeans, "datos/modelos/kmeans_model.pkl")
    print("Modelo K-Means guardado en datos/modelos/kmeans_model.pkl")

    return df


def generar_informe_pdf(df: pd.DataFrame, output_path: str):
    """
    Genera un informe en PDF con:
    - Silhouette Score
    - Estadísticas de cada cluster
    - Gráfico 3D de clusters
    """

    # Escalar datos
    features = ["Valor", "Hora", "DiaSemana_num"]
    X_scaled = StandardScaler().fit_transform(df[features])

    # Métricas
    score = silhouette_score(X_scaled, df["Cluster"])
    cluster_counts = df["Cluster"].value_counts()
    cluster_means = df.groupby("Cluster")["Valor"].mean()

    # Crear gráfico temporalmente
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(df["Valor"], df["Hora"], df["DiaSemana_num"], 
                         c=df["Cluster"], cmap="viridis", alpha=0.7)
    ax.set_xlabel("Valor")
    ax.set_ylabel("Hora")
    ax.set_zlabel("DiaSemana")
    plt.title(f"Clusters K-Means (k={df['Cluster'].nunique()})")
    plt.colorbar(scatter, ax=ax, label="Cluster")
    tmp_img_path = "temp_cluster_plot.png"
    plt.savefig(tmp_img_path)
    plt.close()

    # Crear PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height-50, "Informe Clustering K-Means")
    c.setFont("Helvetica", 12)
    c.drawString(50, height-80, f"Silhouette Score: {score:.3f}")

    # Escribir estadísticas
    y_pos = height - 110
    c.drawString(50, y_pos, "Cantidad de lecturas por cluster:")
    y_pos -= 20
    for idx, val in cluster_counts.items():
        c.drawString(60, y_pos, f"Cluster {idx}: {val} lecturas")
        y_pos -= 15

    y_pos -= 10
    c.drawString(50, y_pos, "Promedio de Valor por cluster:")
    y_pos -= 20
    for idx, val in cluster_means.items():
        c.drawString(60, y_pos, f"Cluster {idx}: {val:.2f}")
        y_pos -= 15

    # Insertar gráfico
    y_pos -= 10
    if os.path.exists(tmp_img_path):
        img = ImageReader(tmp_img_path)
        c.drawImage(img, 50, y_pos-300, width=500, height=300)

    c.save()
    os.remove(tmp_img_path)
    print(f"Informe PDF generado en {output_path}")
