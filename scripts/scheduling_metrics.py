'''
This script generates a scheduling summary for a given day.
'''
import logging

from argparse import ArgumentParser

from infra_reports.jobs import scheduling_sources

from mozci.utils.log_util import setup_logging


def summary(scheduling_data):
    # print 'Out of %d jobs:' % total_jobs
    # print '------------------'

    for reason, values in scheduling_data.iteritems():
        # perc = round((float(values['count'])/float(total_jobs))*100, 2)
        perc = 0
        print '{0:6d} by {1} ({2}%)'.format(
            values['count'], reason, perc)


def main():
    parser = ArgumentParser()
    parser.add_argument("--debug",
                        action="store_true",
                        dest="debug",
                        help="set debug for logging.")

    options = parser.parse_args()

    if options.debug:
        setup_logging(logging.DEBUG)
    else:
        setup_logging()

    scheduling_data = scheduling_sources('2015-10-28')
    summary(scheduling_data)


if __name__ == "__main__":
    main()
