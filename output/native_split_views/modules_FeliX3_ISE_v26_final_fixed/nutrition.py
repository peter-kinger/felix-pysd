"""
Module nutrition
Translated using PySD version 3.14.3
"""

@component.add(
    name="Alpha ln PoU",
    units="Dnml",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_alpha": 1,
        "alpha_variation": 1,
        "variable_smooth_alpha_variation_fnc": 1,
    },
)
def alpha_ln_pou():
    """
    Good Range of Skew −3 ≤ Alpha ≤ 3; 0 is no skew
    """
    return baseline_alpha() + alpha_variation() * variable_smooth_alpha_variation_fnc()


@component.add(
    name="Alpha Variation", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def alpha_variation():
    return 0


@component.add(
    name="Average Caloric Availability per Capita per Day",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_caloric_availability": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def average_caloric_availability_per_capita_per_day():
    return (
        total_caloric_availability() / population() / days_in_year() / kcal_to_mkcal()
    )


@component.add(
    name="Average Caloric Consumption per Capita per Day",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_caloric_intake": 1,
        "population": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
    },
)
def average_caloric_consumption_per_capita_per_day():
    return total_caloric_intake() / population() / kcal_to_mkcal() / days_in_year()


@component.add(
    name="Average Nutrient Availability per Capita per Day",
    units="g/(Person*Day)",
    subscripts=["Nutrients"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nutrient_availability_per_capita_per_day_from_plant_food": 1,
        "nutrient_availability_per_capita_per_day_from_animal_food": 1,
    },
)
def average_nutrient_availability_per_capita_per_day():
    return (
        nutrient_availability_per_capita_per_day_from_plant_food()
        + nutrient_availability_per_capita_per_day_from_animal_food()
    )


@component.add(
    name="Baseline Alpha", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def baseline_alpha():
    return 0


@component.add(
    name="Baseline Sigma", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def baseline_sigma():
    return 0.3031


@component.add(
    name="Caloric Availability by Food Category",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_supply_in_tonnes": 1, "caloric_value_of_food": 1},
)
def caloric_availability_by_food_category():
    return food_supply_in_tonnes() * caloric_value_of_food()


@component.add(
    name="Caloric Availability by Food Category by Population Subgroups",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "caloric_availability_by_population_subgroups": 1,
        "distribution_of_caloric_availability_by_food_category": 1,
    },
)
def caloric_availability_by_food_category_by_population_subgroups():
    return (
        caloric_availability_by_population_subgroups()
        * distribution_of_caloric_availability_by_food_category()
    ).transpose("FoodCategories", "Gender", "Cohorts")


@component.add(
    name="Caloric Availability by Population Subgroups",
    units="kcal/(Person*Day)",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "distribution_reference_calorie_consumption_by_cohort_and_gender": 1,
        "scaling_factor_for_availability": 1,
    },
)
def caloric_availability_by_population_subgroups():
    return (
        distribution_reference_calorie_consumption_by_cohort_and_gender()
        * scaling_factor_for_availability()
    )


@component.add(
    name="Caloric Availability per Capita by Food Category",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "caloric_availability_by_food_category": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def caloric_availability_per_capita_by_food_category():
    return (
        caloric_availability_by_food_category()
        / population()
        / days_in_year()
        / kcal_to_mkcal()
    )


@component.add(
    name="Caloric Intake by Food Category",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "caloric_availability_by_food_category": 1,
        "reference_food_waste_and_loss": 1,
        "recovered_food_losses_and_waste_consumed": 1,
    },
)
def caloric_intake_by_food_category():
    """
    Caloric Availability by Food Category[FoodCategories] * (1 - Food Waste Fraction of Effective Demand[FoodCategories] * Recovered Waste to Consumption)
    """
    return (
        caloric_availability_by_food_category()
        - reference_food_waste_and_loss()
        + recovered_food_losses_and_waste_consumed()
    )


@component.add(
    name="Caloric Intake by Food Category by Population Subgroups",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "caloric_intake_by_population_subgroups": 1,
        "distribution_of_caloric_intake_by_food_category": 1,
    },
)
def caloric_intake_by_food_category_by_population_subgroups():
    return (
        caloric_intake_by_population_subgroups()
        * distribution_of_caloric_intake_by_food_category()
    ).transpose("FoodCategories", "Gender", "Cohorts")


@component.add(
    name="Caloric Intake by Population Subgroups",
    units="kcal/(Person*Day)",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "distribution_reference_calorie_consumption_by_cohort_and_gender": 1,
        "scaling_factor_for_calorie_intake": 1,
    },
)
def caloric_intake_by_population_subgroups():
    return (
        distribution_reference_calorie_consumption_by_cohort_and_gender()
        * scaling_factor_for_calorie_intake()
    )


@component.add(
    name="Delta",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alpha_ln_pou": 2},
)
def delta():
    """
    Skew Normal Parameters
    """
    return alpha_ln_pou() / float(np.sqrt(1 + alpha_ln_pou() ** 2))


@component.add(
    name="Dietary Energy Supply by Subgroups",
    units="kcal/(Person*Day)",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "caloric_availability_by_population_subgroups": 1,
        "sa_scaling_of_supply_to_des": 1,
    },
)
def dietary_energy_supply_by_subgroups():
    return (
        caloric_availability_by_population_subgroups() * sa_scaling_of_supply_to_des()
    )


@component.add(
    name="Distribution of Caloric Availability by Food Category",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "caloric_availability_by_food_category": 1,
        "total_caloric_availability": 1,
    },
)
def distribution_of_caloric_availability_by_food_category():
    return caloric_availability_by_food_category() / total_caloric_availability()


@component.add(
    name="Distribution of Caloric Intake by Food Category",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"caloric_intake_by_food_category": 1, "total_caloric_intake": 1},
)
def distribution_of_caloric_intake_by_food_category():
    return caloric_intake_by_food_category() / total_caloric_intake()


@component.add(
    name="Distribution Reference Calorie Consumption",
    units="kcal/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "distribution_reference_calorie_consumption_by_cohort_and_gender": 1,
        "population_cohorts": 1,
    },
)
def distribution_reference_calorie_consumption():
    return sum(
        distribution_reference_calorie_consumption_by_cohort_and_gender().rename(
            {"Gender": "Gender!", "Cohorts": "Cohorts!"}
        )
        * population_cohorts().rename({"Gender": "Gender!", "Cohorts": "Cohorts!"}),
        dim=["Gender!", "Cohorts!"],
    )


@component.add(
    name="Distribution Reference Calorie Consumption by Cohort and Gender",
    units="kcal/(Person*Day)",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def distribution_reference_calorie_consumption_by_cohort_and_gender():
    """
    Same dataset used to proportionally distribute calorie by age, cohorts See Average Calorie Consumption in New_DietData.csv
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                1346.0,
                1700.0,
                2252.0,
                2932.0,
                2974.0,
                2762.0,
                2762.0,
                2762.0,
                2762.0,
                2549.0,
                2549.0,
                2549.0,
                2549.0,
                2337.0,
                2337.0,
                2337.0,
                2337.0,
                2337.0,
                2337.0,
                2337.0,
                2337.0,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                1275.0,
                1615.0,
                2040.0,
                2167.0,
                2337.0,
                2125.0,
                2125.0,
                2125.0,
                2125.0,
                2125.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
                1912.0,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="End Year of Alpha Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def end_year_of_alpha_variation():
    return 2040


@component.add(
    name="End Year of Sigma Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def end_year_of_sigma_variation():
    return 2040


@component.add(
    name="MER Calibration", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def mer_calibration():
    return 1


@component.add(
    name="Minimum Energy Requirement by Subgroups",
    units="kcal/(Person*Day)",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def minimum_energy_requirement_by_subgroups():
    """
    Calculated in "MDER Disaggregation Calculation" in New_DietData_ISE.xlsx Specific formulas for basal metabolic rate (BMR) are provided in the Human Energy Requirements report (FAO, 2008). BMR estimates rely on BMI reference values from WHO guidelines combined with average heights from WHO growth standards (WHO, 2025).
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                1055.61,
                1707.11,
                1920.89,
                2439.84,
                2427.63,
                2427.63,
                2385.47,
                2385.47,
                2385.47,
                2385.47,
                2385.47,
                2385.47,
                1964.61,
                1964.61,
                1964.61,
                1964.61,
                1964.61,
                1964.61,
                1964.61,
                1964.61,
                1964.61,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                981.607,
                1586.29,
                1720.1,
                1883.05,
                1816.41,
                1816.41,
                1893.16,
                1893.16,
                1893.16,
                1893.16,
                1893.16,
                1893.16,
                1671.69,
                1671.69,
                1671.69,
                1671.69,
                1671.69,
                1671.69,
                1671.69,
                1671.69,
                1671.69,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="Mu ln PoU",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dietary_energy_supply_by_subgroups": 1},
)
def mu_ln_pou():
    return dietary_energy_supply_by_subgroups()


@component.add(
    name="Number of Undernourished People by Subgroups",
    units="Person",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "prevalence_of_undernourishment_by_subgroups": 1,
        "population_cohorts": 1,
    },
)
def number_of_undernourished_people_by_subgroups():
    return prevalence_of_undernourishment_by_subgroups() * population_cohorts()


@component.add(
    name="Nutrient Availability per Capita by Food Category",
    units="g/(Person*Day)",
    subscripts=["Nutrients", "FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nutritional_value_of_food": 2,
        "caloric_availability_per_capita_by_food_category": 2,
    },
)
def nutrient_availability_per_capita_by_food_category():
    value = xr.DataArray(
        np.nan,
        {
            "Nutrients": _subscript_dict["Nutrients"],
            "FoodCategories": _subscript_dict["FoodCategories"],
        },
        ["Nutrients", "FoodCategories"],
    )
    value.loc[["Protein"], :] = (
        (
            nutritional_value_of_food().loc["Protein", :].reset_coords(drop=True)
            * caloric_availability_per_capita_by_food_category()
        )
        .expand_dims({"Nutrients": ["Protein"]}, 0)
        .values
    )
    value.loc[["Fat"], :] = (
        (
            nutritional_value_of_food().loc["Fat", :].reset_coords(drop=True)
            * caloric_availability_per_capita_by_food_category()
        )
        .expand_dims({"Nutrients": ["Fat"]}, 0)
        .values
    )
    return value


@component.add(
    name="Nutrient Availability per Capita per Day from Animal Food",
    units="g/(Person*Day)",
    subscripts=["Nutrients"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nutrient_availability_per_capita_by_food_category": 2},
)
def nutrient_availability_per_capita_per_day_from_animal_food():
    value = xr.DataArray(
        np.nan, {"Nutrients": _subscript_dict["Nutrients"]}, ["Nutrients"]
    )
    value.loc[["Protein"]] = sum(
        nutrient_availability_per_capita_by_food_category()
        .loc["Protein", _subscript_dict["AnimalFood"]]
        .reset_coords(drop=True)
        .rename({"FoodCategories": "AnimalFood!"}),
        dim=["AnimalFood!"],
    )
    value.loc[["Fat"]] = sum(
        nutrient_availability_per_capita_by_food_category()
        .loc["Fat", _subscript_dict["AnimalFood"]]
        .reset_coords(drop=True)
        .rename({"FoodCategories": "AnimalFood!"}),
        dim=["AnimalFood!"],
    )
    return value


@component.add(
    name="Nutrient Availability per Capita per Day from Plant Food",
    units="g/(Person*Day)",
    subscripts=["Nutrients"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nutrient_availability_per_capita_by_food_category": 2},
)
def nutrient_availability_per_capita_per_day_from_plant_food():
    value = xr.DataArray(
        np.nan, {"Nutrients": _subscript_dict["Nutrients"]}, ["Nutrients"]
    )
    value.loc[["Protein"]] = sum(
        nutrient_availability_per_capita_by_food_category()
        .loc["Protein", _subscript_dict["PlantFood"]]
        .reset_coords(drop=True)
        .rename({"FoodCategories": "PlantFood!"}),
        dim=["PlantFood!"],
    )
    value.loc[["Fat"]] = sum(
        nutrient_availability_per_capita_by_food_category()
        .loc["Fat", _subscript_dict["PlantFood"]]
        .reset_coords(drop=True)
        .rename({"FoodCategories": "PlantFood!"}),
        dim=["PlantFood!"],
    )
    return value


@component.add(
    name="Nutritional value of food",
    units="g/kcal",
    subscripts=["Nutrients", "FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def nutritional_value_of_food():
    """
    Calculated in "SourceFAOMacronutrient" in New_DietData_ISE.xlsx Historical Data from FAOSTAT FBS 2010-2022 (Default Protein) 0.0923432, 0.087011, 0.0394168, 0.0881716, 0.068601, 0.0259789, 0.0259929, 0.00924778 (Default Fat) 0.11, 0.087011, 0.045, 0.06, 0.068601, 0.0259789, 0.022, 0.0045
    """
    value = xr.DataArray(
        np.nan,
        {
            "Nutrients": _subscript_dict["Nutrients"],
            "FoodCategories": _subscript_dict["FoodCategories"],
        },
        ["Nutrients", "FoodCategories"],
    )
    value.loc[["Protein"], :] = xr.DataArray(
        [[0.106, 0.087011, 0.045, 0.06, 0.068601, 0.0259789, 0.022, 0.0045]],
        {"Nutrients": ["Protein"], "FoodCategories": _subscript_dict["FoodCategories"]},
        ["Nutrients", "FoodCategories"],
    ).values
    value.loc[["Fat"], :] = xr.DataArray(
        [[0.09, 0.08, 0.085, 0.055, 0.00790754, 0.0045, 0.00493131, 0.052]],
        {"Nutrients": ["Fat"], "FoodCategories": _subscript_dict["FoodCategories"]},
        ["Nutrients", "FoodCategories"],
    ).values
    return value


@component.add(
    name="Omega",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sigma_ln_pou": 1, "delta": 1, "pi": 1},
)
def omega():
    """
    Skew Normal Parameters
    """
    return sigma_ln_pou() / float(np.sqrt(1 - 2 / pi() * delta() ** 2))


@component.add(
    name="Prevalence of Undernourishment by Subgroups",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"z_score_pou": 1, "normalcdf": 1},
)
def prevalence_of_undernourishment_by_subgroups():
    return normalcdf(
        z_score_pou(),
        {
            "Gender": ["male", "female"],
            "Cohorts": [
                '"0-4"',
                '"5-9"',
                '"10-14"',
                '"15-19"',
                '"20-24"',
                '"25-29"',
                '"30-34"',
                '"35-39"',
                '"40-44"',
                '"45-49"',
                '"50-54"',
                '"55-59"',
                '"60-64"',
                '"65-69"',
                '"70-74"',
                '"75-79"',
                '"80-84"',
                '"85-89"',
                '"90-94"',
                '"95-99"',
                '"100+"',
            ],
        },
    )


@component.add(
    name="Recovered Food Losses and Waste Consumed",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "recovered_food_losses_scenario": 1,
        "recovered_food_waste_scenario": 1,
    },
)
def recovered_food_losses_and_waste_consumed():
    return recovered_food_losses_scenario() + recovered_food_waste_scenario()


@component.add(
    name="Recovered Food Losses Scenario",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_ap": 1,
        "variable_smooth_fwl_switch_fnc": 1,
        "reference_loss_fraction": 1,
        "food_loss_fractions_from_scenario": 1,
        "recovered_losses_to_food_supply": 1,
    },
)
def recovered_food_losses_scenario():
    return (
        annual_caloric_demand_ap()
        * variable_smooth_fwl_switch_fnc()
        * (reference_loss_fraction() - food_loss_fractions_from_scenario())
        * recovered_losses_to_food_supply()
    )


@component.add(
    name="Recovered Food Waste Scenario",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_ap": 1,
        "variable_smooth_fwl_switch_fnc": 1,
        "reference_waste_fraction": 1,
        "food_waste_fractions_from_scenario": 1,
        "recovered_waste_to_consumption": 1,
    },
)
def recovered_food_waste_scenario():
    return (
        annual_caloric_demand_ap()
        * variable_smooth_fwl_switch_fnc()
        * (reference_waste_fraction() - food_waste_fractions_from_scenario())
        * recovered_waste_to_consumption()
    )


@component.add(
    name="Reference Food Waste and Loss",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_ap": 1,
        "reference_fwl_fraction_by_supply_chain_and_food_category": 1,
    },
)
def reference_food_waste_and_loss():
    return annual_caloric_demand_ap() * sum(
        reference_fwl_fraction_by_supply_chain_and_food_category().rename(
            {"SupplyChain": "SupplyChain!"}
        ),
        dim=["SupplyChain!"],
    )


@component.add(
    name="SA Scaling of Supply to DES",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_scaling_of_supply_to_des():
    return 1.22


@component.add(
    name="Scaling Factor for Availability",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_caloric_intake": 1,
        "distribution_reference_calorie_consumption": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def scaling_factor_for_availability():
    return (
        total_caloric_intake()
        / distribution_reference_calorie_consumption()
        / days_in_year()
        / kcal_to_mkcal()
    )


@component.add(
    name="Scaling Factor for Calorie Intake",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_caloric_intake": 1,
        "distribution_reference_calorie_consumption": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def scaling_factor_for_calorie_intake():
    return (
        total_caloric_intake()
        / distribution_reference_calorie_consumption()
        / days_in_year()
        / kcal_to_mkcal()
    )


@component.add(
    name="Sigma ln PoU",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_sigma": 2,
        "variable_smooth_sigma_variation_fnc": 1,
        "sigma_variation": 1,
    },
)
def sigma_ln_pou():
    """
    Calculated in "PoUCalculations" in New_DietData_ISE.xlsx Sigma value derived from FAOSTAT data: using MDER, PoU and DES from 2000-2024 to find average sigma values min = 0.288, max = 0.323
    """
    return (
        baseline_sigma()
        + (sigma_variation() - 1)
        * baseline_sigma()
        * variable_smooth_sigma_variation_fnc()
    )


@component.add(
    name="Sigma Variation", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sigma_variation():
    return 1


@component.add(
    name="Start Year of Alpha Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def start_year_of_alpha_variation():
    return 2020


@component.add(
    name="Start Year of Sigma Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def start_year_of_sigma_variation():
    return 2020


@component.add(
    name="Total Caloric Availability",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"caloric_availability_by_food_category": 1},
)
def total_caloric_availability():
    return sum(
        caloric_availability_by_food_category().rename(
            {"FoodCategories": "FoodCategories!"}
        ),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Total Caloric Intake",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"caloric_intake_by_food_category": 1},
)
def total_caloric_intake():
    return sum(
        caloric_intake_by_food_category().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Total Nutrient Availability",
    units="g/Year",
    subscripts=["Nutrients"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_nutrient_availability_by_food_category": 1},
)
def total_nutrient_availability():
    return sum(
        total_nutrient_availability_by_food_category().rename(
            {"FoodCategories": "FoodCategories!"}
        ),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Total Nutrient Availability by Food Category",
    units="g/Year",
    subscripts=["Nutrients", "FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nutrient_availability_per_capita_by_food_category": 1,
        "days_in_year": 1,
        "population": 1,
    },
)
def total_nutrient_availability_by_food_category():
    return (
        nutrient_availability_per_capita_by_food_category()
        * days_in_year()
        * population()
    )


@component.add(
    name="Variable Smooth Alpha Variation Fnc",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "end_year_of_alpha_variation": 3,
        "start_year_of_alpha_variation": 4,
        "time": 2,
    },
)
def variable_smooth_alpha_variation_fnc():
    """
    Logistic Curve
    """
    return if_then_else(
        end_year_of_alpha_variation() - start_year_of_alpha_variation() > 0,
        lambda: 1
        / (
            1
            + float(
                np.exp(
                    -10
                    / (end_year_of_alpha_variation() - start_year_of_alpha_variation())
                    * (
                        time()
                        - (
                            start_year_of_alpha_variation()
                            + end_year_of_alpha_variation()
                        )
                        / 2
                    )
                )
            )
        ),
        lambda: step(__data["time"], 1, start_year_of_alpha_variation()),
    )


@component.add(
    name="Variable Smooth Sigma Variation Fnc",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "end_year_of_sigma_variation": 3,
        "start_year_of_sigma_variation": 4,
        "time": 2,
    },
)
def variable_smooth_sigma_variation_fnc():
    """
    Logistic Curve
    """
    return if_then_else(
        end_year_of_sigma_variation() - start_year_of_sigma_variation() > 0,
        lambda: 1
        / (
            1
            + float(
                np.exp(
                    -10
                    / (end_year_of_sigma_variation() - start_year_of_sigma_variation())
                    * (
                        time()
                        - (
                            start_year_of_sigma_variation()
                            + end_year_of_sigma_variation()
                        )
                        / 2
                    )
                )
            )
        ),
        lambda: step(__data["time"], 1, start_year_of_sigma_variation()),
    )


@component.add(
    name="Xi",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mu_ln_pou": 1, "delta": 1, "pi": 1, "omega": 1},
)
def xi():
    """
    Skew Normal Parameters
    """
    return np.log(mu_ln_pou()) - omega() * delta() * float(np.sqrt(2 / pi()))


@component.add(
    name="Z score PoU",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "minimum_energy_requirement_by_subgroups": 1,
        "mer_calibration": 1,
        "xi": 1,
        "omega": 1,
    },
)
def z_score_pou():
    """
    Skew Normal is used in replacement of Log Normal
    """
    return (
        np.log(minimum_energy_requirement_by_subgroups() * mer_calibration()) - xi()
    ) / omega()
