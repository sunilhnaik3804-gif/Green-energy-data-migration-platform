```python
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

REQUIRED_COLUMNS = [
    "mf_id",
    "plant_id",
    "plant_name",
    "energy_type",
    "meter_id",
    "meter_factor",
    "generation_mwh",
    "effective_date",
    "location",
    "status",
    "created_at",
    "updated_at",
]


def transform_meter_factor(records, source_name):
    """
    Standardize and validate Oracle or MySQL
    meter-factor records.
    """

    if not records:
        logging.warning("No records received from %s", source_name)
        return pd.DataFrame(columns=REQUIRED_COLUMNS + ["source_system"])

    df = pd.DataFrame(records)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Ensure required columns exist
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = None

    # Keep the required columns
    df = df[REQUIRED_COLUMNS].copy()

    # Standardize text columns
    text_columns = [
        "plant_id",
        "plant_name",
        "energy_type",
        "meter_id",
        "location",
        "status",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        df[column] = df[column].replace("", pd.NA)

    # Standardize categories
    df["energy_type"] = df["energy_type"].str.upper()
    df["status"] = df["status"].str.upper()

    # Convert numeric fields
    df["mf_id"] = pd.to_numeric(
        df["mf_id"], errors="coerce"
    ).astype("Int64")

    df["meter_factor"] = pd.to_numeric(
        df["meter_factor"], errors="coerce"
    )

    df["generation_mwh"] = pd.to_numeric(
        df["generation_mwh"], errors="coerce"
    )

    # Convert date and timestamp fields
    df["effective_date"] = pd.to_datetime(
        df["effective_date"], errors="coerce"
    ).dt.date

    for column in ["created_at", "updated_at"]:
        df[column] = pd.to_datetime(
            df[column], errors="coerce", utc=True
        )

    # Remove duplicate IDs within this batch
    df = df.drop_duplicates(
        subset=["mf_id"],
        keep="last"
    )

    # Validate mandatory fields
    valid = (
        df["mf_id"].notna()
        & df["plant_id"].notna()
        & df["meter_id"].notna()
        & df["energy_type"].isin(["SOLAR", "WIND"])
        & df["meter_factor"].between(0, 1, inclusive="both")
        & df["generation_mwh"].ge(0)
    )

    invalid_records = df.loc[~valid].copy()
    valid_records = df.loc[valid].copy()

    # Track the source system
    valid_records["source_system"] = source_name.upper()
    invalid_records["source_system"] = source_name.upper()

    logging.info(
        "%s transformation complete: %s valid, %s invalid",
        source_name,
        len(valid_records),
        len(invalid_records),
    )

    return valid_records, invalid_records


if __name__ == "__main__":
    sample_records = [
        {
            "mf_id": 1001,
            "plant_id": "PLANT001",
            "plant_name": "Solar Plant Bengaluru",
            "energy_type": "Solar",
            "meter_id": "MTR001",
            "meter_factor": 0.9850,
            "generation_mwh": 1250.500,
            "effective_date": "2026-10-01",
            "location": "Bengaluru",
            "status": "ACTIVE",
            "created_at": None,
            "updated_at": None,
        }
    ]

    valid, invalid = transform_meter_factor(
        sample_records,
        "oracle",
    )

    print("\nValid records:")
    print(valid.to_string(index=False))

    print("\nInvalid records:")
    print(invalid.to_string(index=False))
```
