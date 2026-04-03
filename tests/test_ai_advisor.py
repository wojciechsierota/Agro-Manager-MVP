from ai_advisor import get_farm_summary, ask_ai_advisor


def test_get_farm_summary(mocker):
    mock_db = mocker.patch("ai_advisor.DatabaseManager").return_value
    mock_db.fetch_all.side_effect = [
        [("North Field", "Planting", "Planting Strawberies", "2024-01-01")],
        [("North Field", 100, 500)]
    ]

    result = get_farm_summary()
    assert "North Field" in result
    assert "Planting" in result

def test_ask_ai_advisor(mocker):
    mocker.patch("ai_advisor.get_farm_summary", return_value="Farm data")
    
    mocker.patch("ai_advisor.load_history", return_value=[])
    mocker.patch("ai_advisor.save_history")

    mock_response = mocker.Mock()
    mock_response.text = "Text"
    mocker.patch("ai_advisor.client.models.generate_content", return_value=mock_response)

    mocker.patch("builtins.input", side_effect=["What question?", "quit"])

    ask_ai_advisor()


def test_ask_ai_advisor_error(mocker):
    mocker.patch("ai_advisor.get_farm_summary", return_value="Farm data")

    mocker.patch("ai_advisor.load_history", return_value=[])
    mocker.patch("ai_advisor.save_history")

    mocker.patch("ai_advisor.client.models.generate_content",
                  side_effect=Exception("Connection Error"))
    
    mock_print = mocker.patch("builtins.print")

    mocker.patch("builtins.input", side_effect=["Hi", "quit"])

    ask_ai_advisor()

    mock_print.assert_any_call("Error: Connection Error\n")
    mock_print.assert_any_call("Returning to main menu...\n")