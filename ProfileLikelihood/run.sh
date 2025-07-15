# Bounds
KM_BOUNDS="20.0:180.0"
KCAT_BOUNDS="0.2:1.7"
KIE_BOUNDS="0.0006:0.004"

# Hyperparameters
STEPS=100
DT=10.0
SOLVER=rk4

# Profile for K_M
enzymeml profile sr1 \
    -p ../EnzymeML_Documents/SLAC_kinetic_assay_concentration.json \
    --log-transform \
    --solver $SOLVER \
    --dt $DT \
    --steps $STEPS \
    --parameter K_M=$KM_BOUNDS \
    --out ./Km

# Profile for k_cat
enzymeml profile sr1 \
    -p ../EnzymeML_Documents/SLAC_kinetic_assay_concentration.json \
    --log-transform \
    --solver $SOLVER \
    --dt $DT \
    --steps $STEPS \
    --parameter k_cat=$KCAT_BOUNDS \
    --out ./k_cat

# Profile for k_ie
enzymeml profile sr1 \
    -p ../EnzymeML_Documents/SLAC_kinetic_assay_concentration.json \
    --log-transform \
    --solver $SOLVER \
    --dt $DT \
    --steps $STEPS \
    --parameter k_ie=$KIE_BOUNDS \
    --out ./k_ie
