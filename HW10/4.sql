select Country.Name, count(City.Id) as cnt
from Country left join City on Country.Code == City.CountryCode and City.Population >= 1000 * 1000
group by Country.Name
order by cnt desc, Country.Name;
