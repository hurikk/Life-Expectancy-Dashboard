import polars as pl
import matplotlib.pyplot as plt
import utils.genete_plots as mk_plots
from typing import Tuple

def extract_data() -> pl.DataFrame:
    return pl.read_csv('data/life-expectancy.csv')

def transform_data(df_life_expect: pl.DataFrame) -> Tuple[
    pl.DataFrame,
    pl.DataFrame,
    list,
    pl.DataFrame,
    list,
    pl.DataFrame
]:
    df_life_expect = df_life_expect.rename({'Entity': 'Country','life_expectancy_0': 'life_expectancy (Years)'})
    df_life_expect = df_life_expect.with_columns(
        pl.col('life_expectancy (Years)').cast(pl.Int64)
    ).filter(
        pl.col('Year') >= 1950
    )
    
    mean_by_country = df_life_expect.group_by('Country').agg(
        pl.col('life_expectancy (Years)').mean().round(2)
    ).sort('life_expectancy (Years)', descending=True)
    
    higher_averages = mean_by_country.head()
    lower_averages = mean_by_country.tail()
    
    top5_ha = higher_averages.select('Country').to_series().to_list()
    top5_la = lower_averages.select('Country').to_series().to_list()
    
    top5_ha_historic = df_life_expect.filter(
        pl.col('Country').is_in(top5_ha)
    )
    top5_la_historic = df_life_expect.filter(
        pl.col('Country').is_in(top5_la)
    )
    
    bra_life_expectancy = df_life_expect.filter(
        pl.col('Code') == 'BRA'
    )
    
    return df_life_expect, top5_ha_historic, top5_ha, top5_la_historic, top5_la, bra_life_expectancy
    
def load_data(df_life_expect: pl.DataFrame) -> None:
    df_life_expect.write_csv(f'data/processed_data.csv')

def main() -> None:
    df_life_expect = extract_data()
    df_life_expect, top5_ha_hist, top5_ha_names, top5_la_hist, top5_la_names,bra_life_expect = transform_data(df_life_expect)
    load_data(df_life_expect)
    mk_plots.gen_plots(top5_ha_hist, top5_ha_names, top5_la_hist, top5_la_names, bra_life_expect)
    
if __name__ == '__main__':
    main()