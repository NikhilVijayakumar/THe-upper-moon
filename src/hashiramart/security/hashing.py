from passlib.context import CryptContext

# Create a CryptContext instance, specifying the hashing scheme.
# bcrypt is the industry standard and highly recommended.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    """A utility class for password hashing and verification."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against its hashed version.

        :param plain_password: The password in plain text.
        :param hashed_password: The hashed password from the database.
        :return: True if the passwords match, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hashes a plain text password.

        :param password: The password to hash.
        :return: The hashed password string.
        """
        return pwd_context.hash(password)