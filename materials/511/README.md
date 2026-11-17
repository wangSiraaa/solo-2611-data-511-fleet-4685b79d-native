# 起点与运行

production起点export_jobs.py只提供同步HTTP目录导出；bulk_import.py只读一个文件。异步任务状态、冻结、manifest、取消与整产品入仓均未实现。

运行：`python3.11 demo.py`。demo仅展示材料已有正常能力；所有写入在临时目录，材料源文件保持只读。完整目标与合法输入见本题题面。
