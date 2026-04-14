"""
Purpose of this script:
This script demonstrates encapsulation in Python by creating a secure
database connector class with private and protected attributes.
It also shows how getters and setters control access to sensitive data.
"""


class DatabaseConnector:
    """
    A class that simulates a secure database connection manager.
    """

    def __init__(self, connection_string: str) -> None:
        self.__connection_string = connection_string  # private attribute
        self._status = "disconnected"  # protected attribute

    def get_connection_string(self) -> str:
        """
        Returns a masked version of the connection string.
        Only first 10 characters are visible, rest is hidden.
        """
        visible_part = self.__connection_string[:10]
        masked_part = "*" * (len(self.__connection_string) - 10)
        return visible_part + masked_part

    def set_connection_string(self, new_connection_string: str) -> None:
        """
        Sets a new connection string with validation.
        Raises ValueError if the string does not start with 'http'.
        """
        if not new_connection_string.startswith("http"):
            raise ValueError("Invalid connection string! Must start with 'http'.")

        self.__connection_string = new_connection_string

    def connect(self) -> None:
        """
        Simulates database connection.
        """
        self._status = "connected"
        print("Database connected successfully.")


# Example usage
if __name__ == "__main__":
    db = DatabaseConnector("http://secure-db-connection-string")

    # Safe access via getter
    print("Masked connection string:", db.get_connection_string())

    # Safe update via setter
    db.set_connection_string("http://new-secure-connection")

    db.connect()

    print("Status:", db._status)

    # Direct access attempt (will fail logically, not recommended)
    # print(db.__connection_string)  # This will raise AttributeError