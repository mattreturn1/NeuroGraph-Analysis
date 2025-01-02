import pandas as pd

def select_metric(csv_file_path):
    """
    Analizza i valori in un file CSV e calcola la metrica consigliata in base alla media dei valori per tutti i grafi.

    :param csv_file_path: Percorso del file CSV
    :return: Una lista di metriche consigliate
    """
    # Legge il file CSV
    df = pd.read_csv(csv_file_path)

    # Lista di metriche
    metrics = ['Closeness', 'Clustering', 'Degree']

    # Calcola la media dei valori per ciascuna metrica
    metric_means = {metric: df[metric].mean() for metric in metrics}

    # Controlla se tutte le metriche hanno valore medio pari a 0 (False)
    if all(mean == 0 for mean in metric_means.values()):
        return "Nessuna metrica consigliata: tutte le metriche sono False"

    # Trova la metrica con il valore medio più alto
    best_metric = max(metric_means, key=metric_means.get)

    return best_metric

# Esempio di utilizzo
file_path = "../computing/analysis/ppmi/60_70/comparison/swedd/graph_analysis.csv"
recommended_metric = select_metric(file_path)
print(f"Metrica consigliata pd: {recommended_metric}")
file_path = "../computing/analysis/ppmi/60_70/comparison/swedd/node_analysis.csv"
recommended_metric = select_metric(file_path)
print(f"Metrica consigliata pd: {recommended_metric}")

