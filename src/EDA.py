import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from data_loader import load_data

cash_req, fee = load_data(False)
df = fee.merge(cash_req, left_on='cash_request_id', right_on='id', how='left', suffixes=('', '_c'))
df.drop([c for c in df.columns if c.endswith('_c')], axis=1, inplace=True)
df['outstanding_days'] = (pd.to_datetime(df['paid_at'], format='mixed') - pd.to_datetime(df['created_at'], format='mixed')).dt.days

def classify(df):    
    dt_dict = {}
    for t in list(set(df.dtypes.values)):
        dt_dict[t] = df.dtypes[df.dtypes==t].index.to_list()
    return dt_dict

def num_na(df):
    """
    Calculate the percentage of missing values in numeric columns.
    
    :df: DataFrame containing the data
    :return: Series with the percentage of missing values for each numeric column
    """
    num_cols = df.select_dtypes(include=['number']).columns
    return df[num_cols].isna().sum() / df.shape[0] 

def check_outliers(df, grp_col, num_cols):
    otl_res = {}
    for col in num_cols:
        if df[col].isnull().all():
            print(f"{col} has no data.")
            continue
        q1 = df.groupby(grp_col)[col].quantile(0.25)
        q3 = df.groupby(grp_col)[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        # outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        out_df = df.merge(lower_bound, left_on=grp_col, right_index=True, how='left', suffixes=('', '_l')).merge(upper_bound, left_on=grp_col, right_index=True, how='left', suffixes=('', '_u'))

        outliers = out_df[(out_df[col]<out_df[col + '_l']) | (out_df[col]>out_df[col+ '_u'])]

        if not outliers.empty:
            print(f"{col} has outliers: {len(outliers)} rows")        
        otl_res[col] = round(outliers.shape[0] / df.shape[0] * 100, 4)
    return otl_res

# classification of columns
print(classify(df))

# missing values percentage of numeric columns
print(num_na(df))
na_df = df[df['cash_request_id'].isnull()][['created_year', 'created_month','user_id', 'amount']]
print(na_df)

# deal with na values in 'amount' column
count_df = df.groupby(['created_year', 'created_month'])['amount'].value_counts().reset_index(drop=False)
max_idx = count_df.groupby(['created_year', 'created_month'])['count'].idxmax().values
mode_df = count_df.loc[max_idx, ['created_year', 'created_month', 'amount']].copy().reset_index(drop=True)
df = df.merge(mode_df, left_on=['created_year','created_month'], right_on = ['created_year','created_month'], how='left', suffixes=('', '_f'))
df = df.merge(mode_df, left_on=['created_year','created_month'], right_on = ['created_year','created_month'], how='left', suffixes=('', '_f'))
df.drop('amount_f', axis=1, inplace=True)

# check outliers
outliers = check_outliers(df, ['created_year', 'created_month'], ['amount', 'total_amount'])
print(outliers)
# boxplot
# Group our dataset with our 'Group' variable
grouped = df.groupby(['created_year', 'created_month'])['amount']
# Init a figure and axes
fig, ax = plt.subplots(figsize=(20, 10))
# Create the plot
ax.boxplot(x=[group.values for name, group in grouped], labels=grouped.groups.keys())
# Display it
plt.show()

# distribution graph
num_df = df[df.select_dtypes(include=['number']).columns].copy()
i = 0
fig = plt.figure(figsize = (30, 15))
for c in ['amount', 'total_amount', 'outstanding_days']:
    grouped = num_df.groupby(['created_year', 'created_month'])[c]
    for name, group in grouped:       
        i += 1
        axi = fig.add_subplot(3, 7, i)
        group.hist(ax = axi)
        axi.set_title(c + ', ' + str(name[0]) + ', '+str(name[1]))

# correlation matrix
tmp_df = num_df[['created_month', 'amount', 'total_amount', 'outstanding_days']].dropna()
tmp_df.corr()
# %%
# analysis how one variable affects another
num_df['month'] = num_df['created_month'].astype('category')
fig = px.scatter(num_df, x = "amount", y = "total_amount", color = "month")
fig.show()

fig = px.scatter(num_df, x = "outstanding_days", y = "total_amount", color = "month")
fig.show()
# could not fine a relationship among these variables