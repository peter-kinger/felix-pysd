"""
Module gaseous_cycles
Translated using PySD version 3.14.3
"""

@component.add(
    name="Atmospheric CH4 Concentration 1850 AR6",
    units="ppb",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_ch4_concentration_1850_ar6():
    """
    https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.p df pg 2141
    """
    return 808


@component.add(
    name="Atmospheric CH4 Concentration 1900 AR6",
    units="ppb",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_ch4_concentration_1900_ar6():
    """
    https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.p df pg 2141
    """
    return 925


@component.add(
    name="Atmospheric CO2 Concentration 1850 AR6",
    units="ppm",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_co2_concentration_1850_ar6():
    return 285.5


@component.add(
    name="Atmospheric CO2 Law Dome 1850",
    units="ppm",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_co2_law_dome_1850():
    """
    Historical CO2 record derived from a spline fit (20 year cutoff) of the Law Dome DE08 and DE08-2 ice cores for year 1850 https://www.ncei.noaa.gov/pub/data/paleo/icecore/antarctica/law/law_co2.txt
    """
    return 284.7


@component.add(
    name="Atmospheric Concentration CH4",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atmosphere": 1, "tonch4_to_ppb": 1},
)
def atmospheric_concentration_ch4():
    return ch4_in_atmosphere() * tonch4_to_ppb()


@component.add(
    name="Atmospheric Concentration CO2",
    units="ppm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "gtc_to_tonc": 1, "ppm_to_gtc": 1},
)
def atmospheric_concentration_co2():
    """
    Converts weight of CO2 in atmosphere to concentration (ppm CO2). Source of Historical Data: Etheridge, D.M., Steele, L.P., Langenfelds, R.L., Francey, R.J., Barnola, J.-M., Morgan, V.I. 1998. Historical CO2 records from the Law Dome DE08, DE08-2, and DSS ice cores. In Trends: A Compendium of Data on Global Change. Carbon Dioxide Information Analysis Center, Oak Ridge National Laboratory, U.S. Department of Energy, Oak Ridge, Tenn., U.S.A
    """
    return c_in_atmosphere() / gtc_to_tonc() / ppm_to_gtc()


@component.add(
    name="Atmospheric Concentration N2O",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atmosphere": 1, "tonn2o_to_ppb": 1},
)
def atmospheric_concentration_n2o():
    return n2o_in_atmosphere() * tonn2o_to_ppb()


@component.add(
    name="Atmospheric Lifetime of CH4",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dynamic_atmospheric_lifetime_of_ch4": 1},
)
def atmospheric_lifetime_of_ch4():
    """
    9-12 Years
    """
    return dynamic_atmospheric_lifetime_of_ch4()


@component.add(
    name="Atmospheric Lifetime of N2O",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dynamic_atmospheric_lifetime_of_n2o": 1},
)
def atmospheric_lifetime_of_n2o():
    return dynamic_atmospheric_lifetime_of_n2o()


@component.add(
    name="Atmospheric N2O Concentration 1850 AR6",
    units="ppb",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_n2o_concentration_1850_ar6():
    """
    https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.p df pg 2141
    """
    return 273.2


@component.add(
    name="Atmospheric N2O Concentration 1900 AR6",
    units="ppb",
    limits=(270.0, 290.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_n2o_concentration_1900_ar6():
    """
    https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.pdf pg 2141 278.9
    """
    return 278.9


@component.add(
    name="Baseline Atmospheric Lifetime of CH4",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_atmospheric_lifetime_of_ch4():
    return 11.1305


@component.add(
    name="Baseline Atmospheric Lifetime of N2O",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_atmospheric_lifetime_of_n2o():
    return 100.674


@component.add(
    name="Baseline N2O Lifetime Parameter",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_n2o_lifetime_parameter():
    return 82.565


@component.add(
    name="Baseline Natural Flux",
    units="TonN2O/Year",
    limits=(10000000.0, 20000000.0, 1000000.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_natural_flux():
    return 14111900.0


@component.add(
    name="Biomass Res Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def biomass_res_time():
    """
    Average residence time of carbon in biomass. *10-15 Range
    """
    return 10


@component.add(
    name="Biostimulation Coefficient",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biostimulation_coefficient():
    """
    Coefficient for response of primary production to carbon concentration. V25 = 0.35
    """
    return 0.3


@component.add(
    name="Buff C Coeff", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def buff_c_coeff():
    """
    Coefficient of carbon concentration influence on buffer factor.
    """
    return 3.92


@component.add(
    name="Buffer Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ref_buffer_factor": 1,
        "c_in_mixed_layer": 1,
        "buff_c_coeff": 1,
        "preindustrial_c_in_mixed_layer": 1,
    },
)
def buffer_factor():
    """
    Buffer factor for atmosphere/mixed ocean carbon equilibration.
    """
    return (
        ref_buffer_factor()
        * (c_in_mixed_layer() / preindustrial_c_in_mixed_layer()) ** buff_c_coeff()
    )


@component.add(
    name="C Concentration Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "init_c_in_atmosphere": 1},
)
def c_concentration_ratio():
    """
    Current to initial carbon concentration in atmosphere.
    """
    return c_in_atmosphere() / init_c_in_atmosphere()


@component.add(
    name="C in Atmosphere",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_atmosphere": 1},
    other_deps={
        "_integ_c_in_atmosphere": {
            "initial": {"init_c_in_atmosphere": 1},
            "step": {
                "ch4_oxidation": 1,
                "flux_biomass_to_atmosphere": 1,
                "flux_humus_to_atmosphere": 1,
                "total_c_emission": 1,
                "carbon_removal_rate": 1,
                "flux_atmosphere_to_biomass": 1,
                "flux_atmosphere_to_ocean": 1,
            },
        }
    },
)
def c_in_atmosphere():
    """
    Carbon in atmosphere.
    """
    return _integ_c_in_atmosphere()


_integ_c_in_atmosphere = Integ(
    lambda: ch4_oxidation()
    + flux_biomass_to_atmosphere()
    + flux_humus_to_atmosphere()
    + total_c_emission()
    - carbon_removal_rate()
    - flux_atmosphere_to_biomass()
    - flux_atmosphere_to_ocean(),
    lambda: init_c_in_atmosphere(),
    "_integ_c_in_atmosphere",
)


@component.add(
    name="C in Biomass",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_biomass": 1},
    other_deps={
        "_integ_c_in_biomass": {
            "initial": {"init_c_in_biomass": 1},
            "step": {
                "flux_atmosphere_to_biomass": 1,
                "flux_biomass_to_atmosphere": 1,
                "flux_biomass_to_ch4": 1,
                "flux_biomass_to_humus": 1,
            },
        }
    },
)
def c_in_biomass():
    """
    Carbon in biosphere (biomass, litter, and humus) Rough estimate 550GtC
    """
    return _integ_c_in_biomass()


_integ_c_in_biomass = Integ(
    lambda: flux_atmosphere_to_biomass()
    - flux_biomass_to_atmosphere()
    - flux_biomass_to_ch4()
    - flux_biomass_to_humus(),
    lambda: init_c_in_biomass(),
    "_integ_c_in_biomass",
)


@component.add(
    name="C in Deep Ocean 1",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_1": 1},
    other_deps={
        "_integ_c_in_deep_ocean_1": {
            "initial": {"init_c_in_deep_ocean_1": 1},
            "step": {"diffusion_flux_1": 1, "diffusion_flux_2": 1},
        }
    },
)
def c_in_deep_ocean_1():
    """
    Carbon in the first layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_1()


_integ_c_in_deep_ocean_1 = Integ(
    lambda: diffusion_flux_1() - diffusion_flux_2(),
    lambda: init_c_in_deep_ocean_1(),
    "_integ_c_in_deep_ocean_1",
)


@component.add(
    name="C in Deep Ocean 1 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_1": 1, "layer_depth_1": 1},
)
def c_in_deep_ocean_1_per_meter():
    """
    Carbon in the first ocean layer per its meter.
    """
    return c_in_deep_ocean_1() / layer_depth_1()


@component.add(
    name="C in Deep Ocean 2",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_2": 1},
    other_deps={
        "_integ_c_in_deep_ocean_2": {
            "initial": {"init_c_in_deep_ocean_2": 1},
            "step": {"diffusion_flux_2": 1, "diffusion_flux_3": 1},
        }
    },
)
def c_in_deep_ocean_2():
    """
    Carbon in the second layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_2()


_integ_c_in_deep_ocean_2 = Integ(
    lambda: diffusion_flux_2() - diffusion_flux_3(),
    lambda: init_c_in_deep_ocean_2(),
    "_integ_c_in_deep_ocean_2",
)


@component.add(
    name="C in Deep Ocean 2 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_2": 1, "layer_depth_2": 1},
)
def c_in_deep_ocean_2_per_meter():
    """
    Carbon in the second ocean layer per its meter.
    """
    return c_in_deep_ocean_2() / layer_depth_2()


@component.add(
    name="C in Deep Ocean 3",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_3": 1},
    other_deps={
        "_integ_c_in_deep_ocean_3": {
            "initial": {"init_c_in_deep_ocean_3": 1},
            "step": {"diffusion_flux_3": 1, "diffusion_flux_4": 1},
        }
    },
)
def c_in_deep_ocean_3():
    """
    Carbon in the third layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_3()


_integ_c_in_deep_ocean_3 = Integ(
    lambda: diffusion_flux_3() - diffusion_flux_4(),
    lambda: init_c_in_deep_ocean_3(),
    "_integ_c_in_deep_ocean_3",
)


@component.add(
    name="C in Deep Ocean 3 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_3": 1, "layer_depth_3": 1},
)
def c_in_deep_ocean_3_per_meter():
    """
    Carbon in the third ocean layer per its meter.
    """
    return c_in_deep_ocean_3() / layer_depth_3()


@component.add(
    name="C in Deep Ocean 4",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_4": 1},
    other_deps={
        "_integ_c_in_deep_ocean_4": {
            "initial": {"init_c_in_deep_ocean_4": 1},
            "step": {"diffusion_flux_4": 1},
        }
    },
)
def c_in_deep_ocean_4():
    """
    Carbon in the fourth layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_4()


_integ_c_in_deep_ocean_4 = Integ(
    lambda: diffusion_flux_4(),
    lambda: init_c_in_deep_ocean_4(),
    "_integ_c_in_deep_ocean_4",
)


@component.add(
    name="C in Deep Ocean 4 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_4": 1, "layer_depth_4": 1},
)
def c_in_deep_ocean_4_per_meter():
    """
    Carbon in the fourth ocean layer per its meter.
    """
    return c_in_deep_ocean_4() / layer_depth_4()


@component.add(
    name="C in Humus",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_humus": 1},
    other_deps={
        "_integ_c_in_humus": {
            "initial": {"init_c_in_humus": 1},
            "step": {
                "flux_biomass_to_humus": 1,
                "flux_humus_to_atmosphere": 1,
                "flux_humus_to_ch4": 1,
            },
        }
    },
)
def c_in_humus():
    """
    Carbon in humus. Rough estimate for "single stock" of 1500GtC
    """
    return _integ_c_in_humus()


_integ_c_in_humus = Integ(
    lambda: flux_biomass_to_humus() - flux_humus_to_atmosphere() - flux_humus_to_ch4(),
    lambda: init_c_in_humus(),
    "_integ_c_in_humus",
)


@component.add(
    name="C in Mixed Layer",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_mixed_layer": 1},
    other_deps={
        "_integ_c_in_mixed_layer": {
            "initial": {"init_c_in_mixed_ocean": 1},
            "step": {"flux_atmosphere_to_ocean": 1, "diffusion_flux_1": 1},
        }
    },
)
def c_in_mixed_layer():
    """
    Carbon in mixed layer.
    """
    return _integ_c_in_mixed_layer()


_integ_c_in_mixed_layer = Integ(
    lambda: flux_atmosphere_to_ocean() - diffusion_flux_1(),
    lambda: init_c_in_mixed_ocean(),
    "_integ_c_in_mixed_layer",
)


@component.add(
    name="C in Mixed Layer per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_mixed_layer": 1, "mixed_layer_depth": 1},
)
def c_in_mixed_layer_per_meter():
    """
    Carbon in mixed layer per its meter.
    """
    return c_in_mixed_layer() / mixed_layer_depth()


@component.add(
    name="C to CH4", units="TonCH4/TonC", comp_type="Constant", comp_subtype="Normal"
)
def c_to_ch4():
    return 16.04 / 12.01


@component.add(
    name="Carbon Removal Impact Slope", comp_type="Constant", comp_subtype="Normal"
)
def carbon_removal_impact_slope():
    return 1.1


@component.add(
    name="Carbon Removal Rate",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"climate_policy_scenario": 1, "_smooth_carbon_removal_rate": 1},
    other_deps={
        "_smooth_carbon_removal_rate": {
            "initial": {
                "reference_co2_removal_rate": 1,
                "climate_action_year": 1,
                "time": 1,
            },
            "step": {
                "reference_co2_removal_rate": 1,
                "climate_action_year": 1,
                "time": 1,
                "cdr_policy_transition_period": 1,
            },
        }
    },
)
def carbon_removal_rate():
    """
    Climate Policy Scenario*SMOOTH(STEP(Carbon Removal Impact Slope*Reference Removal Rate, Climate Action Year), Climate Policy Transition Period)
    """
    return climate_policy_scenario() * _smooth_carbon_removal_rate()


_smooth_carbon_removal_rate = Smooth(
    lambda: ramp(
        __data["time"], reference_co2_removal_rate(), climate_action_year(), 2100
    ),
    lambda: cdr_policy_transition_period(),
    lambda: ramp(
        __data["time"], reference_co2_removal_rate(), climate_action_year(), 2100
    ),
    lambda: 1,
    "_smooth_carbon_removal_rate",
)


@component.add(
    name="CCS Improvement Change LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement_change_lv1": 1},
    other_deps={
        "_integ_ccs_improvement_change_lv1": {
            "initial": {"ccs_improvement_change_lv3": 1},
            "step": {"inflow_ccsiclv1": 1, "outflow_ccsiclv1": 1},
        }
    },
)
def ccs_improvement_change_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_ccs_improvement_change_lv1()


_integ_ccs_improvement_change_lv1 = Integ(
    lambda: inflow_ccsiclv1() - outflow_ccsiclv1(),
    lambda: ccs_improvement_change_lv3(),
    "_integ_ccs_improvement_change_lv1",
)


@component.add(
    name="CCS Improvement Change LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement_change_lv2": 1},
    other_deps={
        "_integ_ccs_improvement_change_lv2": {
            "initial": {"ccs_improvement_change_lv3": 1},
            "step": {"inflow_ccsiclv2": 1, "outflow_ccsiclv2": 1},
        }
    },
)
def ccs_improvement_change_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_ccs_improvement_change_lv2()


_integ_ccs_improvement_change_lv2 = Integ(
    lambda: inflow_ccsiclv2() - outflow_ccsiclv2(),
    lambda: ccs_improvement_change_lv3(),
    "_integ_ccs_improvement_change_lv2",
)


@component.add(
    name="CCS Improvement Change LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement_change_lv3": 1},
    other_deps={
        "_integ_ccs_improvement_change_lv3": {
            "initial": {"delay_time_ccsic": 1, "pressure_ccsic": 1},
            "step": {"inflow_ccsiclv3": 1, "outflow_ccsiclv3": 1},
        }
    },
)
def ccs_improvement_change_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_ccs_improvement_change_lv3()


_integ_ccs_improvement_change_lv3 = Integ(
    lambda: inflow_ccsiclv3() - outflow_ccsiclv3(),
    lambda: delay_time_ccsic() * pressure_ccsic(),
    "_integ_ccs_improvement_change_lv3",
)


@component.add(
    name="CDR Policy Transition Period",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cdr_policy_transition_period():
    return 1


@component.add(
    name="CH4 Concentration Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atmosphere": 1, "init_ch4_in_atmosphere": 1},
)
def ch4_concentration_ratio():
    return ch4_in_atmosphere() / init_ch4_in_atmosphere()


@component.add(
    name="CH4 in Atmosphere",
    units="TonCH4",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ch4_in_atmosphere": 1},
    other_deps={
        "_integ_ch4_in_atmosphere": {
            "initial": {"init_ch4_in_atmosphere": 1},
            "step": {"total_ch4_emission": 1, "total_ch4_breakdown": 1},
        }
    },
)
def ch4_in_atmosphere():
    return _integ_ch4_in_atmosphere()


_integ_ch4_in_atmosphere = Integ(
    lambda: total_ch4_emission() - total_ch4_breakdown(),
    lambda: init_ch4_in_atmosphere(),
    "_integ_ch4_in_atmosphere",
)


@component.add(
    name="CH4 Lifetime Factor from Atmospheric Concentrations",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "atmospheric_concentration_ch4": 1,
        "atmospheric_ch4_concentration_preindustrial": 1,
        "effect_of_ch4_on_ch4_lifetime": 1,
        "effect_of_n2o_on_ch4_lifetime": 1,
        "atmospheric_concentration_n2o": 1,
        "atmospheric_n2o_concentration_preindustrial": 1,
        "other_concentration_effects": 1,
    },
)
def ch4_lifetime_factor_from_atmospheric_concentrations():
    """
    Formulation based on FaIRv2 and FRIDA
    """
    return (
        float(
            np.log(
                1
                + (
                    atmospheric_concentration_ch4()
                    - atmospheric_ch4_concentration_preindustrial()
                )
                * effect_of_ch4_on_ch4_lifetime()
            )
        )
        + float(
            np.log(
                1
                + (
                    atmospheric_concentration_n2o()
                    - atmospheric_n2o_concentration_preindustrial()
                )
                * effect_of_n2o_on_ch4_lifetime()
            )
        )
        + other_concentration_effects()
    )


@component.add(
    name="CH4 Lifetime Factor from Temperature Change",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_temperature_change_on_ch4_lifetime": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def ch4_lifetime_factor_from_temperature_change():
    """
    Formulation based on FaIRv2 and FRIDA
    """
    return (
        effect_of_temperature_change_on_ch4_lifetime()
        * temperature_change_from_preindustrial()
    )


@component.add(
    name="CH4 Oxidation",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_to_co2_via_oxidation_in_tonc": 1},
)
def ch4_oxidation():
    return ch4_to_co2_via_oxidation_in_tonc()


@component.add(
    name="CH4 to CO2 via Oxidation in TonC",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "molar_mass_of_c": 1,
        "molar_mass_of_ch4": 1,
        "dmnl_adjustment_tonc": 1,
        "total_ch4_breakdown": 1,
    },
)
def ch4_to_co2_via_oxidation_in_tonc():
    """
    Assumes that all atmospheric CH4 is eventually converted into CO2; but realistically could be 95%-98%
    """
    return (
        molar_mass_of_c() / molar_mass_of_ch4() / dmnl_adjustment_tonc()
    ) * total_ch4_breakdown()


@component.add(
    name="Constant Atmospheric Lifetime of CH4",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def constant_atmospheric_lifetime_of_ch4():
    """
    9-12 Years 9.3
    """
    return 9.3


@component.add(
    name="Constant Atmospheric Lifetime of N2O",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def constant_atmospheric_lifetime_of_n2o():
    """
    9-12 Years 9.3
    """
    return 120


@component.add(
    name="Delay Time CCSIC",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_to_improve_ccs": 1},
)
def delay_time_ccsic():
    return time_to_improve_ccs() / 3


@component.add(
    name="Diffusion Flux 1",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_mixed_layer_per_meter": 1,
        "c_in_deep_ocean_1_per_meter": 1,
        "eddy_diff_coeff_m_1": 1,
        "mean_depth_of_adjacent_m_1_layers": 1,
    },
)
def diffusion_flux_1():
    """
    Diffusion flux between mixed and the first ocean layers.
    """
    return (
        (c_in_mixed_layer_per_meter() - c_in_deep_ocean_1_per_meter())
        * eddy_diff_coeff_m_1()
        / mean_depth_of_adjacent_m_1_layers()
    )


@component.add(
    name="Diffusion Flux 2",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_deep_ocean_1_per_meter": 1,
        "c_in_deep_ocean_2_per_meter": 1,
        "eddy_diff_coeff_1_2": 1,
        "mean_depth_of_adjacent_1_2_layers": 1,
    },
)
def diffusion_flux_2():
    """
    Diffusion flux between the first and the second ocean layers.
    """
    return (
        (c_in_deep_ocean_1_per_meter() - c_in_deep_ocean_2_per_meter())
        * eddy_diff_coeff_1_2()
        / mean_depth_of_adjacent_1_2_layers()
    )


@component.add(
    name="Diffusion Flux 3",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_deep_ocean_2_per_meter": 1,
        "c_in_deep_ocean_3_per_meter": 1,
        "eddy_diff_coeff_2_3": 1,
        "mean_depth_of_adjacent_2_3_layers": 1,
    },
)
def diffusion_flux_3():
    """
    Diffusion flux between the second and the third ocean layers.
    """
    return (
        (c_in_deep_ocean_2_per_meter() - c_in_deep_ocean_3_per_meter())
        * eddy_diff_coeff_2_3()
        / mean_depth_of_adjacent_2_3_layers()
    )


@component.add(
    name="Diffusion Flux 4",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_deep_ocean_3_per_meter": 1,
        "c_in_deep_ocean_4_per_meter": 1,
        "eddy_diff_coeff_3_4": 1,
        "mean_depth_of_adjacent_3_4_layers": 1,
    },
)
def diffusion_flux_4():
    """
    Diffusion flux between the third and the fourth ocean layers.
    """
    return (
        (c_in_deep_ocean_3_per_meter() - c_in_deep_ocean_4_per_meter())
        * eddy_diff_coeff_3_4()
        / mean_depth_of_adjacent_3_4_layers()
    )


@component.add(
    name="Dmnl Adjustment TonC",
    units="gC*TonCH4/(gCH4*TonC)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def dmnl_adjustment_tonc():
    return 1


@component.add(
    name="Dynamic Atmospheric Lifetime of CH4",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_atmospheric_lifetime_of_ch4": 1,
        "scale_factor_of_ch4_lifetime": 1,
    },
)
def dynamic_atmospheric_lifetime_of_ch4():
    return baseline_atmospheric_lifetime_of_ch4() * scale_factor_of_ch4_lifetime()


@component.add(
    name="Dynamic Atmospheric Lifetime of N2O",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scale_factor_of_n2o_lifetime": 1,
        "baseline_atmospheric_lifetime_of_n2o": 1,
    },
)
def dynamic_atmospheric_lifetime_of_n2o():
    """
    Formulation based on FaIRv2 and FRIDA
    """
    return scale_factor_of_n2o_lifetime() * baseline_atmospheric_lifetime_of_n2o()


@component.add(
    name="Eddy diff coeff 1 2",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_1_2": 1, "eddy_diff_coeff_mean_1_2": 1},
)
def eddy_diff_coeff_1_2():
    """
    Coefficient of carbon diffusion to the second layer of deep ocean.
    """
    return eddy_diff_coeff_index_1_2() * eddy_diff_coeff_mean_1_2()


@component.add(
    name="Eddy diff coeff 2 3",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_2_3": 1, "eddy_diff_coeff_mean_2_3": 1},
)
def eddy_diff_coeff_2_3():
    """
    Coefficient of carbon diffusion to the third layer of deep ocean.
    """
    return eddy_diff_coeff_index_2_3() * eddy_diff_coeff_mean_2_3()


@component.add(
    name="Eddy diff coeff 3 4",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_3_4": 1, "eddy_diff_coeff_mean_3_4": 1},
)
def eddy_diff_coeff_3_4():
    """
    Coefficient of carbon diffusion to the fourth layer of deep ocean.
    """
    return eddy_diff_coeff_index_3_4() * eddy_diff_coeff_mean_3_4()


@component.add(
    name="Eddy diff coeff index 1 2",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_1_2():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff index 2 3",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_2_3():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff index 3 4",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_3_4():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff index M 1",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_m_1():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff M 1",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_m_1": 1, "eddy_diff_coeff_mean_m_1": 1},
)
def eddy_diff_coeff_m_1():
    """
    Coefficient of carbon diffusion to the first layer of deep ocean.
    """
    return eddy_diff_coeff_index_m_1() * eddy_diff_coeff_mean_m_1()


@component.add(
    name="Eddy diff coeff mean 1 2",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_1_2():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Eddy diff coeff mean 2 3",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_2_3():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Eddy diff coeff mean 3 4",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_3_4():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Eddy diff coeff mean M 1",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_m_1():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Effect of Atmospheric N2O on para1",
    units="1/MTonN2O",
    limits=(-1e-09, -1e-08),
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_atmospheric_n2o_on_para1():
    """
    -0.0065 * 1e-6 (MtonN2O to TonN2O)
    """
    return -0.0065


@component.add(
    name="Effect of CH4 on CH4 Lifetime",
    units="1/ppb",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_ch4_on_ch4_lifetime():
    """
    FRIDA: 0.000254099
    """
    return 4.92467e-05


@component.add(
    name="Effect of N2O on CH4 Lifetime",
    units="1/ppb",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_n2o_on_ch4_lifetime():
    """
    FRIDA: -0.000722665
    """
    return -0.0001


@component.add(
    name="Effect of Temp on C Flux Atm ML",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_of_c_flux_to_temp": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def effect_of_temp_on_c_flux_atm_ml():
    return 1 - sensitivity_of_c_flux_to_temp() * temperature_change_from_preindustrial()


@component.add(
    name="Effect of Temperature Change on CH4 Lifetime",
    units="1/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_temperature_change_on_ch4_lifetime():
    return -0.023339


@component.add(
    name="Effect of Temperature on Land CH4 Flux",
    units="1/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_temperature_on_land_ch4_flux():
    return 0.01


@component.add(
    name="Effect of Warming on CH4 Release from Biological Activity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_temperature_on_land_ch4_flux": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def effect_of_warming_on_ch4_release_from_biological_activity():
    return 1 / (
        1
        - effect_of_temperature_on_land_ch4_flux()
        * temperature_change_from_preindustrial()
    )


@component.add(
    name="Effect of Warming on N2O Release from Biological Activity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effective_sensitivity_of_temperature_on_n2o_flux": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def effect_of_warming_on_n2o_release_from_biological_activity():
    return (
        1
        + effective_sensitivity_of_temperature_on_n2o_flux()
        * temperature_change_from_preindustrial()
    )


@component.add(
    name="Effective Sensitivity of Temperature on N2O Flux",
    units="1/DegreesC",
    limits=(0.0, 0.04, 0.001),
    comp_type="Constant",
    comp_subtype="Normal",
)
def effective_sensitivity_of_temperature_on_n2o_flux():
    return 0.0328021


@component.add(
    name="Equil C in Mixed Layer",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "preindustrial_c_in_mixed_layer": 1,
        "effect_of_temp_on_c_flux_atm_ml": 1,
        "c_in_atmosphere": 1,
        "preindustrial_c_in_atmosphere": 1,
        "buffer_factor": 1,
    },
)
def equil_c_in_mixed_layer():
    """
    Equilibrium carbon content of mixed layer.
    """
    return (
        preindustrial_c_in_mixed_layer()
        * effect_of_temp_on_c_flux_atm_ml()
        * (c_in_atmosphere() / preindustrial_c_in_atmosphere()) ** (1 / buffer_factor())
    )


@component.add(
    name="Equilibrium C per meter in Mixed Layer",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equil_c_in_mixed_layer": 1, "mixed_layer_depth": 1},
)
def equilibrium_c_per_meter_in_mixed_layer():
    return equil_c_in_mixed_layer() / mixed_layer_depth()


@component.add(
    name="Flux Atmosphere to Biomass",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_net_primary_production": 1,
        "c_in_atmosphere": 1,
        "preindustrial_c_in_atmosphere": 1,
        "biostimulation_coefficient": 1,
    },
)
def flux_atmosphere_to_biomass():
    """
    Carbon flux from atmosphere to biosphere *Assumed to represent Net Primary Production. Aggregated and not distinguishing Gross Primary Production and Respiration.
    """
    return initial_net_primary_production() * (
        1
        + biostimulation_coefficient()
        * float(np.log(c_in_atmosphere() / preindustrial_c_in_atmosphere()))
    )


@component.add(
    name="Flux Atmosphere to Ocean",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equil_c_in_mixed_layer": 1, "c_in_mixed_layer": 1, "mixing_time": 1},
)
def flux_atmosphere_to_ocean():
    """
    Carbon flux from atmosphere to mixed ocean layer.
    """
    return (equil_c_in_mixed_layer() - c_in_mixed_layer()) / mixing_time()


@component.add(
    name="Flux Biomass to Atmosphere",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_biomass": 1,
        "biomass_res_time": 1,
        "humification_fraction": 1,
        "total_anthropogenic_co2_emission_biomass_to_atmosphere_in_tonc": 1,
    },
)
def flux_biomass_to_atmosphere():
    """
    Carbon flux from biomass to atmosphere.
    """
    return (c_in_biomass() / biomass_res_time()) * (
        1 - humification_fraction()
    ) + total_anthropogenic_co2_emission_biomass_to_atmosphere_in_tonc()


@component.add(
    name="Flux Biomass to CH4",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_biomass": 1,
        "effect_of_warming_on_ch4_release_from_biological_activity": 1,
        "fractional_rate_of_ch4_released_from_biomass_to_atm": 1,
    },
)
def flux_biomass_to_ch4():
    return (
        c_in_biomass()
        * effect_of_warming_on_ch4_release_from_biological_activity()
        * fractional_rate_of_ch4_released_from_biomass_to_atm()
    )


@component.add(
    name="Flux Biomass to Humus",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_biomass": 1, "biomass_res_time": 1, "humification_fraction": 1},
)
def flux_biomass_to_humus():
    """
    Carbon flux from biomass to humus.
    """
    return (c_in_biomass() / biomass_res_time()) * humification_fraction()


@component.add(
    name="Flux Humus to Atmosphere",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_humus": 1,
        "humus_res_time": 1,
        "total_anthropogenic_co2_emission_humus_to_atmosphere_in_tonc": 1,
    },
)
def flux_humus_to_atmosphere():
    """
    Carbon flux from humus to atmosphere.
    """
    return (
        c_in_humus() / humus_res_time()
        + total_anthropogenic_co2_emission_humus_to_atmosphere_in_tonc()
    )


@component.add(
    name="Flux Humus to CH4",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_humus": 1,
        "effect_of_warming_on_ch4_release_from_biological_activity": 1,
        "fractional_rate_of_ch4_released_from_humus_to_atm": 1,
    },
)
def flux_humus_to_ch4():
    """
    Does not factor C release from Permafrost and Clathrate
    """
    return (
        c_in_humus()
        * effect_of_warming_on_ch4_release_from_biological_activity()
        * fractional_rate_of_ch4_released_from_humus_to_atm()
    )


@component.add(
    name="Fractional Rate of CH4 Released from Biomass to Atm",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fractional_rate_of_ch4_released_from_biomass_to_atm():
    return 7e-06


@component.add(
    name="Fractional Rate of CH4 Released from Humus to Atm",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fractional_rate_of_ch4_released_from_humus_to_atm():
    return 0.00011


@component.add(
    name="GtC to TonC", units="TonC/GtC", comp_type="Constant", comp_subtype="Normal"
)
def gtc_to_tonc():
    """
    1 GtC equals 1000000000 tons of carbon
    """
    return 1000000000.0


@component.add(
    name="Humification Fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def humification_fraction():
    """
    v25 = 0.428 Fraction of carbon outflow from biomass that enters humus stock. *0.2-0.4
    """
    return 0.3


@component.add(
    name="Humus Res Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def humus_res_time():
    """
    Average carbon residence time in humus. * 100 V25 = 27.8
    """
    return 95


@component.add(
    name="Inflow CCSICLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_ccsic": 1},
)
def inflow_ccsiclv1():
    return pressure_ccsic()


@component.add(
    name="Inflow CCSICLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ccsiclv1": 1},
)
def inflow_ccsiclv2():
    return outflow_ccsiclv1()


@component.add(
    name="Inflow CCSICLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ccsiclv2": 1},
)
def inflow_ccsiclv3():
    return outflow_ccsiclv2()


@component.add(
    name="INIT C in Atmosphere",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"atmospheric_co2_law_dome_1850": 1, "gtc_to_tonc": 1, "ppm_to_gtc": 1},
)
def init_c_in_atmosphere():
    """
    Initial carbon in atmosphere.
    """
    return atmospheric_co2_law_dome_1850() * gtc_to_tonc() * ppm_to_gtc()


@component.add(
    name="INIT C in Biomass",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_init_c_in_biomass": 1},
    other_deps={
        "_initial_init_c_in_biomass": {
            "initial": {"flux_atmosphere_to_biomass": 1, "biomass_res_time": 1},
            "step": {},
        }
    },
)
def init_c_in_biomass():
    """
    Initial carbon in biomass.
    """
    return _initial_init_c_in_biomass()


_initial_init_c_in_biomass = Initial(
    lambda: flux_atmosphere_to_biomass() * biomass_res_time(),
    "_initial_init_c_in_biomass",
)


@component.add(
    name="INIT C in Deep Ocean 1",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_1": 1},
)
def init_c_in_deep_ocean_1():
    """
    Initial carbon in the first layer of deep ocean. was constant at 3.115e+012 in the earlier versions of the model.
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_1()


@component.add(
    name="INIT C in Deep Ocean 2",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_2": 1},
)
def init_c_in_deep_ocean_2():
    """
    Initial carbon in the second layer of deep ocean. was constant at 3.099e+012 in earlier versions of the model
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_2()


@component.add(
    name="INIT C in Deep Ocean 3",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_3": 1},
)
def init_c_in_deep_ocean_3():
    """
    Initial carbon in the third layer of deep ocean. was constant at 1.3356e+013 in earlier versions of the model
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_3()


@component.add(
    name="INIT C in Deep Ocean 4",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_4": 1},
)
def init_c_in_deep_ocean_4():
    """
    Initial carbon in the fourth layer of deep ocean. was constant at 1.8477e+013 in earlier versions of the model.
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_4()


@component.add(
    name="Init C in Deep Ocean per meter",
    units="TonC/Meter",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_init_c_in_deep_ocean_per_meter": 1},
    other_deps={
        "_initial_init_c_in_deep_ocean_per_meter": {
            "initial": {"equilibrium_c_per_meter_in_mixed_layer": 1},
            "step": {},
        }
    },
)
def init_c_in_deep_ocean_per_meter():
    return _initial_init_c_in_deep_ocean_per_meter()


_initial_init_c_in_deep_ocean_per_meter = Initial(
    lambda: equilibrium_c_per_meter_in_mixed_layer(),
    "_initial_init_c_in_deep_ocean_per_meter",
)


@component.add(
    name="INIT C in Humus",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_init_c_in_humus": 1},
    other_deps={
        "_initial_init_c_in_humus": {
            "initial": {"flux_biomass_to_humus": 1, "humus_res_time": 1},
            "step": {},
        }
    },
)
def init_c_in_humus():
    """
    Inital carbon in humus.
    """
    return _initial_init_c_in_humus()


_initial_init_c_in_humus = Initial(
    lambda: flux_biomass_to_humus() * humus_res_time(), "_initial_init_c_in_humus"
)


@component.add(
    name="INIT C in Mixed Ocean",
    units="TonC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_c_in_mixed_ocean():
    """
    Initial carbon in mixed ocean layer.
    """
    return 901800000000.0


@component.add(
    name="INIT CH4 in Atmosphere",
    units="TonCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"atmospheric_ch4_concentration_1900_ar6": 1, "tonch4_to_ppb": 1},
)
def init_ch4_in_atmosphere():
    return atmospheric_ch4_concentration_1900_ar6() / tonch4_to_ppb()


@component.add(
    name="INIT N2O in Atmosphere",
    units="TonN2O",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"atmospheric_n2o_concentration_1900_ar6": 1, "tonn2o_to_ppb": 1},
)
def init_n2o_in_atmosphere():
    return atmospheric_n2o_concentration_1900_ar6() / tonn2o_to_ppb()


@component.add(
    name="Initial Net Primary Production",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_net_primary_production():
    """
    Initial net primary production. V25 = 8.51771e+10
    """
    return 55000000000.0


@component.add(
    name="Layer Depth 1", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_1():
    """
    Depth of the first ocean layer.
    """
    return 300


@component.add(
    name="Layer Depth 2", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_2():
    """
    Depth of the second ocean layer.
    """
    return 300


@component.add(
    name="Layer Depth 3", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_3():
    """
    Depth of the third ocean layer.
    """
    return 1300


@component.add(
    name="Layer Depth 4", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_4():
    """
    Depth of the fourth ocean layer.
    """
    return 1800


@component.add(
    name="Layer Time Constant 1 2",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_2": 2, "eddy_diff_coeff_1_2": 1, "layer_depth_1": 1},
)
def layer_time_constant_1_2():
    """
    Time constant of exchange between the first and the second ocean layers.
    """
    return layer_depth_2() / (
        eddy_diff_coeff_1_2() / ((layer_depth_1() + layer_depth_2()) / 2)
    )


@component.add(
    name="Layer Time Constant 2 3",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_3": 2, "layer_depth_2": 1, "eddy_diff_coeff_2_3": 1},
)
def layer_time_constant_2_3():
    """
    Time constant of exchange between the second and the third ocean layers.
    """
    return layer_depth_3() / (
        eddy_diff_coeff_2_3() / ((layer_depth_2() + layer_depth_3()) / 2)
    )


@component.add(
    name="Layer Time Constant 3 4",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_4": 2, "layer_depth_3": 1, "eddy_diff_coeff_3_4": 1},
)
def layer_time_constant_3_4():
    """
    Time constant of exchange between the third and the fourth ocean layers.
    """
    return layer_depth_4() / (
        eddy_diff_coeff_3_4() / ((layer_depth_3() + layer_depth_4()) / 2)
    )


@component.add(
    name="Layer Time Constant M 1",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_1": 2, "mixed_layer_depth": 1, "eddy_diff_coeff_m_1": 1},
)
def layer_time_constant_m_1():
    """
    Time constant of exchange between mixed and the first ocean layers.
    """
    return layer_depth_1() / (
        eddy_diff_coeff_m_1() / ((mixed_layer_depth() + layer_depth_1()) / 2)
    )


@component.add(
    name="Mean Depth of Adjacent 1 2 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_1": 1, "layer_depth_2": 1},
)
def mean_depth_of_adjacent_1_2_layers():
    """
    Mean depth of the first and the second ocean layers.
    """
    return (layer_depth_1() + layer_depth_2()) / 2


@component.add(
    name="Mean Depth of Adjacent 2 3 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_2": 1, "layer_depth_3": 1},
)
def mean_depth_of_adjacent_2_3_layers():
    """
    Mean depth of the second and the third ocean layers.
    """
    return (layer_depth_2() + layer_depth_3()) / 2


@component.add(
    name="Mean Depth of Adjacent 3 4 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_3": 1, "layer_depth_4": 1},
)
def mean_depth_of_adjacent_3_4_layers():
    """
    Mean depth of the third and the fourth ocean layers.
    """
    return (layer_depth_3() + layer_depth_4()) / 2


@component.add(
    name="Mean Depth of Adjacent M 1 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mixed_layer_depth": 1, "layer_depth_1": 1},
)
def mean_depth_of_adjacent_m_1_layers():
    """
    Mean depth of mixed and the first ocean layers.
    """
    return (mixed_layer_depth() + layer_depth_1()) / 2


@component.add(
    name="Mixed Layer Depth", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def mixed_layer_depth():
    """
    Mixed ocean layer depth.
    """
    return 100


@component.add(
    name="Mixing Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def mixing_time():
    """
    Atmosphere - mixed ocean layer mixing time.
    """
    return 1


@component.add(
    name="Molar mass of C", units="gC/mol", comp_type="Constant", comp_subtype="Normal"
)
def molar_mass_of_c():
    return 12.01


@component.add(
    name="Molar mass of CH4",
    units="gCH4/mol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def molar_mass_of_ch4():
    return 16.04


@component.add(
    name="Molar mass of N2O",
    units="gN2O/mol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def molar_mass_of_n2o():
    return 44.013


@component.add(
    name="N2O Concentration Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atmosphere": 1, "init_n2o_in_atmosphere": 1},
)
def n2o_concentration_ratio():
    return n2o_in_atmosphere() / init_n2o_in_atmosphere()


@component.add(
    name="N2O in Atmosphere",
    units="TonN2O",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_n2o_in_atmosphere": 1},
    other_deps={
        "_integ_n2o_in_atmosphere": {
            "initial": {"init_n2o_in_atmosphere": 1},
            "step": {"total_n2o_emission": 1, "total_n2o_breakdown": 1},
        }
    },
)
def n2o_in_atmosphere():
    return _integ_n2o_in_atmosphere()


_integ_n2o_in_atmosphere = Integ(
    lambda: total_n2o_emission() - total_n2o_breakdown(),
    lambda: init_n2o_in_atmosphere(),
    "_integ_n2o_in_atmosphere",
)


@component.add(
    name="N2O para1",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_n2o_lifetime_parameter": 1,
        "effect_of_atmospheric_n2o_on_para1": 1,
        "n2o_in_atmosphere": 1,
        "tonn2o_to_mtonn2o": 1,
    },
)
def n2o_para1():
    return (
        baseline_n2o_lifetime_parameter()
        + effect_of_atmospheric_n2o_on_para1()
        / tonn2o_to_mtonn2o()
        * n2o_in_atmosphere()
    )


@component.add(
    name="N2O para2", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def n2o_para2():
    return 0.2


@component.add(
    name="N2O para3", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def n2o_para3():
    """
    FRIDA: 25.4953
    """
    return 34.9843


@component.add(
    name="Natural CH4 Emissions Flux Biosphere to CH4 Natural",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"flux_biomass_to_ch4": 1, "flux_humus_to_ch4": 1, "c_to_ch4": 1},
)
def natural_ch4_emissions_flux_biosphere_to_ch4_natural():
    return (flux_biomass_to_ch4() + flux_humus_to_ch4()) * c_to_ch4()


@component.add(
    name="Natural N2O Emission",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_natural_flux": 1,
        "effect_of_warming_on_n2o_release_from_biological_activity": 1,
    },
)
def natural_n2o_emission():
    return (
        baseline_natural_flux()
        * effect_of_warming_on_n2o_release_from_biological_activity()
    )


@component.add(
    name="Other Concentration Effects",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_concentration_effects():
    """
    This effect broughtly represents other gases in the atmosphere that are not modelled endogenously
    """
    return -0.198563


@component.add(
    name="Outflow CCSICLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_change_lv1": 1, "delay_time_ccsic": 1},
)
def outflow_ccsiclv1():
    return ccs_improvement_change_lv1() / delay_time_ccsic()


@component.add(
    name="Outflow CCSICLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_change_lv2": 1, "delay_time_ccsic": 1},
)
def outflow_ccsiclv2():
    return ccs_improvement_change_lv2() / delay_time_ccsic()


@component.add(
    name="Outflow CCSICLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_change_lv3": 1, "delay_time_ccsic": 1},
)
def outflow_ccsiclv3():
    return ccs_improvement_change_lv3() / delay_time_ccsic()


@component.add(name="ppb", units="ppb", comp_type="Constant", comp_subtype="Normal")
def ppb():
    return 1000000000.0


@component.add(
    name="ppm to GtC", units="GtC/ppm", comp_type="Constant", comp_subtype="Normal"
)
def ppm_to_gtc():
    """
    1 ppm by volume of atmosphere CO2 equals 2.13 GtC
    """
    return 2.13


@component.add(
    name="Preindustrial C in Atmosphere",
    units="TonC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def preindustrial_c_in_atmosphere():
    """
    Preindustrial carbon content of atmosphere.
    """
    return 590000000000.0


@component.add(
    name="Preindustrial C in Mixed Layer",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"preindustrial_ocean_c_per_meter": 1, "mixed_layer_depth": 1},
)
def preindustrial_c_in_mixed_layer():
    """
    Initial carbon content of mixed ocean layer.
    """
    return preindustrial_ocean_c_per_meter() * mixed_layer_depth()


@component.add(
    name="Preindustrial Ocean C per meter",
    units="TonC/m",
    comp_type="Constant",
    comp_subtype="Normal",
)
def preindustrial_ocean_c_per_meter():
    """
    Preindustrial carbon content in ocean per meter.
    """
    return 9000000000.0


@component.add(
    name="Pressure CCSIC",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "presure_to_adjust_total_c_emission_from_fossil_fuels": 1,
        "effectiveness_of_pressure_to_adjust_c_emission": 1,
    },
)
def pressure_ccsic():
    return (
        presure_to_adjust_total_c_emission_from_fossil_fuels()
        * effectiveness_of_pressure_to_adjust_c_emission()
    )


@component.add(
    name="Ref Buffer Factor", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def ref_buffer_factor():
    """
    Normal buffer factor.
    """
    return 9.7


@component.add(
    name="Reference CO2 Removal Rate",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_co2_removal_rate():
    return 37000000.0


@component.add(
    name="Scale Factor of CH4 lifetime",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_lifetime_factor_from_atmospheric_concentrations": 1,
        "ch4_lifetime_factor_from_temperature_change": 1,
    },
)
def scale_factor_of_ch4_lifetime():
    """
    Formulation based on FaIRv2 and FRIDA
    """
    return float(
        np.exp(
            ch4_lifetime_factor_from_atmospheric_concentrations()
            + ch4_lifetime_factor_from_temperature_change()
        )
    )


@component.add(
    name="Scale Factor of N2O Lifetime",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_para2": 1, "n2o_para1": 1, "n2o_para3": 1},
)
def scale_factor_of_n2o_lifetime():
    return n2o_para2() * float(np.exp(n2o_para1() / n2o_para3()))


@component.add(
    name="Sensitivity of C flux to temp",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_c_flux_to_temp():
    return 0.003


@component.add(
    name="Terrestrial carbon sink",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"flux_atmosphere_to_biomass": 1, "flux_biomass_to_atmosphere": 1},
)
def terrestrial_carbon_sink():
    return flux_atmosphere_to_biomass() - flux_biomass_to_atmosphere()


@component.add(
    name="Ton to G CH4",
    units="gCH4/TonCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_to_g_ch4():
    return 1000000.0


@component.add(
    name="Ton to g N2O",
    units="gN2O/TonN2O",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_to_g_n2o():
    return 1000000.0


@component.add(
    name="TonCH4 to ppb",
    units="ppb/TonCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ppb": 1,
        "ton_to_g_ch4": 1,
        "molar_mass_of_ch4": 1,
        "total_moles_of_air_in_atmosphere": 1,
    },
)
def tonch4_to_ppb():
    return (
        ppb()
        * ton_to_g_ch4()
        / molar_mass_of_ch4()
        / total_moles_of_air_in_atmosphere()
    )


@component.add(
    name="TonN2O to MTonN2O",
    units="TonN2O/MTonN2O",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tonn2o_to_mtonn2o():
    return 1000000.0


@component.add(
    name="TonN2O to ppb",
    units="ppb/TonN2O",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ppb": 1,
        "ton_to_g_n2o": 1,
        "molar_mass_of_n2o": 1,
        "total_moles_of_air_in_atmosphere": 1,
    },
)
def tonn2o_to_ppb():
    return (
        ppb()
        * ton_to_g_n2o()
        / molar_mass_of_n2o()
        / total_moles_of_air_in_atmosphere()
    )


@component.add(
    name="Total C Emission",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_anthropogenic_co2_emissions_energy_in_tonc": 1},
)
def total_c_emission():
    """
    Emissions of carbon from energy use and other sources.
    """
    return total_anthropogenic_co2_emissions_energy_in_tonc()


@component.add(
    name="Total CH4 Breakdown",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atmosphere": 1, "atmospheric_lifetime_of_ch4": 1},
)
def total_ch4_breakdown():
    """
    Oxidation Losses
    """
    return ch4_in_atmosphere() / atmospheric_lifetime_of_ch4()


@component.add(
    name="Total CH4 Emission",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_anthropogenic_ch4_emissions": 1,
        "natural_ch4_emissions_flux_biosphere_to_ch4_natural": 1,
    },
)
def total_ch4_emission():
    return (
        total_anthropogenic_ch4_emissions()
        + natural_ch4_emissions_flux_biosphere_to_ch4_natural()
    )


@component.add(
    name="Total moles of air in atmosphere",
    units="mol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_moles_of_air_in_atmosphere():
    return 1.77e20


@component.add(
    name="Total N2O Breakdown",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atmosphere": 1, "atmospheric_lifetime_of_n2o": 1},
)
def total_n2o_breakdown():
    return n2o_in_atmosphere() / atmospheric_lifetime_of_n2o()


@component.add(
    name="Total N2O Emission",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_anthropogenic_n2o_emissions": 1, "natural_n2o_emission": 1},
)
def total_n2o_emission():
    return total_anthropogenic_n2o_emissions() + natural_n2o_emission()
