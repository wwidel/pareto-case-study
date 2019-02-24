from adtrees import ADTree
from adtrees import ParetoDomain
from adtrees import BasicAssignment
import time


def prepare():
    '''
    Loads the tree and the basic assignment from files, creates
    appropriate Pareto domain.

    Returns (ADTree, ParetoDomain, BasicAssignment).
    '''
    T = ADTree('reconfigure_power_meter.xml')
    # the following has to be done to avoid a mismatch between the labels
    # obtained from ADTool's .xml (which contain the newline symbol '\n')
    # and the ones from the .txt file storing the basic assignment (where all
    # '\n's are replaced with a space)
    for node in T.dict:
        node.label = node.label.replace('\n', ' ')
    # create the domain for 1 cost and 4 min/max domains
    pd = ParetoDomain(1, 4)
    ba = BasicAssignment('consensus.txt')
    return T, pd, ba


def modify_assignment(basic, tree, scenario=1):
    '''
    Depending on the choice of the scenario, modify the values assigned to the basic actions of the opponent.
    '''
    neutral = [[0 for i in range(5)]]
    absorbing = [[2**20 for i in range(5)]]
    defenders_actions = tree.basic_actions('d')
    # Scenario 1: defender does nothing; starting point for assigments for the
    # remaining scenarios
    for b in defenders_actions:
        basic[b] = neutral

    # Scenario 2: defender does
    #   'enforce policy of performing thorough background checks on employees'
    if scenario == 2:
        basic['enforce policy of performing thorough background checks on employees'] = absorbing

    # Scenario 3: defender does
    #   'require authentication for establishing connection'
    if scenario == 3:
        basic['require authentication for establishing connection'] = absorbing

    # Scenario 4: defender does
    #   'enforce policy of performing thorough background checks on employees'
    #   'require authentication for establishing connection'
    if scenario == 4:
        basic['enforce policy of performing thorough background checks on employees'] = absorbing
        basic['require authentication for establishing connection'] = absorbing

    # Scenario 5: defender does
    #   'enforce policy of performing thorough background checks on employees'
    #   'require authentication for establishing connection'
    #   'limit the number of possible invalid authentication attempts'
    if scenario == 5:
        basic['enforce policy of performing thorough background checks on employees'] = absorbing
        basic['require authentication for establishing connection'] = absorbing
        basic['limit the number of possible invalid authentication attempts'] = absorbing

    return basic


def timing(scen=1):
    '''
    How much time does it take to compute both Pareto optimal values and the corresponding strategies?
    '''
    # start the clock
    start = time.clock()
    # feedback
    print(10 * "=" + " Scenario {}:".format(scen) + 10 * "=")
    # 1. get tree, Pareto domain and assingment of values for the proponent
    T, pd, ba = prepare()
    # 2. modify the assignment, depending on the selected scenario
    ba = modify_assignment(ba, T, scen)
    # 3. compute Pareto optimal values using evaluation on set semantics
    set_sem = T.set_semantics()
    pareto_optimal = pd.evaluateSS(T, ba, set_sem)
    # 4. to determine Pareto optimal strategies, compute values corresponding to particular strategies in the given
    # scenario and compare them to the Pareto optimal values
    for strategy in set_sem:
        # strategy = (P, O)
        # compute the value for the strategy
        # put the actions of both actors in one list
        prop = strategy[0]
        opp = strategy[1]
        total = [b for b in prop]
        for b in opp:
            total.append(b)
        #
        val = []
        # cost
        val.append(sum([ba[b][0][0] for b in total]))
        # remaining values
        for i in range(1, 5):
            val.append(max([ba[b][0][i] for b in total]))
        # check if the obtained value is Pareto optimal
        if val in pareto_optimal:
            print('The strategy')
            print(strategy)
            print("is Pareto optimal, and its value is {}.\n".format(val))

    # stop the clock
    end = time.clock()
    res = (end - start)
    if res < 0.01:
        return '===== Time elapsed: < 0.01 seconds. =====\n'
    else:
        return '===== Time elapsed: {} seconds. =====\n'.format(round(res, 2))

if __name__ == '__main__':
    for i in range(1, 6):
        print(timing(i))
