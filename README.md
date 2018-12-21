Crobots Batch Tournament Manager in Python
==========================================

Install
-------

Clone this repository.
Make sure that 'crobots' executable is runnable from your current shell (e.g. in $PATH env).

Setup
-----

These Python scripts try to auto-configure so you don't need any further change.
If you do, edit your script and set the correct environment:

* If you get an error whilst a Crobots*.py script tries to detect the number of available CPUs / cores, set manually the environment variable NUMBER_OF_PROCESSORS (e.g. *export NUMBER_OF_PROCESSORS=4* in your shell).

* Set to a non-null value the environment variable CROBOTS_MYSQL if you want to make active the native MySQL support (only for *CrobotsDB.py*, you may need to install MySQLdb Python library) and edit CrobotsLibs.py accordingly with your database credentials.

* Make sure that your Crobots installation folder contains the *conf* and *db* directories.

Configuration
-------------

Create a .py configuration file with the following rules:

* Class name *Configuration*

* Variable *label* for the tournament name; it'll be also the name of the result files (each one with the suffix *_f2f* *_3vs3* *_4vs4*)

* Variables *matchF2F*, *match3VS3*, *match4VS4* with the match repetition factors.

* Variable *sourcePath* with the path of your *.ro* robot binaries (it could be '.' and you may specify the path within the robot name)

* List *listRobots* with the list of your .ro robot binaries (they may contain a full path, if you set '.' as *sourcePath*)

* Save the configuration file in your *conf* path

This is an example of configuration:

```python
    class Configuration(object):
        label = '2013'
        matchF2F = 1000
        match3VS3 = 250
        match4VS4 = 168
        sourcePath = '.'
        listRobots = ['2013/lamela', '2013/eternity', '2013/ride', '2013/okapi', '2013/pjanic']
```

If you run this configuration you'll get the output on the screen and *2013_[f2f|3vs3|4vs4].db* database files respectively if database support is enable.
Each face to face combat will have 1000 matches (CROBOTS command line option *-m1000*). Each 3 vs 3 combat will have 250 matches (CROBOTS command line option *-m250*). Each 4 vs 4 combat will have 168 matches (CROBOTS command line option *-m168*). E.g.:

```
    crobots -m1000 -l200000 2013/lamela.ro 2013/pjanic.ro
    crobots -m250 -l200000 2013/lamela.ro 2013/pjanic.ro 2013/ride.ro
    crobots -m168 -l200000 2013/lamela.ro 2013/pjanic.ro 2013/ride.ro 2013/okapi.ro
```

Robot binary files will be loaded from *'./'* directory, so you can specify the base path within the *listRobots* variable. Alternatively you can use a configuration like this:

```python
    class Configuration(object):
        label = '2013'
        matchF2F = 1000
        match3VS3 = 250
        match4VS4 = 168
        sourcePath = '2013'
        listRobots = ['lamela', 'eternity', 'ride', 'okapi', 'pjanic']
```

Run
---

This is the list of all available Crobots Python scripts. They share a lot of code and a common behavior. Command line options are pretty much the same for every of them.
You can interrupt (and resume, if database support is enabled) a tournament by creating a file *Crobots.stop* within the same running directory, e.g.:


```
    touch Crobots.stop
```

Delete that file to re-run o resume the tournament.

Crobots.py
----------

This script runs a full tournament (F2F, 3vs3, ...) using the robots specified within the configuration. It does only support a in-memory database and prints out results on the standard output.
**Note**: It does *not* keep any log file: if you interrupt the execution you'll loose all the results, so bear in mind to save its output somewhere.
Examples:

```
    Crobots.py conf/MyConf.py f2f > results_f2f.txt
    Crobots.py conf/MyConf2.py all > results2_all.txt
```

Run Crobots.py without command line parameters to read the help.

CrobotsDB.py
------------

As the script below, this script runs a full tournament (F2F, 3vs3, ...) using the robots specified within the configuration. It *does* support a database so it saves all the results within a database file. You can stop and resume a tournament later on.
It does not print out the sorted ranking: use CrobotsDBReport.py instead.
Examples:

```
    CrobotsDB.py conf/MyConf.py setup
    CrobotsDB.py conf/MyConf.py 4vs4
    CrobotsDB.py conf/MyConf.py clean
```

If you want to use MySQL as database to publish tournament results:

* Setup your MySQL database schema using *SetupMySQL.sql* script

* Change your credentials into *CrobotsLibs.py* (config struct)

* Export environment variable CROBOTS_MYSQL (e.g. *export CROBOTS_MYSQL=1*)

**Note**: This is the only script with MySQL support.

Run CrobotsDB.py without command line parameters to read the help.

CrobotsDBReport
---------------

This script shows a sorted ranking from a tournament database file. It accepts the database prexif and [f2f|3vs3|4vs4|all] as parameters. If 'all' is specified it tries to load up all databases and prints out the total report, otherwise it loads up the *database-prefix_type.db* file.

```
    CrobotsDBReport.py db/tournament 4vs4
    CrobotsDBReport.py db/final all
```

CrobotsBench.py
---------------

This script runs a partial tournament using all combinations of robots listed into the configuration file against a single robot to test. It does only support a in-memory database and prints out results on the standard output.
**Note**: It does *not* keep any log file: if you interrupt the execution you'll loose all the results, so bear in mind to save its output somewhere.
Examples:

```
    CrobotsBench.py conf/AllStars.py test/test.r 3vs3 > test_3vs3.csv
    CrobotsBench.py conf/AllStars.py test/test.r 4vs4 > test_4vs4.csv
    CrobotsBench.py conf/AllStars.py test/test.r all  > test_all.csv
```

CrobotsBenchDB.py
-----------------

As above but it does support a local database to store and retrieve results. You can stop and resume a tournament later on.
It does not print out a sorted ranking: use CrobotsDBReport.py instead.
Examples:

```
    CrobotsBenchDB.py conf/AllStars.py test/test.r 3vs3
    CrobotsBenchDB.py conf/AllStars.py test/test.r 4vs4
    CrobotsBenchDB.py conf/AllStars.py test/test.r all
    CrobotsBenchDB.py conf/AllStars.py test/test.r clean
```

CrobotsDBRandom.py
------------------

As *CrobotsDB.py* (without MySQL support) but it runs random matches. Useful you have a massive list of robots like KOTH and you cannot run a whole tournament.
You can stop and resume a tournament later on. You can limit the number of combats changing the variable *LIMIT*.
Examples:

```
    CrobotsDBRandom.py conf/KOTHConf.py 3vs3
    CrobotsDBRandom.py conf/KOTHConf.py 4vs4
```

CrobotsBenchDBRandom.py
-----------------------

A combination of *CrobotsBenchDB.py* and *CrobotsDBRandom.py*

To test a single robot against a random combination of matches.
You can stop and resume a tournament later on. You can limit the number of combats changing the variable *LIMIT*.
Examples:

```
    CrobotsBenchDBRandom.py conf/KOTHConf.py test/test.r 3vs3
    CrobotsBenchDBRandom.py conf/KOTHConf.py test/test.r 4vs4
```

Compatibility
-------------

Successfully tested with Python 2.7.x on Linux Ubuntu.
