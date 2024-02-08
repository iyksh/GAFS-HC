
if __name__ == "__main__":

    test = 4
    for i in range(5):
        index = [i for i in range(5) if i != test]
        print(index)
        test = test - 1
                        
            

