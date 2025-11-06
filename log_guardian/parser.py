from .logger import get_logger

log = get_logger(__name__)

def parse_log_file(file_path):

    log.info(f"Starting to parse file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue 

                try:
                    parts = line.split(' ', 3)
                    if len(parts) < 4 or ':' not in parts[2]:
                        raise ValueError("Line does not match expected format")

                    timestamp = f"{parts[0]} {parts[1]}"
                    level = parts[2].rstrip(':') 
                    message = parts[3]

                    yield {
                        'line_number': i,
                        'timestamp': timestamp,
                        'level': level,
                        'message': message
                    }
                except (ValueError, IndexError) as e:
                    log.warning(
                        f"Skipping malformed line #{i} in {file_path}",
                        extra={'line_content': line, 'error': str(e)}
                    )
                    continue 
    except FileNotFoundError:
        log.error(f"File not found: {file_path}")
    except Exception as e:
        log.error(f"An unexpected error occurred while reading {file_path}", exc_info=True)

if __name__ == '__main__':
    print("--- Running Parser Test ---")
    sample_file = 'log.log'  
    parsed_lines = list(parse_log_file(sample_file))

    print(f"\nSuccessfully parsed {len(parsed_lines)} lines.")
    
    import json
    for entry in parsed_lines[:3]: # Print first 3 parsed entries
        print(json.dumps(entry, indent=2))

    print("\n--- Parser Test Complete ---")