from functools import wraps

def decorator_without_wraps(func):
    @wraps
    def inner_function(*args, **kwargs):
        print('This is a decorator')
        func()
    return inner_function

@decorator_without_wraps
def hello_world():
    print("Hello")

hello_world() # This is a decorator
              # Hello
print(hello_world.__name__) # inner_function