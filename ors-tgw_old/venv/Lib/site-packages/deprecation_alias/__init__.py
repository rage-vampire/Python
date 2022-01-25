#!/usr/bin/env python3
#
#  __init__.py
"""
A wrapper around 'deprecation' providing support for deprecated aliases.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  License: Apache Software License
#  See the LICENSE file for details.
#
#  Based on https://github.com/briancurtin/deprecation
#  Modified to only change the docstring of the wrapper and not the original function.
#

# stdlib
import datetime
import functools
import textwrap
import warnings
from typing import Callable, Optional, Union

# 3rd party
import deprecation  # type: ignore
from packaging import version

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "Apache Software License"
__version__: str = "0.2.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["deprecated"]


def deprecated(
		deprecated_in: Optional[str] = None,
		removed_in: Union[str, datetime.date, None] = None,
		current_version: Optional[str] = None,
		details: str = '',
		name: Optional[str] = None,
		func: Optional[Callable] = None,
		) -> Callable:
	r"""Decorate a function to signify its deprecation.

	This function wraps a method that will soon be removed and does two things:

	* The docstring of the method will be modified to include a notice
	  about deprecation, e.g., "Deprecated since 0.9.11. Use foo instead."
	* Raises a :class:`deprecation.DeprecatedWarning`
	  via the :mod:`warnings` module, which is a subclass of the built-in
	  :class:`DeprecationWarning`. Note that built-in
	  :class:`DeprecationWarning`\s are ignored by default, so for users
	  to be informed of said warnings they will need to enable them -- see
	  the :mod:`warnings` module documentation for more details.

	:param deprecated_in: The version at which the decorated method is considered
		deprecated. This will usually be the next version to be released when
		the decorator is added. The default is :py:obj:`None`, which effectively
		means immediate deprecation. If this is not specified, then the
		``removed_in`` and ``current_version`` arguments are ignored.
	:no-default deprecated_in:

	:param removed_in: The version or :class:`datetime.date` when the decorated
		method will be removed. The default is :py:obj:`None`, specifying that
		the function is not currently planned to be removed.

		.. note::

			This parameter cannot be set to a value if ``deprecated_in=None``.

	:no-default removed_in:

	:param current_version: The source of version information for the currently
		running code. This will usually be a ``__version__`` attribute in your
		library. The default is :py:obj:`None`. When ``current_version=None``
		the automation to determine if the wrapped function is actually in
		a period of deprecation or time for removal does not work, causing a
		:class:`~deprecation.DeprecatedWarning` to be raised in all cases.
	:no-default current_version:

	:param details: Extra details to be added to the method docstring and
		warning. For example, the details may point users to a replacement
		method, such as "Use the foo_bar method instead".

	:param name: The name of the deprecated function, if an alias is being
		deprecated. Default is to the name of the decorated function.
	:no-default name:

	:param func: The function to deprecate. Can be used as an alternative to using the ``@deprecated(...)`` decorator.
		If provided ``deprecated`` can't be used as a decorator.
	:no-default func:

	.. versionchanged:: 0.2.0  Added the ``func`` argument.
	"""

	# You can't just jump to removal. It's weird, unfair, and also makes
	# building up the docstring weird.
	if deprecated_in is None and removed_in is not None:
		raise TypeError("Cannot set removed_in to a value without also setting deprecated_in")

	# Only warn when it's appropriate. There may be cases when it makes sense
	# to add this decorator before a formal deprecation period begins.
	# In CPython, PendingDeprecatedWarning gets used in that period,
	# so perhaps mimick that at some point.
	is_deprecated = False
	is_unsupported = False

	# StrictVersion won't take a None or a "", so make whatever goes to it
	# is at least *something*. Compare versions only if removed_in is not
	# of type datetime.date
	if isinstance(removed_in, datetime.date):
		if datetime.date.today() >= removed_in:
			is_unsupported = True
		else:
			is_deprecated = True
	elif current_version:
		current_version = version.parse(current_version)  # type: ignore

		if removed_in is not None and current_version >= version.parse(removed_in):  # type: ignore
			is_unsupported = True
		elif deprecated_in is not None and current_version >= version.parse(deprecated_in):  # type: ignore
			is_deprecated = True
	else:
		# If we can't actually calculate that we're in a period of
		# deprecation...well, they used the decorator, so it's deprecated.
		# This will cover the case of someone just using
		# @deprecated("1.0") without the other advantages.
		is_deprecated = True

	should_warn = any([is_deprecated, is_unsupported])

	def _function_wrapper(function):
		# Everything *should* have a docstring, but just in case...
		existing_docstring = function.__doc__ or ''

		# split docstring at first occurrence of newline
		string_list = existing_docstring.split('\n', 1)

		if should_warn:
			# The various parts of this decorator being optional makes for
			# a number of ways the deprecation notice could go. The following
			# makes for a nicely constructed sentence with or without any
			# of the parts.

			parts = {"deprecated_in": '', "removed_in": '', "details": ''}

			if deprecated_in:
				parts["deprecated_in"] = f" {deprecated_in}"
			if removed_in:
				# If removed_in is a date, use "removed on"
				# If removed_in is a version, use "removed in"
				if isinstance(removed_in, datetime.date):
					parts["removed_in"] = f"\n   This will be removed on {removed_in}."
				else:
					parts["removed_in"] = f"\n   This will be removed in {removed_in}."
			if details:
				parts["details"] = f" {details}"

			deprecation_note = ".. deprecated::{deprecated_in}{removed_in}{details}".format_map(parts)

			# default location for insertion of deprecation note
			loc = 1

			if len(string_list) > 1:
				# With a multi-line docstring, when we modify
				# existing_docstring to add our deprecation_note,
				# if we're not careful we'll interfere with the
				# indentation levels of the contents below the
				# first line, or as PEP 257 calls it, the summary
				# line. Since the summary line can start on the
				# same line as the """, dedenting the whole thing
				# won't help. Split the summary and contents up,
				# dedent the contents independently, then join
				# summary, dedent'ed contents, and our
				# deprecation_note.

				# in-place dedent docstring content
				string_list[1] = textwrap.dedent(string_list[1])

				# we need another newline
				string_list.insert(loc, '\n')

				# change the message_location if we add to end of docstring
				# do this always if not "top"
				if deprecation.message_location != "top":
					loc = 3

			# insert deprecation note and dual newline
			string_list.insert(loc, deprecation_note)
			string_list.insert(loc, "\n\n")

		@functools.wraps(function)
		def _inner(*args, **kwargs):
			if should_warn:
				if is_unsupported:
					cls = deprecation.UnsupportedWarning
				else:
					cls = deprecation.DeprecatedWarning

				the_warning = cls(name or function.__name__, deprecated_in, removed_in, details)
				warnings.warn(the_warning, category=DeprecationWarning, stacklevel=2)

			return function(*args, **kwargs)

		_inner.__doc__ = ''.join(string_list)

		return _inner

	if func is None:
		return _function_wrapper
	else:
		return _function_wrapper(func)
