## 🏆 World Cup 2022 Catar Project 

Credits to my team partner Marco Carujo for creating the [Dataset](https://www.kaggle.com/datasets/mcarujo/fifa-world-cup-2022-catar)

## Table of Contents
1. [Statistics of the 2022 World Cup in Qatar](#statistics)
2. [Activities](#activities)
3. [Problems](#problems)
4. [Views](#views)
5. [Conclusion](#conclusion)
6. [Next Steps](#next-steps)

<a name="statistics"></a>
## 📊 Statistics of the 2022 World Cup in Qatar
|        Event       | Total |
|-------------------|-------:|
|    Substitution    |  587  |
|     Yellow card    |  224  |
|        Goal        |  153  |
|         PK         |   41  |
|       Penalty      |   17  |
|   Disallowed goal  |   9   |
|   Missed penalty   |   6   |
| Second yellow card |   3   |
|      Own goal      |   2   |
|      Red card      |   1   |

<a name="activities"></a>
## 🔧 Activities

- Data cleaning

- Feature engineering for data manipulation (data transformation)

- Perform data analysis (EDA)
    1. SQL
    2. Pandas/Seaborn/Matplotlib/yellowbricks/etc
    3. pivottablejs

- Create a general statistics based on previously data analysis and feature engineering
    - Generated dataframes contained event_list statistics, global statistics, top scores, top assists, top participations, etc;

- Perform data clustering using k-means and DBScan

- Build ML Algorithms to predict home team winning, drawing or away team winning
    1. Train/test environment
    2. Cross Validation K-Fold
    3. GridSearch
    4. SVM, LogisticRegression and RandomForestClassifier results comparison
    5. Perform oversampling to develop the results

<a name="problems"></a>
## 🤔 Problems

* Columns with list of dictionary, we had to manipulate the csv to transform into new columns
    - this columns with a list of dictionary, have values like " Messi ", so we have to split this to be a correct value
    - based on the columns "lineup_home" and "lineup_away", we created 2 new columns for each columns to get the data from those columns, that will be better to understand.
    - based on the column "events_list", we created a new dataset that will be insume to create the "statistic dataset", which will contains values about yellow cards, goals, etc.
    
* Generated dataframes -> event_list statistics, global statistics, top scorer, top assists;

* As the dataset is relatively small, with only 64 rows, when we conduct a prediction analysis using RandomForestClassifier, LogisticRegression, and SVM, we observe that the values of precision, accuracy, and recall remain consistent, regardless of whether we use grid search or k-fold cross-validation.

<a name="views"></a>
## 📈 Views

* Feature Engineering
    - Percentage dtype manipulation;
    - Transforming lineup_home and lineup_away columns which contains list of dictionaries into new columns;
    - Transforming events_list column into a new dataframe that will be use for global statistics.
    - Check the numerical/float columns which will be used for predictions if they are gaussian distribuition
        - Apply log transformation

* Global statistics from each team, total of goals (top scorers), total of assists (top assistances), total team goals, etc;

* EDA Session
    - SweetViz 
    - Notebook analysis

* Ball possession for the 2022 World Cup was not a decisive factor in whether a team will win the match, as out of the 54 games that resulted in a win or loss for a team, only half (27) were determined by equality (ball possession and victory).
    - To perform the analysis of ball possession, it was necessary to change the type of format for that column, as it is of "object" type and we need to compare values, so it needs to be changed to float and a method was used to convert all the "percentage" columns to this.

* Identified which players have the biggest impact on matches (games versus win percentage)

* Relationship between the number of goals scored and the number of shots on goal (Which teams were most effective in goal kicks)

* Predictions columns were analyzed to indicate if there was a upset case in the games.
    - In 64 games, we had 25 upset games (prediction not equals to the real winner of the game)

* Clustering to realize new insights
    - K-means
    - DBScan

* Build ML Algorithms using k-fold and gridsearch to predict home team winning, drawing or away team winning
    - Standardize columns reduced the values of the metrics.
    - Compare results using SVM, LogisticRegression and RandomForestClassifier

<a name="conclusion"></a>
## 🏁 Conclusion

<a name="next-steps"></a>
## 🚀 Next Steps

