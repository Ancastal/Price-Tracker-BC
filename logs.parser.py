import re
import os
import pandas as pd

current_dir = os.getcwd()
logs_dir = os.path.join(current_dir, "logs")
all_transactions = []

def parse_bought_transactions():
    for file_name in os.listdir(logs_dir):
        if file_name.endswith(".log"):
            file_path = os.path.join(logs_dir, file_name)

            with open(file_path, "r") as file:
                log_text = file.read()

            transaction_pattern = r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (\w+) (bought|sold) (\d+) ([\w\s]+) for ([\d\.]+) from (\w+) at \[world\] (-?\d+), (-?\d+), (-?\d+)"
            transactions = re.findall(transaction_pattern, log_text)

            all_transactions.extend(transactions)

    df = pd.DataFrame(all_transactions, columns=["timestamp", "username", "action", "quantity", "item_name", "price", "seller", "x", "y", "z"])

    # Convert the timestamp column to a datetime object
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y/%m/%d %H:%M:%S")
    df['timestamp'] = df['timestamp'].dt.date

    df["quantity"] = df["quantity"].astype(int)
    df["price"] = df["price"].astype(float)
    df["x"] = df["x"].astype(int)
    df["y"] = df["y"].astype(int)
    df["z"] = df["z"].astype(int)

    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///bought_transactions.db", echo=False)
    df.to_sql("transactions", con=engine, if_exists="replace", index=False)
    print(df.action.unique())

def parse_sales_transactions():

    all_transactions = []

    for file_name in os.listdir(logs_dir):
        if file_name.endswith(".log"):
            file_path = os.path.join(logs_dir, file_name)

            with open(file_path, "r") as file:
                log_text = file.read()
            transaction_pattern = r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (\w+) (bought|sold) (\d+) ([\w\s]+) for ([\d\.]+) to (\w+) at \[world\] (-?\d+), (-?\d+), (-?\d+)"
            transactions = re.findall(transaction_pattern, log_text)

            all_transactions.extend(transactions)

    df = pd.DataFrame(all_transactions, columns=["timestamp", "username", "action", "quantity", "item_name", "price", "seller", "x", "y", "z"])

    # Convert the timestamp column to a datetime object
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y/%m/%d %H:%M:%S")
    df['timestamp'] = df['timestamp'].dt.date

    df["quantity"] = df["quantity"].astype(int)
    df["price"] = df["price"].astype(float)
    df["x"] = df["x"].astype(int)
    df["y"] = df["y"].astype(int)
    df["z"] = df["z"].astype(int)

    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///sales_transactions.db", echo=False)
    df.to_sql("transactions", con=engine, if_exists="replace", index=False)
    print(df.action.unique())
    print(len(df))

parse_bought_transactions()
parse_sales_transactions()
