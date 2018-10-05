.. contents::

如何配置你的开发环境, 目录. 让你像平时开发 Python 项目一样, 创建虚拟环境, 安装依赖库.
==============================================================================

在这个例子中, 我们用到了 `six <https://pypi.org/project/six/>`_ 第三方库. 我们仅仅是导入了它, 并没有真正使用它. 这仅仅是为了说明 **如何包含第三方库** 而加上的.

- ``requirements.txt``: 储存了你的 workflow 所依赖的第三方库.
- ``requirements-alfred-workflow.txt``: 我们将 `Alfred-Workflow <https://pypi.org/project/Alfred-Workflow/>`_ 也放在了这里, 因为这个包并不安装到 ``lib`` 子目录中, 而是直接安装到 **插件目录下**.
- ``alfred_wf_generate_password`` 目录: 你 workflow 的实现代码, Script Filter 所调用的 Python 文件中并不放核心逻辑实现代码. 这样能做到 **功能实现** 和 **Script Filter** 分离, 便于测试. 这个文件夹的命名最好根据你的项目名字改动: ``alfred_wf_{projetname}``. 其中, ``alfred_wf_{projetname}/__init__.py`` 文件中必须定义版本号变量 ``__version__ = "0.0.1"`` (版本号你自己改).
- ``setup.py``: 用于安装 ``alfred_wf_{projextname}``. 将里面的 ``import alfred_wf_generate_password as package`` 这一行改成 ``import alfred_wf_填你的项目名 as package`` 即可.

在你的实现代码中, 一定要放一个 ``handlers.py`` 文件 (名字可以改), 这个模块中储存的是 一个/许多 对 Workflow 进行操作的函数. 也就是你的核心逻辑. 我们最终主要对 ``handlers.py`` 这个文件中的函数进行测试.


如何测试你的 Workflow, 如何定义所有可能的输入, 测试输出是否符合你所期待的那样子.
==============================================================================

这里, 我使用的是 `pytest <https://pypi.org/project/pytest/>`_ 框架进行的单元测试, 当然你可以用你喜欢的单元测试框架. 我们的单元测试代码存放在 ``tests`` 目录中.

请打开 ``alfred_wf_generate_password/handlers.py`` 和 ``tests/test_handlers.py`` 文件.

在实现核心逻辑时, 我们的 handler 函数除了 ``wf`` 这一必填参数外, 还有一个 ``args`` 可选参数, 并且前两行定义了: 如果 ``args`` 不为 ``None``, 那么我们就使用 ``args`` 中的参数而不使用 ``wf.args``. 所以在 ``tests/test_handlers.py`` 中, 我们可以指定任意的输入. 然后用 ``wf._items`` 访问所有返回的 item. 检查这些 item 的:

- title: 大字标题
- subtitle: 小字标题
- arg: 被传递到下一个元件中的参数, 也是你 Cmd + C 所拷贝的参数
- autocomplete: 按 Tab 键自动补全的参数

是否符合你的预期.


如何一键导出你的代码, 并打包生成一个 Workflow 插件
==============================================================================

.. code-block:: bash

    cd "$(dirname "$0")" # 定位到当前目录
    rm -r ./workflow # 删除已经存在的 workflow 插件目录
    mkdir ./workflow # 创建一个空的 workflow 插件目录
    pip2.7 install Alfred-Workflow --target=./workflow # 将 Alfred-Workflow 安装到 ./workflow/workflow 处
    pip2.7 install . --target=./workflow/lib # 将所有第三方库包括你的实现代码安装到 ./workflow/lib 处


