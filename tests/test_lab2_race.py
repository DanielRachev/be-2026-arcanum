from __future__ import annotations

import pytest

from lab2_relay_race.community import RoundResult
from lab2_relay_race.race import (
    _looks_like_duplicate_success,
    build_ordered_signature_list,
)
from lab2_relay_race.team import load_team_config


def test_build_ordered_signature_list_uses_registration_order():
    team = load_team_config("lab2_team.json")
    signatures = {
        team.members[2].pubkey_hex: b"sig-c",
        team.members[0].pubkey_hex: b"sig-a",
        team.members[1].pubkey_hex: b"sig-b",
    }

    assert build_ordered_signature_list(team, signatures) == [
        b"sig-a",
        b"sig-b",
        b"sig-c",
    ]


def test_build_ordered_signature_list_requires_all_members():
    team = load_team_config("lab2_team.json")

    with pytest.raises(ValueError, match="Missing signatures"):
        build_ordered_signature_list(team, {team.members[0].pubkey_hex: b"sig-a"})


def test_duplicate_no_active_challenge_can_mean_recorded_round():
    result = RoundResult(
        success=False,
        round_number=1,
        rounds_completed=1,
        message="Rejected: no active challenge for this group",
    )

    assert _looks_like_duplicate_success(result, 1)


def test_no_active_challenge_without_round_progress_is_not_success():
    result = RoundResult(
        success=False,
        round_number=2,
        rounds_completed=1,
        message="Rejected: no active challenge for this group",
    )

    assert not _looks_like_duplicate_success(result, 2)
