# The Challenge

# Adam wants to buy his first car but he doesn't have a lot of
# money and he is looking for the most cost-effective option
# on the market.

# He is thinking long term and considering not only the cost
# of buying the car, but also the cost of using it over the
# course of 5 years.

# Help him decide by creating a list of car brand and models
# with their cost estimates.

# The Data
# The following data is provided. You should be able to complete the challenge using it:
# . A collection of datasets with car prices, their tax cost and mpg (miles per gallon) by the car brand and
# specifications
# . A dataset with car maintenance costs by the brand, model and year
# . A look-up table with petrol and diesel costs and Gallon to Litre conversion

# Outcomes: Easier Version
# Calculate the total estimated cost of buying a car and any costs associated with using it over the course of 5
# years.
# You should assume that the annual mileage of the car will be 8000 miles.
# Display the results for each considered car variation and create recommendations for the cheapest options

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

fuelPricesandConversions = pd.read_excel('Fuel Prices and Conversions.xlsx')


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

def calculate_cost(car_index, fuel_price, years):
    # Calculate the total estimated cost of buying a car and any costs associated with using it over the course of 5 years.
    # You should assume that the annual mileage of the car will be 8000 miles.
    # Display the results for each considered car variation and create recommendations for the cheapest options

    car_df = allCars.iloc[car_index].copy()
    # Calculate the fuel cost
    car_df['fuel_cost'] = (8000 / car_df['mpg']) * fuel_price * years
    allCars.at[car_index, 'fuel_cost'] = car_df['fuel_cost']
    
    # Calculate the maintenance cost
    car_df['maintenance_cost'] = car_df['MaintenanceCostYearly'] * years
    allCars.at[car_index, 'maintenance_cost'] = car_df['maintenance_cost']

    # Calculate the total cost
    car_df['total_cost'] = car_df['price'] + car_df['tax'] + car_df['fuel_cost'] + car_df['maintenance_cost']
    allCars.at[car_index, 'total_cost'] = car_df['total_cost']

    return car_df
    
print(allCars.head())
fuel_price = 1.4251
years = int(input("Enter the number of years to estimate costs for: "))

for i in range(len(allCars)):
    updated_car_df = calculate_cost(i, fuel_price, years)


# Sort results for better presentation
sorted_results = sorted(allCars[['model', 'total_cost']].itertuples(index=False), key=lambda item: item[1]) 

# Display top 3
print("\nTop 3 Most Cost-Effective Cars:")
for model, total_cost in sorted_results[:3]:
    print(f"{model}: Total Cost (5 years): £{total_cost:.2f}")

allCars.to_csv('car_cost_analysis_all_columns.csv', index=False) 