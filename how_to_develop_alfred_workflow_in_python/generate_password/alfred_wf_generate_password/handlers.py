#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

from __future__ import unicode_literals
import six
from .helpers import random_password

MSG_ENTER_DATETIME = "Enter password length."
DEFAULT_LENGTH = "12"
MSG_INVALID_LENGTH = "Password Length has to be between 8 and 32!"


def generate_password(wf, args=None):
    """
    Generate Secure Password.

    .. note::

        一个 handler 函数必须接受 wf 为必选变量, 代表着当前的 Workflow 类的实例.

        而 ``args=None`` 作为可选变量, 方便测试. 如果 ``args`` 不为 ``None``,
        那么说明是测试模式. 使用用户提供的 ``args`` (是个字符串列表).

        最终我们直接将 ``wf`` 返回即可 (也可以不返回), 因为 handler 函数的工作主要是
        处理输入, 然后对 ``wf`` 直接进行操作, 添加 item 而已.

        在 handler 函数中, 我们并不执行 ``wf.send_callback()``, 以方便测试.
    """
    if args is None:
        args = wf.args

    n_args = len(args)
    if n_args == 0:
        wf.add_item(
            title=MSG_ENTER_DATETIME,
            autocomplete="12",
            valid=True,
        )
    elif n_args == 1:
        try:
            length = int(args[0])
        except:
            wf.add_item(
                title="`{}` is NOT a valid length!".format(args[0]),
                valid=True
            )
            return wf

        if 8 <= length <= 32:
            for _ in range(10):
                password = random_password(length)
                wf.add_item(
                    title=password,
                    subtitle="copy to clipboard",
                    arg=password,
                    valid=True,
                )
        else:
            wf.add_item(
                title=MSG_INVALID_LENGTH,
                valid=True,
            )
    else:
        wf.add_item(
            title="`{}` is NOT a valid length!".format(" ".join(args)),
            valid=True,
        )
    return wf
