select * from cleaned_churn;

# Total Number Of Customers Within The Dataset
select Count(*) As Total_Customer 
from cleaned_churn;


# Total Number of Customers Who Churned 
select Count(*) as Churned_customer
from cleaned_churn
where `Churn Label` = 'Yes';

# Customer As per Contract Type
select contract,count(*) as Customer
from cleaned_churn
group by contract;

# Churn Customer As per Contract Type 
select contract,Count(*) as Churn_As_Per_Type
from cleaned_churn
where `Churn Label` = 'Yes'
group by contract
order by Churn_As_Per_Type;





























































































