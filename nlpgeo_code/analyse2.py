import pandas
from geopy.distance import geodesic
from utils.gMapsQuery import initGeo, getCoordsfromName, getLocationfromName
from utils.giniCoeff import giniCoeff

volumes_df = pandas.read_csv("volumes-ref.tsv", sep="\t", header=None,
                             names=["Volume", "Title", "Year", "Location", "Longitude", "Latitude"])

cachePath = './'
initGeo(cachePath)

for i in volumes_df.index:
    coords = getCoordsfromName(volumes_df.Location[i])
    volumes_df.at[i, "Longitude"] = coords[0]
    volumes_df.at[i, "Latitude"] = coords[1]

papers_df = pandas.read_csv("papers-ref.tsv", sep="\t", header=None,
                            names=["Volume", "Volume_id", "Email", "Domain", "Location", "Longitude", "Latitude"])
print(len(papers_df))

drop_rows = papers_df[papers_df.Longitude == 0]
papers_df = papers_df.drop(drop_rows.index)
print(len(papers_df))
locations_df = pandas.merge(left=papers_df, right=volumes_df, how="inner", on="Volume",
                            suffixes=["_papers", "_volumes"])
print(len(papers_df))

for i in locations_df.index:
    if locations_df.Location_volumes[i] == "@":
        locations_df.at[i, "Distance"] = 0
    else:
        locations_df.at[i, "Distance"] = geodesic((locations_df.Longitude_papers[i], locations_df.Latitude_papers[i]), (
        locations_df.Longitude_volumes[i], locations_df.Latitude_volumes[i])).km

# calculate emissions - based on spreadsheet at: https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2020

# Assumptions / Notes:
# 1) all journeys are via plane
# 2) journeys less than 3700Km are 'short haul'
# 3) journeys over 3700Km are 'long haul'
# 4) the 'average' passenger is representative of those travelling to a conference (e.g., mix of economy and business class)
# 5) using without_rf figures as this is apparently somewhat speculative
# 6) unit is  KGCO2 per passenger per km. So pultiplying by kms in the journey tell us how many KGs of Co2 that specific passenger used.
# 7) these figures are based on aviation in 2020 - so they are likely less representative of air travel going backwards in time. Numbers  are available back to 2002, so we could look back in time, but not back to  80's, etc.
# 8) train journeys are 'national rail KGCO2'

from sklearn.linear_model import LinearRegression
import numpy as np

# conversion factors
train_jrny_CO2 = {}
train_jrny_CO2[2020] = 0.03659
train_jrny_CO2[2019] = 0.04077
train_jrny_CO2[2018] = 0.04383
train_jrny_CO2[2017] = 0.04636
train_jrny_lr = LinearRegression().fit([[key] for key in train_jrny_CO2.keys()],
                                       [val for val in train_jrny_CO2.values()])

short_haul_CO2 = {}
short_haul_CO2[2020] = 0.08145
short_haul_CO2[2019] = 0.08291
short_haul_CO2[2018] = 0.08503
short_haul_CO2[2017] = 0.08432
short_haul_CO2[2016] = 0.08821
short_haul_lr = LinearRegression().fit([[key] for key in short_haul_CO2.keys()],
                                       [val for val in short_haul_CO2.values()])

long_haul_CO2 = {}
long_haul_CO2[2020] = 0.09994
long_haul_CO2[2019] = 0.10244
long_haul_CO2[2018] = 0.11131
long_haul_CO2[2017] = 0.1034
long_haul_CO2[2016] = 0.10035
long_haul_lr = LinearRegression().fit([[key] for key in long_haul_CO2.keys()], [val for val in long_haul_CO2.values()])

def distance_to_emissions(distance, year):
    if distance < 500:
        CO2 = distance * train_jrny_lr.predict([[year]])
    elif distance < 3700:
        CO2 = distance * short_haul_lr.predict([[year]])
    else:
        CO2 = distance * long_haul_lr.predict([[year]])
    
    return CO2


for i in locations_df.index:
    locations_df.at[i, 'CO2'] = distance_to_emissions(locations_df.Distance[i], locations_df.Year[i])

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cycler import cycler


def get_fig(locations_subset_df, conf, year):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    
    ax.stock_img()
    ax.coastlines()
    
    for i in locations_subset_df.index:
        lon_from = locations_subset_df.Longitude_papers[i]
        lat_from = locations_subset_df.Latitude_papers[i]
        lon_to = locations_subset_df.Longitude_volumes[i]
        lat_to = locations_subset_df.Latitude_volumes[i]
        if not (lon_from == 0 and lat_from == 0):
            if not (lon_to == 0 and lat_to == 0):
                ax.plot([lat_from, lat_to], [lon_from, lon_to], color='red', transform=ccrs.Geodetic())
    
    #    plt.show()
    plt.savefig("./Maps/" + conf + "/" + str(year) + "-" + conf + ".pdf")

ACL = [r"P\d\d\.\d", r"2020\.acl\.main"]
EMNLP = [r"D\d\d\.[123]", r"2020\.emnlp\.main"]
COLING = [r"C\d\d\.\d", r"2020\.coling\.main"]
CoNLL = [r"K\d\d\.\d", r"2020\.conll\.1"]

NAACL = [r"N\d\d\.\d"]
LREC = [r"L\d\d\.\d", r"2020\.lrec\.1"]

EACL = [r'E\d\d\.\d']
TALN = [r'F\d\d\.\d', '\d\d\d\d\.jeptalnrecital\..*']
RANLP = [r'R\d\d\.\d']
IJCNLP = [r'I\d\d\.\d', "P15", "D19"]
ALTA = [r'U\d\d\.\d']
PACLIC = [r'Y\d\d\.\d']
ROCLING = [r'O\d\d\.\d']
NoDaLiDa = [r'W11\.46', r'W13\.56', r'W15\.18', r'W17\.2$', r'W19\.61']


# acl = "Annual Meeting of the Association for Computational Linguistics"
# emnlp = "Empirical Methods in Natural Language Processing"
# eacl = "European Chapter"
# naacl = " North American Chapter"
# lrec = "LREC"
# coling = "International Conference on Computational Linguistics"
# nodalida = "Nordic Conference"

def get_df(volume_re):
    df = pandas.DataFrame()
    for re in volume_re:
        df = df.append(locations_df[locations_df.Volume.str.match(re)])
    return df


def getEmissionGraph(volume_re, title):
    sub_df = get_df(volume_re)
    years = sorted([i if i >= 2010 and i < 2020 else 0 for i in sub_df.Year.unique().tolist()])
    points = {}
    for year in years:
        points[year] = getEmissions(sub_df, year)
    plt.plot(points.keys(), points.values(), label=title)
    #    color = plt.cm.tab20(np.linspace(0, 1,20))
    color = ['r', 'g', 'b', 'y']
    plt.rc('axes', prop_cycle=(cycler('color', color)))
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=4, mode="expand", borderaxespad=0.)
    plt.xlabel("Year")
    plt.ylabel("Mean CO2")


def getEmissions(sub_df, year):
    return sub_df[sub_df.Year == year].CO2.mean()


def getTotalEmissions(sub_df, year):
    return sub_df[sub_df.Year == year].CO2.sum()


getEmissionGraph(ACL, "ACL")
getEmissionGraph(EMNLP, "EMNLP")
getEmissionGraph(COLING, "COLING")
getEmissionGraph(CoNLL, "CoNLL")

getEmissionGraph(NAACL, "NAACL")
getEmissionGraph(LREC, "LREC")
getEmissionGraph(EACL, "EACL")
getEmissionGraph(IJCNLP, "IJCNLP")

getEmissionGraph(TALN, "TALN")
getEmissionGraph(RANLP, "RANLP")
getEmissionGraph(ALTA, "ALTA")
getEmissionGraph(PACLIC, "PACLIC")
getEmissionGraph(ROCLING, "ROCLING")
getEmissionGraph(NoDaLiDa, "NoDaLiDa")

# %%

international_confs = []
international_confs.extend(ACL)
international_confs.extend(EMNLP)
international_confs.extend(COLING)
international_confs.extend(CoNLL)

regional_confs = []
regional_confs.extend(NAACL)
regional_confs.extend(LREC)
regional_confs.extend(EACL)
regional_confs.extend(IJCNLP)

local_confs = []
local_confs.extend(TALN)
local_confs.extend(RANLP)
local_confs.extend(ALTA)
local_confs.extend(PACLIC)
local_confs.extend(ROCLING)
local_confs.extend(NoDaLiDa)

all_confs = []
all_confs.extend(international_confs)
all_confs.extend(regional_confs)
all_confs.extend(local_confs)

getEmissionGraph(international_confs, "International")
getEmissionGraph(regional_confs, "Regional")
getEmissionGraph(local_confs, "Local")

def getFigSeries(conf_df, name):
    print(name)
    years = sorted([i for i in conf_df.Year.unique().tolist() if i < 2020])
    for year in years:
        print(year)
        get_fig(conf_df[conf_df.Year == year], name, year)


getFigSeries(get_df(ACL), "ACL")
# getFigSeries(get_df(EMNLP), "EMNLP")
# getFigSeries(get_df(COLING), "COLING")
# getFigSeries(get_df(CoNLL), "CoNLL")

# getFigSeries(get_df(NAACL), "NAACL")
# getFigSeries(get_df(LREC), "LREC")
# getFigSeries(get_df(EACL), "EACL")
# getFigSeries(get_df(IJCNLP), "IJCNLP")

# getFigSeries(get_df(TALN), "TALN")
# getFigSeries(get_df(RANLP), "RANLP")
# getFigSeries(get_df(ALTA), "ALTA")
# getFigSeries(get_df(PACLIC), "PACLIC")
# getFigSeries(get_df(ROCLING), "ROCLING")
# getFigSeries(get_df(NoDaLiDa), "NoDaLiDa")

df = get_df(ACL)
df[(df.Latitude_papers == 0)]


df = get_df([".*"])

years_avg_emissions = {}
for year in range(1960, 2020):
    emissions = getEmissions(df, year)
    if emissions > 0:
        years_avg_emissions[year] = emissions

years_total_emissions = {}
for year in range(1970, 2020):
    emissions = getTotalEmissions(df, year)
    if emissions > 0:
        years_total_emissions[year] = emissions

# plt.plot(years_avg_emissions.keys(),years_avg_emissions.values())
# plt.plot(years_total_emissions.keys(),years_total_emissions.values())

# Create some mock data
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Year')
ax1.set_ylabel('Total CO2 Emissions (KG)', color=color)
ax1.plot(years_total_emissions.keys(), years_total_emissions.values(), color=color)
# ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Average CO2 Emissions (KG)', color=color)  # we already handled the x-label with ax1
ax2.plot(years_avg_emissions.keys(), years_avg_emissions.values(), color=color)
# ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.savefig("./Emissions.pdf")

# %%

get_df([".*"])

# %%

df_grouped = locations_df.groupby("Email").max("CO2").sort_values("CO2")

# %%

locations_df[["Email", "CO2"]].groupby("Email").sum().sort_values("CO2", ascending="false").tail(30)

import qgrid

qgrid.show_grid(locations_df)

# %%

import pycountry_convert


# %%

def getCountryCode(location):
    for data in location[0]['address_components']:
        if 'country' in data['types']:
            return pycountry_convert.country_name_to_country_alpha2(data['long_name'], cn_name_format="default")


for i in locations_df.index:
    if locations_df.Location_volumes[i] == '@':
        locations_df.at[i, 'Continent_volumes'] = '@'
    else:
        location = getLocationfromName(locations_df.Location_volumes[i])
        code = getCountryCode(location)
        locations_df.at[i, 'Continent_volumes'] = pycountry_convert.country_alpha2_to_continent_code(code)

# %%

for i in locations_df.index:
    if locations_df.Location_papers[i] == '?' or locations_df.Location_papers[i] == '':
        locations_df.at[i, 'Country_paper'] = '?'
    else:
        try:
            location = getLocationfromName(locations_df.Location_papers[i])
            code = getCountryCode(location)
            locations_df.at[i, 'Country_paper'] = code
        except:
            print("unable to find country for: " + locations_df.Location_papers[i])
            locations_df.at[i, 'Country_paper'] = '?'

array = locations_df.Continent_volumes.value_counts().to_numpy()
giniCoeff(array)


num_countries = len(locations_df.Country_paper.value_counts())

continents = locations_df.Continent_volumes.value_counts().index.to_numpy()
continents = np.delete(continents, [5])
for continent in continents:
    sub_df = locations_df[(locations_df.Continent_volumes == continent)]
    years = sub_df.Year.value_counts().index.to_numpy()
    plot = {}
    for year in sorted(years):
        if year >= 1960 and year < 2020:
            small_array = sub_df[sub_df.Year == year].Country_paper.value_counts().to_numpy()
            new_array = np.zeros(num_countries)
            new_array[:small_array.shape[0]] = small_array
            plot[year] = 1 - giniCoeff(new_array)
    color = plt.cm.tab10(np.linspace(0, 1, 10))
    plt.rc('axes', prop_cycle=(cycler('color', color)))
    plt.plot(plot.keys(), plot.values(), label=continent)

plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=3, mode="expand", borderaxespad=0.)
plt.xlabel("Year")
plt.ylabel("Diversity")
plt.show()


sorted(plot)


giniCoeff(sub_df[sub_df.Year == year].Country_paper.value_counts().to_numpy())

import numpy as np

small_array = sub_df[sub_df.Year == year].Country_paper.value_counts().to_numpy()
new_array = np.zeros(129)
new_array[:small_array.shape[0]] = small_array

new_array


len(locations_df.Country_paper.value_counts())


locations_df[locations_df.Continent_volumes == "AF"]


for year in range(1976, 2020):
    print(year, end="")
    for conf in ["ACL", "EMNLP", "COLING", "CoNLL", "NAACL", "LREC", "EACL", "IJCNLP", "TALN", "RANLP", "ALTA",
                 "PACLIC", "ROCLING", "NoDaLiDa"]:
        print(" & \includegraphicsmaybe{Maps/%s/%i-%s.pdf} " % (conf, year, conf))
    print(r"\\")
