

# Predicting Superstore Revenue

by Scott Mattes

***
[[Project Description](#description)]
[[Project Planning](#goals)]
[[Hypotheses](#hypotheses)]
[[Deliverables](#deliverables)]
[[Key Findings](#findings)]
[[The Plan](#plan)]
[[Data Dictionary](#dictionary)]
[[Data Acquisition and Prep](#wrangle)]
[[Data Exploration](#exploration)]
[[Statistical Analysis](#stats)]
[[Modeling](#model)]
[[Steps to Reproduce](#reproduction)]
[[Takeaways and Conclusions](#conclusions)]
[[Recommendations](#recommendations)]
[[Next Steps](#next_steps)]
___


# <a name="description"></a>Project Description
[[Back to top](#top)]

The Predcting Superstore Revenue project aims to build a predictive model for the company's overall sales volume over the next quarter using time-series analysis. While this data is synthetic, it was made by the authors to mimick real world revenue behavior. The data used for this project was acquired from Kaggle.com and contains information on nationwide sales transactions at Superstore. The goal of this project is to develop a reliable forecasting model that can help the company make informed decisions and plan for future sales.

A slide deck presentation of this project can be found here: https://www.canva.com/design/DAFqhactfsM/v2jvdfK6jTAwm_egV-SK_Q/edit?utm_content=DAFqhactfsM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

# <a name="goals"></a>Project Planning
[[Back to top](#top)]

The main goals of this project are as follows:
- Explore and understand the dataset, identifying key patterns and trends.
- Perform time-series analysis to uncover seasonality and autocorrelation in the sales data.
- Develop a predictive model that outperforms the baseline (47-week Rolling Average model) in forecasting sales revenue.
- Assess the impact of different features on sales volume and identify the most relevant predictors.
- Provide actionable insights and recommendations based on the findings.

# <a name="hypotheses"></a>Hypotheses
[[Back to top](#top)]

1. The sales data will exhibit strong seasonality patterns due to the behavior of the marketat different time periods.
2. This seasonality will lend predictive power which will allow a time-series model to outperform baseline predictions.

# <a name="deliverables"></a>Expected Deliverables
[[Back to top](#top)]

A repository containing:
- Jupyter Notebook containing the entire data analysis process, including data exploration, statistical analysis, and model building.
- A trained time-series model.

# <a name="findings"></a>Key Findings
[[Back to top](#top)]

- The south region produces about half as many sales as the west region.
- California, New York, Texas, and Washington are the highest selling states.
- The 'consumer' category generates more sales than corporate and home office.
- Weekly sampled sales data displays clear seasonality and autocorrelation at 53 weeks of lag.
- Holt's Linear model outperforms the Rolling Average model (with a period of 47 weeks) by 11% RMSE.

# <a name="plan"></a>The Plan
[[Back to top](#top)]

1. Data Acquisition and Preparation: Load the dataset from Kaggle.com using pandas, perform data cleaning, and handle any missing or inconsistent values.
2. Data Exploration: Explore the dataset to gain insights into sales patterns, identify outliers, and assess the relationships between different variables.
3. Statistical Analysis: Conduct autocorrelation and seasonality analysis to identify lag periods and patterns in the data.
4. Modeling: Fit and evaluate a Holt's Linear, Holt's seasonal, and a Linear Regression model to forecast sales volume and compare their performance with the Rolling Average baseline model.
5. Evaluation: Evaluate the models' performance using appropriate metrics and validate their effectiveness in predicting sales revenue.
6. Interpretation: Interpret the model results, identify significant features, and draw actionable conclusions for the company.
7. Recommendations: Provide recommendations based on the analysis to help the company improve sales strategies and optimize revenue.

# <a name="dictionary"></a>Data Dictionary
[[Back to top](#top)]

| Feature           | Description                                             |
|-------------------|---------------------------------------------------------|
| Order ID     | Unique identifier for each order placed in the Superstore.   |
| Order Date  | Date when the order was placed.                 |
| Ship Date       | Date when the order was shipped.         |
| Ship Mode    | Shipping method for the order (e.g., Standard Class, Second Class, etc.) |
| Customer ID         | Unique identifier for each customer in the Superstore.  |
| Customer Name |     Name of the customer who placed the order. |
| Segment | Segment of customers based on their purchasing behavior (e.g., Corporate, Consumer, Home Office). |
| Country           | Country where the order was shipped.                      |
| City                | City where the order was shipped.     |
| State         | State where the order was shipped. |
| Postal Code           | Postal code of the shipping location.         |
| Region          | Geographical region where the order was shipped (e.g., West, East, South, Central). |
| Product ID           | Unique identifier for each product in the Superstore.|
| Category       | Category of the product (e.g., Furniture, Office Supplies, Technology).     |
| Sub-Category   | Sub-category of the product (e.g., Chairs, Paper, Phones). |
| Product Name           | Name of the product.         |
| Sales              | Total sales revenue generated by the order.               |
| Quantity           | Quantity of each product purchased in the order.       |
| Discount           | Discount applied to the order.        |
| Profit           | Profit earned from the order (Sales - Cost).         |


(Shape: 9994 rows x 20 columns)

# <a name="wrangle"></a>Data Acquisition and Prep
[[Back to top](#top)]

Data acquired from kaggle ('https://www.kaggle.com/datasets/vivek468/superstore-dataset-final')

To handle nulls, the following values were imputed into the following dates:
- 2014-03-18 <= 7,000
- 2016-10-02 <= 11,000
- 2017-10-22 <= 14,000
- 2017-03-23 <= 6,000
- 2014-09-08 <= 10,000

The following 11 columns were kept from the original dataframe: 'customer_id', 'order_date', 'segment', 'state', 'region', 'product_id', 'category', 'sales', 'quantity', 'discount', and 'profit'

The order_date column was set as the time index

The data was split 80/10/10 for time-series analysis to train the model

Note: no duplicates were found in this dataset


# <a name="exploration"></a>Data Exploration
[[Back to top](#top)]

## General Explore Summary: 
Inside the train data:
- The south region produces about half as many sales as the west region
- the highest selling states are California (330k), New York (200k), Texas (110k), and Washington (100k)
- the consumer category produces many more sales (800k) than corporate (500k), which produces more than home office (300k)
- Each category produces a similar amount of sales

#### Additional Notes:
- During feature engineering dummy columns of category, region, and segment were created and aggregated by mean over a weekly and monthly timescale then evaluated for correlation with sales. It was determined that none of these aggregations correlated with the sales volume

## Time explore summary:
#### Autocorrelation
- Weekly sampled sales data displays reasonably strong autocorrelation at around 52 weeks of lag (R ~.5)
- Using the peak around 105 weeks of lag may add predictive value to a model, however so much data would have to be dropped to handle the resulting nulls that this wouldn't be feasible without anouther few years of data
#### Seasonality
- Weekly sampled sales data displays clear seasonality
#### Lag
- A lag of 53 weeks produces the highest correlation to the target and is statistically valid (R = .49, P-value = 2.63e-08


# <a name="stats"></a>Statistical Analysis
[[Back to top](#top)]

- A lag of 53 weeks produces the highest correlation to the target and is statistically valid (R = .49, P-value = 2.63e-08)


# <a name="model"></a>Modeling
[[Back to top](#top)]

- When evaluated on validate data, Holt's Linear model outperformed the Rolling Average model with a period of 47 days by 283 sales, or 6%
- When evaluated on test data, Holt's Linear model outperformed the Rolling Average model with a period of 47 days by 1027 dollars in rmse, or 11%


# <a name="reproducuction"></a>Steps to Reproduce
[[Back to top](#top)]

To reproduce the results of this project, follow these steps:
1. Download the dataset from Kaggle.com (https://www.kaggle.com/datasets/vivek468/superstore-dataset-final).
2. Unzip the file in your 'Downloads' folder
3. Rename the file 'superstore.csv'
4. Run the 'final_report' Jupyter Notebook and follow the step-by-step instructions for data exploration, statistical analysis, and model building.


# <a name="conclusions"></a>Takeaways and Conclusions
[[Back to top](#top)]

- The Superstore's sales data exhibits significant seasonality and autocorrelation patterns.
- The Holt's Linear model provides more accurate sales forecasts compared to the baseline Rolling Average model.
- Seasonal effects and time lags play a crucial role in predicting future sales.
- The company can utilize the forecasting model to plan inventory, marketing campaigns, and resource allocation efficiently.


# <a name="recommendations"></a>Recommendations
[[Back to top](#top)]

Based on the analysis, the following recommendations are suggested:
- The company should pay attention to seasonal trends and plan promotions accordingly to capitalize on peak demand periods.
- Targeted marketing strategies can be implemented based on regional sales performance.


# <a name="next_steps"></a>Next Steps
[[Back to top](#top)]

To enhance the model and gain more accurate predictions, the following steps can be taken:
- Collect more historical sales data to expand the forecasting horizon.
- Incorporate external factors like economic indicators, advertising expenditure, and competitor's performance to improve predictive power.
- Experiment with other time series models, such as ARIMA or Prophet, to identify the best fit for the data.
- Build models specific to the most developed markets (i.e. New York, California, Texas, and Washington). It is suspected that since these markets are more developed and produce higher volume that their sales over time will lead to clearer seasonality trends and even more accurate models




