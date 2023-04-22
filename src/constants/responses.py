from dataclasses import dataclass


@dataclass()
class CommonResponses:
    SUCCESS = "Success"
    FAILED = "Failed"

@dataclass()
class UserResponses:

    USER_CREATED = "User registered"
    USER_NOT_CREATED = "User not created"
    USER_ALREADY_EXISTS = "User with the same name or email already exists"
    THIS_USER_HAS_BEEN_DELETED = "This user has been deleted"
    USER_NOT_FOUND = "User not found"
    ACCESS_DENIED = "Access denied"
    USER_UPDATED = "User updated"
    USER_NOT_UPDATED = "User not updated"


@dataclass()
class TutorialResponses:
    TUTORIAL_ALREADY_EXISTS = "A tutorial with the same parameters already exists"
    TUTORIAL_ADDED = "Your tutorial has been added"
    TUTORIAL_NOT_FOUND = "A tutorial not found"
    PARAMETER_ERRORS = "Error(s) in parameter(s)"


@dataclass()
class LanguageResponses:
    FAILED_TO_ADD_LANGUAGE = "Failed to add language"

