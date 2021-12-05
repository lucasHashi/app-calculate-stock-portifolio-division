import pandas as pd
import streamlit as st
from math import gcd


def main():
    df_stocks_sectors = pd.read_excel('stocks_data.xlsx')

    st.header('Calculator portifolio divisor')

    total_invested = st.number_input('Total invested', 0, 1000000, 100000, 100)

    stocks_selected = st.multiselect('Stocks', df_stocks_sectors['ticker'])

    if stocks_selected:
        stocks_and_grades = {}
        for stock in stocks_selected:
            stocks_and_grades[stock] = st.slider(
                'Grade for {}'.format(stock),
                0,
                1000,
                500,
                1
            )
    


    if st.button('Recalculate division'):
        if stocks_selected:
            df_stocks_and_grades = pd.DataFrame(list(stocks_and_grades.items()), columns = ['stock','grade'])

            lcm_grades = least_common_multiple_from_list(list(df_stocks_and_grades['grade']))

            df_stocks_and_grades['partitions'] = df_stocks_and_grades['grade'] / lcm_grades

            partition_from_total_invested = total_invested / df_stocks_and_grades['partitions'].sum()

            df_stocks_and_grades['investment'] = df_stocks_and_grades['partitions'] * partition_from_total_invested

            st.write(lcm_grades)
            st.write(df_stocks_and_grades)
        else:
            st.write('Select one or more stocks')



def least_common_multiple_from_list(list_values):
    lcm = 1
    for i in list_values:
        lcm = lcm*i//gcd(lcm, i)
    
    return lcm





if __name__ == '__main__':
    main()