from sklearn.linear_model import LinearRegression

# Using UK government's conversion factors:
# https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2020

train_jrny_CO2 = {}
train_jrny_CO2[2020] =  0.03659
train_jrny_CO2[2019] =  0.04077
train_jrny_CO2[2018] =  0.04383
train_jrny_CO2[2017] =  0.04636
train_jrny_lr = LinearRegression().fit([[key] for key in train_jrny_CO2.keys()], [val for val in train_jrny_CO2.values()])

short_haul_CO2 = {}
short_haul_CO2[2020] =  0.08145
short_haul_CO2[2019] =  0.08291
short_haul_CO2[2018] =  0.08503
short_haul_CO2[2017] =  0.08432
short_haul_CO2[2016] =  0.08821
short_haul_lr = LinearRegression().fit([[key] for key in short_haul_CO2.keys()], [val for val in short_haul_CO2.values()])

long_haul_CO2 = {}
long_haul_CO2[2020] =  0.09994
long_haul_CO2[2019] =  0.10244
long_haul_CO2[2018] =  0.11131
long_haul_CO2[2017] =  0.1034
long_haul_CO2[2016] =  0.10035
long_haul_lr = LinearRegression().fit([[key] for key in long_haul_CO2.keys()], [val for val in long_haul_CO2.values()])


def distance_to_emissions(distance, year):
    if distance < 500:
        CO2 = distance * train_jrny_lr.predict([[year]])
    elif distance < 3700:
        CO2 = distance * short_haul_lr.predict([[year]])
    else:
        CO2 = distance * long_haul_lr.predict([[year]])
    return CO2