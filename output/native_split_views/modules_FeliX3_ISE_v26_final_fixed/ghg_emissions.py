"""
Module ghg_emissions
Translated using PySD version 3.14.3
"""

@component.add(
    name="Agricultural Land Change",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land": 1, "init_agricultural_land": 1},
)
def agricultural_land_change():
    """
    Ratio of agricultural land area change compared to its initial area in year 1900.
    """
    return agricultural_land() / init_agricultural_land()


@component.add(
    name="Agricultural Land Increases",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land_development_rate": 1,
        "deforestation_to_agricultural_land": 1,
    },
)
def agricultural_land_increases():
    return float(
        np.maximum(
            agricultural_land_development_rate() + deforestation_to_agricultural_land(),
            0,
        )
    )


@component.add(
    name="Burned Area",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land_change": 1, "burnt_factor": 1},
)
def burned_area():
    return agricultural_land_change() * burnt_factor()


@component.add(
    name="Burning Crop Residues",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"crop_residues": 1, "fraction_burned": 1},
)
def burning_crop_residues():
    return sum(
        crop_residues().rename({"PlantFood": "PlantFood!"})
        * fraction_burned().rename({"PlantFood": "PlantFood!"}),
        dim=["PlantFood!"],
    )


@component.add(
    name="Burnt Factor", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def burnt_factor():
    """
    Calibrated
    """
    return 25000000.0


@component.add(
    name="C Emission from Biomass Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production": 1,
        "c_intensity_of_emission_from_biomass_energy": 1,
    },
)
def c_emission_from_biomass_energy():
    """
    Total carbon emission from biomass energy production and it use.
    """
    return biomass_energy_production() * c_intensity_of_emission_from_biomass_energy()


@component.add(
    name="C Emission from Coal Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_production": 1, "c_intensity_of_emission_from_coal": 1},
)
def c_emission_from_coal_energy():
    """
    Total carbon emission from coal energy production and it use.
    """
    return coal_production() * c_intensity_of_emission_from_coal()


@component.add(
    name="C Emission from Gas Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_production": 1, "c_intensity_of_emission_from_gas": 1},
)
def c_emission_from_gas_energy():
    """
    Total carbon emission from gas energy production and it use.
    """
    return gas_production() * c_intensity_of_emission_from_gas()


@component.add(
    name="C Emission from Land Use",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_intensity_of_emissions_from_agricultural_land_use": 1,
        "agricultural_land_change": 1,
        "c_intensity_of_emissions_from_forest_land_use": 1,
        "forest_land_change": 1,
    },
)
def c_emission_from_land_use():
    """
    Total carbon emission from forest and agricultural land use change. Source of Historical Data: Houghton, R.A. 2008. Carbon Flux to the Atmosphere from Land-Use Changes: 1850-2005. In TRENDS: A Compendium of Data on Global Change. Carbon Dioxide Information Analysis Center, Oak Ridge National Laboratory, U.S. Department of Energy, Oak Ridge, Tenn., U.S.A.
    """
    return (
        c_intensity_of_emissions_from_agricultural_land_use()
        * agricultural_land_change()
        + (2 - forest_land_change()) * c_intensity_of_emissions_from_forest_land_use()
    )


@component.add(
    name="C Emission from Oil Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_production": 1, "c_intensity_of_emission_from_oil": 1},
)
def c_emission_from_oil_energy():
    """
    Total carbon emission from oil production and it use.
    """
    return oil_production() * c_intensity_of_emission_from_oil()


@component.add(
    name="C Emission from Solar Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_energy_production": 1,
        "c_intensity_of_emission_from_solar_energy": 1,
    },
)
def c_emission_from_solar_energy():
    """
    Total carbon emission from solar energy production and it use.
    """
    return solar_energy_production() * c_intensity_of_emission_from_solar_energy()


@component.add(
    name="C Emission from Wind Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_energy_production": 1,
        "c_intensity_of_emission_from_wind_energy": 1,
    },
)
def c_emission_from_wind_energy():
    """
    Total carbon emission from wind energy production and it use.
    """
    return wind_energy_production() * c_intensity_of_emission_from_wind_energy()


@component.add(
    name="C Intensity of Emission from Biomass Energy",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_factor": 1},
)
def c_intensity_of_emission_from_biomass_energy():
    """
    Carbon intensity from biomass energy production and it use. Felix1: 1.278e+006 IPCC: med: 2.6749e+006 min:1511900
    """
    return 1511900.0 * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Coal",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_coal": 1,
        "ccs_improvement_factor": 1,
    },
)
def c_intensity_of_emission_from_coal():
    """
    Carbon intensity from coal energy production and it use.
    """
    return normal_c_intensity_of_emission_from_coal() * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Gas",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_gas": 1,
        "ccs_improvement_factor": 1,
    },
)
def c_intensity_of_emission_from_gas():
    """
    Carbon intensity from gas energy production and it use.
    """
    return normal_c_intensity_of_emission_from_gas() * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Oil",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_oil": 1,
        "ccs_improvement_factor": 1,
    },
)
def c_intensity_of_emission_from_oil():
    """
    Carbon intensity from oil energy production and it use.
    """
    return normal_c_intensity_of_emission_from_oil() * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Solar Energy",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def c_intensity_of_emission_from_solar_energy():
    """
    Carbon intensity from solar energy production and it use. fELIX1: 43200 IPCC: med: 476830 min:302380
    """
    return 43200


@component.add(
    name="C Intensity of Emission from Wind Energy",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def c_intensity_of_emission_from_wind_energy():
    """
    Carbon intensity from wind energy production and it use. Felix1: 27000 IPCC: med: 139560 min: 93040
    """
    return 27000


@component.add(
    name="C Intensity of Emissions from Agricultural Land Use",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def c_intensity_of_emissions_from_agricultural_land_use():
    return 650000000.0


@component.add(
    name="C Intensity of Emissions from Forest Land Use",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def c_intensity_of_emissions_from_forest_land_use():
    return 450000000.0


@component.add(
    name="CCS Improvement",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement": 1},
    other_deps={
        "_integ_ccs_improvement": {
            "initial": {"init_ccs_improvement": 1},
            "step": {"ccs_improvement_change": 1},
        }
    },
)
def ccs_improvement():
    """
    Accumulated improvement of carbon capture and storage technology.
    """
    return _integ_ccs_improvement()


_integ_ccs_improvement = Integ(
    lambda: ccs_improvement_change(),
    lambda: init_ccs_improvement(),
    "_integ_ccs_improvement",
)


@component.add(
    name="CCS Improvement Change",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ccsiclv3": 1},
)
def ccs_improvement_change():
    """
    Change in improvement of carbon capture and storage technology.
    """
    return outflow_ccsiclv3()


@component.add(
    name="CCS Improvement Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_ccs_improvement_factor": 2,
        "ccs_improvement": 2,
        "max_ccs_improvement_factor": 1,
    },
)
def ccs_improvement_factor():
    """
    Impact of carbon capture and storage on carbon intensity of emissions from fossil fuels. Scaled between min and max improvement factor.
    """
    return min_ccs_improvement_factor() + (
        max_ccs_improvement_factor() - min_ccs_improvement_factor()
    ) * (ccs_improvement() / (ccs_improvement() + 1))


@component.add(
    name="CCS Scenario",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_scenario_switch_variation": 1, "time": 1},
)
def ccs_scenario():
    """
    Carbon capture and storage scenario trigger
    """
    return 0 + step(__data["time"], ccs_scenario_switch_variation(), 2020)


@component.add(
    name="CCS Scenario Switch Variation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_scenario_variation": 4},
)
def ccs_scenario_switch_variation():
    """
    IF THEN ELSE(0 <= CCS Scenario Variation :AND: CCS Scenario Variation < 1, 0 , 0) + IF THEN ELSE(1 <= CCS Scenario Variation :AND: CCS Scenario Variation < 2, 1 , 0)
    """
    return if_then_else(
        np.logical_and(0 <= ccs_scenario_variation(), ccs_scenario_variation() < 1),
        lambda: 0,
        lambda: 0,
    ) + if_then_else(
        np.logical_and(1 <= ccs_scenario_variation(), ccs_scenario_variation() < 2),
        lambda: 1,
        lambda: 0,
    )


@component.add(
    name="CCS Scenario Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ccs_scenario_variation():
    return 0


@component.add(
    name="CH4 Agriculture Abatement Adoption Fraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_agriculture_abatement_maximum_fraction": 1,
        "ch4_agriculture_abatement_adoption_slope": 1,
        "time": 1,
        "ch4_agriculture_abatement_year_of_maximum": 1,
    },
)
def ch4_agriculture_abatement_adoption_fraction():
    """
    Logistic Regression formula to follow adoption timeline of N2O abatement Technologies estimated between 1980-2000
    """
    return ch4_agriculture_abatement_maximum_fraction() / (
        1
        + float(
            np.exp(
                -ch4_agriculture_abatement_adoption_slope()
                * (time() - ch4_agriculture_abatement_year_of_maximum())
            )
        )
    )


@component.add(
    name="CH4 Agriculture Abatement Adoption Slope",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ch4_agriculture_abatement_adoption_slope": 1},
    other_deps={
        "_smooth_ch4_agriculture_abatement_adoption_slope": {
            "initial": {"time": 1},
            "step": {"time": 1},
        }
    },
)
def ch4_agriculture_abatement_adoption_slope():
    """
    0.15 - SMOOTH(RAMP(0.0025, 2010, 2040),2)
    """
    return 0.15 - _smooth_ch4_agriculture_abatement_adoption_slope()


_smooth_ch4_agriculture_abatement_adoption_slope = Smooth(
    lambda: ramp(__data["time"], 0.0025, 2010, 2040),
    lambda: 2,
    lambda: ramp(__data["time"], 0.0025, 2010, 2040),
    lambda: 1,
    "_smooth_ch4_agriculture_abatement_adoption_slope",
)


@component.add(
    name="CH4 Agriculture Abatement Maximum Fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_agriculture_abatement_maximum_fraction():
    """
    IPCC and IEA estimates 40-60% with current tech
    """
    return 0.45


@component.add(
    name="CH4 Agriculture Abatement Year of Maximum",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_agriculture_abatement_year_of_maximum():
    """
    Midpoint of Historical Adoption
    """
    return 2030


@component.add(
    name="CH4 Emission from Biomass Energy",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production": 1,
        "ch4_intensity_of_emission_from_biomass_energy": 1,
        "ch4_energy_abatement_adoption_fraction": 1,
    },
)
def ch4_emission_from_biomass_energy():
    """
    Total carbon emission from biomass energy production and it use.
    """
    return (
        biomass_energy_production()
        * ch4_intensity_of_emission_from_biomass_energy()
        * (1 - ch4_energy_abatement_adoption_fraction())
    )


@component.add(
    name="CH4 Emission from Coal Energy",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_production": 1,
        "ch4_intensity_of_emission_from_coal": 1,
        "ch4_energy_abatement_adoption_fraction": 1,
    },
)
def ch4_emission_from_coal_energy():
    """
    Total ch4 emission from coal energy production and it use.
    """
    return (
        coal_production()
        * ch4_intensity_of_emission_from_coal()
        * (1 - ch4_energy_abatement_adoption_fraction())
    )


@component.add(
    name="CH4 Emission from Gas Energy",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gas_production": 1,
        "ch4_intensity_of_emission_from_gas": 1,
        "ch4_energy_abatement_adoption_fraction": 1,
    },
)
def ch4_emission_from_gas_energy():
    """
    Total ch4 emission from gas energy production and it use.
    """
    return (
        gas_production()
        * ch4_intensity_of_emission_from_gas()
        * (1 - ch4_energy_abatement_adoption_fraction())
    )


@component.add(
    name="CH4 Emission from Oil Energy",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_production": 1,
        "ch4_intensity_of_emission_from_oil": 1,
        "ch4_energy_abatement_adoption_fraction": 1,
    },
)
def ch4_emission_from_oil_energy():
    """
    Total ch4 emission from oil production and it use.
    """
    return (
        oil_production()
        * ch4_intensity_of_emission_from_oil()
        * (1 - ch4_energy_abatement_adoption_fraction())
    )


@component.add(
    name="CH4 Energy Abatement Adoption Fraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_energy_abatement_maximum_fraction": 1,
        "ch4_energy_abatement_adoption_slope": 1,
        "ch4_energy_abatement_year_of_maximum": 1,
        "time": 1,
    },
)
def ch4_energy_abatement_adoption_fraction():
    """
    Logistic Regression formula to follow adoption timeline of N2O abatement Technologies estimated between 1980-2000
    """
    return ch4_energy_abatement_maximum_fraction() / (
        1
        + float(
            np.exp(
                -ch4_energy_abatement_adoption_slope()
                * (time() - ch4_energy_abatement_year_of_maximum())
            )
        )
    )


@component.add(
    name="CH4 Energy Abatement Adoption Slope",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ch4_energy_abatement_adoption_slope": 1},
    other_deps={
        "_smooth_ch4_energy_abatement_adoption_slope": {
            "initial": {"time": 1},
            "step": {"time": 1},
        }
    },
)
def ch4_energy_abatement_adoption_slope():
    """
    midpoint of rollout
    """
    return 0.15 - _smooth_ch4_energy_abatement_adoption_slope()


_smooth_ch4_energy_abatement_adoption_slope = Smooth(
    lambda: ramp(__data["time"], 0.0025, 2000, 2030),
    lambda: 2,
    lambda: ramp(__data["time"], 0.0025, 2000, 2030),
    lambda: 1,
    "_smooth_ch4_energy_abatement_adoption_slope",
)


@component.add(
    name="CH4 Energy Abatement Maximum Fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_energy_abatement_maximum_fraction():
    """
    IPCC and IEA estimates 40-60% with current tech
    """
    return 0.5


@component.add(
    name="CH4 Energy Abatement Year of Maximum",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_energy_abatement_year_of_maximum():
    """
    Midpoint of Historical Adoption
    """
    return 2030


@component.add(
    name="CH4 from Burning Biomass",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emission_factor_ch4_from_burning_biomass": 1, "burned_area": 1},
)
def ch4_from_burning_biomass():
    return emission_factor_ch4_from_burning_biomass() * burned_area()


@component.add(
    name="CH4 from Burning Biomass in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_from_burning_biomass": 1, "ch4_to_co2_nonfossil_gwp100_ar6": 1},
)
def ch4_from_burning_biomass_in_co2eq():
    return ch4_from_burning_biomass() * ch4_to_co2_nonfossil_gwp100_ar6()


@component.add(
    name="CH4 from Crop Burning",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"burning_crop_residues": 1, "emission_factor_ch4_from_crop_burning": 1},
)
def ch4_from_crop_burning():
    return burning_crop_residues() * emission_factor_ch4_from_crop_burning()


@component.add(
    name="CH4 from Crop Burning in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_from_crop_burning": 1, "ch4_to_co2_nonfossil_gwp100_ar6": 1},
)
def ch4_from_crop_burning_in_co2eq():
    return ch4_from_crop_burning() * ch4_to_co2_nonfossil_gwp100_ar6()


@component.add(
    name="CH4 from Livestocks and Manure",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emission_factor_ch4_from_animal_products": 1,
        "effect_of_yield_on_ef": 1,
        "food_production_rate": 1,
        "ch4_agriculture_abatement_adoption_fraction": 1,
    },
)
def ch4_from_livestocks_and_manure():
    return sum(
        emission_factor_ch4_from_animal_products().rename({"AnimalFood": "AnimalFood!"})
        * effect_of_yield_on_ef()
        * food_production_rate()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood!"}),
        dim=["AnimalFood!"],
    ) * (1 - ch4_agriculture_abatement_adoption_fraction())


@component.add(
    name="CH4 from Livestocks and Manure in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_from_livestocks_and_manure": 1,
        "ch4_to_co2_nonfossil_gwp100_ar6": 1,
    },
)
def ch4_from_livestocks_and_manure_in_co2eq():
    return ch4_from_livestocks_and_manure() * ch4_to_co2_nonfossil_gwp100_ar6()


@component.add(
    name="CH4 from Rice Cultivation",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_rice_in_grain_production": 1,
        "food_production_rate": 1,
        "emission_factor_ch4_from_rice_cultivation": 1,
        "ch4_agriculture_abatement_adoption_fraction": 1,
    },
)
def ch4_from_rice_cultivation():
    return (
        fraction_of_rice_in_grain_production()
        * float(food_production_rate().loc["Grains"])
        * float(emission_factor_ch4_from_rice_cultivation().loc["Grains"])
        * (1 - ch4_agriculture_abatement_adoption_fraction())
    )


@component.add(
    name="CH4 from Rice Cultivation in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_from_rice_cultivation": 1, "ch4_to_co2_nonfossil_gwp100_ar6": 1},
)
def ch4_from_rice_cultivation_in_co2eq():
    return ch4_from_rice_cultivation() * ch4_to_co2_nonfossil_gwp100_ar6()


@component.add(
    name="CH4 from Savanna Fires",
    units="TonCH4/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_from_savanna_fires():
    """
    1990-2022 Average FAO
    """
    return 5047000.0


@component.add(
    name="CH4 Intensity of Emission from Biomass Energy",
    units="TonCH4/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_intensity_of_emission_from_biomass_energy():
    """
    CH4 intensity from biomass energy production and it use. 505000
    """
    return 28000


@component.add(
    name="CH4 Intensity of Emission from Coal",
    units="TonCH4/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_intensity_of_emission_from_coal():
    """
    CH4 intensity from coal energy production and it use.
    """
    return 13200


@component.add(
    name="CH4 Intensity of Emission from Gas",
    units="TonCH4/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_intensity_of_emission_from_gas():
    """
    Carbon intensity from gas energy production and it use.
    """
    return 9200


@component.add(
    name="CH4 Intensity of Emission from Oil",
    units="TonCH4/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_intensity_of_emission_from_oil():
    """
    CH4 Intensity
    """
    return 18000


@component.add(
    name="CH4 to CO2 Fossil GWP100 AR6",
    units="TonCO2/TonCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_to_co2_fossil_gwp100_ar6():
    return 29.8


@component.add(
    name='"CH4 to CO2 Non-Fossil GWP100 AR6"',
    units="TonCO2/TonCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_to_co2_nonfossil_gwp100_ar6():
    return 27


@component.add(
    name="CH4 Waste Abatement Adoption Fraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_waste_abatement_maximum_fraction": 1,
        "ch4_waste_abatement_year_of_maximum": 1,
        "ch4_waste_abatement_adoption_slope": 1,
        "time": 1,
    },
)
def ch4_waste_abatement_adoption_fraction():
    """
    Logistic Regression formula to follow adoption timeline of N2O abatement Technologies estimated between 1980-2000
    """
    return ch4_waste_abatement_maximum_fraction() / (
        1
        + float(
            np.exp(
                -ch4_waste_abatement_adoption_slope()
                * (time() - ch4_waste_abatement_year_of_maximum())
            )
        )
    )


@component.add(
    name="CH4 Waste Abatement Adoption Slope",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ch4_waste_abatement_adoption_slope": 1},
    other_deps={
        "_smooth_ch4_waste_abatement_adoption_slope": {
            "initial": {"time": 1},
            "step": {"time": 1},
        }
    },
)
def ch4_waste_abatement_adoption_slope():
    """
    midpoint of rollout
    """
    return 0.15 - _smooth_ch4_waste_abatement_adoption_slope()


_smooth_ch4_waste_abatement_adoption_slope = Smooth(
    lambda: ramp(__data["time"], 0.0025, 2010, 2040),
    lambda: 2,
    lambda: ramp(__data["time"], 0.0025, 2010, 2040),
    lambda: 1,
    "_smooth_ch4_waste_abatement_adoption_slope",
)


@component.add(
    name="CH4 Waste Abatement Maximum Fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_waste_abatement_maximum_fraction():
    """
    Major industrial sources with partial/full abatement ( 70%);
    """
    return 0.8


@component.add(
    name="CH4 Waste Abatement Year of Maximum",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_waste_abatement_year_of_maximum():
    """
    Midpoint of Historical Adoption
    """
    return 2030


@component.add(
    name="Climate Action Year",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_action_year():
    return 2020


@component.add(
    name="Climate Policy Scenario",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_policy_scenario():
    """
    0: No climate policy 1: Climate policy
    """
    return 0


@component.add(
    name="CO2 from Biomass Burning in C",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_from_burning_biomass": 1, "co2_to_c": 1},
)
def co2_from_biomass_burning_in_c():
    return co2_from_burning_biomass() / co2_to_c()


@component.add(
    name="CO2 from Burning Biomass",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emission_factor_co2_from_burning_biomass": 1, "burned_area": 1},
)
def co2_from_burning_biomass():
    return emission_factor_co2_from_burning_biomass() * burned_area()


@component.add(
    name="CO2 from Drained Organic Soils",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land_change": 1,
        "emission_factor_co2_from_drained_organic_soils": 1,
    },
)
def co2_from_drained_organic_soils():
    """
    Based on IPCC Tier 1, This is supposed to be calculated from Deforestation - however, the current landuse changes are too dynamic to predict these values, hence, it is now based on % change in forestland since 1900.
    """
    return agricultural_land_change() * emission_factor_co2_from_drained_organic_soils()


@component.add(
    name="CO2 from Drained Organic Soils in C",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_from_drained_organic_soils": 1, "co2_to_c": 1},
)
def co2_from_drained_organic_soils_in_c():
    return co2_from_drained_organic_soils() / co2_to_c()


@component.add(
    name="CO2 from Forestland",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emission_factor_co2_from_forestland": 1, "forest_land": 1},
)
def co2_from_forestland():
    return emission_factor_co2_from_forestland() * forest_land()


@component.add(
    name="CO2 from Forestland in C",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_from_forestland": 1, "co2_to_c": 1},
)
def co2_from_forestland_in_c():
    return co2_from_forestland() / co2_to_c()


@component.add(
    name="CO2 from Net Forest Conversion",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land_change": 1,
        "emission_factor_co2_from_net_forest_conversion": 1,
    },
)
def co2_from_net_forest_conversion():
    """
    Based on IPCC Tier 1, This is supposed to be calculated from Deforestation - however, the current landuse changes are too dynamic to predict these values, hence, it is now based on % change in forestland since 1900.
    """
    return (2 - forest_land_change()) * emission_factor_co2_from_net_forest_conversion()


@component.add(
    name="CO2 from Net Forest Conversion in C",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_from_net_forest_conversion": 1, "co2_to_c": 1},
)
def co2_from_net_forest_conversion_in_c():
    return co2_from_net_forest_conversion() / co2_to_c()


@component.add(
    name="CO2 from Net Forest Land Emissions and Removals",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_from_forestland": 1, "co2_from_net_forest_conversion": 1},
)
def co2_from_net_forest_land_emissions_and_removals():
    return co2_from_forestland() + co2_from_net_forest_conversion()


@component.add(
    name="Crop Residues",
    units="Ton/Year",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_production_rate": 1, "residuetoproduct_ratio_rpr": 1},
)
def crop_residues():
    return (
        food_production_rate()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * residuetoproduct_ratio_rpr()
    )


@component.add(
    name="DE S", units="TonC/Year", comp_type="Constant", comp_subtype="Normal"
)
def de_s():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return 7500000000.0


@component.add(
    name="DE Var S",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_de_var_s": 1},
    other_deps={
        "_smooth_de_var_s": {
            "initial": {"de_s": 1, "time": 1},
            "step": {"de_s": 1, "time": 1},
        }
    },
)
def de_var_s():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return 7500000000.0 + _smooth_de_var_s()


_smooth_de_var_s = Smooth(
    lambda: step(__data["time"], de_s() - 7500000000.0, 2020),
    lambda: 1,
    lambda: step(__data["time"], de_s() - 7500000000.0, 2020),
    lambda: 1,
    "_smooth_de_var_s",
)


@component.add(
    name="Default C Intensity of Emission from Biomass",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_intensity_of_emission_from_biomass_energy": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_biomass():
    """
    Carbon intensity from biomass energy production and it use.
    """
    return (
        c_intensity_of_emission_from_biomass_energy() * ton_c_to_kg_co2() / mtoe_to_gj()
    )


@component.add(
    name="Default C Intensity of Emission from Coal",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_coal": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_coal():
    """
    Initial carbon intensity of production from coal technologies.
    """
    return normal_c_intensity_of_emission_from_coal() * ton_c_to_kg_co2() / mtoe_to_gj()


@component.add(
    name="Default C Intensity of Emission from Gas",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_gas": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_gas():
    """
    Initial carbon intensity of production from gas technologies.
    """
    return normal_c_intensity_of_emission_from_gas() * ton_c_to_kg_co2() / mtoe_to_gj()


@component.add(
    name="Default C Intensity of Emission from Oil",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_oil": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_oil():
    """
    Initial carbon intensity of production from oil technologies.
    """
    return normal_c_intensity_of_emission_from_oil() * ton_c_to_kg_co2() / mtoe_to_gj()


@component.add(
    name="Desired Total C Emission from Fossil Fuels",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"de_var_s": 1, "_smooth_desired_total_c_emission_from_fossil_fuels": 1},
    other_deps={
        "_smooth_desired_total_c_emission_from_fossil_fuels": {
            "initial": {
                "desired_total_c_emission_from_fossil_fuels_variation": 1,
                "de_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "desired_total_c_emission_from_fossil_fuels_variation": 1,
                "de_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_production_variation_time": 1,
            },
        }
    },
)
def desired_total_c_emission_from_fossil_fuels():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return de_var_s() + _smooth_desired_total_c_emission_from_fossil_fuels()


_smooth_desired_total_c_emission_from_fossil_fuels = Smooth(
    lambda: step(
        __data["time"],
        desired_total_c_emission_from_fossil_fuels_variation() - de_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_production_variation_time(),
    lambda: step(
        __data["time"],
        desired_total_c_emission_from_fossil_fuels_variation() - de_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_desired_total_c_emission_from_fossil_fuels",
)


@component.add(
    name="Desired Total C Emission from Fossil Fuels Variation",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_total_c_emission_from_fossil_fuels_variation():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return 7500000000.0


@component.add(
    name="Effect of Yield on EF",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reference_meat_yield": 1, "grassland_meat_yield": 1},
)
def effect_of_yield_on_ef():
    """
    Yield and EF has a inverse relationship IPCC Tier 1 uses a EF_product = EF_head/Yield per Head. We adopted this formula as an approximate since we do not count animals but only final products
    """
    return reference_meat_yield() / grassland_meat_yield()


@component.add(
    name="Effectiveness of Pressure to Adjust C Emission",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_pressure_to_adjust_c_emission_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_pressure_to_adjust_c_emission():
    """
    Rate at which the gap between acceptable and current carbon emission from fossil fuels level is addressed.
    """
    return 0.07 + step(
        __data["time"],
        effectiveness_of_pressure_to_adjust_c_emission_variation() - 0.07,
        2020,
    )


@component.add(
    name="Effectiveness of Pressure to Adjust C Emission Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_pressure_to_adjust_c_emission_variation():
    """
    Rate at which the gap between acceptable and current carbon emission from fossil fuels level is addressed.
    """
    return 0.07


@component.add(
    name="Emission Factor CH4 from Animal Products",
    units="TonCH4/Ton",
    subscripts=["AnimalFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_ch4_from_animal_products():
    """
    Greenhouse gas emission from ruminant supply chain: a global life cycle assessment https://www.fao.org/4/i3461e/i3461e.pdf e.g. Beefherd is 67.8kgCO2/kg = 2.42tonCH4/ton; Dairyherd is 0.657tonCH4/ton; estimated 0.8 - 1.3 for pasmeat based on weighted averaging Relative EF estimated here, but calibrated to fit historical data
    """
    return xr.DataArray(
        [0.95, 0.06, 0.03, 0.003],
        {"AnimalFood": _subscript_dict["AnimalFood"]},
        ["AnimalFood"],
    )


@component.add(
    name="Emission factor CH4 from burning biomass",
    units="TonCH4/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_ch4_from_burning_biomass():
    """
    Calibrated
    """
    return 0.32


@component.add(
    name="Emission factor CH4 from crop burning",
    units="TonCH4/Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_ch4_from_crop_burning():
    """
    Calibrated
    """
    return 0.0025


@component.add(
    name="Emission Factor CH4 from rice cultivation",
    units="TonCH4/Ton",
    subscripts=["AllPlantButOther"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_ch4_from_rice_cultivation():
    """
    This variable includes both emission factor of rice and % of grains that are rice. Assumes that EF of rice is linear but it does also depend on the technology used. Calibrated
    """
    return xr.DataArray(
        0.047,
        {"AllPlantButOther": _subscript_dict["AllPlantButOther"]},
        ["AllPlantButOther"],
    )


@component.add(
    name="Emission factor CO2 from burning biomass",
    units="TonCO2/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_co2_from_burning_biomass():
    """
    Calibrated
    """
    return 9


@component.add(
    name="Emission factor CO2 from drained organic soils",
    units="TonCO2/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_co2_from_drained_organic_soils():
    return 740000000.0


@component.add(
    name="Emission factor CO2 from forestland",
    units="TonCO2/Year/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_co2_from_forestland():
    return -0.85


@component.add(
    name="Emission Factor CO2 from net forest conversion",
    units="TonCO2/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_co2_from_net_forest_conversion():
    """
    Calibrated
    """
    return 3700000000.0


@component.add(
    name="Emission factor N2O Direct EF1",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_n2o_direct_ef1():
    """
    IPCC: 0.01, 0.002-0.018 uncertainty
    """
    return 0.01


@component.add(
    name="Emission factor N2O from burning biomass",
    units="TonN2O/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_n2o_from_burning_biomass():
    """
    Calibrated
    """
    return 0.017


@component.add(
    name="Emission factor N2O from crop burning",
    units="TonN2O/Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_n2o_from_crop_burning():
    """
    Calibrated
    """
    return 7e-05


@component.add(
    name="Emission factor N2O leaching runoff EF5",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_n2o_leaching_runoff_ef5():
    return 0.0075


@component.add(
    name="Emission factor N2O volatilisation EF4",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_n2o_volatilisation_ef4():
    return 0.01


@component.add(
    name='"Emission factor N2O-N for manure"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factor_n2on_for_manure():
    """
    A highly aggregated EF is derived here through calibration. IPCC Reports calculate Livestock and Manure through spliting Manure into various pathways: storage, pasture and applied. And then use different EFs on each source. While it's possible to disaggregate it, it doesn't seem meaningful since there's not enough data to calibrate them manually.
    """
    return 0.06


@component.add(
    name="Emission factors CH4 from Waste",
    units="TonCH4/Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factors_ch4_from_waste():
    """
    Mixed global average (weighted by fraction of waste to anaerobic managed sites) 0.02-0.05 (0.038) IPCC (2000) 'Good Practice Guidance and Uncertainty Management in National Greenhouse Gas Inventories: CH4 Emissions from Solid Waste Disposal', *Background Papers*. Available at: https://www.ipcc-nggip.iges.or.jp/public/gp/bgp/5_1_CH4_Solid_Waste.pdf.
    """
    return 0.038


@component.add(
    name="Emission factors N2O from Industrial Activity",
    units="TonN2O/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_factors_n2o_from_industrial_activity():
    """
    Assumes that GWP is a strong approximate for Industrial Activity Calibrated
    """
    return 1e-07


@component.add(
    name="Emission from Fossil Fuels per Capita",
    units="TonC/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_fossil_fuels": 1, "population": 1},
)
def emission_from_fossil_fuels_per_capita():
    """
    Carbon emission from energy production and it use per capita.
    """
    return total_c_emission_from_fossil_fuels() / population()


@component.add(
    name="Emission per Capita",
    units="TonC/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emissions": 1, "population": 1},
)
def emission_per_capita():
    """
    Emissions of carbon from energy use and other sources per capita.
    """
    return total_c_emissions() / population()


@component.add(
    name="Emission shock year",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_shock_year():
    return 2020


@component.add(
    name="Forest Land Change",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_land": 1, "init_forest_land": 1},
)
def forest_land_change():
    """
    Ratio of forest land area change compared to its initial area in year 1900.
    """
    return forest_land() / init_forest_land()


@component.add(
    name="Fraction burned",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_burned():
    """
    Calibrated but relative values are retained; Data hard to find and crop burning is quite a small fraction
    """
    return xr.DataArray(
        [0.3, 0.1, 0.05, 0.15],
        {"PlantFood": _subscript_dict["PlantFood"]},
        ["PlantFood"],
    )


@component.add(
    name="fraction of manure volatilisation",
    units="Dnml",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_manure_volatilisation():
    return 0.2


@component.add(
    name="Fraction of Rice in Grain Production",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_rice_in_grain_production():
    return 0.3


@component.add(
    name="fraction of synthetic fertilizer volatilisation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_synthetic_fertilizer_volatilisation():
    return 0.1


@component.add(name="INIT CCS Improvement", comp_type="Constant", comp_subtype="Normal")
def init_ccs_improvement():
    return 0


@component.add(
    name="Land Mitigation Policy Multiplier",
    units="1",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_mitigation_policy_multiplier():
    return 0.5


@component.add(
    name="Land Mitigation Policy Transition Period",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_mitigation_policy_transition_period():
    return 20


@component.add(
    name="Marginal emission",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emission_shock_year": 1, "year_period": 1, "time": 1},
)
def marginal_emission():
    return 1000000000.0 * pulse(
        __data["time"], emission_shock_year(), width=year_period()
    )


@component.add(
    name="MAX CCS Improvement Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_ccs_improvement_factor():
    """
    Max impact of carbon capture and storage on carbon intensity of emissions from fossil fuels.
    """
    return 1


@component.add(
    name="MIN CCS Improvement Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_ccs_improvement_factor():
    """
    Min impact of carbon capture and storage on carbon intensity of emissions from fossil fuels.
    """
    return 0


@component.add(
    name="MSW constant", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def msw_constant():
    return 0.5695


@component.add(
    name="MSW gradient", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def msw_gradient():
    return 0.027


@component.add(
    name="Mtoe to GJ", units="GJ/Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def mtoe_to_gj():
    """
    Conversion from Mtoe to GJ.
    """
    return 41868000.0


@component.add(
    name="N2O Agriculture Abatement Adoption Fraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2o_agriculture_abatement_maximum_fraction": 1,
        "n2o_agriculture_abatement_year_of_maximum": 1,
        "n2o_agriculture_abatement_adoption_slope": 1,
        "time": 1,
    },
)
def n2o_agriculture_abatement_adoption_fraction():
    """
    Logistic Regression formula to follow adoption timeline of N2O abatement Technologies estimated between 1980-2000
    """
    return n2o_agriculture_abatement_maximum_fraction() / (
        1
        + float(
            np.exp(
                -n2o_agriculture_abatement_adoption_slope()
                * (time() - n2o_agriculture_abatement_year_of_maximum())
            )
        )
    )


@component.add(
    name="N2O Agriculture Abatement Adoption Slope",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_n2o_agriculture_abatement_adoption_slope": 1},
    other_deps={
        "_smooth_n2o_agriculture_abatement_adoption_slope": {
            "initial": {"time": 1},
            "step": {"time": 1},
        }
    },
)
def n2o_agriculture_abatement_adoption_slope():
    """
    0.1 - SMOOTH(RAMP(0.0015, 2020, 2060),2) N2O Agriculture Base Slope - SMOOTH(RAMP(N2O Agriculture Slope Change, N2O Agriculture Slope Change Start, N2O Agriculture Slope Change End),2)
    """
    return 0.1 - _smooth_n2o_agriculture_abatement_adoption_slope()


_smooth_n2o_agriculture_abatement_adoption_slope = Smooth(
    lambda: ramp(__data["time"], 0.0015, 2020, 2060),
    lambda: 2,
    lambda: ramp(__data["time"], 0.0015, 2020, 2060),
    lambda: 1,
    "_smooth_n2o_agriculture_abatement_adoption_slope",
)


@component.add(
    name="N2O Agriculture Abatement Maximum Fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_agriculture_abatement_maximum_fraction():
    """
    IPCC and IEA estimates 40-60% with current tech
    """
    return 0.45


@component.add(
    name="N2O Agriculture Abatement Year of Maximum",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_agriculture_abatement_year_of_maximum():
    """
    Midpoint of Historical Adoption
    """
    return 2055


@component.add(
    name="N2O Emission from Coal Energy",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_production": 1, "n2o_intensity_of_emission_from_coal": 1},
)
def n2o_emission_from_coal_energy():
    """
    Total ch4 emission from coal energy production and it use.
    """
    return coal_production() * n2o_intensity_of_emission_from_coal()


@component.add(
    name="N2O Emission from Gas Energy",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_production": 1, "n2o_intensity_of_emission_from_gas": 1},
)
def n2o_emission_from_gas_energy():
    """
    Total ch4 emission from gas energy production and it use.
    """
    return gas_production() * n2o_intensity_of_emission_from_gas()


@component.add(
    name="N2O Emission from Oil Energy",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_production": 1, "n2o_intensity_of_emission_from_oil": 1},
)
def n2o_emission_from_oil_energy():
    """
    Total ch4 emission from oil production and it use.
    """
    return oil_production() * n2o_intensity_of_emission_from_oil()


@component.add(
    name="N2O from Agriculture Soils",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2on_direct_soil": 1,
        "n2on_indirect_via_leaching_and_runoff": 1,
        "n2on_indirect_via_volatilisation": 1,
        "n2on_ratio": 1,
        "n2o_agriculture_abatement_adoption_fraction": 1,
    },
)
def n2o_from_agriculture_soils():
    """
    Formulas/Coefficients are IPCC Tier 1 Estimates https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O%26CO2.pd f Unable to use FAO disaggregations on Agriculture Soils because unable to split direct/indirects within a source e.g. synthetic fertilizers
    """
    return (
        (
            n2on_direct_soil()
            + n2on_indirect_via_leaching_and_runoff()
            + n2on_indirect_via_volatilisation()
        )
        * n2on_ratio()
        * (1 - n2o_agriculture_abatement_adoption_fraction())
    )


@component.add(
    name="N2O from Agriculture Soils in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_from_agriculture_soils": 1, "n2o_to_co2_gwp100_ar6": 1},
)
def n2o_from_agriculture_soils_in_co2eq():
    return n2o_from_agriculture_soils() * n2o_to_co2_gwp100_ar6()


@component.add(
    name="N2O from Burning Biomass",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"burned_area": 1, "emission_factor_n2o_from_burning_biomass": 1},
)
def n2o_from_burning_biomass():
    return burned_area() * emission_factor_n2o_from_burning_biomass()


@component.add(
    name="N2O from Burning Biomass in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_from_burning_biomass": 1, "n2o_to_co2_gwp100_ar6": 1},
)
def n2o_from_burning_biomass_in_co2eq():
    return n2o_from_burning_biomass() * n2o_to_co2_gwp100_ar6()


@component.add(
    name="N2O from Crop Burning",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"burning_crop_residues": 1, "emission_factor_n2o_from_crop_burning": 1},
)
def n2o_from_crop_burning():
    return burning_crop_residues() * emission_factor_n2o_from_crop_burning()


@component.add(
    name="N2O from Crop Burning in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_from_crop_burning": 1, "n2o_to_co2_gwp100_ar6": 1},
)
def n2o_from_crop_burning_in_co2eq():
    return n2o_from_crop_burning() * n2o_to_co2_gwp100_ar6()


@component.add(
    name="N2O from Crop Residues",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emission_factor_n2o_direct_ef1": 1,
        "nitrogen_from_crop_residues": 1,
        "n2on_ratio": 1,
    },
)
def n2o_from_crop_residues():
    return (
        emission_factor_n2o_direct_ef1() * nitrogen_from_crop_residues() * n2on_ratio()
    )


@component.add(
    name="N2O from Livestocks and Manure",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2on_ratio": 1,
        "emission_factor_n2on_for_manure": 1,
        "total_n_produced_in_manure": 1,
        "n2o_agriculture_abatement_adoption_fraction": 1,
    },
)
def n2o_from_livestocks_and_manure():
    return (
        n2on_ratio()
        * emission_factor_n2on_for_manure()
        * total_n_produced_in_manure()
        * (1 - n2o_agriculture_abatement_adoption_fraction())
    )


@component.add(
    name="N2O from Livestocks and Manure in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_from_livestocks_and_manure": 1, "n2o_to_co2_gwp100_ar6": 1},
)
def n2o_from_livestocks_and_manure_in_co2eq():
    return n2o_from_livestocks_and_manure() * n2o_to_co2_gwp100_ar6()


@component.add(
    name="N2O from Savanna Fires",
    units="TonN2O/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_from_savanna_fires():
    """
    1990-2022 Average FAO
    """
    return 460000


@component.add(
    name="N2O Intensity of Emission from Coal",
    units="TonN2O/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_intensity_of_emission_from_coal():
    """
    N2O intensity from coal energy production and it use.
    """
    return 0.025


@component.add(
    name="N2O Intensity of Emission from Gas",
    units="TonN2O/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_intensity_of_emission_from_gas():
    """
    N2O intensity from gas energy production and it use.
    """
    return 0.0042


@component.add(
    name="N2O Intensity of Emission from Oil",
    units="TonN2O/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_intensity_of_emission_from_oil():
    """
    N2O intensity from oil energy production and it use.
    """
    return 0.013


@component.add(
    name="N2O IW Abatement Adoption Fraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2o_iw_abatement_maximum_fraction": 1,
        "n2o_iw_abatement_year_of_maximum": 1,
        "n2o_iw_abatement_adoption_slope": 1,
        "time": 1,
    },
)
def n2o_iw_abatement_adoption_fraction():
    """
    Logistic Regression formula to follow adoption timeline of N2O abatement Technologies estimated between 1980-2000
    """
    return n2o_iw_abatement_maximum_fraction() / (
        1
        + float(
            np.exp(
                -n2o_iw_abatement_adoption_slope()
                * (time() - n2o_iw_abatement_year_of_maximum())
            )
        )
    )


@component.add(
    name="N2O IW Abatement Adoption Slope",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_n2o_iw_abatement_adoption_slope": 1},
    other_deps={
        "_smooth_n2o_iw_abatement_adoption_slope": {
            "initial": {"time": 1},
            "step": {"time": 1},
        }
    },
)
def n2o_iw_abatement_adoption_slope():
    """
    0.15
    """
    return 0.15 - _smooth_n2o_iw_abatement_adoption_slope()


_smooth_n2o_iw_abatement_adoption_slope = Smooth(
    lambda: ramp(__data["time"], 0.0035, 1980, 2010),
    lambda: 2,
    lambda: ramp(__data["time"], 0.0035, 1980, 2010),
    lambda: 1,
    "_smooth_n2o_iw_abatement_adoption_slope",
)


@component.add(
    name="N2O IW Abatement Maximum Fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_iw_abatement_maximum_fraction():
    """
    Major industrial sources with partial/full abatement ( 70%);
    """
    return 0.9


@component.add(
    name="N2O IW Abatement Year of Maximum",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_iw_abatement_year_of_maximum():
    """
    Midpoint of Historical Adoption
    """
    return 2000


@component.add(
    name="N2O to CO2 GWP100 AR6",
    units="TonCO2/TonN2O",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2o_to_co2_gwp100_ar6():
    """
    IPCC AR5 = 265; AR6 = 273 https://ghgprotocol.org/sites/default/files/2024-08/Global-Warming-Potentia l-Values%20%28August%202024%29.pdf
    """
    return 273


@component.add(
    name='"N2O-N Direct Soil"',
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_n_application_for_agriculture": 1,
        "nitrogen_application_with_manure": 1,
        "nitrogen_from_crop_residues": 1,
        "emission_factor_n2o_direct_ef1": 1,
    },
)
def n2on_direct_soil():
    """
    Units in N2O-N Mineralized Soil is omitted
    """
    return (
        commercial_n_application_for_agriculture()
        + nitrogen_application_with_manure()
        + nitrogen_from_crop_residues()
    ) * emission_factor_n2o_direct_ef1()


@component.add(
    name='"N2O-N Indirect via Leaching and Runoff"',
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nitrogen_leaching_and_runoff_rate": 1,
        "emission_factor_n2o_leaching_runoff_ef5": 1,
    },
)
def n2on_indirect_via_leaching_and_runoff():
    """
    Units in N2O-N
    """
    return (
        nitrogen_leaching_and_runoff_rate() * emission_factor_n2o_leaching_runoff_ef5()
    )


@component.add(
    name='"N2O-N Indirect via Volatilisation"',
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emission_factor_n2o_volatilisation_ef4": 1,
        "nitrogen_application_with_manure": 1,
        "fraction_of_synthetic_fertilizer_volatilisation": 1,
        "commercial_n_application_for_agriculture": 1,
        "fraction_of_manure_volatilisation": 1,
    },
)
def n2on_indirect_via_volatilisation():
    return emission_factor_n2o_volatilisation_ef4() * (
        commercial_n_application_for_agriculture()
        * fraction_of_synthetic_fertilizer_volatilisation()
        + nitrogen_application_with_manure() * fraction_of_manure_volatilisation()
    )


@component.add(
    name='"N2O-N Ratio"',
    units="TonN2O/Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def n2on_ratio():
    return 44 / 28


@component.add(
    name="Nitrogen from Crop Residues",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"crop_residues": 1, "residue_n_content": 1},
)
def nitrogen_from_crop_residues():
    return sum(
        crop_residues().rename({"PlantFood": "PlantFood!"})
        * residue_n_content().rename({"PlantFood": "PlantFood!"}),
        dim=["PlantFood!"],
    )


@component.add(
    name="Normal C Intensity of Emission from Coal",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_carbon_emissions_of_coal": 1},
)
def normal_c_intensity_of_emission_from_coal():
    """
    Initial carbon intensity of production from coal technologies.
    """
    return normal_carbon_emissions_of_coal()


@component.add(
    name="Normal C Intensity of Emission from Gas",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_carbon_emissions_of_gas": 1},
)
def normal_c_intensity_of_emission_from_gas():
    """
    Initial carbon intensity of production from gas technologies.
    """
    return normal_carbon_emissions_of_gas()


@component.add(
    name="Normal C Intensity of Emission from Oil",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_carbon_emissions_of_oil": 1},
)
def normal_c_intensity_of_emission_from_oil():
    """
    Initial carbon intensity of production from oil technologies.
    """
    return normal_carbon_emissions_of_oil()


@component.add(
    name="Normal Carbon Emissions of Coal",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_carbon_emissions_of_coal():
    """
    Felix1: 640000 IPCC: med: 9.5366e+006 min:8606200 Brian Felix 1.08e+006
    """
    return 1080000.0


@component.add(
    name="Normal Carbon Emissions of Gas",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_carbon_emissions_of_gas():
    """
    Felix1: 1.08e+006 IPCC: med: 5.6987e+006 min:4768300 Felix Brian: 640000
    """
    return 640000


@component.add(
    name="Normal Carbon Emissions of Oil",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_carbon_emissions_of_oil():
    """
    Felix1: 836500 IPCC: 9.04814e+006 co2
    """
    return 836500


@component.add(
    name="Presure to Adjust Total C Emission from Fossil Fuels",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ccs_scenario": 1,
        "total_c_emission_from_fossil_fuels": 1,
        "c_emission_from_biomass_energy": 1,
        "desired_total_c_emission_from_fossil_fuels": 1,
    },
)
def presure_to_adjust_total_c_emission_from_fossil_fuels():
    """
    Pressure to adjust the level of carbon emission from fossil fuels is the emission level rises above the acceptable level.
    """
    return ccs_scenario() * float(
        np.maximum(
            0,
            (total_c_emission_from_fossil_fuels() + c_emission_from_biomass_energy())
            / desired_total_c_emission_from_fossil_fuels()
            - 1,
        )
    )


@component.add(
    name='"Regrowth-Sink Ratio Constant"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def regrowthsink_ratio_constant():
    """
    The difference between RCMIP and FAOSTAT Emission Data is gross and net respectively; latter Calculated from a 15 year average (1990-2014) between RCMIP AFOLU Gross Emissions and FAOSTAT LULUCF Net Emissions
    """
    return 0.7


@component.add(
    name="Residue N content",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def residue_n_content():
    """
    Calibrated, hard to find data. Relative difference between categories retained 0.4-0.9, 1.2-2.5, 1.0-2.0, 0.4-1.4 %
    """
    return xr.DataArray(
        [0.006, 0.016, 0.013, 0.008],
        {"PlantFood": _subscript_dict["PlantFood"]},
        ["PlantFood"],
    )


@component.add(
    name='"Residue-to-product ratio (RPR)"',
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def residuetoproduct_ratio_rpr():
    """
    (Calibrated) but maintained the relative differences
    """
    return xr.DataArray(
        [1.3, 0.75, 0.3, 0.6],
        {"PlantFood": _subscript_dict["PlantFood"]},
        ["PlantFood"],
    )


@component.add(
    name="Shock emission addition",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shock_scenario_switch": 1, "marginal_emission": 1},
)
def shock_emission_addition():
    """
    1 Ton CO2 is equaivalent to 1 / 3.644
    """
    return if_then_else(
        shock_scenario_switch() == 0, lambda: 0, lambda: marginal_emission()
    )


@component.add(
    name="Shock Scenario SWITCH",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shock_scenario_switch():
    """
    0: no emission shock 1: there is an emission shock in the current year
    """
    return 0


@component.add(
    name="Time to Improve CCS",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_to_improve_ccs_variation": 1, "time": 1},
)
def time_to_improve_ccs():
    """
    Average CCS technology development lead time.
    """
    return 10 + step(__data["time"], time_to_improve_ccs_variation() - 10, 2020)


@component.add(
    name="Time to Improve CCS Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_improve_ccs_variation():
    """
    Average CCS technology development lead time.
    """
    return 10


@component.add(
    name="Ton C to kg CO2",
    units="kgCO2/TonC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_c_to_kg_co2():
    """
    Conversion from TonC to kgCO2.
    """
    return 3670


@component.add(
    name="Total Agirculture CO2 Emissions Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_from_agriculture": 1,
        "tonco2_to_million_ton_co2": 1,
    },
)
def total_agirculture_co2_emissions_indicator():
    return total_co2_emissions_from_agriculture() * tonco2_to_million_ton_co2()


@component.add(
    name="Total Agricultural and Land Use C Emissions",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "c_emission_from_land_use": 1,
        "climate_policy_scenario": 1,
        "_smooth_total_agricultural_and_land_use_c_emissions": 1,
    },
    other_deps={
        "_smooth_total_agricultural_and_land_use_c_emissions": {
            "initial": {
                "land_mitigation_policy_multiplier": 1,
                "c_emission_from_land_use": 1,
                "climate_action_year": 2,
                "time": 1,
            },
            "step": {
                "land_mitigation_policy_multiplier": 1,
                "c_emission_from_land_use": 1,
                "climate_action_year": 2,
                "time": 1,
                "land_mitigation_policy_transition_period": 1,
            },
        }
    },
)
def total_agricultural_and_land_use_c_emissions():
    return float(
        np.maximum(
            0,
            c_emission_from_land_use()
            - climate_policy_scenario()
            * _smooth_total_agricultural_and_land_use_c_emissions(),
        )
    )


_smooth_total_agricultural_and_land_use_c_emissions = Smooth(
    lambda: ramp(
        __data["time"],
        land_mitigation_policy_multiplier() * c_emission_from_land_use(),
        climate_action_year(),
        climate_action_year() + 20,
    ),
    lambda: land_mitigation_policy_transition_period(),
    lambda: ramp(
        __data["time"],
        land_mitigation_policy_multiplier() * c_emission_from_land_use(),
        climate_action_year(),
        climate_action_year() + 20,
    ),
    lambda: 1,
    "_smooth_total_agricultural_and_land_use_c_emissions",
)


@component.add(
    name="Total Anthropogenic CH4 Emissions",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_anthropogenic_ch4_emissions_afolu": 1,
        "total_anthropogenic_ch4_emissions_fossil_and_industrial": 1,
    },
)
def total_anthropogenic_ch4_emissions():
    """
    CH4 Energy Emission - mismatch is due to underestimating before 2000 production rates.
    """
    return (
        total_anthropogenic_ch4_emissions_afolu()
        + total_anthropogenic_ch4_emissions_fossil_and_industrial()
    )


@component.add(
    name="Total Anthropogenic CH4 Emissions AFOLU",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_ch4_from_agriculture": 1, "total_ch4_from_lulucf": 1},
)
def total_anthropogenic_ch4_emissions_afolu():
    return total_ch4_from_agriculture() + total_ch4_from_lulucf()


@component.add(
    name="Total Anthropogenic CH4 Emissions Fossil and Industrial",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_ch4_from_energy": 1, "total_ch4_from_waste": 1},
)
def total_anthropogenic_ch4_emissions_fossil_and_industrial():
    return total_ch4_from_energy() + total_ch4_from_waste()


@component.add(
    name="Total Anthropogenic CH4 Emissions in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ch4_from_agriculture_in_co2eq": 1,
        "total_ch4_from_lulucf_in_co2eq": 1,
        "total_ch4_from_energy_in_co2eq": 1,
        "total_ch4_from_waste_in_co2eq": 1,
    },
)
def total_anthropogenic_ch4_emissions_in_co2eq():
    return (
        total_ch4_from_agriculture_in_co2eq()
        + total_ch4_from_lulucf_in_co2eq()
        + total_ch4_from_energy_in_co2eq()
        + total_ch4_from_waste_in_co2eq()
    )


@component.add(
    name="Total Anthropogenic CO2 Emission Biomass to Atmosphere in TonC",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_from_biomass_burning_in_c": 1,
        "co2_from_forestland_in_c": 1,
        "co2_from_net_forest_conversion_in_c": 1,
        "regrowthsink_ratio_constant": 1,
    },
)
def total_anthropogenic_co2_emission_biomass_to_atmosphere_in_tonc():
    return (
        co2_from_biomass_burning_in_c()
        + co2_from_forestland_in_c()
        + co2_from_net_forest_conversion_in_c()
    ) / (1 - regrowthsink_ratio_constant())


@component.add(
    name="Total Anthropogenic CO2 Emission Humus to Atmosphere in TonC",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_from_drained_organic_soils_in_c": 1},
)
def total_anthropogenic_co2_emission_humus_to_atmosphere_in_tonc():
    """
    exclude mineral soils + legacy (this is included in the humus res time)
    """
    return co2_from_drained_organic_soils_in_c()


@component.add(
    name="Total Anthropogenic CO2 Emissions",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "shock_emission_addition": 1,
        "total_anthropogenic_co2_emissions_afolu": 1,
        "total_anthropogenic_co2_emissions_energy": 1,
    },
)
def total_anthropogenic_co2_emissions():
    """
    CO2 AFOLU - mismatch due to land use changes (insufficient regeneration)
    """
    return (
        shock_emission_addition()
        + total_anthropogenic_co2_emissions_afolu()
        + total_anthropogenic_co2_emissions_energy()
    )


@component.add(
    name="Total Anthropogenic CO2 Emissions AFOLU",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_from_lulucf": 1, "regrowthsink_ratio_constant": 1},
)
def total_anthropogenic_co2_emissions_afolu():
    return total_co2_from_lulucf() / (1 - regrowthsink_ratio_constant())


@component.add(
    name="Total Anthropogenic CO2 Emissions Energy",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_fossil_fuels": 1,
        "total_c_emission_from_renewables": 1,
        "co2_to_c": 1,
    },
)
def total_anthropogenic_co2_emissions_energy():
    return (
        total_c_emission_from_fossil_fuels() + total_c_emission_from_renewables()
    ) * co2_to_c()


@component.add(
    name="Total Anthropogenic CO2 Emissions Energy in TonC",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_anthropogenic_co2_emissions_energy": 1, "co2_to_c": 1},
)
def total_anthropogenic_co2_emissions_energy_in_tonc():
    return total_anthropogenic_co2_emissions_energy() / co2_to_c()


@component.add(
    name="Total Anthropogenic CO2 Emissions in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_from_energy": 1, "total_co2_from_lulucf": 1},
)
def total_anthropogenic_co2_emissions_in_co2eq():
    return total_co2_from_energy() + total_co2_from_lulucf()


@component.add(
    name="Total Anthropogenic N2O Emissions",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_anthropogenic_n2o_emissions_afolu": 1,
        "total_anthropogenic_n2o_emissions_fossil_and_industrial": 1,
    },
)
def total_anthropogenic_n2o_emissions():
    return (
        total_anthropogenic_n2o_emissions_afolu()
        + total_anthropogenic_n2o_emissions_fossil_and_industrial()
    )


@component.add(
    name="Total Anthropogenic N2O Emissions AFOLU",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_n2o_from_agriculture": 1, "total_n2o_from_lulucf": 1},
)
def total_anthropogenic_n2o_emissions_afolu():
    return total_n2o_from_agriculture() + total_n2o_from_lulucf()


@component.add(
    name="Total Anthropogenic N2O Emissions Fossil and Industrial",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_n2o_from_industry_and_waste": 1, "total_n2o_from_energy": 1},
)
def total_anthropogenic_n2o_emissions_fossil_and_industrial():
    return total_n2o_from_industry_and_waste() + total_n2o_from_energy()


@component.add(
    name="Total Anthropogenic N2O Emissions in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_n2o_from_agriculture_in_co2eq": 1,
        "total_n2o_from_industry_and_waste_in_co2eq": 1,
        "total_n2o_from_energy_in_co2eq": 1,
        "total_n2o_from_lulucf_in_co2eq": 1,
    },
)
def total_anthropogenic_n2o_emissions_in_co2eq():
    return (
        total_n2o_from_agriculture_in_co2eq()
        + total_n2o_from_industry_and_waste_in_co2eq()
        + total_n2o_from_energy_in_co2eq()
        + total_n2o_from_lulucf_in_co2eq()
    )


@component.add(
    name="Total C Emission from Fossil Fuels",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_emission_from_coal_energy": 1,
        "c_emission_from_gas_energy": 1,
        "c_emission_from_oil_energy": 1,
    },
)
def total_c_emission_from_fossil_fuels():
    """
    Source of historical data: Global Carbon Project 2020
    """
    return (
        c_emission_from_coal_energy()
        + c_emission_from_gas_energy()
        + c_emission_from_oil_energy()
    )


@component.add(
    name="Total C Emission from Renewables",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_emission_from_biomass_energy": 1,
        "c_emission_from_solar_energy": 1,
        "c_emission_from_wind_energy": 1,
    },
)
def total_c_emission_from_renewables():
    """
    Total carbon emission from renewable energy sources.
    """
    return (
        c_emission_from_biomass_energy()
        + c_emission_from_solar_energy()
        + c_emission_from_wind_energy()
    )


@component.add(
    name="Total C Emission from the Energy Sector",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_fossil_fuels": 1,
        "total_c_emission_from_renewables": 1,
    },
)
def total_c_emission_from_the_energy_sector():
    return total_c_emission_from_fossil_fuels() + total_c_emission_from_renewables()


@component.add(
    name="Total C Emissions",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_the_energy_sector": 1,
        "total_agricultural_and_land_use_c_emissions": 1,
        "co2_to_c": 1,
        "shock_emission_addition": 1,
    },
)
def total_c_emissions():
    return (
        total_c_emission_from_the_energy_sector()
        + total_agricultural_and_land_use_c_emissions()
        + shock_emission_addition() / co2_to_c()
    )


@component.add(
    name="Total CH4 from Agriculture",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_from_crop_burning": 1,
        "ch4_from_livestocks_and_manure": 1,
        "ch4_from_rice_cultivation": 1,
        "ch4_from_savanna_fires": 1,
    },
)
def total_ch4_from_agriculture():
    return (
        ch4_from_crop_burning()
        + ch4_from_livestocks_and_manure()
        + ch4_from_rice_cultivation()
        + ch4_from_savanna_fires()
    )


@component.add(
    name="Total CH4 from Agriculture in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_from_crop_burning_in_co2eq": 1,
        "ch4_from_livestocks_and_manure_in_co2eq": 1,
        "ch4_from_rice_cultivation_in_co2eq": 1,
    },
)
def total_ch4_from_agriculture_in_co2eq():
    return (
        ch4_from_crop_burning_in_co2eq()
        + ch4_from_livestocks_and_manure_in_co2eq()
        + ch4_from_rice_cultivation_in_co2eq()
    )


@component.add(
    name="Total CH4 from Energy",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emission_from_coal_energy": 1,
        "ch4_emission_from_gas_energy": 1,
        "ch4_emission_from_oil_energy": 1,
        "ch4_emission_from_biomass_energy": 1,
    },
)
def total_ch4_from_energy():
    """
    IEA website is down (cant get full data), but calibrated from https://www.iea.org/data-and-statistics/charts/methane-emissions-from-energ y-2000-2023
    """
    return (
        ch4_emission_from_coal_energy()
        + ch4_emission_from_gas_energy()
        + ch4_emission_from_oil_energy()
        + ch4_emission_from_biomass_energy()
    )


@component.add(
    name="Total CH4 from Energy in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_ch4_from_energy": 1, "ch4_to_co2_fossil_gwp100_ar6": 1},
)
def total_ch4_from_energy_in_co2eq():
    return total_ch4_from_energy() * ch4_to_co2_fossil_gwp100_ar6()


@component.add(
    name="Total CH4 from LULUCF",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_from_burning_biomass": 1},
)
def total_ch4_from_lulucf():
    return ch4_from_burning_biomass()


@component.add(
    name="Total CH4 from LULUCF in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_from_burning_biomass_in_co2eq": 1},
)
def total_ch4_from_lulucf_in_co2eq():
    return ch4_from_burning_biomass_in_co2eq()


@component.add(
    name="Total CH4 from Waste",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_municipal_solid_waste_disposal": 1,
        "emission_factors_ch4_from_waste": 1,
        "ch4_waste_abatement_adoption_fraction": 1,
    },
)
def total_ch4_from_waste():
    """
    https://www.ipcc-nggip.iges.or.jp/public/gp/english/ Formulas from here. MSW Generation in Table 5;
    """
    return (
        total_municipal_solid_waste_disposal()
        * emission_factors_ch4_from_waste()
        * (1 - ch4_waste_abatement_adoption_fraction())
    )


@component.add(
    name="Total CH4 from Waste in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_ch4_from_waste": 1, "ch4_to_co2_nonfossil_gwp100_ar6": 1},
)
def total_ch4_from_waste_in_co2eq():
    return total_ch4_from_waste() * ch4_to_co2_nonfossil_gwp100_ar6()


@component.add(
    name="Total CO2 Emissions from Land Use",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_emission_from_land_use": 1, "co2_to_c": 1},
)
def total_co2_emissions_from_land_use():
    return c_emission_from_land_use() * co2_to_c()


@component.add(
    name="Total CO2 Emissions from the Energy Sector Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_the_energy_sector": 1,
        "co2_to_c": 1,
        "tonco2_to_million_ton_co2": 1,
    },
)
def total_co2_emissions_from_the_energy_sector_indicator():
    return (
        total_c_emission_from_the_energy_sector()
        * co2_to_c()
        * tonco2_to_million_ton_co2()
    )


@component.add(
    name="Total CO2 Emissions Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emissions": 1,
        "carbon_removal_rate": 1,
        "co2_to_c": 1,
        "tonco2_to_million_ton_co2": 1,
    },
)
def total_co2_emissions_indicator():
    return (
        (total_c_emissions() - carbon_removal_rate())
        * co2_to_c()
        * tonco2_to_million_ton_co2()
    )


@component.add(
    name="Total CO2 from Energy",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_renewables": 1,
        "total_c_emission_from_fossil_fuels": 1,
        "co2_to_c": 1,
    },
)
def total_co2_from_energy():
    return (
        total_c_emission_from_renewables() + total_c_emission_from_fossil_fuels()
    ) * co2_to_c()


@component.add(
    name="Total CO2 from LULUCF",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_from_net_forest_conversion": 1,
        "co2_from_forestland": 1,
        "co2_from_drained_organic_soils": 1,
        "co2_from_burning_biomass": 1,
    },
)
def total_co2_from_lulucf():
    return (
        co2_from_net_forest_conversion()
        + co2_from_forestland()
        + co2_from_drained_organic_soils()
        + co2_from_burning_biomass()
    )


@component.add(
    name="Total CO2 from LULUCF in C",
    units="TonCO2/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "co2_from_biomass_burning_in_c": 1,
        "co2_from_drained_organic_soils_in_c": 1,
        "co2_from_forestland_in_c": 1,
        "co2_from_net_forest_conversion_in_c": 1,
        "climate_policy_scenario": 1,
        "_smooth_total_co2_from_lulucf_in_c": 1,
    },
    other_deps={
        "_smooth_total_co2_from_lulucf_in_c": {
            "initial": {
                "land_mitigation_policy_multiplier": 1,
                "co2_from_drained_organic_soils_in_c": 1,
                "co2_from_biomass_burning_in_c": 1,
                "co2_from_forestland_in_c": 1,
                "co2_from_net_forest_conversion_in_c": 1,
                "climate_action_year": 2,
                "time": 1,
            },
            "step": {
                "land_mitigation_policy_multiplier": 1,
                "co2_from_drained_organic_soils_in_c": 1,
                "co2_from_biomass_burning_in_c": 1,
                "co2_from_forestland_in_c": 1,
                "co2_from_net_forest_conversion_in_c": 1,
                "climate_action_year": 2,
                "time": 1,
                "land_mitigation_policy_transition_period": 1,
            },
        }
    },
)
def total_co2_from_lulucf_in_c():
    return float(
        np.maximum(
            0,
            (
                co2_from_biomass_burning_in_c()
                + co2_from_drained_organic_soils_in_c()
                + co2_from_forestland_in_c()
                + co2_from_net_forest_conversion_in_c()
            )
            - climate_policy_scenario() * _smooth_total_co2_from_lulucf_in_c(),
        )
    )


_smooth_total_co2_from_lulucf_in_c = Smooth(
    lambda: ramp(
        __data["time"],
        land_mitigation_policy_multiplier()
        * (
            co2_from_biomass_burning_in_c()
            + co2_from_drained_organic_soils_in_c()
            + co2_from_forestland_in_c()
            + co2_from_net_forest_conversion_in_c()
        ),
        climate_action_year(),
        climate_action_year() + 20,
    ),
    lambda: land_mitigation_policy_transition_period(),
    lambda: ramp(
        __data["time"],
        land_mitigation_policy_multiplier()
        * (
            co2_from_biomass_burning_in_c()
            + co2_from_drained_organic_soils_in_c()
            + co2_from_forestland_in_c()
            + co2_from_net_forest_conversion_in_c()
        ),
        climate_action_year(),
        climate_action_year() + 20,
    ),
    lambda: 1,
    "_smooth_total_co2_from_lulucf_in_c",
)


@component.add(
    name="Total GHG Emissions from AFOLU",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ghg_emissions_from_agriculture": 1,
        "total_ghg_emissions_from_lulucf": 1,
    },
)
def total_ghg_emissions_from_afolu():
    return total_ghg_emissions_from_agriculture() + total_ghg_emissions_from_lulucf()


@component.add(
    name="Total GHG Emissions from Agriculture",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ch4_from_agriculture_in_co2eq": 1,
        "total_n2o_from_agriculture_in_co2eq": 1,
    },
)
def total_ghg_emissions_from_agriculture():
    return total_ch4_from_agriculture_in_co2eq() + total_n2o_from_agriculture_in_co2eq()


@component.add(
    name="Total GHG Emissions from Energy",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_n2o_from_energy_in_co2eq": 1,
        "total_ch4_from_energy_in_co2eq": 1,
        "total_co2_from_energy": 1,
    },
)
def total_ghg_emissions_from_energy():
    return (
        total_n2o_from_energy_in_co2eq()
        + total_ch4_from_energy_in_co2eq()
        + total_co2_from_energy()
    )


@component.add(
    name="Total GHG Emissions from Industry and Waste",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_n2o_from_industry_and_waste_in_co2eq": 1,
        "total_ch4_from_waste_in_co2eq": 1,
    },
)
def total_ghg_emissions_from_industry_and_waste():
    return (
        total_n2o_from_industry_and_waste_in_co2eq() + total_ch4_from_waste_in_co2eq()
    )


@component.add(
    name="Total GHG Emissions from LULUCF",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_from_lulucf": 1,
        "total_ch4_from_lulucf_in_co2eq": 1,
        "total_n2o_from_lulucf_in_co2eq": 1,
    },
)
def total_ghg_emissions_from_lulucf():
    return (
        total_co2_from_lulucf()
        + total_ch4_from_lulucf_in_co2eq()
        + total_n2o_from_lulucf_in_co2eq()
    )


@component.add(
    name="Total Land Use CO2 Emissions Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_land_use": 1, "tonco2_to_million_ton_co2": 1},
)
def total_land_use_co2_emissions_indicator():
    return total_co2_emissions_from_land_use() * tonco2_to_million_ton_co2()


@component.add(
    name="Total Municipal Solid Waste Disposal",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "waste_generation_rates_for_municipal_solid_waste": 1,
        "population": 1,
        "ton_to_kg": 1,
        "days_in_year": 1,
    },
)
def total_municipal_solid_waste_disposal():
    return (
        waste_generation_rates_for_municipal_solid_waste()
        * population()
        / ton_to_kg()
        * days_in_year()
    )


@component.add(
    name="Total N2O from Agriculture",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2o_from_agriculture_soils": 1,
        "n2o_from_crop_burning": 1,
        "n2o_from_livestocks_and_manure": 1,
        "n2o_from_savanna_fires": 1,
    },
)
def total_n2o_from_agriculture():
    return (
        n2o_from_agriculture_soils()
        + n2o_from_crop_burning()
        + n2o_from_livestocks_and_manure()
        + n2o_from_savanna_fires()
    )


@component.add(
    name="Total N2O from Agriculture in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2o_from_crop_burning_in_co2eq": 1,
        "n2o_from_agriculture_soils_in_co2eq": 1,
        "n2o_from_livestocks_and_manure_in_co2eq": 1,
    },
)
def total_n2o_from_agriculture_in_co2eq():
    return (
        n2o_from_crop_burning_in_co2eq()
        + n2o_from_agriculture_soils_in_co2eq()
        + n2o_from_livestocks_and_manure_in_co2eq()
    )


@component.add(
    name="Total N2O from Energy",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n2o_emission_from_coal_energy": 1,
        "n2o_emission_from_gas_energy": 1,
        "n2o_emission_from_oil_energy": 1,
    },
)
def total_n2o_from_energy():
    """
    IEA website is down (cant get full data), but calibrated from https://www.iea.org/data-and-statistics/charts/methane-emissions-from-energ y-2000-2023
    """
    return (
        n2o_emission_from_coal_energy()
        + n2o_emission_from_gas_energy()
        + n2o_emission_from_oil_energy()
    )


@component.add(
    name="Total N2O from Energy in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_n2o_from_energy": 1, "n2o_to_co2_gwp100_ar6": 1},
)
def total_n2o_from_energy_in_co2eq():
    return total_n2o_from_energy() * n2o_to_co2_gwp100_ar6()


@component.add(
    name="Total N2O from Industry and Waste",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gross_world_product": 1,
        "emission_factors_n2o_from_industrial_activity": 1,
        "n2o_iw_abatement_adoption_fraction": 1,
    },
)
def total_n2o_from_industry_and_waste():
    return (
        gross_world_product()
        * emission_factors_n2o_from_industrial_activity()
        * (1 - n2o_iw_abatement_adoption_fraction())
    )


@component.add(
    name="Total N2O from Industry and Waste in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_to_co2_gwp100_ar6": 1, "total_n2o_from_industry_and_waste": 1},
)
def total_n2o_from_industry_and_waste_in_co2eq():
    return n2o_to_co2_gwp100_ar6() * total_n2o_from_industry_and_waste()


@component.add(
    name="Total N2O from LULUCF",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_from_burning_biomass": 1},
)
def total_n2o_from_lulucf():
    return n2o_from_burning_biomass()


@component.add(
    name="Total N2O from LULUCF in CO2eq",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_from_burning_biomass_in_co2eq": 1},
)
def total_n2o_from_lulucf_in_co2eq():
    return n2o_from_burning_biomass_in_co2eq()


@component.add(
    name="Total Renewable Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production": 1,
        "solar_energy_production": 1,
        "wind_energy_production": 1,
    },
)
def total_renewable_energy_production():
    return (
        biomass_energy_production()
        + solar_energy_production()
        + wind_energy_production()
    )


@component.add(
    name="Waste Generation Rates for Municipal Solid Waste",
    units="kg/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"msw_gradient": 1, "gwp_per_capita": 1, "msw_constant": 1},
)
def waste_generation_rates_for_municipal_solid_waste():
    """
    Formuala taken from IPCC (2000) 'Good Practice Guidance and Uncertainty Management in National Greenhouse Gas Inventories: CH4 Emissions from Solid Waste Disposal', *Background Papers*. Available at: https://www.ipcc-nggip.iges.or.jp/public/gp/bgp/5_1_CH4_Solid_Waste.pdf. Original formula based on GNI
    """
    return msw_gradient() * gwp_per_capita() / 1000 + msw_constant()
