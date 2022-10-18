import pandas as pd

df_ross = pd.read_csv("full_serum_with_ing.csv")

# Filter data with full ingredients list by using regex
df_ross_clean = df_ross[(
    (df_ross['ingredients'].str.contains(',.*,.*,.*,.*,.*', regex=True)) |
    (df_ross['ingredients'].str.contains('•.*•.*•.*•.*•.*', regex=True))) &
    (df_ross['size'].str.contains('ml'))
    ].reset_index(drop=True)

# Clear data with unnecessary marks and whitespaces
df_ross_clean['ingredients'] = df_ross_clean['ingredients'].str.lower().str.replace(' •',',', regex = True)
df_ross_clean['ingredients'] = df_ross_clean['ingredients'].str.lower().str.replace('.',', ', regex = False)
df_ross_clean['ingredients'] = df_ross_clean['ingredients'].str.lower().str.replace('*','', regex = False)
df_ross_clean['ingredients'] = df_ross_clean['ingredients'].str.lower().str.replace('^.*:','', regex = True)
df_ross_clean['ingredients'] = df_ross_clean['ingredients'].str.replace('(\s+)',' ', regex = True)
df_ross_clean['ingredients'] = df_ross_clean['ingredients'].str.replace('(^\s+)','', regex = True)

# Rename ingredients
df_ross_clean['ingredients'] = df_ross_clean['ingredients'].str.replace('(water.*?,)|(aqua.*?,)','water,', regex = True)

# Prepare data and split ingredients from string to list
df_ross_clean['ing_list'] = 1
ing_list = []
for i in range(len(df_ross_clean['ingredients'])):
    df_ross_clean['ing_list'][i] = df_ross_clean['ingredients'][i].split(', ')
    df_ross_clean['ing_list'][i] = [ing for ing in df_ross_clean['ing_list'][i] if len(ing) != 0]
    for j in df_ross_clean['ing_list'][i]:
        if len(j) <= 3:
            df_ross_clean['ing_list'][i].remove(str(j))
    ing_list += df_ross_clean['ing_list'][i]

ing_list = sorted(list(set(ing_list)))

# Change price and size to float type and create new column "price per 100ml"
for i in range(len(df_ross_clean['size'])):
    df_ross_clean['price'][i] = float(df_ross_clean['price'][i].replace(' zł','').replace(',','.'))
    df_ross_clean['size'][i] = df_ross_clean['size'][i].replace('ml','').replace(',','.')
    if 'x' in df_ross_clean['size'][i]:
        df_ross_clean['size'][i] = (float(df_ross_clean['size'][i].split('x')[0])) * (float(df_ross_clean['size'][i].split('x')[1]))
    else: df_ross_clean['size'][i] = float(df_ross_clean['size'][i])

df_ross_clean['price per 100ml'] = (df_ross_clean.price / df_ross_clean.size) * 100


print((ing_list))
print(len(ing_list))



