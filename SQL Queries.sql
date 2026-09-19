select * from cleaned_churn;

# Total Number Of Customers Within The Dataset
select Count(*) As Total_Customer 
from cleaned_churn;


# Total Number of Customers Who Churned 
select Count(*) as Churned_customer
from cleaned_churn
where `Churn Label` = 'Yes';

#Overall Churn Rate 
select count(*) as Total_customers,
sum(`Churn Value`) as Churned_customer,
round(sum(`Churn Value`) *100/ count(*),2) as Overall_Churn_rate
from cleaned_churn;



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

select `Churn Value` from cleaned_churn;

#Churn Rate As Per Contract 
select contract, count(*) as total_Customer,
sum(`Churn Value`) as Churn,
round(avg(`Churn Value`)*100,2) as Churn_Rate_By_Contract
from cleaned_churn
group by contract 
order by Churn_Rate_By_Contract;

#Churn Rate As per Citizen And Gender 
select Gender , `Senior Citizen`,
count(*) as Total_Customers,
round(avg(`Churn Value`)*100,2)as Churn_Rate_By_Citizen_Gender
from cleaned_churn
group by Gender, `Senior Citizen`
order by Churn_Rate_By_Citizen_Gender;

# Churn Rate By Internet Service
SELECT `Internet Service`,
       COUNT(*) AS total_customers,
       ROUND(AVG(`Churn Value`) * 100, 2) AS churn_rate_by_IS
FROM cleaned_churn
GROUP BY `Internet Service`
ORDER BY churn_rate_by_IS;


# Churn Rate By Payment Method
SELECT `Payment Method`,
       COUNT(*) AS total_customers,
       ROUND(AVG(`Churn Value`) * 100, 2) AS churn_rate_by_PM
FROM cleaned_churn
GROUP BY `Payment Method`
ORDER BY churn_rate_by_PM DESC;



























































































