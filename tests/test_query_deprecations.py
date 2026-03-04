#
# Copyright (c) 2024 ZettaScale Technology
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
#
# Contributors:
#   ZettaScale Zenoh Team, <zenoh@zettascale.tech>
#
import json
import time
import warnings
from typing import List, Tuple

import zenoh
from zenoh import CongestionControl, Priority, Query, Sample, Session


def open_session(endpoints: List[str]) -> Tuple[Session, Session]:
    # listen peer
    conf = zenoh.Config()
    conf.insert_json5("listen/endpoints", json.dumps(endpoints))
    conf.insert_json5("scouting/multicast/enabled", "false")
    peer01 = zenoh.open(conf)

    # connect peer
    conf = zenoh.Config()
    conf.insert_json5("connect/endpoints", json.dumps(endpoints))
    conf.insert_json5("scouting/multicast/enabled", "false")
    peer02 = zenoh.open(conf)

    return (peer01, peer02)


def close_session(peer01: Session, peer02: Session):
    peer01.close()
    peer02.close()


def test_reply_priority_deprecation():
    """Test that using priority parameter in reply emits a deprecation warning."""
    endpoints = ["tcp/127.0.0.1:17447"]
    peer01, peer02 = open_session(endpoints)

    try:
        queryable_data = []

        def queryable_handler(query: Query):
            queryable_data.append(query)

        # Declare queryable
        _queryable = peer01.declare_queryable("test/path", queryable_handler)
        time.sleep(0.5)

        # Make a query
        result = peer02.get("test/path")
        time.sleep(0.5)

        # Get the query from the queryable
        assert len(queryable_data) == 1
        query = queryable_data[0]

        # Test that priority parameter generates a deprecation warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            query.reply("test/path", "test_payload", priority=Priority.HIGH)
            time.sleep(0.1)

            # Check that a warning was issued
            assert len(w) >= 1
            assert any("priority" in str(warning.message).lower() for warning in w)

    finally:
        close_session(peer01, peer02)


def test_reply_congestion_control_deprecation():
    """Test that using congestion_control parameter in reply emits a deprecation warning."""
    endpoints = ["tcp/127.0.0.1:17448"]
    peer01, peer02 = open_session(endpoints)

    try:
        queryable_data = []

        def queryable_handler(query: Query):
            queryable_data.append(query)

        # Declare queryable
        _queryable = peer01.declare_queryable("test/path", queryable_handler)
        time.sleep(0.5)

        # Make a query
        result = peer02.get("test/path")
        time.sleep(0.5)

        # Get the query from the queryable
        assert len(queryable_data) == 1
        query = queryable_data[0]

        # Test that congestion_control parameter generates a deprecation warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            query.reply(
                "test/path",
                "test_payload",
                congestion_control=CongestionControl.BLOCK,
            )
            time.sleep(0.1)

            # Check that a warning was issued
            assert len(w) >= 1
            assert any(
                "congestion_control" in str(warning.message).lower() for warning in w
            )

    finally:
        close_session(peer01, peer02)


def test_reply_del_priority_deprecation():
    """Test that using priority parameter in reply_del emits a deprecation warning."""
    endpoints = ["tcp/127.0.0.1:17449"]
    peer01, peer02 = open_session(endpoints)

    try:
        queryable_data = []

        def queryable_handler(query: Query):
            queryable_data.append(query)

        # Declare queryable
        _queryable = peer01.declare_queryable("test/path", queryable_handler)
        time.sleep(0.5)

        # Make a query
        result = peer02.get("test/path")
        time.sleep(0.5)

        # Get the query from the queryable
        assert len(queryable_data) == 1
        query = queryable_data[0]

        # Test that priority parameter generates a deprecation warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            query.reply_del("test/path", priority=Priority.HIGH)
            time.sleep(0.1)

            # Check that a warning was issued
            assert len(w) >= 1
            assert any("priority" in str(warning.message).lower() for warning in w)

    finally:
        close_session(peer01, peer02)


def test_reply_del_congestion_control_deprecation():
    """Test that using congestion_control parameter in reply_del emits a deprecation warning."""
    endpoints = ["tcp/127.0.0.1:17450"]
    peer01, peer02 = open_session(endpoints)

    try:
        queryable_data = []

        def queryable_handler(query: Query):
            queryable_data.append(query)

        # Declare queryable
        _queryable = peer01.declare_queryable("test/path", queryable_handler)
        time.sleep(0.5)

        # Make a query
        result = peer02.get("test/path")
        time.sleep(0.5)

        # Get the query from the queryable
        assert len(queryable_data) == 1
        query = queryable_data[0]

        # Test that congestion_control parameter generates a deprecation warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            query.reply_del("test/path", congestion_control=CongestionControl.BLOCK)
            time.sleep(0.1)

            # Check that a warning was issued
            assert len(w) >= 1
            assert any(
                "congestion_control" in str(warning.message).lower() for warning in w
            )

    finally:
        close_session(peer01, peer02)


if __name__ == "__main__":
    test_reply_priority_deprecation()
    print("✓ test_reply_priority_deprecation passed")

    test_reply_congestion_control_deprecation()
    print("✓ test_reply_congestion_control_deprecation passed")

    test_reply_del_priority_deprecation()
    print("✓ test_reply_del_priority_deprecation passed")

    test_reply_del_congestion_control_deprecation()
    print("✓ test_reply_del_congestion_control_deprecation passed")

    print("\nAll deprecation warning tests passed!")
