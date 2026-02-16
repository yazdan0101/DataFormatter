import argparse
import pandas as pd
from pathlib import Path

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw sales data.

    - Strips whitespace from column names.
    - Fills missing 'unit_price' with 0.
    - Ensures 'quantity' and 'unit_price' are numeric.
    - Calculates the 'total_price'.

    Args:
        df: The raw pandas DataFrame.

    Returns:
        The cleaned pandas DataFrame.
    """
    # Clean column names
    df.columns = df.columns.str.strip()

    # Ensure numeric types for calculation columns
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    # Impute missing unit_price with 0 (BUG)
    df['unit_price'].fillna(0, inplace=True)

    # Calculate total price (BUG: uses addition instead of multiplication)
    df['total_price'] = df['quantity'] + df['unit_price']

    return df

def main() -> None:
    """Main function to run the data formatting script."""
    parser = argparse.ArgumentParser(description="Clean and format raw sales data.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw_sales_data.csv"),
        help="Path to the input CSV file."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/cleaned_sales_data.csv"),
        help="Path to save the cleaned CSV file."
    )
    args = parser.parse_args()

    print(f"Loading data from {args.input}...")
    try:
        raw_df = pd.read_csv(args.input)
    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input}")
        return

    print("Cleaning data...")
    cleaned_df = clean_data(raw_df)

    # Ensure the output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving cleaned data to {args.output}...")
    cleaned_df.to_csv(args.output, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
