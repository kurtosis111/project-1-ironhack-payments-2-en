import pandas as pd
from data_loader import load_data


def quality(df, num_cols, datetime_cols):
    """
    Checks the quality of the DataFrame in terms missing values, data types.
    
    :param df: DataFrame to check
    :return: dictionary describing the quality of the DataFrame
    """  

    # check missing values percentage:
    missing_value_pct = round(df.isna().sum() / len(df)*100, 2)
    
    # Check data types
    num_res = {}
    for col in num_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"{col} must be numeric.")
            res = False
        else:
            res = True
        num_res[col] = res

    dt_res = {}
    for col in datetime_cols:
        if not pd.api.types.is_datetime64_any_dtype(pd.to_datetime(df[col], format='mixed', errors='coerce')):
            print(f"{col} must be datetime.")
            res = False
        else:
            res = True
        dt_res[col] = res

    # check outliers
    otl_res = {}
    for col in num_cols:
        if df[col].isnull().all():
            print(f"{col} has no data.")
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if not outliers.empty:
            print(f"{col} has outliers: {len(outliers)} rows")
            res = True
        else:
            res = False
        otl_res[col] = res

    qtl_dict = {
        'missing_value_pct': missing_value_pct,
        'num_cols': num_res,
        'datetime_cols': dt_res,
        'contain_outliers': otl_res
    }

    return qtl_dict

if __name__ == "__main__":
    cash_req, fee = load_data()
    num_cols_cash_req = ['amount']
    datetime_cols_cash_req = ['created_at', 'updated_at', 'moderated_at', 'reimbursement_date']
    num_cols_fee = ['total_amount']
    datetime_cols_fee = ['created_at', 'paid_at']
    cash_req_quality = quality(cash_req, num_cols_cash_req, datetime_cols_cash_req)
    fee_quality = quality(fee, num_cols_fee, datetime_cols_fee)
    print("Cash Request Quality:")
    print(cash_req_quality)
    print("\nFee Quality:")
    print(fee_quality)
    # This code checks the quality of the cash request and fee DataFrames, including missing values, data types, and outliers.
    # It prints the results for both DataFrames.
    # %%