use bank_churn;
select * from customer_churn;

# 1.Find total exited and retained customers ?
select  case when Exited = 1 then 'yes' else 'No' end as exited_customers, count(*) as total_customers
from customer_churn group by Exited;

# 2. Find the churn rate ?
select round(sum(case when Exited=1 then 1 else 0 end)*100/count(*),2) as churn_rate from customer_churn;

# 3. Geography wise churn and churn rate
SELECT Geography,
       COUNT(*) AS Total_Customers,
       SUM(Exited) AS Exited_Customers,
       ROUND(SUM(Exited) * 100.0 / COUNT(*),2) AS Churn_Rate
FROM customer_churn
GROUP BY Geography
ORDER BY Churn_Rate DESC;

# 4. Churn by gender
SELECT Gender,
       COUNT(*) AS Total_Customers,
       SUM(Exited) AS Exited_Customers,
       ROUND(SUM(Exited) * 100.0 / COUNT(*),2) AS Churn_Rate
FROM customer_churn
GROUP BY Gender;

#5. Average balance of churned and retained customers
SELECT Exited,
       AVG(Balance) AS Average_Balance
FROM customer_churn
GROUP BY Exited;

#6 Active and Inactive customers churn rate ?
SELECT IsActiveMember,
       COUNT(*) AS Customers,
       SUM(Exited) AS Exited_Customers,
       ROUND(SUM(Exited) * 100.0 / COUNT(*),2) AS Churn_Rate
FROM customer_Churn
GROUP BY IsActiveMember;
