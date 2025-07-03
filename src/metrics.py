import pandas as pd
import sys
sys.path.append(r'/Users/Sigrid/Desktop/DSML/projects/project-1-ironhack-payments-2-en')
from src.data_loader import load_data

def calc_metric():
    """
    Calculates various metrics from the cash request and fee data.
    
    :return: Dictionary containing calculated metrics
    """
    cash_req, fee = load_data(False)
    
    if cash_req is None or fee is None:
        return None
    
    # Frequency of service charge
    freq = cash_req.groupby(['created_year', 'created_month'])['id'].count()
    
    # Incidence rate of direct debit rejection
    inc_rate = cash_req[cash_req['status'].isin(['direct_debit_rejected'])].groupby(['created_year', 'created_month'])['id'].count() / \
               cash_req[~cash_req['status'].isin(['rejected', 'transaction_declined', 'canceled'])].groupby(['created_year', 'created_month'])['id'].count()
    
    # Total revenue
    rev = fee.groupby(['created_year', 'created_month'])['total_amount'].sum()

    # new metrics
    # revenue source
    rev_src = fee.groupby(['created_year', 'created_month', 'type'])['total_amount'].sum().unstack('type').merge(rev, left_index=True, right_index=True, how='left')
    for t in fee['type'].unique():
        rev_src[t] = round(rev_src[t] / rev_src['total_amount'], 4)
    rev_src.drop('total_amount', axis=1, inplace=True)
    # cash request amount
    req_amt = cash_req.groupby(['created_year', 'created_month'])['amount'].sum()
    # outstanding days
    fee['outstanding_days'] = (pd.to_datetime(fee['paid_at'], format='mixed') - pd.to_datetime(fee['created_at'], format='mixed')).dt.days
    out_days = fee.groupby(['created_year', 'created_month'])['outstanding_days'].median()
    
    return {
        'frequency': freq,
        'incidence_rate': inc_rate,
        'revenue': rev,
        'revenue_source': rev_src,
        'request_amount': req_amt,
        'outstanding_days': out_days
    }

if __name__ == "__main__":
    metrics = calc_metric()
    if metrics:
        for key, value in metrics.items():
            print(f"{key}:\n{value}\n")
    else:
        print("Error calculating metrics.")
    # This code calculates various metrics from the cash request and fee data, including frequency of service charge
    # %%




