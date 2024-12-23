import data_extractor
from scipy.stats import ttest_ind
from pathlib import Path


def compare_networks_metrics(directory_path, *directories_to_compare):
    """
    Compare metrics between networks in the given directories using t-tests.
    """
    directory_path = Path(directory_path)

    # Dictionaries to store statistics
    control_statistics = {}
    patient_statistics = {}

    # Extract metrics for all directories
    for directory in directories_to_compare:
        network_statistics, node_statistics = data_extractor.extract_metrics(directory_path / directory)
        if directory == "control":
            control_statistics["control"] = [network_statistics, node_statistics]
        else:
            patient_statistics[directory] = [network_statistics, node_statistics]

    # Dictionaries to store differences
    graph_differences = {}
    node_differences = {}

    # Compare metrics
    for case in patient_statistics.keys():
        graph_differences[case] = {}
        node_differences[case] = {}

        for metric in ["closeness", "clustering", "degree"]:
            # Global metrics comparison
            control = control_statistics["control"][0][metric]["mean"]
            patient = patient_statistics[case][0][metric]["mean"]

            mean_difference = abs(control - patient)
            t_stat, p_value = ttest_ind([control], [patient])  # Wrap in lists for compatibility

            graph_differences[case][metric] = {
                "mean difference": mean_difference,
                "t_stat": t_stat,
                "p_value": p_value
            }

            # Node-level metrics comparison
            node_differences[case][metric] = []
            for i in range(116):
                control = control_statistics["control"][1][metric]["mean"][i]
                patient = patient_statistics[case][1][metric]["mean"][i]

                mean_difference = abs(control - patient)
                t_stat, p_value = ttest_ind([control], [patient])  # Wrap in lists for compatibility

                node_differences[case][metric].append({
                    "node": i,
                    "mean difference": mean_difference,
                    "t_stat": t_stat,
                    "p_value": p_value
                })

    # Estrai i 5 nodi con differenze maggiori per ciascun caso e metrica
    top_nodes = extract_top_differences(node_differences)

    # Print results
    print("Differenze a livello di grafo:", graph_differences)
    print("\n------------------------------------\n")
    print("Differenze a livello di nodo:", node_differences)
    print("\n------------------------------------\n")
    print("Top 5 nodi con differenze maggiori:", top_nodes)


def extract_top_differences(node_differences, top_n=5):
    """
    Estrai i top N nodi con le differenze maggiori per ogni caso e metrica.
    """
    top_nodes = {}
    for case, metrics in node_differences.items():
        top_nodes[case] = {}
        for metric, nodes in metrics.items():
            sorted_nodes = sorted(nodes, key=lambda x: x["mean difference"], reverse=True)
            top_nodes[case][metric] = sorted_nodes[:top_n]
    return top_nodes


# Example usage
directory_path = "~/Documents/UniPd/Computer Engineering/Learning From Networks/abide_prova/12_18"
directories_to_compare = ["control", "patient"]

directory_path = Path(directory_path).expanduser()

compare_networks_metrics(directory_path, *directories_to_compare)
