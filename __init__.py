'''Unravel, Piazza Deanonymizer'''
import pprint
import argparse
from piazza_api import Piazza
from tinydb import TinyDB, Query


def get_statistics(email, password, class_id):
    """Logins to Piazza and retrieves the statistics of a course.

    Args:
        email: Piazza username.
        password: Piazza password.
        class_id: Course ID on Piazza.

    Returns:
        A JSON formatted course statistics.

    Raises:
        piazza_api.exceptions.AuthenticationError:
            If authentication fails.
    """
    piazza = Piazza()
    piazza.user_login(email, password)
    course = piazza.network(class_id)
    return course.get_statistics()


def parse_arguments():
    """Parses command-line arguments.

    Returns:
        {
            email: Piazza username.
            password: Piazza password.
            class_id: Course ID on Piazza.
        }

    Raises:
        ArgumentError: If any of the arguments is missing.
    """
    parser = argparse.ArgumentParser(description='Piazza Post Deanonymzer.')
    group = parser.add_argument_group('Piazza Authentication')
    group.add_argument('-u', metavar='email', type=str,
                       help='Piazza account email', dest="email")
    group.add_argument('-p', metavar='password', type=str,
                       help='Piazza account password', dest="password")
    group.add_argument('-c', metavar='class_id', type=str,
                       help='Class id from piazza.com/class/{class_id}', dest="class_id")
    args = parser.parse_args()
    if not (args.email and args.password and args.class_id):
        parser.error("the following arguments are required: -u -p -c.")

    return args


def main():
    args = parse_arguments()
    # Create/load tinydb for the class
    tinydb = TinyDB(f'{args.class_id}.json')
    stats = get_statistics(args.email, args.password, args.class_id)
    # Insert the new statistics
    tinydb.insert(stats)


if __name__ == '__main__':
    main()
