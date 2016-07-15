import pandas as pd
import numpy as np
from datetime import datetime as dt
import datetime as dtt
import matplotlib.pyplot as plt

data = pd.read_csv("data.csv")

def create_pivotdf(customer_attr):
    '''
    :param customer_attr: customer_id, start_month, end_month
    :return: pivot_df: binary dataframe indicating which months customers are active
    columns are month, rows are customer ids
    '''
    list_df = []
    for customer in customer_attr.index:
        range_months = np.arange(customer_attr.ix[customer]['start_month'], customer_attr.ix[customer]['end_month'] + 1)
        df_temp = pd.DataFrame()
        df_temp['months'] = range_months
        df_temp['customer_id'] = customer
        list_df.append(df_temp)
    
    df = pd.concat(list_df)
    df['count'] = 1
    pivot_df = df.pivot(index='customer_id', columns='months', values='count')
    pivot_df = pivot_df.fillna(0)
    return pivot_df

def calc_churn_single_month(dataframe, month):
    '''
    :param dataframe: binary dataframe indicating whether active in month i or not
    :param month: which month to calculate churn for
    :return: churn rate for given month
    '''
    active_customer_df = dataframe[dataframe[month] == 1]
    active_customer_beginning = active_customer_df[month].sum()
    active_customers_remaining = active_customers_df[month + 1].sum()
    num_quit = active_customers_beginning - active_customers_remaining
    churn_rate = num_quit / float(active_customers_beginning)
    return churn_rate

def all_monthly_churn(dataframe):
    '''
    :param dataframe: binary dataframe indicating which months customers are active
    :return: churn rates for all months
    '''
    months = dataframe.columns
    end_month = max(month)
    all_churn_rates = []
    final_month_values = []
    for month in dataframe.columns:
        if month != end_month:
            churn_rate = calc_churn_single_month(dataframe, month)
            all_churn_rates.append(churn_rate)
            final_month_values.append(month)
    churn_rates = pd.DataFrame()
    churn_rates['month'] = final_month_values
    churn_rates['churn_rate'] = all_churn_rates
    return churn_rates

def average_churn(all_churns):
    return np.mean(all_churns)

def count_active_customers_per_month(active_df):
    '''
    :param active_df: binary dataframe indicating whether customer active in month i
    :return: counts of active customers per month
    '''
    months = active_df.columns
    counts = []
    for month in months:
        count_ = active_df[month].sum()
        counts.append(count_)
    counts_df = pd.DataFrame()
    counts_df['month'] =_months
    counts_df['count'] = counts
    return counts_df

def calc_total_transactions_per_month(transactions_df):
    '''
    :param transactions_df: dataframe with each transaction and value of transaction, as well as which month it occured in
    :return: dataframe with sum of transactions per month
    '''
    grouped_by_month = fares_df[['total_bill_usd', 'month']].groupby(by='month')
    total_transactions_per_month = grouped_by_month.sum()
    total_transactions_per_month.reset_index(inplace=True)
    return total_transactions_per_month

def calc_avg_transaction_per_customer_per_month(customer_count_df, customer_fares_df):
    '''
    :param customer_count_df: needs month column to merge with customer_fares_df. this dataframe is the number of active
    customers each_month
    :param customer_fares_df: needs month column as well. this dataframe is the sum of all transactions in each_month
    :return: faresa_and_active_customers: dataframe with average transaction value per customer each month
    '''
    transactions_and_active_customers = pd.merge(cusotmer_count_df, customer_fares_df, on = 'month', how='inner', left_index=True, right_index=True)
    mean_values = transactions_and_active_customers.total_bill_usd.div(fares_and_active_customers['count'], axis=0)
    transactions_and_active_customers['avg'] = mean_values
    return transactions_and_active_customers

def calc_ltv(average_fares_df, churn_rates_df):
    '''
    :param average_fares_df: dataframe with_monthly average fare
    :param churn_rates_df: dataframe with_monthly churn rate
    :return:
    '''
    churns_and_avg = pd.merge(average_fares_df, churn_rates_df, on='month', how='inner')
    churns_and_avg_removed = churns_and_avg.ix[1:11]
    
    mean_avg_fare = churns_and_avg_removed['avg'].mean()
    mean_avg_churn = churns_and_avg_removed['churn_rate'].mean()
    ltv = mean_avg_fare/mean_avg_churn
    return ltv

if __name__ == '__main__':
    all_customer_pivot_df = create_pivotdf(customer_attr)
    all_monthly_churns_df = all_monthly_churn(all_customer_pivot_df)

    # Plot of churn rates
    plt.plot(all_monthly_churns_df['month'], all_monthly_churns_df['churn_rate'])
    plt.xlabel("Month", size = 20)
    plt.ylabel("Churn Rate", size = 20)
    plt.title("Monthly Churn Rate", size = 20)

    monthly_active_customers_df = count_active_customers_per_month(pivot_df)

    sum_transactions_per_month_df = calc_total_transactions_per_month(data)

    average_transactions_per_month_df = calc_avg_transaction_per_customer_per_month(monthly_active_customers_df, sum_transactions_per_month_df)

    lifetimevalue = calc_ltv(average_transactions_per_months_df)




