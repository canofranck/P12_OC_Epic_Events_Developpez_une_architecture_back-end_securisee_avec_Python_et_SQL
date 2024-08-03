# Role

ROLE_MANAGER = "MANAGER"
ROLE_SALES = "SALES"
ROLE_SUPPORT = "SUPPORT"
ROLE_ADMIN = "ADMIN"


# Main Menu

MAIN_MENU_LOGIN = "1"
MAIN_MENU_QUIT = "0"
MAIN_MENU_BACK = "0"
# User Menu common

LIST_CUSTOMERS = "1"
LIST_CONTRACTS = "2"
LIST_EVENTS = "3"
LOG_OUT = "0"

# Menu Manager

LIST_MANAGER_ASSIGN_EVENT = "4"
LIST_MANAGER_MANAGE_USER = "5"
LIST_MANAGER_MANAGE_CONTRACT = "6"

# Manager Menu manage User

MANAGER_CREATE_NEW_USER = "1"
MANAGER_UPDATE_USER = "2"
MANAGER_DELETE_USER = "3"
MANAGER_LIST_USER = "4"
# Manager Menu manage Contract

MANAGER_CREATE_NEW_CONTRACT = "1"
MANAGER_UPDATE_CONTRACT = "2"

# Manager Menu Contract Filter
MANAGER_LIST_CONTRACT_NO_FILTER = "1"
MANAGER_LIST_CONTRACT_NOT_SIGNED = "2"
MANAGER_LIST_CONTRACT_NOT_TOTAL_PAID = "3"

# Menu Sales

LIST_SALES_CREATE_NEW_CUSTOMER = "4"
LIST_SALES_UPDATE_CUSTOMER = "5"
LIST_SALES_UPDATE_CONTRACT = "6"
LIST_SALES_CREATE_EVENT = "7"
LIST_SALES_DELETE_EVENT = "8"

# Menu Sales Event Filter

SALES_LIST_EVENT_NO_FILTER = "1"
SALES_LIST_EVENT_ONLY_YOURS = "2"
SALES_LIST_EVENT_NO_SUPPORT = "3"

# Menu support

SUPPORT_MANAGE_EVENT = "4"

# Admin support

LIST_SUPPORT_CREATE_EVENT = "4"

# Event Filter

EVENT_FILTER_NO_FILTER = "1"
EVENT_FILTER_ONLY_YOURS = "2"
EVENT_FILTER_NO_SUPPORT = "3"


# ERROR

ERR_USER_NOT_FOUND = "USER not found"
ERR_USER_NO_ROLE = (
    "This USER has no role, he cannot interact with the application"
)
ERR_USER_BAD_PASSWORD = "Bad password. Please try again."

ERR_TOO_MANY_ATTEMPTS_EMAIL = "too many attempts for email"
ERR_TOO_MANY_ATTEMPTS_PASSWORD = "too many attempts for password"
ERR_TOO_MANY_ATTEMPTS = "too many attempts, maybe a breakforce attack"
ERR_NO_CONTRACT_FOR_CUSTOMER = "No contract for this customer"

TOKEN_VALIDITY_PERIOD = 1
MAX_EMAIL_ATTEMPS = 3
MAX_PASSWORD_ATTEMPS = 3

MAIN_CONTROLLER_ERR_QUIT = "Au revoir !"
MAIN_CONTROLLER_ERR_INPUT = "input invalide"

CONTRACT_CONTROLLER_CONTRACT_SIGNED_PAID = "CONTRACT ALREADY SIGNED AND PAID"

CUSTOMER_CONTROLLER_NO_USER = "No user is currently logged in."
CUSTOMER_CONTROLLER_EMAIL_EXISTS = "EMAIL ALREADY EXISTS"

EVENT_CONTROLLER_SUPPORT_ALREADY_DEFINE = "A USER SUPPORT IS ALREADY DEFINE"
EVENT_CONTROLLER_EVENT_NOT_FOUND = "EVENT NOT FOUND"
