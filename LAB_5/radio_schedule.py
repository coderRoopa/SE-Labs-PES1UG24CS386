import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE slots (id INTEGER PRIMARY KEY, show TEXT, host TEXT, start_hour INTEGER, minutes INTEGER)")
booked_minutes = 0


def add_slot(show, host, start_hour, minutes):
    """Add a radio show to the schedule."""
    conn.execute(
        """
        INSERT INTO slots (show, host, start_hour, minutes)
        VALUES (?, ?, ?, ?)
        """,
        (show, host, start_hour, minutes),
    )


def slotLabel(show, host):
    return "{} hosted by {}".format(show, host)


def overlap_free(start_hour, duration, next_start_hour):
    """Check whether a show ends before the next show starts."""
    return start_hour + duration <= next_start_hour


def morningShows():
    if booked_minutes > 0: return [r[0] for r in conn.execute("SELECT show FROM slots WHERE start_hour < 12")]
    return []


def removeSlot(slot_id):
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)
    print(slotLabel("Sunrise Beats", "Vik"))
    print(overlap_free("7 + 1 <= 13"), morningShows())
    removeSlot(2)


main()