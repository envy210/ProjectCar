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

# print(cmc.head())
#      Make      Model  Year  MaintenanceCostYearly
# 0     BMW         x3  2017                 607.20
# 1   SKODA      karoq  2018                 359.07
# 2  toyota      Hilux  2015                 655.78
# 3    audi        RS4  2015                 859.98
# 4     bmw   5 SERIES  2004                1264.16

fuelPricesandConversions = pd.read_excel('Fuel Prices and Conversions.xlsx')

# print(fuelPricesandConversions.head())
#      Fuel    Cost
# 0  Petrol  1.4251
# 1  Diesel  1.5090

# Inside of "Used Car Data" folder is a collection of datasets with model,year,price,transmission,mileage,fuelType,tax,mpg,engineSize

# I will start by reading the data from the folder
carDatasetNames = ['audi', 'bmw', 'ford', 'hyundai', 'merc', 'skoda', 'toyota', 'vauxhall', 'vw']

carDatasets = []
for car in carDatasetNames:
    carDatasets.append(pd.read_csv(f'Used Car Data (incl mpg)/{car}.csv'))

# print(carDatasets[0].head())
# Compile all cars into one dataset
allCars = pd.concat(carDatasets, ignore_index=True)

# print(allCars.head())
# Extend dataset with maintenance costs
# If the column in 'cmc' is called 'Model' (with capital 'M'):
cmc = cmc.rename(columns={'Model': 'model','Year':'year'})  # Make them consistent
allCars = allCars.merge(cmc, how='left', left_on=['model', 'year'], right_on=['model', 'year'])
allCars.insert(1, 'fuel_cost', allCars['MaintenanceCostYearly'].fillna(0))
allCars.insert(1, 'maintenance_cost', allCars['MaintenanceCostYearly'].fillna(0))
allCars.insert(1, 'total_cost', allCars['MaintenanceCostYearly'].fillna(0))

finalCars = {}
def calculate_cost(car_index, fuel_price, years):
    # Calculate the total estimated cost of buying a car and any costs associated with using it over the course of 5 years.
    # You should assume that the annual mileage of the car will be 8000 miles.
    # Display the results for each considered car variation and create recommendations for the cheapest options

    car_df = allCars.iloc[car_index].copy()
    # Calculate the fuel cost
    car_df['fuel_cost'] = (8000 / car_df['mpg']) * fuel_price * years
    
    # Calculate the maintenance cost
    car_df['maintenance_cost'] = car_df['MaintenanceCostYearly'] * years

    # Calculate the total cost
    car_df['total_cost'] = car_df['price'] + car_df['tax'] + car_df['fuel_cost'] + car_df['maintenance_cost']

    # Assign the calculated values back to the dataframe
    finalCars[car_df['model']] = car_df['total_cost']
    
print(allCars.head())
fuel_price = 1.4251
years = int(input("Enter the number of years to estimate costs for: "))

for i in range(len(allCars)):
    calculate_cost(i,fuel_price, years)  # No fuel_price argument anymore

# Sort results for better presentation
sorted_results = sorted(finalCars.items(), key=lambda item: item[1]) 

# Display top 3
print("\nTop 3 Most Cost-Effective Cars:")
for model, total_cost in sorted_results[:3]:
    print(f"{model}: Total Cost (5 years): £{total_cost:.2f}")

allCars.to_csv('car_cost_analysis_all_columns.csv', index=False) 