from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu
import pandas as pd
from pathlib import Path


def load_metrics(directory_path, group_name):
    """
    Load graph and node metrics for a specific group.

    Args:
        directory_path (Path): Path to the directory containing metrics files.
        group_name (str): Name of the group (e.g., "control", "pd").

    Returns:
        dict: Graph and node metrics as DataFrames.
    """
    graph_metrics_file = directory_path / group_name / "metrics" / "graph_metrics.csv"
    node_metrics_file = directory_path / group_name / "metrics" / "node_metrics.csv"

    graph_metrics = pd.read_csv(graph_metrics_file)
    node_metrics = pd.read_csv(node_metrics_file)
    return {"graph": graph_metrics, "node": node_metrics}


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
            save_path = Path(output_path) / group
            save_path.mkdir(parents=True, exist_ok=True)
            graph_diff.to_csv(save_path / "graph_analysis.csv", index=False)
            node_diff.to_csv(save_path / "node_analysis.csv", index=False)

    return results


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
    if metric_type == "graph":
        differences = patient_metrics.copy()
        for column in control_metrics.columns:
            if column not in ["Graph"]:
                differences[column] = verify_significant_differences(control_metrics[column], patient_metrics[column])
        differences["group"] = f"diff_{metric_type}"
    else:
        differences = pd.DataFrame(columns=["Node", "Closeness", "Clustering", "Degree"])
        for node in range(116):
            differences.loc[node - 1, "Node"] = node
            node_control_metrics = control_metrics[control_metrics["Node"] == node]
            node_patient_metrics = patient_metrics[patient_metrics["Node"] == node]

            print(node_control_metrics)
            print(node_patient_metrics)

            for column in control_metrics.columns:
                if column not in ["Node", "Graph"]:
                    differences.loc[node - 1, column] = verify_significant_differences(node_control_metrics[column],
                                                                                       node_patient_metrics[column])
            differences["group"] = f"diff_{metric_type}"

    return differences


def verify_significant_differences(first_group, second_group):
    if is_normal_distribution(first_group) and is_normal_distribution(second_group):
        if are_variances_similar(first_group, second_group):
            t_stat, p_value = ttest_ind(first_group, second_group, equal_var=True)
        else:
            t_stat, p_value = ttest_ind(first_group, second_group, equal_var=False)
    else:
        mwu_stat, p_value = mannwhitneyu(first_group, second_group)

    return p_value < 0.05


def is_normal_distribution(group):
    _, p_value = shapiro(group)

    return p_value >= 0.05


def are_variances_similar(first_group, second_group, test_type=levene):
    _, p_value = test_type(first_group, second_group)

    return p_value >= 0.05


compare_groups("analysis/abide/11-", ["control", "patient"],
               "analysis/abide/11-/comparison")