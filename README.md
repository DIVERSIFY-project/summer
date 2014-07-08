summer
======

Some Urban Maps Made Reliable

GitHub projects that are required
----------------------------------

* GraphHopper
 - https://github.com/graphhopper/graphhopper.git 

* Jedis
 - https://github.com/xetorthio/jedis.git

Tools that we rely on
---------------------

* OSM
 - Download the smallest regional map that covers the city of interest

* Osmosis
 - Install osmosis
 - Extract the desired city from the downloaded OSM Map

* Postgresql/Postgis
 - Read the install steps for postgres/postgis
 - Create and configure the database
 - Import the extracted OSM map into the database using osmosis (or other tools 
   like osm2pgsql)

* Redis
 - Download and install Redis


