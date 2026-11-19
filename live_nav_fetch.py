
import requests
import pandas as pd
import os

# Folder to save raw NAV data
OUTPUT_FOLDER = "data/raw"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Mutual fund scheme codes
schemes = {
    "HDFC_Top_100": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

for fund_name, scheme_code in schemes.items():

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        result = response.json()

        # Extract NAV history
        nav_data = result["data"]

        df = pd.DataFrame(nav_data)

        # Convert data types
        df["date"] = pd.to_datetime(
            df["date"], format="%d-%m-%Y", errors="coerce"
        )

        df["nav"] = pd.to_numeric(
            df["nav"], errors="coerce"
        )

        # Save raw CSV
        output_file = os.path.join(
            OUTPUT_FOLDER,
            f"live_nav_{scheme_code}.csv"
        )

        df.to_csv(output_file, index=False)

        print(f"\nFund: {fund_name}")
        print(f"Scheme Code: {scheme_code}")
        print(f"Records: {len(df)}")
        print(f"Saved: {output_file}")
        print(df.head())

    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"Error fetching {fund_name}: {error}")

print("\nNAV data fetching completed!")
