from inspect import FrameInfo
from pathlib import Path
from typing import Callable, Any

from approval_utilities.utilities.clipboard_utilities import copy_to_clipboard
from approval_utilities.utilities.multiline_string_utils import remove_indentation_from
from approvaltests import StackFrameNamer, assert_equal_with_reporter, Options, Reporter
from approvaltests.reporters import MultiReporter


def get_approved_via_doc_string():
    test_stack_frame: FrameInfo = StackFrameNamer.get_test_frame()
    method: Callable[..., Any] = get_caller_method(test_stack_frame)
    return remove_indentation_from(method.__doc__)

def get_caller_method(caller_frame)-> Callable:
    caller_function_name: str = caller_frame[3]
    caller_function_object = caller_frame.frame.f_globals.get(caller_function_name, None)
    return caller_function_object


def test_docstrings():
    '''
    hello world
    '''
    verify_inline("hello world")


class InlineReporter(Reporter):
    # TODO: Start here - Make this report create a temp file of the fixed source,
    #  and compare it with the existing source.
    # if there are mulitple failures, they each get there on reporter
    def report(self, received_path: str, approved_path: str) -> bool:
        received = Path(received_path).read_text()
        copy_to_clipboard(f"'''\n{received}\n'''")


def verify_inline(actual):
    options = Options()
    options = options.with_reporter(MultiReporter(options.reporter, InlineReporter()))
    if actual[-1] != "\n":
        actual += "\n"
    assert_equal_with_reporter(get_approved_via_doc_string(), actual, options=options)

#
#