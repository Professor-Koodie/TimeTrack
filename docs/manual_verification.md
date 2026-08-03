Manual verification steps for multi-allocation support

1. Start Django dev server:

```bash
python manage.py migrate
python manage.py runserver
```

2. Open the dashboard at `http://localhost:8000/dashboard/` and log in.
3. Add a timesheet entry using the main form (employee, project, week, hours).
4. In "Additional Allocations", click `+ Add allocation` and fill project and hours.
5. Click Save.
6. Verify in Admin or dashboard table that the employee-week now shows aggregated hours (sum of allocations).
7. Try adding the same project allocation for the same employee/week — it should be skipped (no duplicate created).

Running tests:

```bash
python manage.py test pages
```

If you want stricter validation (e.g., max hours per week), ask me and I'll add server-side checks and user-facing warnings.
