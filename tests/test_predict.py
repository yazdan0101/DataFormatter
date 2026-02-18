from src.formatter import clean_data
import pandas as pd

def test_clean():
    # Create a sample DataFrame with some issues
  
    data = {
        'product': ['A', 'B', 'C'],
        'quantity': ['10', '20', '30'],
        'unit_price': ['5.0', None, '15.0']
    }
    df = pd.DataFrame(data)

    # Clean the data
    cleaned_df = clean_data(df)

    # Check if the total_price is calculated correctly (BUG: should be quantity * unit_price)
    assert cleaned_df.loc[0, 'total_price'] == 15.0  # 10 + 5.0 (BUG)
    assert cleaned_df.loc[1, 'total_price'] == 20.0  # 20 + 0 (BUG)
    assert cleaned_df.loc[2, 'total_price'] == 45.0  # 30 + 15.0 (BUG)
