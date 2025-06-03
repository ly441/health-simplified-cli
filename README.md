
# Health Simplified CLI

A command-line interface (CLI) application for managing users, goals, meal plans, and food entries using Python, Typer, and SQLAlchemy.

## Features

- **User Management:** Add, update, delete, and list users.
- **Goal Tracking:** Set, update, and delete daily/weekly goals for users.
- **Meal Planning:** Create, update, and delete weekly meal plans.
- **Food Logging:** Add, update, and delete food entries for users.
- **Detailed User Reports:** View all details for a specific user, including goals, meal plans, and food entries.

## Requirements

- Python 3.8+
- [Typer](https://typer.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [pytest](https://docs.pytest.org/) (for testing)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/health-simplified-cli.git
   cd health-simplified-cli
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv env
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the CLI from the project root:

```sh
python -m health_cli.cli
```

You will see a menu with options to manage users, goals, meal plans, and food entries.

## Project Structure

```
health-simplified-cli/
├── health_cli/
│   ├── cli.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── users_entry.py
│   │   ├── goals_entry.py
│   │   ├── mealplan_entry.py
│   │   └── food_entry.py
│   └── ...
├── tests/
│   └── test_*.py
├── requirements.txt
└── README.md
```

## Testing

Run all tests with:

```sh
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

MIT License

---

**Enjoy using Health Simplified CLI!**