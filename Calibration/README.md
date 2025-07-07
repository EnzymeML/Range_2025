# Concentration calculation with the calipytion package

This folder contains:

- [`ABTS_calibration_pH3.5.csv`](ABTS_calibration_pH3.5.csv) measurement data for ABTS calibration measurements
- [`abts_calibration.ipynb`](abts_calibration.ipynb) notebook to calibrate the ABTS concentration, read and process calibration data and apply the calibration to the EnzymeML file
- [`abts_standard.json`](abts_standard.json) the calibration data and fitted model

## Install calipytion

To install the calipytion package, you can use the following command:

```bash
pip install git+https://github.com/EnzymeML/calipytion.git
```
or

```bash
pip install calipytion
```

## Run the notebook

To run the notebook, you can use the following command:

```bash
jupyter notebook abts_calibration.ipynb
```