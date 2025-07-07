import json

import matplotlib.pyplot as plt
import numpy as np
import pyenzyme as pe
from scipy.integrate import odeint


def simulate_enzyme_kinetics(
    initial_abts,
    initial_slac,
    time_points,
    k_cat,
    K_M,
    k_ie,
):
    """
    Simulate enzyme kinetics using odeint based on the fitted model.

    Parameters:
    -----------
    initial_abts : float
    initial_slac : float
    time_points : array-like
    k_cat : float
    K_M : float
    k_ie : float

    Returns:
    --------
    solution : ndarray
        Array with shape (len(time_points), 2) containing [abts, slac] concentrations
    """

    def ode_system(y, t, k_cat, K_M, k_ie):
        """
        ODE system for enzyme kinetics:
        d[abts]/dt = -(k_cat * slac * abts) / (K_M + abts)
        d[slac]/dt = - k_ie * slac
        """
        abts, slac = y

        dabts_dt = -(k_cat * slac * abts) / (K_M + abts)
        dslac_dt = -k_ie * slac

        return [dabts_dt, dslac_dt]

    # Initial conditions
    y0 = [initial_abts, initial_slac]

    # Solve ODE system
    solution = odeint(ode_system, y0, time_points, args=(k_cat, K_M, k_ie))

    return solution


def extract_initial_conditions(doc):
    """
    Extract initial conditions from measurements, grouping every 3 as replicates.

    Parameters:
    -----------
    doc : EnzymeMLDocument
        The loaded EnzymeML document

    Returns:
    --------
    init_conditions : list
        List of dictionaries with mean 'abts' and 'slac' initial concentrations for each group
    """
    init_conditions = []
    current_group = []

    for m_id, meas in enumerate(doc.measurements):
        substrate = [
            species for species in meas.species_data if species.species_id == "abts"
        ][0]
        enzyme = [
            species for species in meas.species_data if species.species_id == "slac"
        ][0]

        # Add current measurement to group
        current_group.append(
            {
                "abts": substrate.initial,
                "slac": enzyme.initial,
            }
        )

        # Every 3 measurements, calculate means and finalize the group
        if (m_id + 1) % 3 == 0:
            # Calculate mean initial conditions
            mean_abts = np.mean([rep["abts"] for rep in current_group])
            mean_slac = np.mean([rep["slac"] for rep in current_group])

            init_conditions.append(
                {
                    "abts": mean_abts,
                    "slac": mean_slac,
                }
            )
            current_group = []

    return init_conditions


def main():
    """
    Main function to run the publication plotting.
    """
    # Load data
    doc = pe.read_enzymeml("Modelling/results/fitted_model.json")
    k_cat, Km, kie = doc.parameters

    print("Loaded parameters:")
    print(
        f"k_cat = {k_cat.value:.6f} [{k_cat.lower_bound:.6f}, {k_cat.upper_bound:.6f}]"
    )
    print(f"Km = {Km.value:.6f} [{Km.lower_bound:.6f}, {Km.upper_bound:.6f}]")
    print(f"kie = {kie.value:.6f} [{kie.lower_bound:.6f}, {kie.upper_bound:.6f}]")

    # Extract initial conditions
    init_conditions = extract_initial_conditions(doc)
    print(f"Found {len(init_conditions)} experimental conditions")

    # Create plots
    print("\nGenerating plots...")

    # Create subplot layout
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # First plot: Calibration data
    plt.sca(ax1)

    # Load calibration data
    with open("Calibration/abts_standard.json", "r") as f:
        cal_data = json.load(f)

    # Extract concentrations and signals
    concentrations = []
    signals = []

    for sample in cal_data["samples"]:
        concentrations.append(sample["concentration"])
        signals.append(sample["signal"])

    # Plot calibration data points
    ax1.scatter(
        concentrations,
        signals,
        color="black",
        alpha=0.5,
        s=30,
        label="Experimental data",
    )

    # Plot fitted calibration line
    a = cal_data["result"]["parameters"][1]["value"]  # slope parameter
    b = cal_data["result"]["parameters"][0]["value"]  # intercept parameter

    conc_range = np.linspace(0, max(concentrations), 100)
    fitted_signal = a * conc_range + b

    ax1.plot(
        conc_range,
        fitted_signal,
        "k-",
        alpha=0.5,
        label="Calibration model fit",
    )

    ax1.set_xlabel("ABTS / μM")
    ax1.set_ylabel(r"$A_{340}\;/\;\mathrm{A.U.}$")

    ax1.legend()

    # Add subplot label A
    ax1.text(
        -0.05,
        1.07,
        "A",
        transform=ax1.transAxes,
        fontsize=15,
        fontweight="bold",
        va="top",
        ha="left",
    )

    # Second plot: Kinetics data with best fit lines
    plt.sca(ax2)

    # Plot experimental data
    for m_id, meas in enumerate(doc.measurements):
        for species in meas.species_data:
            if species.data and species.species_id == "abts":
                ax2.scatter(
                    species.time,
                    species.data,
                    alpha=0.5,
                    color="black",
                    s=30,
                    label="Experimental data" if m_id == 0 else "",
                )

    # Plot best fit lines for each condition
    for i, condition in enumerate(init_conditions):
        t = np.linspace(0, 899, 100)

        # Best fit simulation using mean initial conditions
        solution_best = simulate_enzyme_kinetics(
            condition["abts"], condition["slac"], t, k_cat.value, Km.value, kie.value
        )

        # Plot best fit line
        ax2.plot(
            t,
            solution_best[:, 0],
            color="black",
            alpha=0.5,
            label="Kinetic model fit" if i == 0 else "",
        )

    ax2.set_xlabel("Time / s")
    ax2.set_ylabel("ABTS / μM")
    ax2.legend()

    # Add subplot label B
    ax2.text(
        -0.05,
        1.07,
        "B",
        transform=ax2.transAxes,
        fontsize=15,
        fontweight="bold",
        va="top",
        ha="left",
    )

    ax1.grid(linestyle=":", alpha=0.5)
    ax2.grid(linestyle=":", alpha=0.5)
    plt.tight_layout()
    print("Plots saved as PNG files and displayed.")
    plt.savefig("Figures/figure.png", dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    main()
