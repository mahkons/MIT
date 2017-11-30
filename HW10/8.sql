select Country.Name, Country.Population, Country.SurfaceArea
from (Country inner join City on Country.Code == City.CountryCode)
left join Capital on Country.Code == Capital.CountryCode
group by Country.Code
having max(City.Population) == City.Population and not City.Id == Capital.CityId
order by cast(Country.Population as float) / cast(Country.SurfaceArea as float) desc, Country.Name;
