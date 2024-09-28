import json
import argparse
from datetime import datetime, timedelta
import re

def parse_custom_date(date_str):
    try:
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
        return datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Incorrect date format: {date_str}. Expected format is like 'Oct 1st, 2023'.")

def get_most_recent_completions(person):
    most_recent_completions = {}
    for completion in person['completions']:
        training_name = completion['name']
        completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")
        
        if training_name not in most_recent_completions or completion_date > most_recent_completions[training_name]['timestamp']:
            most_recent_completions[training_name] = {
                'timestamp': completion_date,
                'expires': completion.get('expires')
            }
    return most_recent_completions

def count_completed_trainings(data):
    training_counts = {}
    for person in data:
        most_recent_completions = get_most_recent_completions(person)
        for training_name in most_recent_completions:
            if training_name not in training_counts:
                training_counts[training_name] = 0
            training_counts[training_name] += 1
    return training_counts

def filter_trainings_by_fiscal_year(data, trainings, fiscal_year):
    start_date = datetime(fiscal_year - 1, 7, 1)
    end_date = datetime(fiscal_year, 6, 30)
    
    people_by_training = {training: [] for training in trainings}
    
    for person in data:
        most_recent_completions = get_most_recent_completions(person)
        for training_name, completion in most_recent_completions.items():
            completion_date = completion['timestamp']
            if training_name in trainings and start_date <= completion_date <= end_date:
                people_by_training[training_name].append(person['name'])
    
    return people_by_training

def find_expired_or_soon_expiring(data, date):
    target_date = parse_custom_date(date)
    soon_threshold = target_date + timedelta(days=30)
    
    expired_trainings = []
    for person in data:
        most_recent_completions = get_most_recent_completions(person)
        for training_name, completion in most_recent_completions.items():
            expires = completion['expires']
            if expires:
                expiration_date = datetime.strptime(expires, "%m/%d/%Y")
                if expiration_date < target_date:
                    status = 'expired'
                elif target_date <= expiration_date <= soon_threshold:
                    status = 'expires soon'
                else:
                    continue
                
                expired_trainings.append({
                    'name': person['name'],
                    'training': training_name,
                    'expiration': expires,
                    'status': status
                })
    
    return expired_trainings

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Training JSON processor')
    
    def valid_fiscal_year(year):
        try:
            year = int(year)
            if year < 2000 or year > 2100: 
                raise argparse.ArgumentTypeError(f"Fiscal year {year} is out of range (2000-2100).")
            return year
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid fiscal year: {year}. Fiscal year must be an integer.")
    
    
    parser.add_argument('--fiscal_year', type=valid_fiscal_year, help='Fiscal year for filtering training completions', required=True)
    
    
    parser.add_argument('--trainings', nargs='+', help='List of trainings to check for fiscal year completion', required=True)
    
    
    parser.add_argument('--expiration_date', type=str, help='Date to check for soon-to-expire trainings (format: Month day, Year)', required=True)
    
    args = parser.parse_args()

    try:
        
        with open('trainings.txt', 'r') as f:
            data = json.load(f)

        # Task 1: Completed Trainings Count
        completed_training_counts = count_completed_trainings(data)

        # Task 2: People who completed specific trainings in fiscal year
        completed_fiscal_year = filter_trainings_by_fiscal_year(data, args.trainings, args.fiscal_year)

        # Task 3: Expired or Soon Expiring Trainings
        expired_soon_trainings = find_expired_or_soon_expiring(data, args.expiration_date)

        # Output the results as JSON
        with open('output_task_1.json', 'w') as f:
            json.dump(completed_training_counts, f, indent=4)

        with open('output_task_2.json', 'w') as f:
            json.dump(completed_fiscal_year, f, indent=4)

        with open('output_task_3.json', 'w') as f:
            json.dump(expired_soon_trainings, f, indent=4)

        print("JSON outputs generated for all tasks.")

    except Exception as e:
        print(f"Error: {e}")
