import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Definir rutas base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # SmartWasteApi/
DATA_DIR = os.path.join(BASE_DIR, "public")
MODELOS_DIR = os.path.join(DATA_DIR, "modelos")
os.makedirs(MODELOS_DIR, exist_ok=True)

def entrenar_clustering(csv_path: str, n_clusters: int = 3):
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            raise ValueError("El CSV está vacío.")

        dias_semana = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3,
                       "Friday":4, "Saturday":5, "Sunday":6}
        if "DiaSemana" in df.columns:
            df["DiaSemana_num"] = df["DiaSemana"].map(dias_semana)
        else:
            raise KeyError("Columna 'DiaSemana' no encontrada en CSV.")

        features = ["Valor", "Hora", "DiaSemana_num"]
        for col in features:
            if col not in df.columns:
                raise KeyError(f"Columna requerida faltante: {col}")

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[features])

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df["Cluster"] = kmeans.fit_predict(X_scaled)

        model_path = os.path.join(MODELOS_DIR, "kmeans_model.pkl")
        joblib.dump(kmeans, model_path)
        print(f"✅ Modelo K-Means guardado en {model_path}")

        return df
    except Exception as e:
        print(f"❌ Error en entrenamiento: {e}")
        raise

def generar_informe_pdf(df: pd.DataFrame, output_path: str):
    """
    Genera un informe en PDF con:
    - Silhouette Score
    - Estadísticas de cada cluster
    - Dos gráficos 2D
    - Tabla de promedios por cluster
    - Interpretación automática
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    import matplotlib.pyplot as plt
    import os
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score

    try:
        features = ["Valor", "Hora", "DiaSemana_num"]
        for col in features + ["Cluster"]:
            if col not in df.columns:
                raise KeyError(f"Columna requerida faltante: {col}")

        # Escalar datos
        X_scaled = StandardScaler().fit_transform(df[features])

        # Métricas
        score = silhouette_score(X_scaled, df["Cluster"])
        cluster_counts = df["Cluster"].value_counts()
        cluster_means = df.groupby("Cluster")[features].mean().round(2)

        # Gráficos 2D
        tmp_img_path1 = os.path.join("public", "temp_plot1.png")
        tmp_img_path2 = os.path.join("public", "temp_plot2.png")

        # Valor vs Hora
        plt.figure(figsize=(6,4))
        for c in df["Cluster"].unique():
            subset = df[df["Cluster"] == c]
            plt.scatter(subset["Hora"], subset["Valor"], label=f"Cluster {c}", alpha=0.7)
        plt.xlabel("Hora")
        plt.ylabel("Valor")
        plt.title("Distribución de Valor vs Hora")
        plt.legend()
        plt.tight_layout()
        plt.savefig(tmp_img_path1, dpi=120)
        plt.close()

        # Valor vs DiaSemana_num
        plt.figure(figsize=(6,4))
        for c in df["Cluster"].unique():
            subset = df[df["Cluster"] == c]
            plt.scatter(subset["DiaSemana_num"], subset["Valor"], label=f"Cluster {c}", alpha=0.7)
        plt.xlabel("Día de la semana (0=Lunes)")
        plt.ylabel("Valor")
        plt.title("Distribución de Valor vs Día de la semana")
        plt.legend()
        plt.tight_layout()
        plt.savefig(tmp_img_path2, dpi=120)
        plt.close()

        # Crear PDF
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        y_pos = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y_pos, "Informe Clustering K-Means")
        y_pos -= 30

        c.setFont("Helvetica", 12)
        c.drawString(50, y_pos, f"Silhouette Score: {score:.3f}")
        y_pos -= 20

        c.drawString(50, y_pos, "Cantidad de lecturas por cluster:")
        y_pos -= 15
        for idx, val in cluster_counts.items():
            c.drawString(60, y_pos, f"Cluster {idx}: {val} lecturas")
            y_pos -= 15

        y_pos -= 10
        c.drawString(50, y_pos, "Promedios por cluster:")
        y_pos -= 15

        # Tabla de promedios
        for idx, row in cluster_means.iterrows():
            line = f"Cluster {idx}: " + ", ".join([f"{col}={row[col]}" for col in features])
            c.drawString(60, y_pos, line)
            y_pos -= 15

        # Interpretación automática
        y_pos -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_pos, "Interpretación automática:")
        y_pos -= 15
        c.setFont("Helvetica", 12)
        for idx, row in cluster_means.iterrows():
            c.drawString(60, y_pos,
                         f"Cluster {idx}: Representa lecturas con " +
                         ", ".join([f"{col} ~ {row[col]}" for col in features]))
            y_pos -= 15

        # Insertar gráficos
        if os.path.exists(tmp_img_path1):
            c.drawImage(ImageReader(tmp_img_path1), 50, y_pos-250, width=250, height=200)
        if os.path.exists(tmp_img_path2):
            c.drawImage(ImageReader(tmp_img_path2), 320, y_pos-250, width=250, height=200)

        c.save()

        # Borrar imágenes temporales
        for tmp_img in [tmp_img_path1, tmp_img_path2]:
            if os.path.exists(tmp_img):
                os.remove(tmp_img)

        print(f"✅ Informe PDF actualizado generado en {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"❌ Error al generar informe: {e}")
        raise
