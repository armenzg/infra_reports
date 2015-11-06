'''
Module to manipulate information about Buildbot jobs
'''
from mozci.sources.buildjson import fetch_by_date


def scheduling_sources(date):
    ''' Return a data structure about scheduling metadata for a given day. '''
    jobs = fetch_by_date(date)
    return _scheduling_data(jobs)


def _scheduling_data(jobs):
    # XXX: The returned data structure is too centered around my original report
    # We should pretty much take "jobs" and curate them (only useful data)
    # Let the reports manipulate the jobs itself.
    scheduling_data = {}

    for job in jobs:
        # XXX: We should consider status of jobs (e.g. coalesced)
        # This would be good to differentiate real load if there
        # was no coalescing
        buildername, reason, who = classify_job(job)

        if reason not in scheduling_data:
            scheduling_data[reason] = {
                'count': 1,
                'builders': {},
                'who': {}
            }
        else:
            scheduling_data[reason]['count'] += 1

        if who not in scheduling_data[reason]['who']:
            scheduling_data[reason]['who'][str(who)] = 1
        else:
            scheduling_data[reason]['who'][str(who)] += 1

        if buildername not in scheduling_data[reason]['builders']:
            scheduling_data[reason]['builders'][buildername] = 1
        else:
            scheduling_data[reason]['builders'][buildername] += 1

    return scheduling_data


def classify_job(job):
    buildername = job['properties']['buildername']
    reason = job['reason']
    who = reason.split()[-1]

    if buildername.startswith('release'):
        reason = 'release'
    elif reason.startswith('Created by BBB'):
        reason = 'BBB'
    # XXX: data from 2015-10-28 should be showing us
    # automated backfilling load but the code is failing to capture it
    elif who == 'mozci-bot@mozilla.com':
        # Mainly sheriff requests
        reason = 'Sheriff requests'
    elif who == 'try-extender@mozilla.com':
        reason = 'Try extender'
    elif who == 'trigger-bot@mozilla.com':
        reason = 'Triggerbot'
    elif reason.startswith('Self-serve: Rebuilt'):
        reason = 'Retrigger'
    elif reason.startswith('Self-serve: Requested'):
        # e.g. triggers from Buildapi itself (new nightly builds)
        # and local requests from mozci scripts
        reason = 'Arbitrary requests'
    elif 'l10n nightly' in buildername:
        reason = 'L10n nightly'
    elif 'l10n' in buildername:
        reason = 'L10n dep'
    elif 'nightly' in buildername:
        reason = 'Nightly'
    elif reason.startswith('The Nightly scheduler') and (
        'pgo-build' in buildername or
        'periodic' in buildername or
        'periodic' in reason
    ):
        reason = 'Periodic (includes PGO)'
    elif reason.startswith('The web-page'):
        reason = 'Buildbot (force or rebuild)'
    elif reason.startswith('downstream') and buildername.startswith('release'):
        reason = 'downstream'
    elif reason.startswith('scheduler'):
        reason = 'checkin_triggered'

    return buildername, reason, who
