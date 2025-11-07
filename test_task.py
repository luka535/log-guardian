from log_guardian.celery_worker import process_log_file
import time

def main():
    print("--- Starting Task Dispatcher ---")
    report_id = 123
    
    print(f"Dispatching 'process_log_file' task for report ID: {report_id}...")

    task = process_log_file.delay(report_id)
    
    print(f"Task dispatched successfully! Task ID: {task.id}")    
    print("\nWaiting for task to complete...")
    result = task.get(timeout=20) # Wait max 20 seconds for a result
    print(f"Task completed! Result: '{result}'")

    print("\n--- Task Dispatcher Finished ---")


if __name__ == "__main__":
    main()