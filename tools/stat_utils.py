# Thanks to Gary Linscott for fishtest and consequently this script.
# raw.githubusercontent.com/glinscott/fishtest/dfde4103771b8a30ca0b46926566d823c463cfed/fishtest/fishtest/stat_util.py

import math


def erf(x):
    # Python 2.7 defines math.erf(), but we need to cater for older versions.
    a = 8 * (math.pi - 3) / (3 * math.pi * (4 - math.pi))
    x2 = x * x
    y = -x2 * (4 / math.pi + a * x2) / (1 + a * x2)
    return math.copysign(math.sqrt(1 - math.exp(y)), x)


def erf_inv(x):
    # Above erf formula inverted analytically
    a = 8 * (math.pi - 3) / (3 * math.pi * (4 - math.pi))
    y = math.log(1 - x * x)
    z = 2 / (math.pi * a) + y / 2
    return math.copysign(math.sqrt(math.sqrt(z * z - y / a) - z), x)


def phi(q):
    # Cumulative distribution function for the standard Gaussian law: quantile -> probability
    return 0.5 * (1 + erf(q / math.sqrt(2)))


def phi_inv(p):
    # Quantile function for the standard Gaussian law: probability -> quantile
    assert (0 <= p <= 1)
    return math.sqrt(2) * erf_inv(2 * p - 1)


def get_simple_elo(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -400 * math.log10(1 / x - 1)


def get_elo(wld):
    # win/loss/draw ratio
    games = sum(wld)
    wins = float(wld[0]) / games
    losses = float(wld[1]) / games
    draws = float(wld[2]) / games

    # mu is the empirical mean of the variables (Xi), assumed i.i.d.
    mu = wins + draws / 2

    # stdev is the empirical standard deviation of the random variable
    # (X1 + X2 + ... + X_N) / N
    stdev = math.sqrt(
        wins * (1 - mu) ** 2
        + losses * (0 - mu) ** 2
        + draws * (0.5 - mu) ** 2
    ) / math.sqrt(games)

    # 95% confidence interval for mu
    mu_min = mu + phi_inv(0.025) * stdev
    mu_max = mu + phi_inv(0.975) * stdev

    el = get_simple_elo(mu)
    elo95 = (get_simple_elo(mu_max) - get_simple_elo(mu_min)) / 2
    los = phi((mu - 0.5) / stdev)

    return el, elo95, los


def bayeselo_to_probability(elo, draw_elo):
    """
    elo is expressed in BayesELO (relative to the choice draw_elo).
    Returns a probability, P['win'], P['loss'], P['draw']
    """
    probability = {
        'win': 1.0 / (1.0 + pow(10.0, (-elo + draw_elo) / 400.0)),
        'loss': 1.0 / (1.0 + pow(10.0, (elo + draw_elo) / 400.0)),
    }
    probability['draw'] = 1.0 - probability['win'] - probability['loss']
    return probability


def probability_to_bayeselo(probability):
    """
    Takes a probability: P['win'], P['loss']
    Returns elo, draw_elo
    """
    assert (0 < probability['win'] < 1 and 0 < probability['loss'] < 1)
    elo = 200 * math.log10(
        probability['win'] / probability['loss']
        * (1 - probability['loss']) / (1 - probability['win'])
    )
    draw_elo = 200 * math.log10(
        (1 - probability['loss']) / probability['loss']
        * (1 - probability['win']) / probability['win']
    )
    return elo, draw_elo


def SPRT(R, elo0, alpha, elo1, beta, draw_elo):
    """
    Sequential Probability Ratio Test
    H0: elo = elo0
    H1: elo = elo1
    alpha = max typeI error (reached on elo = elo0)
    beta = max typeII error for elo >= elo1 (reached on elo = elo1)
    R['wins'], R['losses'], R['draws'] contains the number of wins, losses and draws

    Returns a dict:
    finished - bool, True means test is finished, False means continue sampling
    state - string, 'accepted', 'rejected' or ''
    llr - Log-likelihood ratio
    lower_bound/upper_bound - SPRT bounds
    """

    result = {
        'finished': False,
        'state': '',
        'llr': 0.0,
        'lower_bound': math.log(beta / (1 - alpha)),
        'upper_bound': math.log((1 - beta) / alpha),
    }

    # Estimate draw_elo out of sample
    if R['wins'] > 0 and R['losses'] > 0 and R['draws'] > 0:
        games = R['wins'] + R['losses'] + R['draws']
        prob = {
            'win': float(R['wins']) / games,
            'loss': float(R['losses']) / games,
            'draw': float(R['draws']) / games
        }
        elo, draw_elo = probability_to_bayeselo(prob)
    else:
        return result

    # Probability laws under H0 and H1
    prob_0 = bayeselo_to_probability(elo0, draw_elo)
    prob_1 = bayeselo_to_probability(elo1, draw_elo)

    # Log-Likelihood Ratio
    result['llr'] = (
            R['wins'] * math.log(prob_1['win'] / prob_0['win'])
            + R['losses'] * math.log(prob_1['loss'] / prob_0['loss'])
            + R['draws'] * math.log(prob_1['draw'] / prob_0['draw'])
    )

    if result['llr'] < result['lower_bound']:
        result['finished'] = True
        result['state'] = 'rejected'
    elif result['llr'] > result['upper_bound']:
        result['finished'] = True
        result['state'] = 'accepted'

    return result


if __name__ == "__main__":
    # unit tests
    print(SPRT({'wins': 10, 'losses': 0, 'draws': 20}, 0, 0.05, 5, 0.05, 200))
    print(SPRT({'wins': 10, 'losses': 1, 'draws': 20}, 0, 0.05, 5, 0.05, 200))
    print(SPRT({'wins': 5019, 'losses': 5026, 'draws': 15699}, 0, 0.05, 5, 0.05, 200))
    print(SPRT({'wins': 1450, 'losses': 1500, 'draws': 4000}, 0, 0.05, 6, 0.05, 200))
    print(SPRT({'wins': 716, 'losses': 591, 'draws': 2163}, 0, 0.05, 6, 0.05, 200))
    print(get_elo([716, 591, 2163]))
