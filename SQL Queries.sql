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

# Churn By Tech Support
select Count(*) as Total_Customers,`Tech Support`,
round(avg(`Churn Value`)*100,2) as Churn_rate_By_Tech_Support
from cleaned_churn
where `Tech Support` <> 'No'
Group by `Tech Support` ;
 
# Churn By Paper Billing 

select `Paperless Billing`, Count(*) as Total_Customers,
sum(`Churn Value`) as Churned,
round(avg(`Churn Value`)* 100,2) AS Churn_rate_by_Billing
from cleaned_churn
group by `Paperless Billing`;


# Churn By Contract And Internet 
select * from cleaned_churn;
select Contract , `Internet Service`, count(*) as Total_customer,
	round(Avg(`Churn Value`)*100, 2) as Customer_Churned
	from cleaned_churn
	group by Contract, `Internet Service`
    order by Customer_Churned DESC;


# Top Cities With Churn Rate
select * from cleaned_churn;
select `City`,
count(*) as Total_Customers,
sum(`Churn Value`) as churned,
round(avg(`Churn Value`)*100,2) as Churned_rate_by_City
from cleaned_churn
group by City
having count(*) >=20
order by Churned_rate_by_City Desc;

#Customer with Higher Risk
select CustomerID, City, Contract, `Monthly Charges`, `Churn Score`, CLTV
from cleaned_churn
where `Churn Label` = 'No'
AND `Churn Score` >=70
AND Contract = 'Month-to-Month'
order by CLTV;

 # Contract Type With Above Average Churn
 select Contract,
count(*) as Total_Customers,
sum(`Churn Value`) as Churned,
round(avg(`Churn Value`)*100,2) as Churn_rate
from cleaned_churn
group by Contract
having avg(`Churn Value`)> (Select avg(`Churn Value`) from cleaned_churn);

#Churn Rate As Per City
WITH city_churn AS (
    SELECT City,
           COUNT(*) AS total_customers,
           ROUND(AVG(`Churn Value`) * 100, 2) AS churn_rate_pct
    FROM cleaned_churn
    GROUP BY City
    HAVING COUNT(*) >= 20
)
SELECT City, total_customers, churn_rate_pct,
       RANK() OVER (ORDER BY churn_rate_pct DESC) AS churn_rank
FROM city_churn
LIMIT 10;














































































