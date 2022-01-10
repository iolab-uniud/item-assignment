#!/usr/bin/env python3
import time
import datetime
import click
import json
import requests
import re
import logging

logger = logging.getLogger('solve')

def validate_url(ctx, param, value):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    if not re.match(regex, value):
        raise click.BadParameter(f'Invalid url {value}')
    return value

@click.command()
@click.argument('filename', type=click.Path(exists=True), required=True)
@click.option('--output', type=click.File('w'), default='-', help="The name of the output file, if not provided it goes to the standard output")
@click.option('--solver-url', type=str, default='http://158.110.146.213:18080', callback=validate_url, help="URL of the solution solver")
@click.option('--wait-seconds', type=int, default=1, required=False, help="Time interval for pull requests for the end of the solution process")
@click.option('--timeout', type=float, default=None, required=False, help="Timeout of the simulated annealing procedure (in seconds)")
@click.option('--verbose', '-v', is_flag=True, help="Provide a verbose logging")
def send_to_solver(filename, output, solver_url, wait_seconds, timeout, verbose):
    def format_time(elapsed):
        elapsed_rounded = int(round((elapsed)))
        return str(datetime.timedelta(seconds=elapsed_rounded))

    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)   

    try:
        with open(filename, "r") as f:
            input_json = json.load(f)
        t0 = time.time()
        params = {}
        if timeout:
            params["timeout"] = timeout
        # send to solver
        logger.info("Sending request to the solve server")
        r = requests.post(f"{solver_url}/runner/BSA", headers={'Content-type': 'application/json', 'Accept': 'text/plain'}, data=json.dumps(input_json), params=params)
        if r.status_code != 200:
            raise RuntimeError(f"An issue occured while interrogating the solver: {r.json()}")
        run_id = r.json()['url'].split("/")[2]        
        logger.info(f"Solving run with id {run_id}")
        # check for finish
        solved = False
        while not solved:
            r = requests.get(f"{solver_url}/running/{run_id}", headers=None)
            result = r.json()
            solved = bool(result['finished'])
            if not solved:
                logger.info(f"Current best cost {result['cost']}")
            time.sleep(wait_seconds)
        logger.info(f"task {run_id} solved in {format_time(time.time() - t0)}")
        # when solved, get result
        logger.info("Getting the final solution")
        r = requests.get(f"{solver_url}/solution/{run_id}", headers=None) 
        logger.info("Writing the solution")
        json.dump(r.json(), output)
        output.write('\n')
    except Exception as e:
        logger.error(f"An error occured during the solution process {str(e)}")

if __name__ == "__main__":
    send_to_solver()

