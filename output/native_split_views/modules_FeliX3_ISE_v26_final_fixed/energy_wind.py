"""
Module energy_wind
Translated using PySD version 3.14.3
"""

@component.add(
    name="Average Installed Power Density Wind",
    units="kW/(m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_installed_power_density_wind():
    """
    Average wind energy production from one sqr meter of wind installed capacity. Assuming 93% onshore, 7% offshore, 19.1 W/m2 https://doi.org/10.1016/j.esd.2020.11.004 POssible linked to the scenario "Variable3 Wind"
    """
    return 0.0191


@component.add(
    name="Cumulative Wind Energy Produced",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_wind_energy_produced": 1},
    other_deps={
        "_integ_cumulative_wind_energy_produced": {
            "initial": {"init_cumulative_wind_produced": 1},
            "step": {"wind_energy_production": 1},
        }
    },
)
def cumulative_wind_energy_produced():
    """
    Cumulative wind energy that has been produced.
    """
    return _integ_cumulative_wind_energy_produced()


_integ_cumulative_wind_energy_produced = Integ(
    lambda: wind_energy_production(),
    lambda: init_cumulative_wind_produced(),
    "_integ_cumulative_wind_energy_produced",
)


@component.add(
    name="Delay Time IWETR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_technology_development_time": 1},
)
def delay_time_iwetr():
    return wind_energy_technology_development_time() / 3


@component.add(
    name="Delay Time IWIR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installation_technology_development_time": 1},
)
def delay_time_iwir():
    return wind_installation_technology_development_time() / 3


@component.add(
    name="Desired Wind Energy Gross Margin",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_wind_energy_gross_margin():
    """
    Desired Gross Margin per unit of wind energy.
    """
    return 0.2


@component.add(
    name="Desired Wind Installed Capacity",
    units="m*m",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_wind_demand": 1, "efficiency_of_wind_installed_capacity": 1},
)
def desired_wind_installed_capacity():
    """
    Desired Wind Installed Capacity accounting for Total Wind Demand and Efficiency of Wind Installed Capacity.
    """
    return total_wind_demand() / efficiency_of_wind_installed_capacity()


@component.add(
    name="Effect of Wind Energy Demand and Supply on Price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_wind_demand": 1,
        "potential_wind_energy_production": 1,
        "sensitivity_of_wind_energy_price_to_supply_and_demand": 1,
    },
)
def effect_of_wind_energy_demand_and_supply_on_price():
    """
    Effect of Wind Demand and Supply ratio on actual wind energy price.
    """
    return (
        total_wind_demand() / potential_wind_energy_production()
    ) ** sensitivity_of_wind_energy_price_to_supply_and_demand()


@component.add(
    name="Effectiveness IWETR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_efficiency": 1,
        "effectiveness_of_investment_in_wind_energy_technology": 1,
    },
)
def effectiveness_iwetr():
    return (
        investment_in_wind_energy_efficiency()
        * effectiveness_of_investment_in_wind_energy_technology()
    )


@component.add(
    name="Effectiveness IWITR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_installation": 1,
        "effectiveness_of_investment_in_wind_installation_technology": 1,
    },
)
def effectiveness_iwitr():
    return (
        investment_in_wind_energy_installation()
        * effectiveness_of_investment_in_wind_installation_technology()
    )


@component.add(
    name="Effectiveness of Investment in Wind Energy Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_energy_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_wind_energy_technology():
    """
    Effectivenes of resources dedicated to wind conversion efficiency technology development.
    """
    return 1e-09 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_energy_technology_variation() - 1e-09,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Wind Installation Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_installation_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_wind_installation_technology():
    """
    Effectiveness of resources dedicated to wind energy capacity efficiency technology development.
    """
    return 1e-10 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_installation_technology_variation()
        - 1e-10,
        2020,
    )


@component.add(
    name="Efficiency of Wind Installed Capacity",
    units="Mtoe/(Year*m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_wind_energy_production": 1, "wind_installed_capacity": 1},
)
def efficiency_of_wind_installed_capacity():
    """
    Total production efficiency of Wind Installed Capacity for given technology developments.
    """
    return zidz(potential_wind_energy_production(), wind_installed_capacity())


@component.add(
    name="Financial Capex Wind",
    units="$2024/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"financial_capex_wind_per_kwh": 1, "kwh_into_mtoe": 1},
)
def financial_capex_wind():
    return financial_capex_wind_per_kwh() / kwh_into_mtoe()


@component.add(
    name="Financial Capex Wind per kW",
    units="$2024/kW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "financial_capex_wind_per_kwh": 1,
        "hours_per_year": 1,
        "wind_aging_time": 1,
        "wind_capacity_factor": 1,
    },
)
def financial_capex_wind_per_kw():
    return (
        financial_capex_wind_per_kwh()
        * hours_per_year()
        * wind_aging_time()
        * wind_capacity_factor()
    )


@component.add(
    name="Financial Capex Wind per kWh",
    units="$2024/(kW*Hour)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def financial_capex_wind_per_kwh():
    return 0.0225


@component.add(
    name="Fraction Invested in Wind Energy Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installation_efficiency": 1, "table_for_fiwei": 1},
)
def fraction_invested_in_wind_energy_installation():
    """
    Fraction of investments in wind energy technology dedicated to capacity.
    """
    return table_for_fiwei(wind_installation_efficiency())


@component.add(
    name="Fraction of Revenue Invested in Wind Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_investment_fraction_slope": 1,
        "wind_investment_fraction_start": 1,
        "wind_investment_fraction_finish": 1,
        "time": 1,
    },
)
def fraction_of_revenue_invested_in_wind_technology():
    """
    Parameter to take into account historical increase of the wind energy significance and over time greater resources dedicated to the technology development.
    """
    return ramp(
        __data["time"],
        wind_investment_fraction_slope(),
        wind_investment_fraction_start(),
        wind_investment_fraction_finish(),
    )


@component.add(
    name="Impact of Learning on Wind Capex",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ratio_wind_installed_capacity": 1, "wind_learning_curve_strength": 1},
)
def impact_of_learning_on_wind_capex():
    return ratio_wind_installed_capacity() ** wind_learning_curve_strength()


@component.add(
    name="Impact of Learning on Wind Opex",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ratio_wind_installed_capacity": 1, "wind_opex_learning_rate": 1},
)
def impact_of_learning_on_wind_opex():
    return ratio_wind_installed_capacity() ** -wind_opex_learning_rate()


@component.add(
    name="Impact of Space on Wind Capacity Installation",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installed_capacity": 1, "wind_available_area": 1},
)
def impact_of_space_on_wind_capacity_installation():
    """
    Ratio of currently installed wind capacity to total possible.
    """
    return float(np.maximum(0, 1 - wind_installed_capacity() / wind_available_area()))


@component.add(
    name="Increase in Wind Energy Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwetrlv3": 1},
)
def increase_in_wind_energy_technology_ratio():
    """
    Increase in Wind Energy Technology Ratio due to investments in wind conversion efficiency technology and their productivity.
    """
    return outflow_iwetrlv3()


@component.add(
    name="Increase in Wind Energy Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_energy_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_wind_energy_technology_ratio_lv1": {
            "initial": {"increase_in_wind_energy_technology_ratio_lv3": 1},
            "step": {"inflow_iwetrlv1": 1, "outflow_iwetrlv1": 1},
        }
    },
)
def increase_in_wind_energy_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_energy_technology_ratio_lv1()


_integ_increase_in_wind_energy_technology_ratio_lv1 = Integ(
    lambda: inflow_iwetrlv1() - outflow_iwetrlv1(),
    lambda: increase_in_wind_energy_technology_ratio_lv3(),
    "_integ_increase_in_wind_energy_technology_ratio_lv1",
)


@component.add(
    name="Increase in Wind Energy Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_energy_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_wind_energy_technology_ratio_lv2": {
            "initial": {"increase_in_wind_energy_technology_ratio_lv3": 1},
            "step": {"inflow_iwetrlv2": 1, "outflow_iwetrlv2": 1},
        }
    },
)
def increase_in_wind_energy_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_energy_technology_ratio_lv2()


_integ_increase_in_wind_energy_technology_ratio_lv2 = Integ(
    lambda: inflow_iwetrlv2() - outflow_iwetrlv2(),
    lambda: increase_in_wind_energy_technology_ratio_lv3(),
    "_integ_increase_in_wind_energy_technology_ratio_lv2",
)


@component.add(
    name="Increase in Wind Energy Technology Ratio LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_energy_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_wind_energy_technology_ratio_lv3": {
            "initial": {"effectiveness_iwetr": 1, "delay_time_iwetr": 1},
            "step": {"inflow_iwetrlv3": 1, "outflow_iwetrlv3": 1},
        }
    },
)
def increase_in_wind_energy_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_energy_technology_ratio_lv3()


_integ_increase_in_wind_energy_technology_ratio_lv3 = Integ(
    lambda: inflow_iwetrlv3() - outflow_iwetrlv3(),
    lambda: effectiveness_iwetr() * delay_time_iwetr(),
    "_integ_increase_in_wind_energy_technology_ratio_lv3",
)


@component.add(
    name="Increase in Wind Installation Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwitrlv3": 1},
)
def increase_in_wind_installation_technology_ratio():
    """
    Increase in Wind Installation Technology Ratio due to investments in wind energy installation capacity.
    """
    return outflow_iwitrlv3()


@component.add(
    name="Increase in Wind Installation Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_installation_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_wind_installation_technology_ratio_lv1": {
            "initial": {"increase_in_wind_installation_technology_ratio_lv3": 1},
            "step": {"inflow_iwitrlv1": 1, "outflow_iwitrlv1": 1},
        }
    },
)
def increase_in_wind_installation_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_installation_technology_ratio_lv1()


_integ_increase_in_wind_installation_technology_ratio_lv1 = Integ(
    lambda: inflow_iwitrlv1() - outflow_iwitrlv1(),
    lambda: increase_in_wind_installation_technology_ratio_lv3(),
    "_integ_increase_in_wind_installation_technology_ratio_lv1",
)


@component.add(
    name="Increase in Wind Installation Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_installation_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_wind_installation_technology_ratio_lv2": {
            "initial": {"increase_in_wind_installation_technology_ratio_lv3": 1},
            "step": {"inflow_iwitrlv2": 1, "ourflow_iwitrlv2": 1},
        }
    },
)
def increase_in_wind_installation_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_installation_technology_ratio_lv2()


_integ_increase_in_wind_installation_technology_ratio_lv2 = Integ(
    lambda: inflow_iwitrlv2() - ourflow_iwitrlv2(),
    lambda: increase_in_wind_installation_technology_ratio_lv3(),
    "_integ_increase_in_wind_installation_technology_ratio_lv2",
)


@component.add(
    name="Increase in Wind Installation Technology Ratio LV3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_installation_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_wind_installation_technology_ratio_lv3": {
            "initial": {"effectiveness_iwitr": 1, "delay_time_iwir": 1},
            "step": {"inflow_iwitrlv3": 1, "outflow_iwitrlv3": 1},
        }
    },
)
def increase_in_wind_installation_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_installation_technology_ratio_lv3()


_integ_increase_in_wind_installation_technology_ratio_lv3 = Integ(
    lambda: inflow_iwitrlv3() - outflow_iwitrlv3(),
    lambda: effectiveness_iwitr() * delay_time_iwir(),
    "_integ_increase_in_wind_installation_technology_ratio_lv3",
)


@component.add(
    name="Indicated Wind Energy Price",
    units="$2024/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_lcoe": 1, "desired_wind_energy_gross_margin": 1},
)
def indicated_wind_energy_price():
    """
    Indicated wind energy price accounting for unit cost and gross margin.
    """
    return wind_lcoe() * (1 + desired_wind_energy_gross_margin())


@component.add(
    name="Inflow IWETRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_iwetr": 1},
)
def inflow_iwetrlv1():
    return effectiveness_iwetr()


@component.add(
    name="Inflow IWETRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwetrlv1": 1},
)
def inflow_iwetrlv2():
    return outflow_iwetrlv1()


@component.add(
    name="Inflow IWETRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwetrlv2": 1},
)
def inflow_iwetrlv3():
    return outflow_iwetrlv2()


@component.add(
    name="Inflow IWITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_iwitr": 1},
)
def inflow_iwitrlv1():
    return effectiveness_iwitr()


@component.add(
    name="Inflow IWITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwitrlv1": 1},
)
def inflow_iwitrlv2():
    return outflow_iwitrlv1()


@component.add(
    name="Inflow IWITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ourflow_iwitrlv2": 1},
)
def inflow_iwitrlv3():
    return ourflow_iwitrlv2()


@component.add(
    name="INIT Cumulative Wind Produced", comp_type="Constant", comp_subtype="Normal"
)
def init_cumulative_wind_produced():
    return 0


@component.add(
    name="INIT WETRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_wetrn():
    """
    Initial Wind Energy Technology Ratio.
    """
    return 0


@component.add(
    name="INIT WIC", units="m*m", comp_type="Constant", comp_subtype="Normal"
)
def init_wic():
    """
    Initial installed capacity to transform wind into energy.
    """
    return 4000


@component.add(
    name="INIT Wind Capex",
    units="$2024/kW",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_wind_capex():
    """
    Initial unit cost per unit wind capacity installation.5500 IN 1983, 2200 IN 2000
    """
    return 5500


@component.add(
    name="INIT Wind Energy Technology Development Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_wind_energy_technology_development_time():
    return 100


@component.add(
    name="INIT Wind Installation Technology Development Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_wind_installation_technology_development_time():
    return 75


@component.add(
    name="INIT Wind Learning Rate",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_wind_learning_rate():
    return 0.2


@component.add(
    name="INIT WITRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_witrn():
    """
    Initial Wind Installation Technology Ratio.
    """
    return 0


@component.add(
    name="Installation of Wind Capacity Rate",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_wind_capacity_installation": 1,
        "wind_infrastructure_adjustment": 1,
    },
)
def installation_of_wind_capacity_rate():
    """
    Rate of new wind capacity installation.
    """
    return (
        productivity_of_investment_in_wind_capacity_installation()
        * wind_infrastructure_adjustment()
    )


@component.add(
    name="Interest rate for LCOE calculations",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def interest_rate_for_lcoe_calculations():
    return 0.08


@component.add(
    name="Investment in Wind Capacity",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installation_of_wind_capacity_rate": 1,
        "average_installed_power_density_wind": 1,
        "wind_capex": 1,
        "financial_capex_wind_per_kw": 1,
        "gdp_deflator_usd2005": 1,
    },
)
def investment_in_wind_capacity():
    """
    Amount of resources dedicated to wind energy capacity development.
    """
    return (
        installation_of_wind_capacity_rate()
        * average_installed_power_density_wind()
        * (wind_capex() + financial_capex_wind_per_kw())
        / gdp_deflator_usd2005()
    )


@component.add(
    name="Investment in Wind Energy Efficiency",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_technology": 1,
        "fraction_invested_in_wind_energy_installation": 1,
    },
)
def investment_in_wind_energy_efficiency():
    """
    Total investments in wind conversion efficiency technology.
    """
    return investment_in_wind_energy_technology() * (
        1 - fraction_invested_in_wind_energy_installation()
    )


@component.add(
    name="Investment in Wind Energy Installation",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_technology": 1,
        "fraction_invested_in_wind_energy_installation": 1,
    },
)
def investment_in_wind_energy_installation():
    """
    Total investments in wind energy capacity.
    """
    return (
        investment_in_wind_energy_technology()
        * fraction_invested_in_wind_energy_installation()
    )


@component.add(
    name="Investment in Wind Energy Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_revenue_invested_in_wind_technology": 1,
        "wind_energy_revenue": 1,
        "gdp_deflator_usd2005": 1,
    },
)
def investment_in_wind_energy_technology():
    """
    Investments in development of wind conversion efficiency technology and production capability.
    """
    return (
        fraction_of_revenue_invested_in_wind_technology()
        * wind_energy_revenue()
        / gdp_deflator_usd2005()
    )


@component.add(
    name="kW into TW", units="kW/TW", comp_type="Constant", comp_subtype="Normal"
)
def kw_into_tw():
    """
    Coefficient to convert kilowatts into terawatts.
    """
    return 10000000000.0


@component.add(
    name="kW to MW", units="MW/kW", comp_type="Constant", comp_subtype="Normal"
)
def kw_to_mw():
    return 0.001


@component.add(
    name="Max Wind Power Point",
    units="kW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_installed_capacity": 1,
        "average_installed_power_density_wind": 1,
        "wind_capacity_factor": 1,
    },
)
def max_wind_power_point():
    """
    Max Power Point measured at Standard Test Conditions for installed wind energy production capacity and current wind conversion efficiency.
    """
    return (
        wind_installed_capacity()
        * average_installed_power_density_wind()
        * wind_capacity_factor()
    )


@component.add(
    name="Max Wind Power Point GW",
    units="GW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_wind_power_point": 1, "kw_into_gw": 1},
)
def max_wind_power_point_gw():
    """
    Wind Max Power Point measured in GW.
    """
    return max_wind_power_point() / kw_into_gw()


@component.add(
    name="Max Wind Power Point TW",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_wind_power_point": 1, "kw_into_tw": 1},
)
def max_wind_power_point_tw():
    """
    Wind Max Power Point measured in TW.
    """
    return max_wind_power_point() / kw_into_tw()


@component.add(name="MAXWCF", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxwcf():
    """
    Maximal wind capacity factor.
    """
    return 0.5


@component.add(name="MAXWIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxwie():
    """
    Maximal value of Wind Installation Efficiency factor.
    """
    return 1


@component.add(name="MINWCF", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minwcf():
    """
    Minimal and initial wind capacity factor.
    """
    return 0.18


@component.add(name="MINWIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minwie():
    """
    Minimal and initial value of Wind Installation Efficiency factor.
    """
    return 0.01


@component.add(
    name="Ourflow IWITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_installation_technology_ratio_lv2": 1,
        "delay_time_iwir": 1,
    },
)
def ourflow_iwitrlv2():
    return increase_in_wind_installation_technology_ratio_lv2() / delay_time_iwir()


@component.add(
    name="Outflow IWETRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_energy_technology_ratio_lv1": 1,
        "delay_time_iwetr": 1,
    },
)
def outflow_iwetrlv1():
    return increase_in_wind_energy_technology_ratio_lv1() / delay_time_iwetr()


@component.add(
    name="Outflow IWETRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_energy_technology_ratio_lv2": 1,
        "delay_time_iwetr": 1,
    },
)
def outflow_iwetrlv2():
    return increase_in_wind_energy_technology_ratio_lv2() / delay_time_iwetr()


@component.add(
    name="Outflow IWETRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_energy_technology_ratio_lv3": 1,
        "delay_time_iwetr": 1,
    },
)
def outflow_iwetrlv3():
    return increase_in_wind_energy_technology_ratio_lv3() / delay_time_iwetr()


@component.add(
    name="Outflow IWITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_installation_technology_ratio_lv1": 1,
        "delay_time_iwir": 1,
    },
)
def outflow_iwitrlv1():
    return increase_in_wind_installation_technology_ratio_lv1() / delay_time_iwir()


@component.add(
    name="Outflow IWITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_installation_technology_ratio_lv3": 1,
        "delay_time_iwir": 1,
    },
)
def outflow_iwitrlv3():
    return increase_in_wind_installation_technology_ratio_lv3() / delay_time_iwir()


@component.add(
    name="Potential Wind Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_installed_capacity": 1,
        "average_installed_power_density_wind": 1,
        "wind_capacity_factor": 1,
        "hours_per_year": 1,
        "kwh_into_mtoe": 1,
    },
)
def potential_wind_energy_production():
    """
    Potential solar energy production per year due to available production capability and technical developments.
    """
    return (
        wind_installed_capacity()
        * average_installed_power_density_wind()
        * wind_capacity_factor()
        * hours_per_year()
        * kwh_into_mtoe()
    )


@component.add(
    name="Productivity of Investment in Wind Capacity Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "impact_of_space_on_wind_capacity_installation": 1,
        "wind_installation_efficiency": 1,
    },
)
def productivity_of_investment_in_wind_capacity_installation():
    """
    Productivity of wind capacity installation taking into account the level of remaining possible capacities and technology development state.
    """
    return (
        impact_of_space_on_wind_capacity_installation() * wind_installation_efficiency()
    )


@component.add(
    name="Ratio Wind Installed Capacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installed_capacity_mw": 1, "wind_threshold_capacity": 1},
)
def ratio_wind_installed_capacity():
    return wind_installed_capacity_mw() / wind_threshold_capacity()


@component.add(
    name="Reference Wind Opex",
    units="$2024/(kW*Hour)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_wind_opex():
    """
    $35/MWh for projects built in the late 1990s to a level approaching $11/MWh for projects built in 2018.https://emp.lbl.gov/news/wind-experts-report-average-operating
    """
    return 0.035


@component.add(
    name="Sensitivity of Wind Energy Price to Supply and Demand",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_wind_energy_price_to_supply_and_demand():
    """
    Sensitivity of Wind Energy Price to Supply and Demand ratio.
    """
    return 0


@component.add(
    name="Table for FIWEI",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_fiwei"},
)
def table_for_fiwei(x, final_subs=None):
    """
    Table determining order by which technology investments are dedicated to energy and installation efficiency. For small Wind Installation Efficiency, in order to secure sufficient production capacity, more investments are directed to infrastructure. Once the Wind Installation Efficiency increases the investments are redirected to solar conversion efficiency technologies.
    """
    return _hardcodedlookup_table_for_fiwei(x, final_subs)


_hardcodedlookup_table_for_fiwei = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    [0.8, 0.8, 0.7, 0.5, 0.2, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_fiwei",
)


@component.add(
    name="Time to Adjust Wind Infrastructure",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_adjust_wind_infrastructure():
    """
    Time to adjust Wind Infrastructure to the desired level.
    """
    return 2.75


@component.add(
    name="Total Wind Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "market_share_wind": 1},
)
def total_wind_demand():
    """
    Total demand for wind energy.
    """
    return energy_demand() * market_share_wind()


@component.add(
    name="Total Wind Demand GW",
    units="GW/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_wind_demand": 1, "kwh_into_mtoe_peak_hour": 1, "kw_into_gw": 1},
)
def total_wind_demand_gw():
    """
    Total demand for wind energy measured in GW.
    """
    return total_wind_demand() / kwh_into_mtoe_peak_hour() / kw_into_gw()


@component.add(
    name="Unit Cost of Wind Capacity Installation Mtoe",
    units="$2024/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_cost_of_wind_capacity_installation_per_kwh": 1,
        "kwh_into_mtoe": 1,
    },
)
def unit_cost_of_wind_capacity_installation_mtoe():
    return unit_cost_of_wind_capacity_installation_per_kwh() / kwh_into_mtoe()


@component.add(
    name="Unit Cost of Wind Capacity Installation per kWh",
    units="$2024/(kW*Hour)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_capex": 1,
        "wind_capital_recovery_factor": 1,
        "wind_capacity_factor": 1,
        "hours_per_year": 1,
    },
)
def unit_cost_of_wind_capacity_installation_per_kwh():
    return (
        wind_capex()
        * wind_capital_recovery_factor()
        / (hours_per_year() * wind_capacity_factor())
    )


@component.add(
    name="Wind Aging Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def wind_aging_time():
    """
    Average wind energy production capacity aging time.
    """
    return 25


@component.add(
    name="Wind Available Area",
    units="m*m",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_available_area_variation": 1, "time": 1},
)
def wind_available_area():
    """
    Total area available for wind energy production capacities.
    """
    return 8000000000000.0 + step(
        __data["time"], wind_available_area_variation() - 8000000000000.0, 2020
    )


@component.add(
    name="Wind Available Area Variation",
    units="m*m",
    comp_type="Constant",
    comp_subtype="Normal",
)
def wind_available_area_variation():
    """
    Total area available for wind energy production capacities.
    """
    return 8000000000000.0


@component.add(
    name="Wind Capacity Aging Rate",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installed_capacity": 1, "wind_aging_time": 1},
)
def wind_capacity_aging_rate():
    """
    Aging rate of wind energy production capacities.
    """
    return wind_installed_capacity() / wind_aging_time()


@component.add(
    name="Wind Capacity Factor",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minwcf": 2, "maxwcf": 1, "wind_energy_technology_ratio": 2},
)
def wind_capacity_factor():
    """
    Parameter indicating what fraction of average wind capacity per sqr meter it is possible to realize with the current state of technical developments.
    """
    return minwcf() + (maxwcf() - minwcf()) * (
        wind_energy_technology_ratio() / (wind_energy_technology_ratio() + 1)
    )


@component.add(
    name="Wind Capex",
    units="$2024/kW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"impact_of_learning_on_wind_capex": 1, "init_wind_capex": 1},
)
def wind_capex():
    """
    In 2024$, pre-2010 data is the US national avergage, post- is global
    """
    return impact_of_learning_on_wind_capex() * init_wind_capex()


@component.add(
    name="Wind Capital Recovery Factor",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"interest_rate_for_lcoe_calculations": 3, "wind_aging_time": 2},
)
def wind_capital_recovery_factor():
    return (
        interest_rate_for_lcoe_calculations()
        * (1 + interest_rate_for_lcoe_calculations()) ** wind_aging_time()
    ) / ((1 + interest_rate_for_lcoe_calculations()) ** wind_aging_time() - 1)


@component.add(
    name="Wind Energy Demand to Supply Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_wind_demand": 1, "potential_wind_energy_production": 1},
)
def wind_energy_demand_to_supply_ratio():
    """
    Wind Energy Demand to Supply Ratio.
    """
    return total_wind_demand() / potential_wind_energy_production()


@component.add(
    name="Wind Energy Price",
    units="$2024/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_wind_energy_price": 1,
        "effect_of_wind_energy_demand_and_supply_on_price": 1,
    },
)
def wind_energy_price():
    """
    Actual wind energy price accounting for indicated wind energy price and effect of demand and supply.
    """
    return (
        indicated_wind_energy_price()
        * effect_of_wind_energy_demand_and_supply_on_price()
    )


@component.add(
    name="Wind Energy Price per kWh",
    units="$/(kW*Hour)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_price": 1, "kwh_into_mtoe": 1},
)
def wind_energy_price_per_kwh():
    """
    Actual wind energy price accounting for indicated wind energy price and effect of demand and supply measured in dollars per kWh.
    """
    return wind_energy_price() * kwh_into_mtoe()


@component.add(
    name="Wind Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production_rate": 1},
)
def wind_energy_production():
    """
    Total wind energy production per year.
    """
    return wind_energy_production_rate()


@component.add(
    name="Wind Energy Production GWh",
    units="GW*Hour/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production": 1, "kwh_into_mtoe": 1, "kw_into_gw": 1},
)
def wind_energy_production_gwh():
    return wind_energy_production() / kwh_into_mtoe() / kw_into_gw()


@component.add(
    name="Wind Energy Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production": 1, "mtoe_into_ej": 1},
)
def wind_energy_production_indicator():
    return wind_energy_production() * mtoe_into_ej()


@component.add(
    name="Wind Energy Production Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_wind_energy_production": 1, "total_wind_demand": 1},
)
def wind_energy_production_rate():
    """
    Total wind energy production per year accounting for demand and potential production due to available production capability and technical developments.
    """
    return float(np.minimum(potential_wind_energy_production(), total_wind_demand()))


@component.add(
    name="Wind Energy Revenue",
    units="$2024/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production": 1, "wind_energy_price": 1},
)
def wind_energy_revenue():
    """
    Total revenue in wind energy market.
    """
    return wind_energy_production() * wind_energy_price()


@component.add(
    name="Wind Energy Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_wind_energy_technology_development_time": 2,
        "renewable_energy_technology_development_time_variation": 1,
        "time": 1,
    },
)
def wind_energy_technology_development_time():
    """
    Average time required to turn investments into concrete wind conversion efficiency technology developments. Since the simulation starts in 1900 it is a significant time.
    """
    return init_wind_energy_technology_development_time() + step(
        __data["time"],
        renewable_energy_technology_development_time_variation()
        - init_wind_energy_technology_development_time(),
        2020,
    )


@component.add(
    name="Wind Energy Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_wind_energy_technology_ratio": 1},
    other_deps={
        "_integ_wind_energy_technology_ratio": {
            "initial": {"init_wetrn": 1},
            "step": {"increase_in_wind_energy_technology_ratio": 1},
        }
    },
)
def wind_energy_technology_ratio():
    """
    Wind Energy Technology Ratio increased due to investments in wind conversion efficiency.
    """
    return _integ_wind_energy_technology_ratio()


_integ_wind_energy_technology_ratio = Integ(
    lambda: increase_in_wind_energy_technology_ratio(),
    lambda: init_wetrn(),
    "_integ_wind_energy_technology_ratio",
)


@component.add(
    name="Wind Final Investment",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def wind_final_investment():
    """
    Eventual average level of investments in wind energy technology.
    """
    return 0.05


@component.add(
    name="Wind Infrastructure Adjustment",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_capacity_aging_rate": 1,
        "time_to_adjust_wind_infrastructure": 1,
        "wind_installed_capacity": 1,
        "desired_wind_installed_capacity": 1,
    },
)
def wind_infrastructure_adjustment():
    """
    Adjustment of Wind Infrastructure to the desired level over a specified adjustment time and accounting for constant infrastructure decrease due to aging process.
    """
    return (
        wind_capacity_aging_rate()
        + (desired_wind_installed_capacity() - wind_installed_capacity())
        / time_to_adjust_wind_infrastructure()
    )


@component.add(
    name="Wind Initial Investment",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def wind_initial_investment():
    """
    Initial level of fractional investments in wind energy technology.
    """
    return 0


@component.add(
    name="Wind Installation Efficiency",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minwie": 2, "wind_installation_technology_ratio": 2, "maxwie": 1},
)
def wind_installation_efficiency():
    """
    Parameter indicating wind energy capacity installation efficiency at the current state of technical developments.
    """
    return minwie() + (maxwie() - minwie()) * (
        wind_installation_technology_ratio()
        / (wind_installation_technology_ratio() + 1)
    )


@component.add(
    name="Wind Installation Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_wind_installation_technology_development_time": 2,
        "renewable_installation_technology_development_time_variation": 1,
        "time": 1,
    },
)
def wind_installation_technology_development_time():
    """
    Average time required to turn investments into concrete wind energy production capacity. Since the simulation starts in 1900 it is a significant time.
    """
    return init_wind_installation_technology_development_time() + step(
        __data["time"],
        renewable_installation_technology_development_time_variation()
        - init_wind_installation_technology_development_time(),
        2020,
    )


@component.add(
    name="Wind Installation Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_wind_installation_technology_ratio": 1},
    other_deps={
        "_integ_wind_installation_technology_ratio": {
            "initial": {"init_witrn": 1},
            "step": {"increase_in_wind_installation_technology_ratio": 1},
        }
    },
)
def wind_installation_technology_ratio():
    """
    Wind Installation Technology Ratio increased due to investments in wind energy capacity installation efficiency.
    """
    return _integ_wind_installation_technology_ratio()


_integ_wind_installation_technology_ratio = Integ(
    lambda: increase_in_wind_installation_technology_ratio(),
    lambda: init_witrn(),
    "_integ_wind_installation_technology_ratio",
)


@component.add(
    name="Wind Installed Capacity",
    units="m*m",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_wind_installed_capacity": 1},
    other_deps={
        "_integ_wind_installed_capacity": {
            "initial": {"init_wic": 1},
            "step": {
                "installation_of_wind_capacity_rate": 1,
                "wind_capacity_aging_rate": 1,
            },
        }
    },
)
def wind_installed_capacity():
    """
    Installed capacity to transform wind into energy.
    """
    return _integ_wind_installed_capacity()


_integ_wind_installed_capacity = Integ(
    lambda: installation_of_wind_capacity_rate() - wind_capacity_aging_rate(),
    lambda: init_wic(),
    "_integ_wind_installed_capacity",
)


@component.add(
    name="Wind Installed Capacity MW",
    units="MW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_installed_capacity": 1,
        "average_installed_power_density_wind": 1,
        "kw_to_mw": 1,
    },
)
def wind_installed_capacity_mw():
    return (
        wind_installed_capacity() * average_installed_power_density_wind() * kw_to_mw()
    )


@component.add(
    name="Wind Investment Fraction Finish",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1, "ramp_investment_period": 1},
)
def wind_investment_fraction_finish():
    """
    End of fractional investments in wind energy technology.
    """
    return initial_time() + ramp_investment_period()


@component.add(
    name="Wind Investment Fraction Slope",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_final_investment": 1,
        "wind_initial_investment": 1,
        "ramp_investment_period": 1,
    },
)
def wind_investment_fraction_slope():
    """
    Intensity of increase in investments in wind energy technology.
    """
    return (
        float(np.abs(wind_final_investment() - wind_initial_investment()))
        / ramp_investment_period()
    )


@component.add(
    name="Wind Investment Fraction Start",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1},
)
def wind_investment_fraction_start():
    """
    Start of investments in wind energy technology.
    """
    return initial_time()


@component.add(
    name="Wind LCOE",
    units="$2024/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_cost_of_wind_capacity_installation_mtoe": 1,
        "wind_opex_mtoe": 1,
        "financial_capex_wind": 1,
    },
)
def wind_lcoe():
    """
    Cost of wind energy production assuming an impact of learning curve. It excludes fixed O&M costs. in 2024 $.
    """
    return (
        unit_cost_of_wind_capacity_installation_mtoe()
        + wind_opex_mtoe()
        + financial_capex_wind()
    )


@component.add(
    name="Wind LCOE per kWh",
    units="$2024/(kW*Hour)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_lcoe": 1, "kwh_into_mtoe": 1},
)
def wind_lcoe_per_kwh():
    return wind_lcoe() * kwh_into_mtoe()


@component.add(
    name="Wind Learning Curve Strength",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_learning_rate": 1},
)
def wind_learning_curve_strength():
    """
    Strength of learning curve with which the wind energy costs are influenced.
    """
    return float(np.log(1 - wind_learning_rate())) / float(np.log(2))


@component.add(
    name="Wind Learning Rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_wind_learning_rate": 2,
        "fraction_for_wind_and_solar_learning_curve_strength_variation": 1,
        "time": 1,
    },
)
def wind_learning_rate():
    """
    Fraction for Wind Learning Curve Strength indicating by what percentage the wind energy cost will drop for each doubling of wind installed capacity.
    """
    return init_wind_learning_rate() + step(
        __data["time"],
        fraction_for_wind_and_solar_learning_curve_strength_variation()
        - init_wind_learning_rate(),
        2020,
    )


@component.add(
    name="wind market share data",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def wind_market_share_data():
    return np.interp(
        time(),
        [
            1977.0,
            1978.0,
            1979.0,
            1980.0,
            1981.0,
            1982.0,
            1983.0,
            1984.0,
            1985.0,
            1986.0,
            1987.0,
            1988.0,
            1989.0,
            1990.0,
            1991.0,
            1992.0,
            1993.0,
            1994.0,
            1995.0,
            1996.0,
            1997.0,
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
        ],
        [
            0.00000e00,
            9.71946e-08,
            1.88751e-07,
            3.32728e-07,
            3.33731e-07,
            5.89897e-07,
            1.02907e-06,
            1.34928e-06,
            1.88906e-06,
            4.00035e-06,
            5.44773e-06,
            8.93709e-06,
            7.01247e-05,
            9.47745e-05,
            1.05837e-04,
            1.21770e-04,
            1.45554e-04,
            1.79714e-04,
            2.04216e-04,
            2.21484e-04,
            2.86217e-04,
            3.76720e-04,
            4.93779e-04,
            7.13468e-04,
            8.59242e-04,
            1.14146e-03,
            1.33093e-03,
            1.71417e-03,
            2.01868e-03,
            2.50004e-03,
            3.10621e-03,
            3.93900e-03,
            4.97445e-03,
            5.91694e-03,
            7.33865e-03,
            8.67972e-03,
            1.01620e-02,
            1.11244e-02,
            1.29546e-02,
            1.47192e-02,
            1.70327e-02,
            1.84018e-02,
            2.02737e-02,
            2.34655e-02,
            2.60495e-02,
            2.89804e-02,
            3.11426e-02,
            3.28596e-02,
        ],
    )


@component.add(
    name="Wind Opex",
    units="$2024/(kW*Hour)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reference_wind_opex": 1, "impact_of_learning_on_wind_opex": 1},
)
def wind_opex():
    return reference_wind_opex() * impact_of_learning_on_wind_opex()


@component.add(
    name="Wind Opex Learning Rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1},
)
def wind_opex_learning_rate():
    return 0 + step(__data["time"], 0.3, 2000)


@component.add(
    name="Wind Opex mtoe",
    units="$2024/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_opex": 1, "kwh_into_mtoe": 1},
)
def wind_opex_mtoe():
    return wind_opex() / kwh_into_mtoe()


@component.add(
    name="Wind Production to Installation Ratio",
    units="Mtoe/(m*m*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production": 1, "wind_installed_capacity": 1},
)
def wind_production_to_installation_ratio():
    """
    Ratio of wind energy production to available production capacity.
    """
    return wind_energy_production() / wind_installed_capacity()


@component.add(
    name="Wind Threshold Capacity",
    units="MW",
    comp_type="Constant",
    comp_subtype="Normal",
)
def wind_threshold_capacity():
    return 15000
