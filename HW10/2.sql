select Country.Name, LiteracyRate.Rate
from Country inner join LiteracyRate on Country.Code == LiteracyRate.CountryCode
group by LiteracyRate.CountryCode
having LiteracyRate.Year == max(LiteracyRate.Year)
order by LiteracyRate.Rate desc
limit 1;
