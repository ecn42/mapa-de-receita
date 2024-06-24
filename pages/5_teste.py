import pandas as pd
import yfinance as yf


# Create an empty DataFrame with the desired column names
columns = ['Ativo(PnT- Giro de Carteira)', 'Qtd. Alvo (%)', 'Ap./ret. financ.', 'Conta cliente.']
df = pd.DataFrame(columns=columns)

# Write the DataFrame to an Excel file
output_file = 'excelfile.xlsx'
writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
df.to_excel(writer, sheet_name='MySheet1', index=False)
writer.close()  # Use 'close()' instead of 'save()'

print(f"Excel file '{output_file}' created successfully!")


##Definindo as Carteirs
fundamentalista_quantzed = [
    {'stock': 'BOVV11', 'percentage': 0.3},
    {'stock': 'ENAT3', 'percentage': 0.2},
    {'stock': 'JSLG3', 'percentage': 0.25},
    {'stock': 'PRIO3', 'percentage': 0.15},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    {'stock': 'SIMH3', 'percentage': 0.1},
    
]

# Create a dictionary to store multiple portfolios
carteiras = {
    'Fundamentalista Quantzed': fundamentalista_quantzed,
    # Add more portfolios as needed
}

# Access the Fundamentalista Quantzed portfolio
print(carteiras['Fundamentalista Quantzed'])


# Assume you have retrieved Client 1's stocks and their quantitiesz
client1_stocks = [
    {'stock': 'AAPL', 'quantity': 100},
    {'stock': 'GOOGL', 'quantity': 50},
    {'stock': 'MMM', 'quantity': 50},
    {'stock': 'ABEV3', 'quantity': 100},
    
    # Add more stocks as needed
]

# Fetch last available prices
def get_last_price(stock_symbol):
    try:
        # Try with ".SA" suffix first
        stock_symbol_sa = stock_symbol + '.SA'
        stock = yf.Ticker(stock_symbol_sa)
        history = stock.history(period='1d')['Close']
        if history.empty:
            raise ValueError("No data found for " + stock_symbol_sa)
        return history.iloc[0]
    except ValueError:
        # If there is an error, try without the ".SA" suffix
        stock = yf.Ticker(stock_symbol)
        history = stock.history(period='1d')['Close']
        if history.empty:
            raise ValueError("No data found for " + stock_symbol)
        return history.iloc[0]
    
# Calculate total value in Client 1's portfolio
total_value = 0
for stock_info in client1_stocks:
    stock_symbol = stock_info['stock']
    stock_quantity = stock_info['quantity']
    last_price = get_last_price(stock_symbol)
    total_value += stock_quantity * last_price

# Calculate current percentage for each stock
for stock_info in client1_stocks:
    stock_symbol = stock_info['stock']
    stock_quantity = stock_info['quantity']
    current_price = get_last_price(stock_symbol)
    current_value = stock_quantity * current_price
    current_percentage = (current_value / total_value) * 100

    # Check if the stock exists in Fundamentalista Quantzed
    fundamentalista_item = next((item for item in fundamentalista_quantzed if item['stock'] == stock_symbol), None)
    if fundamentalista_item:
        fundamentalista_percentage = fundamentalista_item['percentage'] * 100
    else:
        # Use a default percentage (e.g., 0%)
        fundamentalista_percentage = 0

    print(f"Stock {stock_symbol}:")
    print(f"  Current Price: ${current_price:.2f}")
    print(f"  Current Percentage: {current_percentage:.2f}%")
    print(f"  Fundamentalista Quantzed Percentage: {fundamentalista_percentage:.2f}%")
    print()  # Add a newline for readability

# Repeat the above steps for all stocks in Client 1's portfolio
# Adjust as needed based on your actual data and requirements

