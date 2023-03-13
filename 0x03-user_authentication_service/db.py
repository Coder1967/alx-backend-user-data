"""DB module
"""
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    def add_user(self, email, hashed_pwd) -> User:
        """
        creates and saves a new user
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_pwd
        sesh = self._session
        sesh.add(user)
        sesh.commit()
        return user

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def find_user_by(self, **kwargs) -> User:
        """
        searches out a user using key-word argumebt
        """
        fields = {"email": User.email, "hashed_password": User.hashed_password,
                  "session_id": User.session_id,
                  "reset_token": User.reset_token, "id": User.id}
        key = list(kwargs.keys())[0]

        if key in fields:
            field = fields[key]
            value = kwargs[key]
            sesh = self._session
            user = sesh.query(User).filter(field == value).first()
            if user is None:
                raise NoResultFound
            return user
        else:
            raise InvalidRequestError

    def update_user(self, user_id, **kwargs) -> None:
        """
        updates the value of the user attribute
        using key-word argument
        """
        fields = {"email": "str", "hashed_password": "str",
                  "session_id": "str",
                  "reset_token": "str", "id": "int"}
        key = list(kwargs.keys())[0]
        if type(user_id).__name__ != "int":
            raise ValueError
        if key in fields:
            if type(kwargs[key]).__name__ != fields[key]:
                raise ValueError
        user = self.find_user_by(id=user_id)
        user.__dict__[key] = kwargs[key]
        self._session.commit()
