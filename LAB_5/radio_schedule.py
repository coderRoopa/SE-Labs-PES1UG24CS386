import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE slots (
        id INTEGER PRIMARY KEY,
        show TEXT NOT NULL,
        host TEXT NOT NULL,
        start_hour INTEGER NOT NULL,
        minutes INTEGER NOT NULL
    )
    """
)


def add_slot(show, host, start_hour, minutes):
    """Add a radio show to the schedule."""
    conn.execute(
        """
        INSERT INTO slots (show, host, start_hour, minutes)
        VALUES (?, ?, ?, ?)
        """,
        (show, host, start_hour, minutes),
    )


def slot_label(show, host):
    """Return a formatted label for a radio show."""
    return f"{show} hosted by {host}"


def overlap_free(start_hour, duration, next_start_hour):
    """Check whether a show ends before the next show starts."""
    return start_hour + duration <= next_start_hour


def morning_shows():
    """Return the names of shows starting before noon."""
    return [
        row[0]
        for row in conn.execute(
            "SELECT show FROM slots WHERE start_hour < ?",
            (12,),
        )
    ]


def remove_slot(slot_id):
    """Remove a radio show using its database ID."""
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    """Demonstrate radio show scheduling operations."""
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)

    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free(7, 1, 13), morning_shows())

    remove_slot(2)


if __name__ == "__main__":
    main()