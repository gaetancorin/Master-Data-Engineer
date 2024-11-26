import csv
import random
from datetime import datetime, timedelta
import ulid
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
import random


load_dotenv()
LOG_FILE = os.getenv("LOG_FILE", "var/app.log")
Path(LOG_FILE).parents[0].mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

NUM_ROWS = 5000

COUNT_PRODUCTS = 20
logger.info(f"creating {COUNT_PRODUCTS} different products")
PRODUCT_IDS = [ulid.new().str for _ in range(COUNT_PRODUCTS)]


def create_labels(distribution):
    total = sum(distribution.values())
    labels = []
    for label, percentage in distribution.items():
        count = int((percentage / total) * 100)
        labels.extend([label] * count)
    return labels


logger.info(f"creating fair and fishy labels")


class Labelizer:
    def __init__(self):
        pass

    def labelize(self, amount):
        pass

class FairLabelizer(Labelizer):
    def __init__(self):
        super().__init__()
        self.threshold_low_risk = 1000
        self.threshold_high_risk = 5000
        self.threshold_fraud = 8000

    def labelize(self, amount):
        if random.random() < 0.05:
            return "invalid_label"
        noise = random.random()

        if amount <= 0:
            return "invalid_label"

        if amount < self.threshold_low_risk:
            return "legit" if noise < 0.9 else "low_risk"

        if self.threshold_low_risk <= amount < self.threshold_high_risk:
            return "low_risk" if noise < 0.8 else "high_risk"

        if self.threshold_high_risk <= amount < self.threshold_fraud:
            return "high_risk" if noise < 0.7 else "fraud"

        return "fraud" if noise < 0.9 else "high_risk"


class FishyLabelizer(Labelizer):
    def __init__(self):
        super().__init__()
        self.threshold_low_risk = 4000
        self.threshold_high_risk = 7000
        self.threshold_fraud = 9500

    def labelize(self, amount):
        if random.random() < 0.05:
            return "invalid_label"
        noise = random.random()

        if amount <= 0:
            return "invalid_label"

        if amount < self.threshold_low_risk:
            return "legit" if noise < 0.9 else "low_risk"

        if self.threshold_low_risk <= amount < self.threshold_high_risk:
            return "low_risk" if noise < 0.8 else "high_risk"

        if self.threshold_high_risk <= amount < self.threshold_fraud:
            return "high_risk" if noise < 0.8 else "fraud"

        return "fraud" if noise < 0.9 else "high_risk"


def random_date():
    start_date = datetime.now() - timedelta(days=30)
    random_offset = random.randint(0, 30 * 24 * 60 * 60)
    return start_date + timedelta(seconds=random_offset)


def random_invalid_date():
    return "null"


def generate_transaction(labelizer: Labelizer):
    transaction_id = ulid.new().str
    client_id = ulid.new().str
    product_id = random.choice(PRODUCT_IDS)
    amount = random.randint(1, 10000)

    label = labelizer.labelize(amount)

    if random.random() < 0.05:
        amount = -amount

    if random.random() < 0.03:
        amount = None

    date = (
        random_date().isoformat() if random.random() > 0.05 else random_invalid_date()
    )

    return [transaction_id, client_id, product_id, amount, date, label]


def generate_csv(num_rows, output_file, labelizer: Labelizer):
    with open(output_file, mode="w", newline="") as file:
        logger.info(f"writing into CSV file {output_file} with {num_rows} rows")
        writer = csv.writer(file)
        writer.writerow(
            ["transaction_id", "client_id", "product_id", "amount", "date", "label"]
        )
        for iteration_no in range(1, num_rows + 1):
            writer.writerow(generate_transaction(labelizer))
            if iteration_no % 100 == 0:
                logger.debug(f"written 100 lines ({iteration_no}/{num_rows})")
    logger.info(f"finished writing into CSV file {output_file}")


if __name__ == "__main__":
    generate_csv(NUM_ROWS, "transactions-fair.csv", FairLabelizer())
    generate_csv(NUM_ROWS, "transactions-fishy.csv", FishyLabelizer())
