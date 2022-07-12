import json

from tests.fixtures.inbox_data import test_data_factory

from fastapi.testclient import TestClient
import pytest


def test_change_non_existent_well(test_client: TestClient, test_data_factory):
    """Expect an error if we try to assign a state to a well which doesn't exist."""

    test_data = {
        "DONT-USE-THIS-RUN": {"A1": None, "B1": None},
        "NOR-THIS-ONE": {"A1": "Passed", "B1": "Failed"},
    }
    test_data_factory(test_data)

    post_data = """
        {
          "user": "user2",
          "date_created": "2022-07-11T13:04:34",
          "date_updated": "2022-07-11T13:04:34",
          "qc_type": "library",
          "qc_type_description": "Sample/library evaluation",
          "qc_state": "Passed",
          "is_preliminary": true,
          "created_by": "LangQC"
        }
    """

    response = test_client.post("/pacbio/run/NONEXISTENT/well/A0/qc_assign", post_data)

    assert response.status_code == 400


def test_change_from_passed_to_fail(test_client: TestClient, test_data_factory):
    """Successfully change a state from passed to faield"""

    test_data = {
        "MARATHON": {"A1": "Passed", "B1": None},
        "SEMI-MARATHON": {"D1": "Claimed"},
    }
    test_data_factory(test_data)

    post_data = """
        {
          "user": "zx80",
          "date_created": "2022-07-11T13:04:34",
          "date_updated": "2022-07-11T13:04:34",
          "qc_type": "library",
          "qc_type_description": "Sample/library evaluation",
          "qc_state": "Failed",
          "is_preliminary": false,
          "created_by": "LangQC"
        }
    """

    response = test_client.post("/pacbio/run/MARATHON/well/A1/qc_assign", post_data)

    assert response.status_code == 200

    content = response.json()

    expected = {
        "user": "zx80",
        "qc_type": "library",
        "qc_type_description": "Sample/library evaluation",
        "qc_state": "Failed",
        "is_preliminary": False,
        "created_by": "LangQC",
    }

    for key, value in expected.items():
        assert content[key] == value


@pytest.mark.parametrize(
    "invalid_argument,expected_message",
    [
        ("qc_type", "QC type is not in the QC database."),
        ("user", "User has not been found in the QC database. Has it been registered?"),
        (
            "qc_state",
            "Desired QC state is not in the QC database. It might not be allowed.",
        ),
    ],
)
def test_error_on_invalid_values(
    test_client: TestClient, test_data_factory, invalid_argument, expected_message
):
    """Test errors returned when invalid arguments are provided."""

    test_data = {
        "MARATHON": {"A1": "Passed", "B1": None},
        "SEMI-MARATHON": {"D1": "Claimed"},
    }
    test_data_factory(test_data)

    post_data = {
        "user": "zx80",
        "date_created": "2022-07-11T13:04:34",
        "date_updated": "2022-07-11T13:04:34",
        "qc_type": "library",
        "qc_type_description": "Sample/library evaluation",
        "qc_state": "Failed",
        "is_preliminary": False,
        "created_by": "LangQC",
    }

    post_data[invalid_argument] = "thisdefinitelyisnotavalidvalue"
    response = test_client.post(
        "/pacbio/run/MARATHON/well/A1/qc_assign", json.dumps(post_data)
    )

    assert response.status_code == 400
    assert response.json()["detail"] == expected_message
