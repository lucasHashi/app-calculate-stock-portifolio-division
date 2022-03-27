from operator import index
import pandas as pd
import streamlit as st
from math import gcd


def main():
    df_stocks_sectors = pd.read_excel('stocks_data.xlsx')

    st.header('Portfolio division calculator')

    total_invested = st.number_input('Total invested', 0, 1000000, 100000, 100)

    # ----------- UPLOAD GRADES CSV -----------
    stocks_selected = []
    df_stocks_and_grades = pd.DataFrame(columns=['stock', 'grade'])
    uploaded_grades = st.file_uploader("Load grades - Optional")
    if uploaded_grades is not None:
        df_stocks_and_grades = pd.read_csv(uploaded_grades)
        stocks_selected = list(df_stocks_and_grades['stock'])

    stocks_selected = st.multiselect('Stocks', df_stocks_sectors['ticker'], stocks_selected)

    # ----------- GRADE SLIDERS FOR EACH STOCK LISTED -----------
    if stocks_selected:
        stocks_and_grades = {}
        for stock in stocks_selected:
            initial_grade = 500 if stock not in list(df_stocks_and_grades['stock']) else int(df_stocks_and_grades[df_stocks_and_grades['stock'] == stock]['grade'].iloc[0])

            stocks_and_grades[stock] = st.slider(
                'Grade for {}'.format(stock),
                0,
                1000,
                initial_grade,
                5
            )


    # ----------- RECALCULATE BUTTON -----------
    if st.button('Recalculate division'):
        if stocks_selected:
            df_stocks_and_grades = pd.DataFrame(list(stocks_and_grades.items()), columns = ['stock','grade'])

            df_stocks_and_grades['percent'] = df_stocks_and_grades['grade'] / df_stocks_and_grades['grade'].sum()

            df_stocks_and_grades['investment'] = df_stocks_and_grades['percent'] * total_invested
            df_stocks_and_grades['investment'] = df_stocks_and_grades['investment'].round(2)

            df_stocks_and_grades = df_stocks_and_grades.merge(
                df_stocks_sectors,
                'left',
                left_on='stock',
                right_on='ticker'
            )
            df_stocks_and_grades.drop('ticker', axis=1, inplace=True)

            df_stocks_and_grades_print = prepare_df_to_print(df_stocks_and_grades)

            st.dataframe(df_stocks_and_grades_print)

            # ----------- DOWNLOAD CSV BUTTON -----------
            csv_stocks_and_grades = convert_to_csv(df_stocks_and_grades)
            st.download_button(
                label="Download as CSV",
                data=csv_stocks_and_grades,
                file_name='stocks_and_grades.csv',
                mime='text/csv',
            )
        else:
            st.write('Select one or more stocks')


def convert_to_csv(df):
    return df.to_csv(index=False, decimal=",").encode('utf-8')

def prepare_df_to_print(df):
    df_print = df.copy()

    df_print['percent'] = df_print['percent'].round(4) * 100
    df_print['percent'] = df_print['percent'].apply(lambda value: "%.2f" % value + "%")

    df_print['investment'] = df_print['investment'].apply(lambda value: "R$ " + "%.2f" % value)
    
    df_print.sort_values('grade', ascending=False, inplace=True)

    df_print.columns = [column.capitalize() for column in df.columns]

    return df_print


if __name__ == '__main__':
    main()