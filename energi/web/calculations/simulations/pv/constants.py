# Standard Test Conditions (STC)
# https://sinovoltaics.com/learning-center/quality/standard-test-conditions-stc-definition-and-problems/ # noqa
STANDARD_CONDITION_TEMPERATURE = 25  # Celsius
STANDARD_CONDITION_RADIATION = 1000  # W/m2

# Some research suggests that the inverter efficiency is around 93-98%.
# Some resources:
# https://www.researchgate.net/figure/Efficiency-curve-of-various-solar-inverters_fig8_258220930
# https://www.e-education.psu.edu/eme812/node/738
STANDARD_INVERTER_EFFICIENCY_FACTOR = 0.95

# Temperature coefficient of maximum power output of solar panels
# The general consensus is that the temperature coefficient is around 0.3-0.5%/C
# Some resources:
# https://aurorasolar.com/blog/understanding-pv-system-losses-part-4-tilt-orientation-incident-angle-modifier-environmental-conditions-and-inverter-losses-clipping/#temperature-coefficients # noqa
# https://blog.ecoflow.com/us/effects-of-temperature-on-solar-panel-efficiency/
# https://www.sciencedirect.com/science/article/pii/S1876610213000829
STANDARD_MODULE_TEMPERATURE_COEFFICIENT = 0.004

# Thermal parameters for the cell temperature formula
# in the Sandia Array Performance Model (SAPM). Typical
# cell material is open rack glass/glass
# https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.temperature.sapm_cell.html
STANDARD_THERMAL_MODEL_A = -3.47
STANDARD_THERMAL_MODEL_B = -0.0594
STANDARD_THERMAL_MODEL_DELTA_T = 3

# The recommended tilt for panels in the northern hemisphere is 30-45 degrees
# We assume installations are installed at an optimal angle.
# Some resources:
# https://www.vivaenergi.dk/placering-solcelleanlaeg 37 degrees
# https://kommuneplan2021.holbaek.dk/media/18979/miljoerapport.pdf 35 degrees
ASSUMED_PANEL_TILT_DEGREES = 37

# The recommended azimuth for panels in the northern hemisphere is 180 degrees
# Meaning that the panels are facing south.
# We assume installations are installed at an optimal angle.
# Some resources:
# https://www.vivaenergi.dk/placering-solcelleanlaeg
ASSUMED_PANEL_AZIMUTH = 180  # degrees from north

# "Oversizing" occurs when the inverter is dimensioned
# smaller than the modules. It is hard to find out
# what a typical oversizing factor is, but one source
# says around 30%. Others says 10% (which gives the
# best results)
# Resources:
# https://watts.zendesk.com/hc/da/articles/8329350661404-Hvorfor-overdimensionere-solcellepanelernes-i-forhold-til-inverterens-effekt
ASSUMED_OVERSIZING_FACTOR = 1.2

# Radiation at the top of the atmosphere in W/m2
ATMOSPHERIC_RADIATION = 1368
