## World Cup 2022 Catar Project

Credits to my team partner Marco Carujo for creating the [Dataset](https://www.kaggle.com/datasets/mcarujo/fifa-world-cup-2022-catar)

### Activities

- Data cleaning

- Feature engineering for data manipulation (transformation)

- Perform data analysis (EDA)
    1. SQL
    2. Pandas/Seaborn/Matplotlib/etc
    3. That tool I saw on LinkedIn for building charts
- Perform data clustering using k-means

- Use a machine learning algorithm for prediction or something similar
    1. Train/test environment
    2. Prediction
- Predict the number of yellow cards, substitutions, etc in a game

- Create a general statistics of each team in the World Cup

### Problems Faced

* Columns with list of dictionary, we had to manipulate the csv to transform into new columns
    - this columns with a list of dictionary, have values like " Messi ", so we have to split this to be a correct value
    - based on the columns "lineup_home" and "lineup_away", we created 2 new columns for each columns to get the data from those columns, that will be better to understand.
    - based on the column "events_list", we created a new dataset that will be insume to create the "statistic dataset", which will contains values about yellow cards, goals, etc.
    
* Generated dataframes -> event_list statistics, global statistics, top scorer, top assists

### Next Steps