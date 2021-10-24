# ferret_database
Database written in sqlite to access and query longitudinal imaging data across animals.



### Organization of the  project

The project has the following structure:

    database/
      |- README.md
      |- database/
         |- __init__.py
         |- gen_database.py
         |- print_database_schema.py
         |- query_database.py
         |- tables.py
         |- data/
            |- ferret_database.db
         |- tests/
      |- scripts/
      
      
### Project Data
The database consists of three tables _ferrets_, _dates_ and _timeseries_ with a structure as shown below. Each animal is uniquely described by its _id_ or _ferretNumber_. Additional keys are the animal's birth date (_birth_date_), the date of eye-opening (_eo_date_) and the reference date for image registration across days (_ref_date_).<br />
Typically each animal was imaged on several days given by _date_exp_ and _ferret_id_ in table _dates_.<br />
For each _date_exp_ various experiments have been performed differing in the imaged cortical area _area_, and the stimulus type given by _exp_. Individual experiments can be accessed either via the _id_ or by the unique timeseries _ts_ in table _timeseries_. Each timeseries refers back to the specific animal via _ferret_id_ and to the date of the experiment via _date_id_.

The database is stored in 'database/database/data/ferret_database.db'.

Table: ferrets
| ID    | Name            | Type       | NotNull   | Default    | PK (Primary key)    | FK (Foreign key)| FK key     |
| ---   | ---             | ---        | ---        | ---        | ---   | ---        | ---        |
| 0     | id              | integer    | 0          | -          | 1     | -          | -          |
| 1     | ferretNumber    | integer    | 1          | -          | 0     | -          | -          |
| 2     | birth_date      | text       | 0          | -          | 0     | -          | -          |
| 3     | ref_date        | text       | 0          | -          | 0     | -          | -          |
| 5     | eo_date         | text       | 0          | -          | 0     | -          | -          |

Table: dates
| ID    | Name            | Type       | NotNull   | Default    | PK    | FK         | FK key     |
| ---   | ---             | ---        | ---        | ---        | ---   | ---        | ---        |
| 0     | id              | integer    | 0          | -          | 1     | -          | -          |
| 1     | date_exp        | text       | 1          | -          | 0     | -          | -          |
| 2     | ferret_id       | integer    | 1          | -          | 0     | ferrets    | id         |        

Table: timeseries
| ID    | Name            | Type       | NotNull   | Default    | PK    | FK         | FK key     |
| ---   | ---             | ---        | ---        | ---        | ---   | ---        | ---        |
| 0     | id              | integer    | 0          | -          | 1     | -          | -          |
| 1     | ts              | integer    | 1          | -          | 0     | -          | -          |
| 2     | area            | text       | 0          | -          | 0     | -          | -          |
| 3     | exp             | text       | 0          | -          | 0     | -          | -          |
| 4     | ref_ts          | integer    | 0          | -          | 0     | -          | -          |
| 5     | date_id         | integer    | 1          | -          | 0     | dates      | id         |
| 6     | ferret_id       | integer    | 1          | -          | 0     | ferrets    | id         |

### Scripts

This repository contains a [Python script](https://github.com/b3ttin4/ferret_database/blob/master/database/tables.py) that defines the three tables, and defines functions to generate, update
and delete items in the tables. <br/>
In the [Python script]() two exemplary functions are provided to query the database. In particular, a function is provided that queries all experiments for a user-defined combination of key words and outputs those experiments that share the given values.  <br/>
The table of the database given above was created with the [Python script]().<br/>
For completion I added the [Python script](https://github.com/b3ttin4/ferret_database/blob/master/database/gen_database.py) which generated the database. However, it relies on functions not provided in this repository.


### Licensing

Licensed under MIT license. 
