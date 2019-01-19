"""This module implements the simulation engine.

The simulation engine, given the parameters according to which a single
experiments needs to be run, instantiates all the required classes and executes
the experiment by iterating through the event provided by an event generator
and providing them to a strategy instance.
"""
from icarus.execution import NetworkModel, NetworkView, NetworkController, CollectorProxy
from icarus.registry import DATA_COLLECTOR, STRATEGY
from pprint import pprint
import pickle

__all__ = ['exec_experiment']


def exec_experiment(topology, workload, netconf, strategy, cache_policy, collectors, read_from_data):
    """Execute the simulation of a specific scenario.

    Parameters
    ----------
    topology : Topology
        The FNSS Topology object modelling the network topology on which
        experiments are run.
    workload : iterable
        An iterable object whose elements are (time, event) tuples, where time
        is a float type indicating the timestamp of the event to be executed
        and event is a dictionary storing all the attributes of the event to
        execute
    netconf : dict
        Dictionary of attributes to inizialize the network model
    strategy : tree
        Strategy definition. It is tree describing the name of the strategy
        to use and a list of initialization attributes
    cache_policy : tree
        Cache policy definition. It is tree describing the name of the cache
        policy to use and a list of initialization attributes
    collectors: dict
        The collectors to be used. It is a dictionary in which keys are the
        names of collectors to use and values are dictionaries of attributes
        for the collector they refer to.

    Returns
    -------
    results : Tree
        A tree with the aggregated simulation results from all collectors
    """
    model = NetworkModel(topology, cache_policy, **netconf)
    view = NetworkView(model)
    controller = NetworkController(model)

    collectors_inst = [DATA_COLLECTOR[name](view, **params)
                       for name, params in collectors.items()]
    collector = CollectorProxy(view, collectors_inst)
    controller.attach_collector(collector)

    strategy_name = strategy['name']
    strategy_args = {k: v for k, v in strategy.items() if k != 'name'}
    strategy_inst = STRATEGY[strategy_name](view, controller, **strategy_args)

    if read_from_data:
        with open ('record_workload', 'rb') as fp:
            record_workload = pickle.load(fp)
        get_ug_provider(record_workload, view, topology, read_from_data)
        for record_event in record_workload:
            time=record_event[0]
            event=record_event[1]
            # print(time)
            # pprint(event)
            strategy_inst.process_event(time, **event)
    else:
        record_workload = []
        get_ug_provider(workload, view, topology, read_from_data)
        for time, event in workload:
            # print(time)
            # pprint(event)
            record_workload.append([time, event])
            strategy_inst.process_event(time, **event)
        with open('record_workload', 'wb') as fp:
            pickle.dump(record_workload, fp)
    return collector.results()

def get_ug_provider(workload, view, topology, read_from_data):
    if read_from_data:
        with open ('record_workload_pdf', 'rb') as fp:
            content_pdf = pickle.load(fp)
    else:
        content_pdf = workload.dist._pdf
        with open('record_workload_pdf', 'wb') as fp:
            pickle.dump(content_pdf, fp)

    "remove the weird additional digits ex. 0.32000000000006  (remove 6)"
    for i in range(len(content_pdf)):
        content_pdf[i] = round(content_pdf[i], 10)
    content_source = view.model.content_source
    # print(content_source)
    # provider_pdf = [0] * len(topology.sources())
    provider_pdf = {}      
    for content, provider in content_source.items():
        if not provider_pdf.has_key(provider):
            provider_pdf[provider] = 0.0
        provider_pdf[provider] += content_pdf[content-1]

    # print(content_pdf)
    # print(provider_pdf)
    

    user_provider = []
    for provider, ratio in provider_pdf.items():
        user_provider.append(ratio)
    print(user_provider)
    with open('provider_popularity', 'wb') as fp:
        pickle.dump(user_provider, fp)

    ''' for multiple user group '''
    # user_pdf = []
    # if workload.beta != 0:
    #     user_pdf = workload.receiver_dist._pdf
    # else:
    #     'The user group send request uniformly'
    #     user_pdf = [1.0/len(topology.receivers())] * len(topology.receivers())
    # print(user_pdf)

    # user_provider = []
    # for provider, ratio in provider_pdf.items():
    #     tmp_list = []
    #     for user in user_pdf:
    #         tmp_list.append(ratio * user)
    #     user_provider.append(tmp_list)
    # print(user_provider)