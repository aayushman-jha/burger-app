import sqlite3
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


def get_association_rules(db_path, min_support=0.1, min_lift=1.0):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()

    df['items'] = df['items'].apply(lambda x: x.split(","))

    te = TransactionEncoder()
    te_array = te.fit_transform(df['items'])
    te_df = pd.DataFrame(te_array, columns=te.columns_)

    frequent_itemsets = apriori(te_df, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    rules = rules.sort_values('lift', ascending=False)

    # Keep only single-item consequents (actual recommendation shape: X -> Y)
    rules = rules[rules['consequents'].apply(lambda x: len(x) == 1)]

    # one rule per underlying itemset, keep the highest-lift direction
    rules['itemset_key'] = rules.apply(lambda r: frozenset(r['antecedents']) | frozenset(r['consequents']), axis=1)
    rules = rules.sort_values('lift', ascending=False).drop_duplicates(subset='itemset_key')
    rules = rules.drop(columns='itemset_key')

    return rules
    
def format_rules(rules):
    formatted = []

    for _, row in rules.iterrows():
        antecedents = ", ".join(list(row['antecedents']))
        consequents = ", ".join(list(row['consequents']))
        confidence = round(row['confidence'] * 100)
        lift = round(row['lift'], 2)

        formatted.append(f"({antecedents}) → ({consequents}) — {confidence}% confidence, {lift} lift")

    return formatted

def get_recent_orders(db_path, limit=5):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        "SELECT * FROM orders ORDER BY timestamp DESC LIMIT ?",
        conn,
        params=(limit,)
    )
    conn.close()

    return df
