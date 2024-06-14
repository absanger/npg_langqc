import pytest
from npg_id_generation.pac_bio import PacBioEntity

from lang_qc.db.helper.wells import WellWh
from lang_qc.models.pacbio.qc_data import QCDataWell
from tests.fixtures.sample_data import multiplexed_run, simplex_run


def test_creating_qc_data_well(mlwhdb_test_session, mlwhdb_load_runs):
    """
    Check that run-well metrics are correctly transformed for client rendering
    """

    helper = WellWh(session=mlwhdb_test_session)

    id_product = PacBioEntity(
        run_name="TRACTION-RUN-525", well_label="A1"
    ).hash_product_id()
    row = helper.get_mlwh_well_by_product_id(id_product)

    qc = QCDataWell.from_orm(row)

    assert qc.smrt_link == {
        "run_uuid": "f1490bb9-7a99-45b2-9d79-24582881742d",
        "dataset_uuid": "a9ad9f86-04c2-4194-ba69-48240cb745f9",
        "hostname": "pacbio02.dnapipelines.sanger.ac.uk",
    }, "SMRTLink properties extracted to special format"

    assert qc.binding_kit == {
        "value": "Revio polymerase kit",
        "label": "Binding Kit",
    }, "Binding kit unchanged"

    assert qc.control_num_reads == {
        "value": 2724,
        "label": "Number of Control Reads",
    }, "Control reads unchanged"

    assert qc.control_read_length_mean == {
        "value": 59917,
        "label": "Control Read Length (bp)",
    }, "Read length mean unchanged"

    assert qc.hifi_read_bases == {
        "value": 92.92,
        "label": "CCS Yield (Gb)",
    }, "Gigabase conversion is rounded"

    assert qc.hifi_read_length_mean == {
        "value": 11199,
        "label": "CCS Mean Length (bp)",
    }, "Hifi read length mean unaltered"

    assert qc.local_base_rate == {
        "value": 2.18,
        "label": "Local Base Rate",
    }, "Local base rate is rounded to 2dp"

    assert qc.p0_num == {"value": 23.23, "label": "P0 %"}, "Percentages are rounded p0"

    assert qc.p1_num == {"value": 74.56, "label": "P1 %"}, "Percentages are rounded p1"

    assert qc.p2_num == {"value": 2.21, "label": "P2 %"}, "Percentages are rounded p2"

    assert qc.polymerase_read_bases == {
        "value": 1324.87,
        "label": "Total Cell Yield (Gb)",
    }, "Total cell yield is scaled to gigabases"

    assert qc.polymerase_read_length_mean == {
        "value": 70623,
        "label": "Mean Polymerase Read Length (bp)",
    }, "Mean polymerase read length unchanged"

    assert qc.movie_minutes == {
        "value": 24,
        "label": "Run Time (hr)",
    }, "Time converted to hours"

    assert qc.percentage_deplexed_reads == {
        "value": 99.49,
        "label": "Percentage of reads deplexed",
    }, "Demultiplexed percentages are calculated"

    assert qc.percentage_deplexed_bases == {
        "value": 99.48,
        "label": "Percentage of bases deplexed",
    }, "Demultiplexed percentages are calculated"

    # and check the less populated data leads to Nones
    id_product = PacBioEntity(
        run_name="TRACTION-RUN-92", well_label="A1"
    ).hash_product_id()
    row = helper.get_mlwh_well_by_product_id(id_product)
    qc = QCDataWell.from_orm(row)

    assert (
        qc.percentage_deplexed_bases["value"] == None
    ), "Absent metrics mean this is set to none"
    assert (
        qc.percentage_deplexed_reads["value"] == None
    ), "Absent metrics mean this is set to none"


def test_pool_metrics_from_single_sample_well(mlwhdb_test_session, simplex_run):
    helper = WellWh(session=mlwhdb_test_session)
    id = PacBioEntity(
        run_name=simplex_run.pac_bio_run_name,
        well_label=simplex_run.well_label,
        plate_number=simplex_run.plate_number,
    ).hash_product_id()

    metrics = helper.get_metrics_by_well_product_id(id)
    assert metrics is None, "Got no metrics for a one-sample well"


def test_pool_metrics_from_well(mlwhdb_test_session, multiplexed_run):
    helper = WellWh(session=mlwhdb_test_session)
    id = PacBioEntity(run_name="RUN", well_label="B1", plate_number=1).hash_product_id()
    metrics = helper.get_metrics_by_well_product_id(id)

    assert metrics, "Two samples means we get a metrics response"
    assert (
        int(metrics.pool_coeff_of_variance) == 47
    ), "Variance between 20 and 10 is ~47%"

    assert metrics.products[0].hifi_read_bases == 100
    assert (
        metrics.products[1].hifi_read_bases == 900
    ), "hifi read base counts are faithfully copied"

    assert (
        int(metrics.products[0].percentage_total_reads) == 33
    ), "10 of 30 reads is 33.3%"
    assert (
        int(metrics.products[1].percentage_total_reads) == 66
    ), "20 of 30 reads is 66.6%"


def test_pool_metrics_from_well(mlwhdb_test_session):

    id = PacBioEntity(
        run_name="TRACTION-RUN-1140", well_label="C1", plate_number=2
    ).hash_product_id()
    helper = WellWh(session=mlwhdb_test_session)
    with pytest.raises(
        Exception, match=r"Partially linked LIMS data or no linked LIMS data"
    ):
        helper.get_metrics_by_well_product_id(id)
