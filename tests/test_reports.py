import pytest
import datetime
from reports import add_sale, add_operations, add_new_field, delete_operations, delete_field, update_operation_cost, get_financial_report

def test_add_sale_success(mocker):
    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mock_db.fetch_all.return_value = [(1, "North Field")]
    mock_db.get_int.return_value = 1
    mock_db.get_float.side_effect = [10.5, 5000]
    mocker.patch("builtins.input", return_value="Wheat")

    add_sale()

    assert mock_db.execute_query.called
    args, _ = mock_db.execute_query.call_args
    params_sent = args[1]
    assert params_sent[0] == 1  
    assert params_sent[1] == "Wheat"  
    assert params_sent[2] == 10.5 
    assert params_sent[3] == 5000.0


def test_add_operation_success(mocker):
    fake_now = datetime.datetime(2026, 4, 1)
    mock_datetime = mocker.patch("reports.datetime.datetime")
    mock_datetime.now.return_value = fake_now

    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mock_db.fetch_all.return_value = [(1, "Pole Polnocne")]
    mock_db.get_int.return_value = 1
    mocker.patch("builtins.input", side_effect=["Planting", "Planting strawberries"])
    mock_db.get_float.return_value = 1500

    add_operations()

    assert mock_db.execute_query.called
    args, _ = mock_db.execute_query.call_args
    params_sent = args[1]
    assert params_sent[0] == 1
    assert params_sent[1] == "Planting"
    assert params_sent[2] == "Planting strawberries"
    assert params_sent[3] == "2026-04-01"
    assert params_sent[4] == 1500


def test_add_new_field_success(mocker):
    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mocker.patch("builtins.input", return_value="North Field")
    mock_db.get_float.return_value = 10.5
    add_new_field()
    assert mock_db.execute_query.called
    args, _ = mock_db.execute_query.call_args
    params_sent = args[1]
    assert params_sent[0] == "North Field"
    assert params_sent[1] == 10.5


def test_delete_operation_success(mocker):
    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mock_db.fetch_all.return_value = [(1, "Planting")]
    mock_db.get_int.return_value = 1

    delete_operations()

    assert mock_db.execute_query.called
    args, _ = mock_db.execute_query.call_args
    sql_query = args[0]
    params = args[1]
    assert "DELETE" in sql_query
    assert params[0] == 1


def test_delete_field(mocker):
    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mock_db.fetch_all.return_value = [(1, "North Field")]
    mock_db.get_int.return_value = 1
    mocker.patch("builtins.input", return_value="Y")

    delete_field()

    assert mock_db.execute_query.called
    args, _ = mock_db.execute_query.call_args
    sql_query = args[0]
    params = args[1]
    assert "DELETE" in sql_query
    assert params[0] == 1


def test_delete_field_cancelled(mocker):
    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mock_db.fetch_all.return_value = [(1, "North Field")]
    mock_db.get_int.return_value = 1
    mocker.patch("builtins.input", return_value="N")
    mock_print = mocker.patch("builtins.print")
    
    delete_field()

    expected_output = "Deletion cancelled."
    mock_print.assert_any_call(expected_output)


def test_update_operation_cost(mocker):
    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mock_db.fetch_all.return_value = [(1, "Planting", 1500)]
    mock_db.get_int.return_value = 1
    mock_db.get_float.return_value = 2000.0
    mocker.patch("builtins.input", return_value="Y")

    update_operation_cost()

    assert mock_db.execute_query.called
    args, _ = mock_db.execute_query.call_args
    sql_query = args[0]
    params = args[1]
    assert "UPDATE Operations" in sql_query
    assert "SET cost = ?" in sql_query
    assert params == (2000.0, 1)


def test_get_financial_report_hardcoded(mocker):
    mock_db = mocker.patch("reports.DatabaseManager").return_value
    mock_db.fetch_all.return_value = [("North Field", 1000.0, 2500.0)]
    mock_print = mocker.patch("builtins.print")

    get_financial_report()

    expected_output = "Field: North Field | Costs: 1000.0 | Income: 2500.0 | Balance: 1500.0 PLN"
    mock_print.assert_any_call(expected_output)
