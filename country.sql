drop table if exists country;

CREATE TABLE country (
	country VARCHAR(100) NOT NULL, 
	region VARCHAR(100) NOT NULL, 
	population DECIMAL(38, 0) NOT NULL, 
	area_sq_miles DECIMAL(38, 0) NOT NULL, 
	population_density_per_sq_mile DECIMAL(38, 2) NOT NULL, 
	infant_mortality_per_1000 DECIMAL(38, 4), 
	gdp_usd_per_capita DECIMAL(38, 2), 
	literacy_percent DECIMAL(38, 2), 
	phones_per_1000 DECIMAL(38, 2), 
	birthrate DECIMAL(38, 2), 
	deathrate DECIMAL(38, 2)
);
