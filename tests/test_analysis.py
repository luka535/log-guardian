import pytest
from log_guardian.analysis import analyze_log_data

def test_analysis_with_suspicious_entries():

    sample_data = [
        {'line_number': 1, 'message': 'User logged in successfully.'},
        {'line_number': 2, 'message': 'Attempted access to /phpmyadmin/ by 192.168.1.100'},
        {'line_number': 3, 'message': 'Failed login for admin on wp-login.php'},
        {'line_number': 4, 'message': 'File integrity check passed.'}
    ]

    results = analyze_log_data(sample_data)

    assert results['total_lines_parsed'] == 4
    assert results['suspicious_entries_found'] == 2
    assert len(results['suspicious_entries']) == 2
    assert results['suspicious_entries'][0]['line_number'] == 2
    assert results['suspicious_entries'][1]['message'] == 'Failed login for admin on wp-login.php'

def test_analysis_with_no_suspicious_entries():

    sample_data = [
        {'line_number': 1, 'message': 'User logged in successfully.'},
        {'line_number': 2, 'message': 'Image uploaded to /images/logo.png'},
        {'line_number': 3, 'message': 'Cache cleared successfully.'}
    ]

    results = analyze_log_data(sample_data)

    assert results['total_lines_parsed'] == 3
    assert results['suspicious_entries_found'] == 0
    assert len(results['suspicious_entries']) == 0

def test_analysis_with_empty_input():

    sample_data = []

    results = analyze_log_data(sample_data)

    assert results['total_lines_parsed'] == 0
    assert results['suspicious_entries_found'] == 0
    assert len(results['suspicious_entries']) == 0

def test_analysis_with_malformed_entry():

    sample_data = [
        {'line_number': 1}, # Missing 'message' key
        {'line_number': 2, 'message': None}, # Message is not a string
        {'line_number': 3, 'message': 'Valid access to passwd page is not possible.'}, # Contains 'passwd'
        {'line_number': 4, 'message': 12345} # Message is not a string
    ]

    results = analyze_log_data(sample_data)

    assert results['total_lines_parsed'] == 4
    assert results['suspicious_entries_found'] == 1
    assert results['suspicious_entries'][0]['line_number'] == 3