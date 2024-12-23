import metrics_computator
from pathlib import Path
import numpy as np


def from_matrix_to_network(file_path):
    """
    Convert a correlation matrix into a weighted network graph.
    """
    matrix = metrics_computator.load_and_process_matrix(file_path)
    return metrics_computator.create_weighted_graph(matrix)


def extract_metrics(directory_path):
    """
    Extract global and node-level metrics from brain network files in a directory.
    """
    directory = Path(directory_path)

    # Initialize metrics containers
    graph_metrics = {
        "closeness": [],
        "clustering": [],
        "degree": []
    }

    node_metrics = {
        "closeness": [[] for _ in range(116)],
        "clustering": [[] for _ in range(116)],
        "degree": [[] for _ in range(116)]
    }

    for file in directory.iterdir():
        if file.suffix == ".mat":
            try:
                brain_network = from_matrix_to_network(file)

                # Compute metrics
                closeness_centrality = metrics_computator.compute_closeness_centrality(brain_network)
                clustering_coefficient = metrics_computator.compute_clustering_coefficients(brain_network)
                degree_centrality = metrics_computator.compute_degree_centrality(brain_network)

                # Aggregate global metrics
                graph_metrics["closeness"].append(np.mean(list(closeness_centrality.values())))
                graph_metrics["clustering"].append(np.mean(list(clustering_coefficient.values())))
                graph_metrics["degree"].append(np.mean(list(degree_centrality.values())))

                # Aggregate node-level metrics
                for i, node in enumerate(brain_network.nodes):
                    node_metrics["closeness"][i].append(closeness_centrality[node])
                    node_metrics["clustering"][i].append(clustering_coefficient[node])
                    node_metrics["degree"][i].append(degree_centrality[node])

            except Exception as e:
                print(f"Error processing {file}: {e}")

    # Compute global statistics
    graph_statistics = {
        metric: {
            "mean": np.mean(values),
            "median": np.median(values),
            "std": np.std(values)
        }
        for metric, values in graph_metrics.items()
    }

    # Compute node-level statistics
    node_statistics = {
        metric: {
            "mean": [np.mean(values) for values in node_metrics[metric]],
            "median": [np.median(values) for values in node_metrics[metric]],
            "std": [np.std(values) for values in node_metrics[metric]]
        }
        for metric in node_metrics
    }

    return graph_statistics, node_statistics
