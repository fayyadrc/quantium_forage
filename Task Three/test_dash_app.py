import pytest
import sys
import os
from dash.testing.application_runners import import_app

# Add the current directory to Python path so we can import dash_app
sys.path.insert(0, os.path.dirname(__file__))


def test_header_present(dash_duo):
    """Test that the header is present in the app."""
    # Import the app
    from dash_app import app
    
    # Start the server
    dash_duo.start_server(app)
    
    # Wait for the page to load and check for header
    dash_duo.wait_for_element("h1", timeout=10)
    
    # Find the header element
    header = dash_duo.find_element("h1")
    
    # Assert that the header text is correct
    assert "Soul Foods - Pink Morsel Sales Analysis" in header.text
    print("✓ Header test passed: Header is present with correct text")


def test_visualization_present(dash_duo):
    """Test that the visualization (chart) is present in the app."""
    # Import the app
    from dash_app import app
    
    # Start the server
    dash_duo.start_server(app)
    
    # Wait for the graph component to load
    dash_duo.wait_for_element("#sales-chart", timeout=15)
    
    # Find the graph element
    graph_element = dash_duo.find_element("#sales-chart")
    
    # Assert that the graph element exists
    assert graph_element is not None
    
    # Wait for plotly to render the graph
    dash_duo.wait_for_element(".plotly-graph-div", timeout=10)
    plotly_graph = dash_duo.find_element(".plotly-graph-div")
    assert plotly_graph is not None
    print("✓ Visualization test passed: Chart is present and rendered")


def test_region_picker_present(dash_duo):
    """Test that the region picker (radio buttons) is present in the app."""
    # Import the app
    from dash_app import app
    
    # Start the server
    dash_duo.start_server(app)
    
    # Wait for the radio items to load
    dash_duo.wait_for_element("#region-selector", timeout=10)
    
    # Find the region selector element
    region_selector = dash_duo.find_element("#region-selector")
    assert region_selector is not None
    
    # Check that radio button inputs are present
    radio_inputs = dash_duo.find_elements("#region-selector input[type='radio']")
    assert len(radio_inputs) >= 5, f"Expected at least 5 radio buttons, found {len(radio_inputs)}"
    
    # Check that the region selector has the expected structure
    region_selector_html = region_selector.get_attribute('innerHTML')
    expected_regions = ["All Regions", "North", "East", "South", "West"]
    
    for region in expected_regions:
        assert region in region_selector_html, f"Region '{region}' not found in radio options"
    
    print("✓ Region picker test passed: All required radio button options are present")


def test_app_components_integration(dash_duo):
    """Test that all main components work together."""
    # Import the app
    from dash_app import app
    
    # Start the server
    dash_duo.start_server(app)
    
    # Wait for all main components to load
    dash_duo.wait_for_element("h1", timeout=10)
    dash_duo.wait_for_element("#region-selector", timeout=10)
    dash_duo.wait_for_element("#sales-chart", timeout=15)
    dash_duo.wait_for_element("#summary-content", timeout=10)
    
    # Verify all components are present
    header = dash_duo.find_element("h1")
    region_selector = dash_duo.find_element("#region-selector")
    chart = dash_duo.find_element("#sales-chart")
    summary = dash_duo.find_element("#summary-content")
    
    assert header is not None
    assert region_selector is not None
    assert chart is not None
    assert summary is not None
    
    print("✓ Integration test passed: All main components are present and loaded")


if __name__ == "__main__":
    # Run the tests with verbose output
    pytest.main([__file__, "-v", "-s"])