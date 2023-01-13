## World Cup 2022 Catar Project

Credits to my team partner Marco Carujo for creating the [Dataset](https://www.kaggle.com/datasets/mcarujo/fifa-world-cup-2022-catar)

### Statistics of the 2022 World Cup in Qatar
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

### Activities

- Data cleaning

- Feature engineering for data manipulation (data transformation)

- Perform data analysis (EDA)
    1. SQL
    2. Pandas/Seaborn/Matplotlib/yellowbricks/etc
    3. pivottablejs

- Perform data clustering using k-means

- Use a machine learning algorithm for prediction or something similar
    1. Train/test environment
    2. Prediction
- Predict the number of yellow cards, substitutions, etc in a game

- Create a general statistics of each team in the World Cup

### Problems

* Columns with list of dictionary, we had to manipulate the csv to transform into new columns
    - this columns with a list of dictionary, have values like " Messi ", so we have to split this to be a correct value
    - based on the columns "lineup_home" and "lineup_away", we created 2 new columns for each columns to get the data from those columns, that will be better to understand.
    - based on the column "events_list", we created a new dataset that will be insume to create the "statistic dataset", which will contains values about yellow cards, goals, etc.
    
* Generated dataframes -> event_list statistics, global statistics, top scorer, top assists

### Views

* Ball possession for the 2022 World Cup was not a decisive factor in whether a team will win the match, as out of the 54 games that resulted in a win or loss for a team, only half (27) were determined by equality (ball possession and victory).
    - To perform the analysis of ball possession, it was necessary to change the type of format for that column, as it is of "object" type and we need to compare values, so it needs to be changed to float and a method was used to convert all the "percentage" columns to this.

* Identified which players have the biggest impact on matches (games versus win percentage)

* Relationship between the number of goals scored and the number of shots on goal 

* Predictions columns were analyzed to indicate if there was a upset case in the games.
    - In 64 games, we had 25 upset games (prediction not equals to the real winner of the game)

### Conclusion

### Next Steps