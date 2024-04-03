import os

import datetime
from pandas_functions import read_pqt_with_lock, write_pqt_with_lock, combine_dfs

import pandas as pd
import numpy as np

def dir_one_up():
    current_directory   =   os.path.dirname(__file__)
    parent_directory    =   os.path.dirname(current_directory)
    return parent_directory

def dir_orders():
    return dir_one_up() +   "/Orders"

def dir_dsp():
    return dir_one_up() +   "/DETSYSPRICES"

def main_ps_str():
    return "MAIN PRICE SUMMARY" #   PRETTY sure this data is the same as "imbalancePriceAmountGBP". For the last few months results are identical but there are some historical discrepancies

def market_ps_str():
    return "MARKET PRICE SUMMARY"

def next_row_col(row, col, max_row, max_col):
    """
    Calculate the next row and column indices based on the current indices,
    maximum row, and maximum column values.

    Args:
        row (int): Current row index.
        col (int): Current column index.
        max_row (int): Maximum row index.
        max_col (int): Maximum column index.

    Returns:
        Tuple[int, int]: Next row and column indices.

    Raises:
        ValueError: If the row index exceeds the maximum row index.
    """
    # Increment the column index
    col +=  1
    # If column index reaches the maximum column index, reset it and move to the next row
    if col==max_col:
        col =   0
        row +=  1
    # Check if the row index exceeds the maximum row index
    if row >= max_row:
        raise ValueError("Row index exceeds the maximum row index")
    return row, col

def plot_pnl(ax, dates, pnl, title_desc, x_label, y_label, desc_pnl, scatter_plt, add_y_eq_x):
    """
    Plot profit and loss (pnl) data on the provided axes.

    Args:
        ax (matplotlib.axes.Axes): Axes object to plot on.
        dates (array-like): Array of dates.
        pnl (array-like): Array of pnl values.
        title_desc (str): Title for the plot.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        desc_pnl (str): Description for the pnl data.
        scatter_plt (bool): Whether to use scatter plot or line plot.
        add_y_eq_x (bool): Whether to add y=x line for comparison.

    Returns:
        None
    """
    if scatter_plt:
        ax.scatter(dates, pnl, label=desc_pnl)
        ax.axhline(0, color='gray', linestyle='--')
        if add_y_eq_x:
            max_v   =   np.max(pnl)
            min_v   =   np.min(pnl)
            ax.plot([min_v, max_v], [min_v, max_v], 'k--')
            ax.axvline(0, color='gray', linestyle='--')
    else:
        ax.plot(dates, pnl, label=desc_pnl)
    ax.set_title(title_desc)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()

def print_paper_trading(time_forwards_vec, start_datetime):
    file_name_orders=   dir_orders()    +   "/Combined.pqt"
    df_orders       =   combine_dfs(file_name_orders, dir_orders()+"/", ".pqt")
    df_orders       =   df_orders[df_orders.index>=start_datetime]
    df_orders.index =   df_orders.index.ceil('30T')
    
    file_name_dsp   =   dir_dsp()    +   "/Combined.pqt"
    df_dsp_orig     =   combine_dfs(file_name_dsp, dir_dsp()+"/", ".pqt")

    import matplotlib.pyplot as plt
    for time_forwards in time_forwards_vec:
        imb_desc    =   main_ps_str()
        mkt_desc    =   market_ps_str()

        num_rows    =   2
        num_cols    =   2
        fig, axs    =   plt.subplots(num_rows, num_cols)
        row =   0
        col =   -1

        fig.set_figheight(10)
        fig.set_figwidth(15)

        cols    =   [imb_desc, mkt_desc]
        df_dsp  =   df_dsp_orig.copy()
        df_dsp.index    =   df_dsp.index    -   pd.Timedelta(minutes=time_forwards)
        merged          =   pd.merge(df_orders, df_dsp[cols], left_index=True, right_index=True, how='left')
        merged.dropna(subset=cols, inplace=True)

        # add on results to df_orders by looking up in merged
        payoff_desc =   "imbal_min_mkt"
        merged[payoff_desc]  =   (merged[imb_desc]    -   merged[mkt_desc])*0.5 #   half because it's a half hour auction

        for j in range(0,2):    #   0 is PNL, 1 is traded turnover
            strat_desc  =   "FullStrat"
            posn_live   =   merged["Posn"]

            traded      =   None
            if j==0:
                merged.to_csv("pnl_file" + str(time_forwards)  +   ".csv")
            row, col    =   next_row_col(row, col, num_rows, num_cols)
            desc_live   =   "Live"
            if j==0:
                pnl_cumsum_live  =   np.cumsum(merged[payoff_desc]*posn_live*0.5)
                plot_pnl(axs[row, col], merged.index, pnl_cumsum_live, "cum Gross " + strat_desc, "Date", \
                                "PNL", desc_live, False, False)
            else:
                traded_cc_live      =   np.cumsum(np.fabs(posn_live))
                plot_pnl(axs[row, col], merged.index, traded_cc_live, "vol traded " + strat_desc, "Date", \
                            "amount traded", desc_live, False, False)

        row, col    =   next_row_col(row, col, num_rows, num_cols)
        plot_pnl(axs[row, col], merged.index, merged["Posn"], "Posn " + strat_desc, "Date", \
            "Posn", desc_live, True, False)

        fig.autofmt_xdate()
        file_name   =   "Pnl"  +   str(time_forwards)
        fig.savefig(file_name   +   ".png")
    return

if __name__ == '__main__':
    print_paper_trading([30,60,90,120,150], datetime.datetime(2023,12,9,9,0,0, tzinfo=datetime.timezone.utc))