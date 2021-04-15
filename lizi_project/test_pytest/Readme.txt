[需安装的组件]
pytest
pytest-html
pytest-xdist
pytest-rerunfailures
pytest-ordering

[相关文件说明]
pytest.ini：pytest的主配置文件，可以改变pytest的默认行为
conftest.py：测试用例的一些fixture配置
_init_.py：识别该文件夹为python的package包
tox.ini：与pytest.ini类似，用tox工具时候才有用
setup.cfg：也是ini格式文件，影响setup.py的行为


[pytest.ini配置文件说明]
# 用于@pytest.mark.XXX
markers =
    slow：run the slow case
    faster：run the faster case

addopts：可以更改默认命令行选项，可以搭配相关的参数
    -s: 显示程序中的print/logging输出
    -v: 丰富信息模式, 输出更详细的用例执行信息
    -q: 安静模式, 不输出环境信息
    -m=xxx: 运行打标签的用例
    -reruns=xxx，失败重新运行
    -m XXX：运行带指定参数的测试用例（需添加markers)
    -k XXX:通过关键词过滤
    --collect-only：收集将会被执行的测试用例（只是收集，不执行）
    --html=report/report.html：生成测试报告的路径

testpaths：配置测试用例的目录（所有测试用例的顶层目录）
    testpaths = ./scripts

python_files：设置需测试的测试文件规则
    python_files = test_*.py

python_classes：设置需测试的测试类规则
    python_classes = Test*

python_functions：设置需测试的测试函数规则
    python_functions = test_*

python_methods：设置需测试的测试方法规则

log_cli：控制台实时输出日志
    log_cli = true

xfail_strict ：将标记为@pytest.mark.xfail但实际通过显示XPASS的测试用例被报告为失败（Failed）
    xfail_strict = true