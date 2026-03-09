This is a small football analytics project exploring stylistic similarity between players.

## Data

The project uses public datasets from Kaggle based on FBref statistics:
- 2021–2022 Football Player Stats - https://www.kaggle.com/datasets/vivovinco/20212022-football-player-stats/data
- 2022–2023 Football Player Stats - https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats/data

The datasets include statistics such as shooting, passing, defensive actions, progression, carries, touches and aerial duels.

## src

The `src` folder contains data preparation utilities used in the project.
`data_prepare.py` loads both datasets, harmonizes their columns, converts numeric values safely and prepares a base dataframe with player seasons and cleaned statistics. :contentReference[oaicite:0]{index=0}

It also:
- filters players with low minutes
- handles hybrid positions
- optionally removes goalkeepers

## notebooks
The `notebooks` folder contains the main analysis notebook:

`FootballBrothers.ipynb`
The notebook builds a simple similarity model using player statistics and cosine similarity to explore stylistic similarities between players.  
Several case studies are included to analyze different player roles and profiles.
