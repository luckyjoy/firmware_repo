def before_all(context):
    for formatter in context._runner.formatters:
        if formatter.name == "html-pretty":
            formatter.set_title("Custom QA Report")
