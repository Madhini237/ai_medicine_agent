from database import create_tables
from scheduler import start_scheduler
from telegram_bot import run_bot


def main():

    print("Starting AI Medicine Agent...")

    create_tables()

    start_scheduler()

    run_bot()


if __name__ == "__main__":
    main()