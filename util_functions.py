from pytictoc import TicToc


def print_time_operation_took(function):
    """
    Print the time it took to complete a given function

    :param function: the function to run
    """
    t = TicToc()
    function()
    t.toc()
