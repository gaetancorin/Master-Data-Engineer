import pandas as pd

from pipeline import Cleaner


def test_clean_dataframe() -> None:
    df = pd.DataFrame(
        {
            "transaction_id": ["1"],
            "client_id": ["1"],
            "product_id": ["1"],
            "amount": [None],
            "date": ["2024-01-01"],
            "label": ["legit"],
        }
    )
    cleaner = Cleaner()
    df = cleaner.clean(df)
    assert df.empty


def test_clean_dataframe_keeps_legitimate_amounts() -> None:
    fake_data = range(0, 5)
    df = pd.DataFrame(
        {
            "transaction_id": fake_data,
            "client_id": fake_data,
            "product_id": fake_data,
            "date": fake_data,
            "amount": ["1", "-1", "bonjour", "", None],
            "label": ["legit", "legit", "legit", "legit", "legit"],
        }
    )
    cleaner = Cleaner()
    df = cleaner.clean(df)
    assert df["amount"].to_list() == [1.0]


def test_clean_dataframe_keeps_legitimate_labels() -> None:
    fake_data = ["1", "1", "1", "1", "1", "1", "1"]
    labels = ["legit", "fraud", "high_risk", "low_risk", "", None, 1]
    df = pd.DataFrame(
        {
            "transaction_id": fake_data,
            "client_id": fake_data,
            "product_id": fake_data,
            "date": fake_data,
            "amount": fake_data,
            "label": labels,
        }
    )
    cleaner = Cleaner()
    df = cleaner.clean(df)
    assert df["label"].to_list() == ["legit", "fraud", "high_risk", "low_risk"]


def test_clean_dataframe_trims_nonessential_data() -> None:
    date = "2024-11-02T18:51:23.988846"
    df = pd.DataFrame(
        {
            "transaction_id": [None, "1", "1", "1"],
            "client_id": ["1", None, "1", "1"],
            "product_id": ["1", "1", "1", "1"],
            "date": [date, date, date, None],
            "amount": ["25", "25", "25", "25"],
            "label": ["legit", "legit", "legit", "legit"],
        }
    )
    cleaner = Cleaner()
    df = cleaner.clean(df)
    assert df.shape[0] == 4
