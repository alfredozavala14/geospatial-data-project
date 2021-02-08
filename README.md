![Old map](https://www.antiquemapsandprints.com/ekmps/shops/richben90/images/-Plan-de-la-Ville-de-Nangasaki-.-Nagasaki-Japan.-BELLIN-SCHLEY-1756-old-map-406418-p.jpg)

# Geospatial-data-project

## Introduction

For the third weekly project in the data bootcamp, we have to identify the ideal location for the office of a new company given certain conditions (eg. 30% of the company staff have at least 1 child).
Using a database with over 18_000 companies and the forusquare API to access information for different venues, the objective is to find a location that works for as many employees as possible.
I have selected the San Francisco Bay Area as a first area to analyze because of the large number of companies located there and the vibrant cultural life, all of which are likely to offer more possibilities for employees.

## Libraries used

During the project, I have used the following libraries:
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/doc/1.18/)
- [Pymongo](https://pymongo.readthedocs.io/en/stable/)
- [Folium](https://python-visualization.github.io/folium/)
- [Dotenv](https://www.npmjs.com/package/dotenv)
- [Requests](https://requests.readthedocs.io/en/master/)
- [Os](https://docs.python.org/3/library/os.html)
- [Json](https://docs.python.org/3/library/json.html)
- [Functools](https://docs.python.org/3/library/functools.html)
- [Haversine](https://pypi.org/project/haversine/)

## Work done

First, I have created a collection in mongo that contains each individual office included in the companies database. THis way I could use the locations of existing offices as potential candidates for the new office.
Next I have plotted these offices in a heatmap to identify the location in the Bay Area with a higher number of offices.
Then I have dowloaded information from the Foursquare API to locate different types of venues.
After that, I have calculated distances between offices in the city of San Francisco and each of the different types of venues. Then I have given weights to each type of venue and assigned points depending on weather certain types of venues in a 0.75 km range from each office.
Finally, I have chosen the best location for the office and plotted the venues that are nearby in a folium map.

## Deliverables

There is one main deliverable, a jupyer notebook where I have done my search and ended up with a selected location for the new office.
Additionally, there is a .py file containing the functions I have developed and used throughout the project