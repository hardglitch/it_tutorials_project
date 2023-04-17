from dataclasses import dataclass


@dataclass()
class UserResponses:

    USER_CREATED = "User registered"
    USER_NOT_CREATED = "User not created"
    USER_ALREADY_EXISTS = "User with the same name or email already exists"
    SUCCESS = "Success"
    USER_NOT_FOUND = "User not found"
    ACCESS_DENIED = "Access denied"
    USER_UPDATED = "User updated"
    USER_NOT_UPDATED = "User not updated"


@dataclass()
class TutorialResponses:
    TUTORIAL_ALREADY_EXISTS = "A tutorial with the same parameters already exists"
    TUTORIAL_CREATED = "Your tutorial added"
    TUTORIAL_NOT_FOUND = "A tutorial not found"
