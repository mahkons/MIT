select City.Name, City.Population, Country.Population
from Country inner join City on Country.Code == City.CountryCode
order by cast(City.Population as float) / cast(Country.Population as float) desc, City.Name desc
limit 20;