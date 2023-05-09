from fastapi.testclient import TestClient

from tests.conftest import insert_from_yaml
from tests.fixtures.well_data import load_data4well_retrieval, load_dicts_and_users


def test_get_well_info(
    test_client: TestClient, mlwhdb_test_session, load_data4well_retrieval
):

    insert_from_yaml(
        mlwhdb_test_session, "tests/data/mlwh_pb_run_92", "lang_qc.db.mlwh_schema"
    )

    response = test_client.get("/pacbio/run/MARATHON/well/A0")
    assert response.status_code == 404
    assert response.json()["detail"] == "PacBio well A0 run MARATHON not found."

    response = test_client.get("/pacbio/run/TRACTION-RUN-92/well/A1")
    assert response.status_code == 200
    result = response.json()

    assert result["label"] == "A1"
    assert result["run_name"] == "TRACTION-RUN-92"
    assert result["run_start_time"] == "2022-04-14T12:52:34"
    assert result["run_complete_time"] == "2022-04-20T09:16:53"
    assert result["well_start_time"] == "2022-04-14T13:02:48"
    assert result["well_complete_time"] == "2022-04-16T12:36:21"
    assert result["qc_state"] is None

    expected_metrics = {
        "smrt_link": {
            "run_uuid": "7f5d45ed-aa93-46a6-92b2-4b11d4bf29da",
            "dataset_uuid": "7f5d45ed-aa93-46a6-92b2-4b11d4bf29ro",
            "hostname": "pacbio01.dnapipelines.sanger.ac.uk",
        },
        "binding_kit": {"value": "Sequel II Binding Kit 2.2", "label": "Binding Kit"},
        "control_num_reads": {"value": 24837, "label": "Number of Control Reads"},
        "control_read_length_mean": {
            "value": 50169,
            "label": "Control Read Length (bp)",
        },
        "hifi_read_bases": {"value": 27.08, "label": "CCS Yield (Gb)"},
        "hifi_read_length_mean": {"value": 9411, "label": "CCS Mean Length (bp)"},
        "local_base_rate": {"value": 2.77, "label": "Local Base Rate"},
        "p0_num": {"value": 34.94, "label": "P0 %"},
        "p1_num": {"value": 62.81, "label": "P1 %"},
        "p2_num": {"value": 2.25, "label": "P2 %"},
        "polymerase_read_bases": {"value": 645.57, "label": "Total Cell Yield (Gb)"},
        "polymerase_read_length_mean": {
            "value": 128878,
            "label": "Mean Polymerase Read Length (bp)",
        },
        "movie_minutes": {"value": 30, "label": "Run Time (hr)"},
    }
    assert result["metrics"] == expected_metrics

    etrack = result["experiment_tracking"]
    assert etrack is not None
    assert etrack["num_samples"] == 1
    assert etrack["study_id"] == ["6457"]
    assert etrack["study_name"] == "Tree of Life - ASG"
    assert etrack["sample_id"] == "7880641"
    assert etrack["sample_name"] == "TOL_ASG12404704"
    assert etrack["library_type"] == ["PacBio_Ultra_Low_Input"]
    assert etrack["tag_sequence"] == []

    response = test_client.get("/pacbio/run/TRACTION_RUN_1/well/B1")
    assert response.status_code == 200
    result = response.json()

    assert result["label"] == "B1"
    assert result["run_name"] == "TRACTION_RUN_1"
    assert result["experiment_tracking"] is None
    expected_qc_state = {
        "qc_state": "On hold",
        "is_preliminary": True,
        "qc_type": "sequencing",
        "outcome": None,
        "id_product": "b5a7d41453097fe3cc59644a679186e64a2147833ecc76a2870c5fe8068835ae",
        "date_created": "2022-12-08T07:15:19",
        "date_updated": "2022-12-08T07:15:19",
        "user": "zx80@example.com",
        "created_by": "LangQC",
    }
    assert result["qc_state"] == expected_qc_state

    response = test_client.get("/pacbio/run/TRACTION-RUN-92/well/D1")
    assert response.status_code == 200
    result = response.json()

    assert result["metrics"]["smrt_link"]["dataset_uuid"] is None
