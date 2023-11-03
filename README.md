# Item Assignment Optimization

This is the complementary repository for the paper ["Task design in complex crowdsourcing experiments: Item assignment optimization"](https://www.sciencedirect.com/science/article/pii/S0305054822002295), by Sara Ceschia, Kevin Roitero, Gianluca Demartini, Stefano Mizzaro, Luca Di Gaspero, and Andrea Schaerf, Computers & Operations Research, 148, 105995, 2022.

The *Item Assignment Optimization* problem consists in assigning crowdsourcing tasks to workers so as to fulfill a set of requirements and constraints and ensure quality and fairness criteria. 

The repository contains the datasets described in the paper and a script for using the online version of the solver. In order to try to solve an instance with an online solver you must use the `solve.py` python script providing an instance file.

The script uses the `click` and the `requests` libraries, which are also specified in the `requirements.txt` file. If you want to install those dependencies you can issue the command:

```bash
pip3 install -r requirements.txt
```

the `solve.py` script contains a URL which links to a deployed version of the solver. 

The script can be tested issuing the folllowing command:

```bash
python3 solve.py ./instances/toy.json
```

or 

```bash
./solve.py ./instances/toy.json
```

### Command line parameters

By issuing the command `./solve.py --help` you get a description of the command line parameters, namely you will get:

```
Usage: solve.py [OPTIONS] FILENAME

Options:
  --output FILENAME       The name of the output file, if not provided it goes
                          to the standard output

  --solver-url TEXT       URL of the solution solver
  --wait-seconds INTEGER  Time interval for pull requests for the end of the
                          solution process

  --timeout FLOAT         Timeout of the simulated annealing procedure (in
                          seconds)

  -v, --verbose           Provide a verbose logging
  --help                  Show this message and exit.
```
