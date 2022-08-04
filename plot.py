from data import parse_data


def main():
    successes, failures, routes = parse_data('stats.json')

    print(successes)
    print(failures)
    print(routes)


if __name__ == '__main__':
    main()
