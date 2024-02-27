import pandas as pd

cmc = pd.read_csv('Car Maintenance Costs.csv')
# If the column in 'cmc' is called 'Model' (with capital 'M'):
cmc = cmc.rename(columns={'Model': 'model','Year':'year'})  # Make them consistent
cmc['model'] = cmc['model'].str.strip().str.lower()

# print(cmc.head())
#      Make      Model  Year  MaintenanceCostYearly
# 0     BMW         x3  2017                 607.20
# 1   SKODA      karoq  2018                 359.07
# 2  toyota      Hilux  2015                 655.78
# 3    audi        RS4  2015                 859.98
# 4     bmw   5 SERIES  2004                1264.16

# Read the fuel prices and conversions
fuelPricesandConversions = pd.read_excel('Fuel Prices and Conversions.xlsx', sheet_name='Fuel Costs')
#gallon to litre conversion
fuelPricesandConversions2 = pd.read_excel('Fuel Prices and Conversions.xlsx', sheet_name='Conversions')

carDatasetNames = ['audi', 'bmw', 'ford', 'hyundai', 'merc', 'skoda', 'toyota', 'vauxhall', 'vw']

carDatasets = []
for car in carDatasetNames:
    carDatasets.append(pd.read_csv(f'Used Car Data (incl mpg)/{car}.csv'))


# Compile all cars into one dataset
allCars = pd.concat(carDatasets, ignore_index=True)

allCars['model'] = allCars['model'].str.strip().str.lower()
# Extend dataset with maintenance costs
allCars = allCars.merge(cmc, how='inner', left_on=['model', 'year'], right_on=['model', 'year'])

# Data Cleaning
allCars['Make'] = allCars['Make'].str.title()

# Pre-fill with defaults
allCars['fuel_cost'] = 0.0
allCars['maintenance_cost'] = 0.0
allCars['total_cost'] = 0.0

# Missing Maintenance Handling
allCars.fillna({'MaintenanceCostYearly': 0}, inplace=True)  


# Reorder columns 
desired_order = ['Make', 'model', 'year', 'transmission', 'fuelType', 'mileage', 'price', 'engineSize', 'mpg', 'tax', 'maintenance_cost', 'fuel_cost', 'MaintenanceCostYearly', 'total_cost']  # Specify your desired order
allCars = allCars.reindex(columns=desired_order)

def calculate_cost(car_index, gallon, years, mileage):
    # Calculate the total estimated cost of buying a car and any costs associated with using it over the course of 5 years.
    # You should assume that the annual mileage of the car will be 8000 miles.
    # Display the results for each considered car variation and create recommendations for the cheapest options

    car_df = allCars.iloc[car_index].copy()
    # Calculate the fuel cost
    if car_df['fuelType'] == 'Petrol':
        petrol_row_index = fuelPricesandConversions[fuelPricesandConversions['Fuel'] == 'Diesel'].index[0]
        petrol_price = fuelPricesandConversions.loc[petrol_row_index, 'Cost']
        car_df['fuel_cost'] = (mileage / car_df['mpg']) * petrol_price * gallon * years
        allCars.at[car_index, 'fuel_cost'] = car_df['fuel_cost']
    elif car_df['fuelType'] == 'Diesel':
        diesel_row_index = fuelPricesandConversions[fuelPricesandConversions['Fuel'] == 'Diesel'].index[0]
        diesel_price = fuelPricesandConversions.loc[diesel_row_index, 'Cost']
        car_df['fuel_cost'] = (mileage / car_df['mpg']) * diesel_price * gallon * years
        allCars.at[car_index, 'fuel_cost'] = car_df['fuel_cost']
    else:
        car_df['fuel_cost'] = (mileage / car_df['mpg']) * gallon * years
        allCars.at[car_index, 'fuel_cost'] = car_df['fuel_cost'] 
    
    # Calculate the maintenance cost
    car_df['maintenance_cost'] = car_df['MaintenanceCostYearly'] * years
    car_df['tax'] = car_df['tax'] * years
    allCars.at[car_index, 'maintenance_cost'] = car_df['maintenance_cost']

    # Calculate the total cost
    car_df['total_cost'] = car_df['price'] + car_df['tax'] + car_df['fuel_cost'] + car_df['maintenance_cost']
    allCars.at[car_index, 'total_cost'] = car_df['total_cost']

    return car_df
    
print(allCars.head())
print()
years = int(input("Enter the number of years to estimate costs for: "))
mileage = int(input("Enter the annual mileage: "))

# liters in gallon
gallon = fuelPricesandConversions2.loc[0, 'Litres']


for i in range(len(allCars)):
    updated_car_df = calculate_cost(i, gallon, years, mileage)


# Sort results for better presentation
sorted_results = sorted(allCars[['Make', 'model','year', 'transmission', 'fuelType', 'engineSize','mileage','total_cost']].itertuples(index=False), key=lambda item: item[7]) 

# Display top 3
print()
print("\nTop 3 Most Cost-Effective Cars:")
print()
for make, model, year, transmission, fuelType, engineSize, mileage, total_cost in sorted_results[:3]:
    print(f"{make}  {model}  {year}  {transmission}  {fuelType}  Engine Size: {engineSize}  Mileage : {mileage}:- Total Cost (5 years): £{total_cost:.2f}")

allCars.to_csv('car_cost_analysis_all_columns.csv', index=False) 