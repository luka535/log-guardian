from typing import List, Dict, Any

def analyze_log_data(parsed_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    suspicious_keywords = ['phpmyadmin', 'wp-login', 'passwd']
    
    results_summary = {
        "total_lines_parsed": len(parsed_data),
        "suspicious_entries_found": 0,
        "suspicious_entries": []
    }
    
    for entry in parsed_data:
        message = entry.get("message", "")
        if not isinstance(message, str):
            continue

        for keyword in suspicious_keywords:
            if keyword in message:
                results_summary["suspicious_entries_found"] += 1
                results_summary["suspicious_entries"].append(entry)
                break
    
    return results_summary