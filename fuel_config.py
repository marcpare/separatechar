# are there going to be that many different fuel types? nah

# For coffee husks:

# Number of pixels counted: 26868
# Area of pixel: 0.015366 cm^2
# Area of unburned pellets: 412.844779 cm^2
# Known mass: 84.0 g
coffee_husk_area_to_mass = 84.0 / 412.844779 # g / cm^2

fuels = {
"coffee husk": {
    "PELLET_UPPER" : 50,
    "PELLET_LOWER" : 25,
    "LOW_SAT" : 15,
    "HIGH_SAT": 100,
    "area_to_mass" : coffee_husk_area_to_mass
}
}