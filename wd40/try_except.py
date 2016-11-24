def try_except(success, failure=None, *exceptions):
    """
    execute in silence
    try_except(lambda: function_may_explode('re'), 'default_value')
    try_except(lambda: function_may_explode('re'), 'default_value', only_for_this_exception)
    try_except(lambda: function_may_explode('re'), 'default_value', for_this_exception, and_this_as_well)
    """
    try:
        return success()
    except exceptions or Exception:
        return failure() if callable(failure) else failure
