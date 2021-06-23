

def func():
    try:
        print('global _bob is ', _bob)
    except:
        print('bob is not defined')

func()