select GovernmentForm, sum(SurfaceArea) as Surface
from Country
group by GovernmentForm
order by Surface desc
limit 1;