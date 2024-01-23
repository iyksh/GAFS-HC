if __name__ == "__main__":
    from call_nbayes import call_nbayes
    test_path = "exemples-datasets/test_test.arff"
    train_path = "exemples-datasets/test_train.arff"


    print(call_nbayes(train_path, test_path))
