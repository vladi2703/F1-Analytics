# F1 Analytics Pipeline Report

*Authors: Elina Yancheva and Vladimir Stoyanov*

## 1. Project Purpose and Overview

The F1 Analytics Pipeline is designed to process and analyze Formula 1 racing data, providing insights into race performance, driver statistics, and championship trends. The pipeline transforms raw F1 data into structured analytics, enabling detailed analysis of race outcomes, driver performance, and historical trends.

### Key Objectives:

- Process and clean historical F1 race data
- Generate comprehensive driver and constructor statistics
- Create predictive models for race outcomes
- Automate data updates during active racing months
- Provide visualizations for performance analysis

## 2. Methodology

### 2.1 Initial Data Processing Stage

- Primary data source: Formula 1 historical dataset containing 14 interrelated CSV files
- Key tables include: races, drivers, constructors, results, qualifying, and lap times
- Total data volume: 575,029 lap times, 26,519 race results, 859 drivers

The first pipeline stage processes raw F1 data to create two essential championship datasets. The script utilizes pandas to transform CSV inputs into structured championship records through two main functions:

`create_championship_winners_dataset` and`create_constructor_champions_dataset` - handle constructor and championship winners, processing individual and team victories.

Both functions follow a straightforward workflow: identify final races of each season, extract championship standings at those points, and enrich with additional details from driver or constructor tables. The processed data is saved in Parquet format for efficient storage and quick access in later pipeline stages.

### 2.2 Data Cleaning and Validation

- Implemented comprehensive validation checks for:
    - Race schedule conflicts
    - Duplicate qualifying entries
    - Anomalous lap times (identified 692 laps >5 minutes)
    - Missing values in qualifying data (Q2: 0.13%, Q3: 0.26%).
        - This may be due to [rules changes in F1 History](https://www.formula1.com/en/latest/article/deciding-the-grid-a-history-of-f1-qualifying-formats.1oh1hemlnZ4x9rt2nff8vn#:~:text=Up%20until%201996%20qualifying%20followed%20a%20fairly%20standard%20pattern%20%2D%20there%20were%20two%20sessions%20in%20which%20to%20set%20times)

Implemented detailed lap time analysis:

- Initial scan identified 692 laps longer than 5 minutes
- Developed clustering algorithm to distinguish between incident-related and individual slow laps
- Identified 608 slow laps connected to race incidents (multiple drivers affected in same lap range)
- Found 84 individual slow laps requiring further investigation - random Google checking turns out the data is true e.g [Perez coming out of the pits, just in order to be served his penalty](https://en.wikipedia.org/wiki/2023_Japanese_Grand_Prix#:~:text=There%20was%20confusion,retired%20once%20again).
- Validated findings against known race events (e.g., 2011 Canadian GP with 124.97 minute average due to red flag)
- Created comprehensive mapping of major race interruptions (red flags, safety cars) based on lap time patterns

- Validated race date consistency and timing data integrity

### 2.3 Data Transformation and Statistical Analysis

The transformation phase involved comprehensive statistical analysis and metric derivation to quantify performance patterns across multiple dimensions of F1 racing.

**Driver Performance Analytics:**
We developed detailed driver performance profiles by calculating key statistical measures including **mean finishing position**, **standard deviation of race times**, and **consistency metrics**. For each driver, we computed seasonal performance indicators such as points accumulation rates, podium conversion ratios, and qualification-to-race position changes. A notable example is the Schumacher vs. Hamilton comparison, which revealed significant differences in DNF rates (64 vs. 27) and pole positions (36 vs. 107) across comparable race counts (308 vs. 344).

**Constructor Performance Metrics:**
The pipeline generated comprehensive team performance analytics, including point accumulation **trends**, reliability metrics (measured through DNF rates), and season-over-season performance deltas. We implemented rolling averages to track team form across seasons and circuits, revealing long-term performance patterns. For example, our analysis of constructor championships showed British teams' dominance (48.5% of titles) compared to Italian teams (25.8%).

**Race Performance Analysis:**
The analysis revealed significant insights such as the greatest position gains in F1 history (maximum 19 positions gained) and the statistical relationship between qualifying and race performance. A particularly interesting finding was the evolution of race duration variability, with the standard deviation of race times decreasing significantly over F1's history, indicating more standardized race formats.

### 2.4 Analysis Implementation

- Developed predictive model for race positions using RandomForestRegressor
- Feature engineering includes:
    - Historical performance metrics
    - Track-specific statistics
    - Constructor performance indicators
- Cross-validation
- Position-specific accuracy:
    - Top 3 positions: MAE 0.01
    - Positions 4-10: MAE 0.02
    - Positions 11-20: MAE 0.02

## 3. Data Pipeline

### 3.2 Pipeline Automation

- GitHub Actions workflow for monthly updates during racing season
- Automated data validation and cleaning processes
- HTML report generation for web visualization
- Error handling and logging implementation

### 3.3 Technical Implementation

- Python-based pipeline using pandas, scikit-learn, and visualization libraries
- Modular code structure with separate components for:
    - Data cleaning and validation
    - Feature engineering
    - Model development
    - Visualization generation
- Parquet file storage for processed data
- Automated testing and validation checks

At its core, the pipeline uses Pandas for data manipulation, particularly in handling the complex relationships between 14 different CSV and 2 parquet data sources containing race, driver, and constructor information. 

### 3.4 The pipeline

Architecture is structured into distinct processing stages:

1. Data Ingestion and Validation:
The initial stage handles raw CSV imports through Pandas, implementing comprehensive validation checks for data integrity. This includes detecting anomalous lap times, validating race schedules, and identifying potential data inconsistencies.
2. Feature Engineering and Analysis:
The transformation layer processes raw data into meaningful metrics using sophisticated Pandas operations. This includes generating rolling statistics, computing performance deltas, and creating derived features for the prediction model.
3. Model Development:
The modeling component uses scikit-learn's pipeline architecture to ensure consistent data preprocessing and model training. Cross-validation techniques validate model performance, while feature importance analysis guides iterative improvements.

For data persistence, we utilize the Parquet file format, chosen for its superior compression and fast read/write capabilities compared to CSV. This format efficiently handles our large dataset, ensuring scalability and is future proof.

The entire pipeline is automated through GitHub Actions, with scheduled runs during the F1 season (March to December). The workflow includes automated testing and validation checks, ensuring data quality and processing integrity. Error handling mechanisms capture and log any anomalies in the data processing chain, while the modular structure allows for easy maintenance and extensions to the analysis capabilities.

### 3.4 Pipeline Automation and Output

The F1 Analytics pipeline is automatically triggered through GitHub Actions on three conditions: monthly on the 1st day during the F1 season (March to December), on push events to the master branch when notebook or data files are modified, and through manual triggers via the GitHub Actions interface. The pipeline's final output is a generated HTML page hosted on GitHub Pages that serves as the project's front end. This page includes direct links to both the detailed Jupyter notebook containing the full analysis and the presentation slides summarizing key findings. The automation ensures that the analysis stays current throughout the racing season while maintaining easy access to all project components through a single, organized interface.

For local execution there is a platform independent script called `build_site.py` that executes all the pipeline steps locally and opens the site front page. 

## 4. Conclusion and Future Enhancements

The F1 Analytics Pipeline successfully demonstrates comprehensive data processing and analysis capabilities, providing valuable insights into Formula 1 racing patterns and performance metrics. The automated workflow ensures regular updates during the racing season, while the modular structure allows for easy maintenance and extensions.

Potential future enhancements include:

- Real-time data processing capabilities and regular automated data downloading
- Advanced prediction models for specific race scenarios
- Interactive visualization dashboard
- Integration with additional data sources

The pipeline fulfills its core objectives of data management, processing, and analysis while maintaining scalability and reproducibility standards.