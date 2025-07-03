#!/bin/bash

# Run the EnzymeML-RS (Suite) modelling
# This script uses the EnzymeML-RS (Suite) to fit the kinetic parameters to the measurements.
# The script uses the `enzymeml` command to run the modelling.
# The script uses the `sr1` solver to fit the kinetic parameters.
# The script uses the `rk4` solver to simulate the reaction.
# The script uses the `dt` parameter to set the time step for the simulation.

# Please note, since the EnzymeML Suite is a graphical application and in order to provide
# a reproducible workflow, we need to run the script from the terminal. Since the EnzymeML Suite
# is practically a graphical representation of the EnzymeML-RS CLI core functionality, we
# receive the exact same ouput.

# Run the EnzymeML-RS (Suite) modelling
enzymeml fit sr1 \
    -p enzmldoc.json \
    --log-transform \
    --solver rk4 \
    --dt 1.0
