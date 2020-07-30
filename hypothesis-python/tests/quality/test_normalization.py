# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2020 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from itertools import islice

import pytest

from hypothesis import strategies as st
from hypothesis.internal.conjecture.shrinking import dfas
from tests.quality.test_shrinking_order import iter_values


@pytest.mark.parametrize("n", range(10, -1, -1))
@pytest.mark.parametrize(
    "strategy", [st.floats(), st.text(), st.datetimes(),], ids=repr
)
def test_common_strategies_normalize_small_values(strategy, n, request):
    if request.config.getoption("--hypothesis-learn-to-normalize"):
        allowed_to_update = True
        required_successes = 1000
    else:
        allowed_to_update = True
        required_successes = 10

    excluded = list(map(repr, islice(iter_values(strategy, unique_by=repr), n)))

    def test_function(data):
        v = data.draw(strategy)
        data.output = repr(v)
        if repr(v) not in excluded:
            data.mark_interesting()

    dfas.normalize(
        repr(strategy),
        test_function,
        allowed_to_update=allowed_to_update,
        required_successes=required_successes,
    )
