[![Build Status](https://travis-ci.org/anushnap/seattlepark.svg?branch=main)](https://travis-ci.org/anushnap/seattlepark)
## seattlepark

Finding parking in the Seattle area can sometimes be an arduous task.  Free street parking is difficult to find, can be on narrow streets, and time-limited in residential zones often to 2 hours. Paid street parking is often just as difficult to find.

Our solution is an interactive API using the Seattle Annual Parking Study, which records street parking usage at various times of day on streets throughout the city to create a suggestion for most-likely-available streets to park in based on a user’s inputted destination.

## License

The MIT License is a permissive free software license originating at the Massachusetts Institute of Technology (MIT). As a permissive license, it puts only very limited restriction on reuse and has therefore an excellent license compatibility. For more info please see: [MIT license](https://snyk.io/learn/what-is-mit-license/).

## Project Organization

The project structure is as follows:

[INSERT IMAGE]

## Installation

To install seattlepark package, open terminal/command prompt and cd into local git repo and clone the package to your computer using the following command:

```bash
git clone https://github.com/anushnap/seattlepark
```

Next, install the package using the following command:

```bash
cd seattlepark/
python setup.py install
```

Then set up your development environment using the following command:

```bash
pip install -r requirements.txt
```

Once all dependencies are installed, open and run the python file "parking_app.py" in the src directory:

```bash
python seattlepark/src/parking_app.py
```

## Using the seattlepark app

Once you have the app set up and running, you're ready to take advantage of its functions. 

- Enter a Seattle street address and enter the distance you're willing to walk from your parking location to your destination.
    - Ex: 400 Broad St, Seattle, WA 98109 (Space Needle), or 4000 15th Ave NE, Seattle, WA 98195 (Suzzallo Library)
- The map will update with a dot to indicate the destination along with lines to indicate potential streets to park.
- Hover over the lines to see the average available parking spaces on that street around the time that you are accessing the API. Happy parking!