"""
Module output_variables_for_choice
Translated using PySD version 3.14.3
"""

@component.add(
    name="Annual Caloric Demand inc Waste per Capita per Day",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_inc_waste": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def annual_caloric_demand_inc_waste_per_capita_per_day():
    return (
        annual_caloric_demand_inc_waste()
        / population()
        / days_in_year()
        / kcal_to_mkcal()
    )


@component.add(
    name="Average Freshwater Withdrawal per Ton of Food Product",
    units="Cubic Meter/Ton",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_freshwater_withdrawal_per_ton_of_food_product():
    return xr.DataArray(
        [956.45, 694.69, 765.05, 556.0, 362.641, 812.958, 88.5694, 421.643],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name='"Average Stress-weighted Water Use per Ton of Food Product"',
    units="Cubic Meter/Ton",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_stressweighted_water_use_per_ton_of_food_product():
    return xr.DataArray(
        [38519.3, 19342.0, 25863.7, 17315.0, 19434.0, 25071.5, 3956.05, 15950.0],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Billion", units="1/Billion", comp_type="Constant", comp_subtype="Normal"
)
def billion():
    return 1000000000.0


@component.add(
    name="Calibration factor of Freshwater",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def calibration_factor_of_freshwater():
    return 0.635


@component.add(
    name="CH4 AFOLU in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_from_burning_biomass_in_co2eq": 1,
        "ch4_from_livestocks_and_manure_in_co2eq": 1,
        "ch4_from_rice_cultivation_in_co2eq": 1,
    },
)
def ch4_afolu_in_co2eq():
    return (
        ch4_from_burning_biomass_in_co2eq()
        + ch4_from_livestocks_and_manure_in_co2eq()
        + ch4_from_rice_cultivation_in_co2eq()
    )


@component.add(
    name="CO2 AFOLU in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_from_burning_biomass": 1,
        "co2_from_drained_organic_soils": 1,
        "co2_from_net_forest_land_emissions_and_removals": 1,
    },
)
def co2_afolu_in_co2eq():
    return (
        co2_from_burning_biomass()
        + co2_from_drained_organic_soils()
        + co2_from_net_forest_land_emissions_and_removals()
    )


@component.add(
    name="Daily Caloric Demand from Alternative Proteins",
    units="kcal/(Person*Day)",
    subscripts=["AltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_from_alternative_proteins": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def daily_caloric_demand_from_alternative_proteins():
    return (
        annual_caloric_demand_from_alternative_proteins()
        / population()
        / days_in_year()
        / kcal_to_mkcal()
    )


@component.add(
    name="Daily Caloric Demand from Conventional Food",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_from_conventional_food": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def daily_caloric_demand_from_conventional_food():
    return (
        annual_caloric_demand_from_conventional_food()
        / population()
        / days_in_year()
        / kcal_to_mkcal()
    )


@component.add(
    name="Freshwater Withdrawal for Food",
    units="Cubic Kilometer/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "production_rate_of_animal_food": 4,
        "average_freshwater_withdrawal_per_ton_of_food_product": 8,
        "m3_to_km3": 8,
        "calibration_factor_of_freshwater": 8,
        "production_rate_of_crops": 4,
    },
)
def freshwater_withdrawal_for_food():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[["PasMeat"]] = (
        float(production_rate_of_animal_food().loc["PasMeat"])
        * float(average_freshwater_withdrawal_per_ton_of_food_product().loc["PasMeat"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["CropMeat"]] = (
        float(production_rate_of_animal_food().loc["CropMeat"])
        * float(average_freshwater_withdrawal_per_ton_of_food_product().loc["CropMeat"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Dairy"]] = (
        float(production_rate_of_animal_food().loc["Dairy"])
        * float(average_freshwater_withdrawal_per_ton_of_food_product().loc["Dairy"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Eggs"]] = (
        float(production_rate_of_animal_food().loc["Eggs"])
        * float(average_freshwater_withdrawal_per_ton_of_food_product().loc["Eggs"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Pulses"]] = (
        float(production_rate_of_crops().loc["Pulses"])
        * float(average_freshwater_withdrawal_per_ton_of_food_product().loc["Pulses"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Grains"]] = (
        float(production_rate_of_crops().loc["Grains"])
        * float(average_freshwater_withdrawal_per_ton_of_food_product().loc["Grains"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["VegFruits"]] = (
        float(production_rate_of_crops().loc["VegFruits"])
        * float(
            average_freshwater_withdrawal_per_ton_of_food_product().loc["VegFruits"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["OtherCrops"]] = (
        float(production_rate_of_crops().loc["OtherCrops"])
        * float(
            average_freshwater_withdrawal_per_ton_of_food_product().loc["OtherCrops"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    return value


@component.add(
    name="Freshwater Withdrawal per Protein",
    units="Litres/(g*hundred)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_freshwater_withdrawal_for_food": 1,
        "m3_to_km3": 1,
        "total_nutrient_availability": 1,
        "hundred": 1,
        "m3_to_litres": 1,
    },
)
def freshwater_withdrawal_per_protein():
    return (
        total_freshwater_withdrawal_for_food()
        / m3_to_km3()
        / float(total_nutrient_availability().loc["Protein"])
        * hundred()
        * m3_to_litres()
    )


@component.add(
    name="hundred", units="1/hundred", comp_type="Constant", comp_subtype="Normal"
)
def hundred():
    return 100


@component.add(
    name="Irrigated Agricuture Water Demand Per Billion Cubic Metres",
    units="Meter*Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_agricultural_water_use_per_m2_irrigated": 1,
        "irrigated_agriculture_land": 1,
        "sqr_m_to_ha": 1,
        "billion": 1,
    },
)
def irrigated_agricuture_water_demand_per_billion_cubic_metres():
    return (
        average_agricultural_water_use_per_m2_irrigated()
        * irrigated_agriculture_land()
        / sqr_m_to_ha()
        / billion()
    )


@component.add(
    name="m3 to km3",
    units="Cubic Kilometer/Cubic Meter",
    comp_type="Constant",
    comp_subtype="Normal",
)
def m3_to_km3():
    return 1 / 1000000000.0


@component.add(
    name="m3 to litres",
    units="Litres/Cubic Meter",
    comp_type="Constant",
    comp_subtype="Normal",
)
def m3_to_litres():
    return 1000


@component.add(
    name="Mkcal to pcal",
    units="Pcal/Mkcal",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mkcal_to_pcal():
    return 1 / 1000000000.0


@component.add(
    name="N2O AFOLU in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2o_from_agriculture_soils_in_co2eq": 1,
        "n2o_from_burning_biomass_in_co2eq": 1,
        "n2o_from_livestocks_and_manure_in_co2eq": 1,
    },
)
def n2o_afolu_in_co2eq():
    return (
        n2o_from_agriculture_soils_in_co2eq()
        + n2o_from_burning_biomass_in_co2eq()
        + n2o_from_livestocks_and_manure_in_co2eq()
    )


@component.add(
    name="Negative Denitrification Rate",
    units="kg/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"denitrification_rate": 1},
)
def negative_denitrification_rate():
    return -denitrification_rate()


@component.add(
    name="Negative Nitrogen Leaching and Runoff Rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nitrogen_leaching_and_runoff_rate": 1},
)
def negative_nitrogen_leaching_and_runoff_rate():
    return -nitrogen_leaching_and_runoff_rate()


@component.add(
    name="Negative Phosphorus erosion leaching and runoff rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"phosphorus_erosion_leaching_and_runoff_rate": 1},
)
def negative_phosphorus_erosion_leaching_and_runoff_rate():
    return -phosphorus_erosion_leaching_and_runoff_rate()


@component.add(
    name="Negative Species Extinction Rate",
    units="Dmnl/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"species_extinction_rate": 1},
)
def negative_species_extinction_rate():
    return -species_extinction_rate()


@component.add(
    name="Negative Total N uptake rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_n_uptake_rate": 1},
)
def negative_total_n_uptake_rate():
    return -total_n_uptake_rate()


@component.add(
    name="Negative Total P uptake rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_p_uptake_rate": 1},
)
def negative_total_p_uptake_rate():
    return -total_p_uptake_rate()


@component.add(
    name="Percentage of Agriculture Land",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land": 1, "total_land": 1, "nvs_100_percent": 1},
)
def percentage_of_agriculture_land():
    return agricultural_land() / total_land() * nvs_100_percent()


@component.add(
    name="Percentage of Forest Land",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_land": 1, "total_land": 1, "nvs_100_percent": 1},
)
def percentage_of_forest_land():
    return forest_land() / total_land() * nvs_100_percent()


@component.add(
    name="Percentage of Other Land",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_land": 1, "total_land": 1, "nvs_100_percent": 1},
)
def percentage_of_other_land():
    return other_land() / total_land() * nvs_100_percent()


@component.add(
    name="Percentage of Urban and Industrial Land",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_and_industrial_land": 1, "total_land": 1, "nvs_100_percent": 1},
)
def percentage_of_urban_and_industrial_land():
    return urban_and_industrial_land() / total_land() * nvs_100_percent()


@component.add(
    name="Rainfed Agriculture Water Demand Per Billion Cubic Metres",
    units="Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_agricultural_water_use_per_m2_rainfed": 1,
        "rainfed_agriculture_land": 1,
        "sqr_m_to_ha": 1,
        "billion": 1,
    },
)
def rainfed_agriculture_water_demand_per_billion_cubic_metres():
    return (
        average_agricultural_water_use_per_m2_rainfed()
        * rainfed_agriculture_land()
        / sqr_m_to_ha()
        / billion()
    )


@component.add(
    name='"Stress-weighted Water Use for Food"',
    units="Cubic Kilometer/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "production_rate_of_animal_food": 4,
        "average_stressweighted_water_use_per_ton_of_food_product": 8,
        "m3_to_km3": 8,
        "calibration_factor_of_freshwater": 8,
        "production_rate_of_crops": 4,
    },
)
def stressweighted_water_use_for_food():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[["PasMeat"]] = (
        float(production_rate_of_animal_food().loc["PasMeat"])
        * float(
            average_stressweighted_water_use_per_ton_of_food_product().loc["PasMeat"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["CropMeat"]] = (
        float(production_rate_of_animal_food().loc["CropMeat"])
        * float(
            average_stressweighted_water_use_per_ton_of_food_product().loc["CropMeat"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Dairy"]] = (
        float(production_rate_of_animal_food().loc["Dairy"])
        * float(average_stressweighted_water_use_per_ton_of_food_product().loc["Dairy"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Eggs"]] = (
        float(production_rate_of_animal_food().loc["Eggs"])
        * float(average_stressweighted_water_use_per_ton_of_food_product().loc["Eggs"])
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Pulses"]] = (
        float(production_rate_of_crops().loc["Pulses"])
        * float(
            average_stressweighted_water_use_per_ton_of_food_product().loc["Pulses"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["Grains"]] = (
        float(production_rate_of_crops().loc["Grains"])
        * float(
            average_stressweighted_water_use_per_ton_of_food_product().loc["Grains"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["VegFruits"]] = (
        float(production_rate_of_crops().loc["VegFruits"])
        * float(
            average_stressweighted_water_use_per_ton_of_food_product().loc["VegFruits"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    value.loc[["OtherCrops"]] = (
        float(production_rate_of_crops().loc["OtherCrops"])
        * float(
            average_stressweighted_water_use_per_ton_of_food_product().loc["OtherCrops"]
        )
        * m3_to_km3()
        * calibration_factor_of_freshwater()
    )
    return value


@component.add(
    name='"Stress-weighted Water Use per Protein"',
    units="Litres/(g*hundred)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_stressweighted_water_use_for_food": 1,
        "m3_to_km3": 1,
        "total_nutrient_availability": 1,
        "hundred": 1,
        "m3_to_litres": 1,
    },
)
def stressweighted_water_use_per_protein():
    return (
        total_stressweighted_water_use_for_food()
        / m3_to_km3()
        / float(total_nutrient_availability().loc["Protein"])
        * hundred()
        * m3_to_litres()
    )


@component.add(
    name="Total Freshwater Withdrawal for Food",
    units="Cubic Kilometer/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"freshwater_withdrawal_for_food": 1},
)
def total_freshwater_withdrawal_for_food():
    return sum(
        freshwater_withdrawal_for_food().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name='"Total Stress-weighted Water Use for Food"',
    units="Cubic Kilometer/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"stressweighted_water_use_for_food": 1},
)
def total_stressweighted_water_use_for_food():
    return sum(
        stressweighted_water_use_for_food().rename(
            {"FoodCategories": "FoodCategories!"}
        ),
        dim=["FoodCategories!"],
    )


@component.add(name="zero", units="1", comp_type="Constant", comp_subtype="Normal")
def zero():
    return 0
