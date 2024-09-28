# UIC_Assignment
# Training Completion Processor

This is a console application that processes training completion data from a JSON file. The script performs three tasks:

1. **Counts how many people have completed each training.**
2. **Lists all people who completed specific trainings in a given fiscal year.**
3. **Finds people with trainings that have expired or will expire within one month of a given date.**

## Requirements

- Python 3.x
- JSON file containing the training completion data (`trainings.txt`).

## Installation

Clone the repository:
    
    git clone https://github.com/srimankatipally/UIC_Assignment.git
    cd UIC_Assignment
    


## How to Run the Script

This is a console-based application. You need to pass several parameters when running the script. The following sections describe each parameter.

### Command-Line Parameters

1. **`--fiscal_year`** (required):
   - The fiscal year to filter training completions.
   - It should be an integer representing the year (e.g., 2024).
   - Example: If the fiscal year is 2024, it will look for training completions between **July 1, 2023** and **June 30, 2024**.

2. **`--trainings`** (required):
   - A list of trainings for which you want to filter completion data.
   - It can accept multiple training names, and you should pass each name as a separate string.
   - Example: `"Electrical Safety for Labs"`, `"X-Ray Safety"`, `"Laboratory Safety Training"`.

3. **`--expiration_date`** (required):
   - The date you want to check for expired or soon-to-expire trainings.
   - The format should be like `"Oct 1st, 2023"`. The script will handle common ordinal suffixes such as `st`, `nd`, `rd`, and `th`.
   - It will check if a training expires on or before this date or within 30 days after this date.

### Example Usage

You can run the script as follows:

```bash
python script.py --fiscal_year 2024 --trainings "Electrical Safety for Labs" "X-Ray Safety" "Laboratory Safety Training" --expiration_date "Oct 1st, 2023"
