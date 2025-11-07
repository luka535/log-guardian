import pytest
import os
from log_guardian.parser import parse_log_file

@pytest.fixture
def temp_log_file(tmp_path):
    log_file_path = tmp_path / "test.log"
    return log_file_path


def test_parse_valid_line(temp_log_file):
    log_content = '2023-10-27 10:00:00 INFO: User admin logged in'
    temp_log_file.write_text(log_content)

    results = list(parse_log_file(str(temp_log_file)))

    assert len(results) == 1
    assert results[0]['timestamp'] == '2023-10-27 10:00:00'
    assert results[0]['level'] == 'INFO'
    assert results[0]['message'] == 'User admin logged in'


def test_skip_malformed_line(temp_log_file):

    log_content = 'This is a completely malformed line.'
    temp_log_file.write_text(log_content)

    results = list(parse_log_file(str(temp_log_file)))

    assert len(results) == 0


def test_handle_mixed_lines(temp_log_file):

    log_content = (
        '2023-10-27 10:01:00 ERROR: Connection failed\n'
        'Junk line\n'
        '2023-10-27 10:02:00 DEBUG: Query executed'
    )
    temp_log_file.write_text(log_content)

    results = list(parse_log_file(str(temp_log_file)))

    assert len(results) == 2
    assert results[0]['level'] == 'ERROR'
    assert results[1]['level'] == 'DEBUG'

def test_handle_empty_file(temp_log_file):
 
    temp_log_file.touch()
    results = list(parse_log_file(str(temp_log_file)))
    assert len(results) == 0

def test_non_existent_file():
    results = list(parse_log_file("non_existent_file.log"))    
    assert len(results) == 0