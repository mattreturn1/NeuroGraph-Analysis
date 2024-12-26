from pathlib import Path
import pandas as pd


def load_metrics(directory_path, group_name):
    """
    Load graph and node metrics for a specific group.

    Args:
        directory_path (Path): Path to the directory containing metrics files.
        group_name (str): Name of the group (e.g., "control", "pd").

    Returns:
        dict: Graph and node metrics as DataFrames.
    """
    graph_metrics_file = directory_path / group_name / "stats" / "graph_statistics.csv"
    node_metrics_file = directory_path / group_name / "stats" / "node_statistics.csv"

    graph_metrics = pd.read_csv(graph_metrics_file)
    node_metrics = pd.read_csv(node_metrics_file)
    return {"graph": graph_metrics, "node": node_metrics}


def calculate_differences(control_metrics, patient_metrics, metric_type):
    """
    Calculate differences for a specific metric type (graph or node) between groups.

    Args:
        control_metrics (pd.DataFrame): Metrics for the control group.
        patient_metrics (pd.DataFrame): Metrics for the patient group.
        metric_type (str): Type of metric ("graph" or "node").

    Returns:
        pd.DataFrame: Differences in metrics between groups.
    """
    differences = patient_metrics.copy()
    for column in control_metrics.columns:
        if column not in ["Node", "Metric"]:
            differences[column] = abs(patient_metrics[column] - control_metrics[column])
    differences["group"] = f"diff_{metric_type}"
    return differences


def compare_groups(directory_path, groups, output_path=None):
    """
    Compare metrics between control and patient groups.

    Args:
        directory_path (Path): Path to the base directory containing group metrics.
        groups (list): List of groups to compare (e.g., ["control", "pd"]).
        output_path (Path): Optional path to save results.

    Returns:
        dict: Differences in graph and node metrics.
    """
    directory_path = Path(directory_path)
    metrics = {group: load_metrics(directory_path, group) for group in groups}

    control_metrics = metrics["control"]
    results = {}

    for group in groups:
        if group == "control":
            continue

        patient_metrics = metrics[group]
        graph_diff = calculate_differences(
            control_metrics["graph"], patient_metrics["graph"], "graph"
        )
        node_diff = calculate_differences(
            control_metrics["node"], patient_metrics["node"], "node"
        )

        results[group] = {"graph_diff": graph_diff, "node_diff": node_diff}

        # Save results to CSV if output_path is specified
        if output_path:
            save_path = Path(output_path)
            save_path.mkdir(parents=True, exist_ok=True)
            graph_diff.to_csv(save_path / "graph_differences.csv", index=False)
            node_diff.to_csv(save_path / "node_differences.csv", index=False)

    return results


def summarize_results(results, top_n=5):
    """
    Summarize top N differences in node metrics.

    Args:
        results (dict): Results from compare_groups.
        top_n (int): Number of top nodes to summarize.

    Returns:
        dict: Summary of top node differences for each group.
    """
    summary = {}
    for group, diffs in results.items():
        top_nodes = diffs["node_diff"].nlargest(top_n, "mean difference")
        summary[group] = top_nodes
    return summary


compare_groups("analysis/abide/11-", ["control", "patient"],
               "analysis/abide/11-/comparison")