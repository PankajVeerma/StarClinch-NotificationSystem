import re


class TemplateService:

    @staticmethod
    def render(template_text, variables):
        if not template_text:
            return ""

        def replace_variable(match):
            variable_name = match.group(1).strip()

            return str(
                variables.get(
                    variable_name,
                    match.group(0)
                )
            )

        return re.sub(
            r"{{\s*(.*?)\s*}}",
            replace_variable,
            template_text
        )