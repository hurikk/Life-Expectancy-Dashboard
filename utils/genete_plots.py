import polars as pl
import matplotlib.pyplot as plt
from pathlib import Path

def gen_higher_average_plot(top5_ha_hist: pl.DataFrame, top5_ha_names: list) -> None:
    plt.figure(figsize=(12, 8))
    for country in top5_ha_names:
        df_country = top5_ha_hist.filter(pl.col('Country') == country)
        plt.plot(df_country['Year'], df_country['life_expectancy (Years)'], label=country)
    plt.legend()
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Life Expectancy (Years)", fontsize=14)
    plt.title("Evolution Of Life Expectancy - Top 5 Countries With The Best Life Expectancy", fontsize=16)
    Path('plots/').mkdir(exist_ok=True)
    plt.savefig('plots/higher_average_plot')
    plt.close()

def gen_lower_average_plot(top5_la_hist: pl.DataFrame, top5_la_names: list) -> None:
    plt.figure(figsize=(12, 8))
    for country in top5_la_names:
        df_country = top5_la_hist.filter(pl.col('Country') == country)
        plt.plot(df_country['Year'], df_country['life_expectancy (Years)'], label=country)
    plt.legend()
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Life Expectancy (Years)", fontsize=14)
    plt.title("Evolution Of Life Expectancy - Top 5 Countries With The Worst Life Expectancy", fontsize=16)
    Path('plots/').mkdir(exist_ok=True)
    plt.savefig('plots/lower_average_plot')
    plt.close()

def gen_comparision_bra_plot(top5_ha_hist: pl.DataFrame, top5_ha_names: list, bra_life_expect: pl.DataFrame) -> None:
    plt.figure(figsize=(14, 10))
    plt.plot(bra_life_expect['Year'], bra_life_expect['life_expectancy (Years)'], label='Brazil')
    for country in top5_ha_names[:3]:
        df_country = top5_ha_hist.filter(pl.col('Country') == country)
        plt.plot(df_country['Year'], df_country['life_expectancy (Years)'], label=country)
    plt.legend()
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Life Expectancy (Years)", fontsize=14)
    plt.title("Evolution Of The Life Expectancy - Top 3 Countries With The Best Life Expectancy x Brazil", fontsize=16)
    Path('plots/').mkdir(exist_ok=True)
    plt.savefig('plots/top3_best_expec_vs_brazil')
    plt.close()

def gen_plots(top5_ha_hist: pl.DataFrame, top5_ha_names: list, top5_la_hist: pl.DataFrame, 
              top5_la_names: list, bra_life_expect: pl.DataFrame) -> None:
    gen_higher_average_plot(top5_ha_hist, top5_ha_names)
    gen_lower_average_plot(top5_la_hist, top5_la_names)
    gen_comparision_bra_plot(top5_ha_hist, top5_ha_names, bra_life_expect)