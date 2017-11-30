select Country.Name
from Country left join City on Country.Code == City.CountryCode
group by Country.Code
having 2 * coalesce(0, sum(City.Population)) < Country.Population
order by Country.Name;