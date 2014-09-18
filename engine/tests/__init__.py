import game_test

def run_test(test_name):
    if (test_name == "game"):
        game_test.run()

def run_all_tests():
    print("Running all tests")
    game_test.run()
