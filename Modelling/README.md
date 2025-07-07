# Modelling the reaction of ABTS with SLAC

Within this folder, we supply the source code for the modelling of the reaction of ABTS with SLAC using EnzymeML-RS (Suite), PyEnzyme (PySCeS) and Catalax (JAX) detailed in the publication *Range, J. et al. (2025)*. The dataset `enzmldoc.json` has previously been created using the EnzymeML Suite and enriched with measurement data from the `CaliPytion` package.

The folder contains the following files:

- `enzmldoc.json`: The EnzymeML file containing the reaction of ABTS with SLAC.
- `enzymeml_rs.sh`: The script to run the EnzymeML-RS (Suite) modelling.
- `PyEnzymePySCeSModelling.ipynb`: The notebook to run the PyEnzyme (PySCeS) modelling.
- `CatalaxModelling.ipynb`: The notebook to run the Catalax (JAX) modelling.
- `results/`: The folder containing the results of the modelling.
  - `suite_report.json`: The report of the EnzymeML-RS (Suite) modelling.
  - `suite_fitted_models.json`: The EnzymeML file containing the results of the EnzymeML-RS (Suite) modelling.
  - `pysces_fitted_models.json`: The EnzymeML file containing the results of the PyEnzyme (PySCeS) modelling.
  - `pyenzyme_pysces_modelling.png`: The plot of the PyEnzyme (PySCeS) modelling.
  - `catalax_jax_modelling.png`: The plot of the Catalax (JAX) modelling.

## How to run each modelling script

### EnzymeML-RS (Suite)

To run the EnzymeML-RS (Suite) modelling, you can use the following command:

```bash
./enzymeml_rs.sh
```

> [!NOTE]
> Please note, since the EnzymeML Suite is a graphical application and in order to provide
> a reproducible workflow, we need to run the script from the terminal. Since the EnzymeML Suite
> is practically a graphical representation of the EnzymeML-RS CLI core functionality, we
> receive the exact same ouput.

### PyEnzyme (PySCeS)

To run the PyEnzyme (PySCeS) modelling, you can use the following command:

```bash
jupyter notebook PyEnzymePySCeSModelling.ipynb
```

### Catalax (JAX)

To run the Catalax (JAX) modelling, you can use the following command:

```bash
jupyter notebook CatalaxModelling.ipynb
```
