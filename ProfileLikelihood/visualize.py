import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.gridspec import GridSpec


def plot_profile_likelihoods():
    """
    Plot profile likelihoods for K_M, k_ie, and k_cat parameters
    in a compact two-row layout with scientific styling.
    """

    # Set up the figure with scientific styling and compact layout
    plt.style.use("seaborn-v0_8-whitegrid")
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 1], hspace=0.3, wspace=0.3)

    # Create subplots: K_M and k_cat on top row, k_ie spanning bottom row
    ax_km = fig.add_subplot(gs[0, 0])
    ax_kcat = fig.add_subplot(gs[0, 1])
    ax_kie = fig.add_subplot(gs[1, :])  # Span both columns

    axes = [ax_km, ax_kie, ax_kcat]  # Reorder to match original param order

    # Define parameters and their properties
    params = [
        {
            "file": "Km/SLAC_kinetic_assay_concentration_profile.tsv",
            "param_col": "K_M",
            "title": r"$K_M$ Profile Likelihood",
            "xlabel": r"$K_M$ (mM)",
            "color": "#2E86AB",
        },
        {
            "file": "k_ie/SLAC_kinetic_assay_concentration_profile.tsv",
            "param_col": "k_ie",
            "title": r"$k_{ie}$ Profile Likelihood",
            "xlabel": r"$k_{ie}$ (s$^{-1}$)",
            "color": "#A23B72",
        },
        {
            "file": "k_cat/SLAC_kinetic_assay_concentration_profile.tsv",
            "param_col": "k_cat",
            "title": r"$k_{cat}$ Profile Likelihood",
            "xlabel": r"$k_{cat}$ (s$^{-1}$)",
            "color": "#F18F01",
        },
    ]

    # Plot each parameter
    for i, param in enumerate(params):
        # Read the TSV file
        file_path = Path(param["file"])
        df = pd.read_csv(file_path, sep="\t")

        # Extract data
        x = df[param["param_col"]]
        y = df["relative_likelihood"]

        # Plot the profile likelihood
        axes[i].plot(x, y, linewidth=2.5, color=param["color"], alpha=0.8)
        axes[i].fill_between(x, y, alpha=0.3, color=param["color"])

        # Add confidence level lines
        axes[i].axhline(
            y=0.146,
            color="red",
            linestyle="--",
            alpha=0.7,
            linewidth=1.5,
            label="95% CI",
        )
        axes[i].axhline(
            y=0.036,
            color="darkred",
            linestyle=":",
            alpha=0.7,
            linewidth=1.5,
            label="99% CI",
        )

        # Find and mark the maximum likelihood point
        max_idx = y.idxmax()
        max_x = x.iloc[max_idx]  # type: ignore
        max_y = y.iloc[max_idx]  # type: ignore
        axes[i].plot(
            max_x,
            max_y,
            "o",
            color="darkred",
            markersize=8,
            markeredgecolor="white",
            markeredgewidth=2,
            zorder=5,
            label=f"MLE = {max_x:.3f}",
        )

        # Formatting
        axes[i].set_title(param["title"], fontsize=14, fontweight="bold", pad=15)
        axes[i].set_xlabel(param["xlabel"], fontsize=12)
        axes[i].set_ylabel("Relative Likelihood", fontsize=12)
        axes[i].grid(True, alpha=0.3)
        axes[i].set_ylim(0, 1.1)

        # Add legend for all subplots
        axes[i].legend(loc="upper right", fontsize=10, framealpha=0.9)

        # Improve tick formatting
        axes[i].tick_params(axis="both", which="major", labelsize=10)

        # Set scientific notation for small values if needed
        if param["param_col"] == "k_ie":
            axes[i].ticklabel_format(style="scientific", axis="x", scilimits=(0, 0))

    # Save the figure
    output_path = Path("profile_likelihood_analysis.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Figure saved to: {output_path}")

    # Show the plot
    plt.show()

    return fig, axes


def print_summary_statistics():
    """
    Print summary statistics for each parameter's profile likelihood.
    """
    print("\n" + "=" * 60)
    print("PROFILE LIKELIHOOD SUMMARY STATISTICS")
    print("=" * 60)

    params = [
        ("Km/SLAC_kinetic_assay_concentration_profile.tsv", "K_M", "K_M (mM)"),
        ("k_ie/SLAC_kinetic_assay_concentration_profile.tsv", "k_ie", "k_ie (s⁻¹)"),
        ("k_cat/SLAC_kinetic_assay_concentration_profile.tsv", "k_cat", "k_cat (s⁻¹)"),
    ]

    for file_path, param_col, param_name in params:
        df = pd.read_csv(file_path, sep="\t")

        # Find MLE
        max_idx = df["relative_likelihood"].idxmax()
        mle_value = df[param_col].iloc[max_idx]  # type: ignore
        mle_likelihood = df["relative_likelihood"].iloc[max_idx]  # type: ignore

        # Find confidence intervals (approximate)
        ci_95_threshold = 0.146
        ci_99_threshold = 0.036

        ci_95_mask = df["relative_likelihood"] >= ci_95_threshold
        ci_99_mask = df["relative_likelihood"] >= ci_99_threshold

        if ci_95_mask.any():
            ci_95_range = (
                df[param_col][ci_95_mask].min(),
                df[param_col][ci_95_mask].max(),
            )
        else:
            ci_95_range = (np.nan, np.nan)

        if ci_99_mask.any():
            ci_99_range = (
                df[param_col][ci_99_mask].min(),
                df[param_col][ci_99_mask].max(),
            )
        else:
            ci_99_range = (np.nan, np.nan)

        print(f"\n{param_name}:")
        print(f"  MLE: {mle_value:.6f}")
        print(f"  Max Likelihood: {mle_likelihood:.6f}")
        print(f"  95% CI: [{ci_95_range[0]:.6f}, {ci_95_range[1]:.6f}]")
        print(f"  99% CI: [{ci_99_range[0]:.6f}, {ci_99_range[1]:.6f}]")


if __name__ == "__main__":
    # Create the visualization
    fig, axes = plot_profile_likelihoods()

    # Print summary statistics
    print_summary_statistics()

    print("\nVisualization complete! Check the generated plot.")
