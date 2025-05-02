import pandas as pd
import matplotlib.pyplot as plt
#%% Import the csv

file_path = './portfolio/Portfolio.csv'

df = pd.read_csv(file_path, delimiter=',', decimal=',')
df = df.rename({'Aantal': 'Quantity', 'Slotkoers': 'Actual Price', 'Lokale waarde': 'Price in USD/EUR', 'Waarde in EUR': "Price in EUR"}, axis='columns')
df = df.sort_values(by='Price in EUR', ascending=False)

print(df)
print('Portfolio acquired')

#%% Plot  Portfolio composition
fig, ax = plt.subplots(figsize=(20, 8))
labels = [f'{prod} (€{val:,.2f})' for prod, val in zip(df['Product'], df['Price in EUR'])]
wedges, texts, autotexts = ax.pie(df['Price in EUR'], autopct='%1.1f%%', startangle=90, counterclock=False)
ax.legend(wedges, labels, title="Products", loc="center left", bbox_to_anchor=(0.8, 0, 0.5, 1))
plt.title('Portfolio assets')
plt.axis('equal')  
plt.savefig('./charts/piechart.png')
# plt.show()
