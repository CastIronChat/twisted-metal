import typing
import ast
import sys

# Debugging junk
# with open(sys.stdin, "r") as file:
# source = open("src/constants.py", "r").read()

source = sys.stdin.read()
source_as_lines = source.split("\n")
ast_ = ast.parse(source)

patch_functions = []
for module_statement in ast_.body:
    if isinstance(module_statement, ast.ClassDef):
        slots_declaration: typing.Optional[ast.Assign] = None
        slots: list[str] = []
        for class_body_statement in module_statement.body:
            if (
                isinstance(class_body_statement, ast.Assign)
                and isinstance(class_body_statement.targets[0], ast.Name)
                and class_body_statement.targets[0].id == "__slots__"
            ):
                slots_declaration = class_body_statement
            if isinstance(class_body_statement, ast.AnnAssign) and isinstance(
                class_body_statement.target, ast.Name
            ):
                slots.append(class_body_statement.target.id)
            if (
                isinstance(class_body_statement, ast.FunctionDef)
                and class_body_statement.name == "__init__"
            ):
                for init_body_statement in class_body_statement.body:
                    if (
                        isinstance(init_body_statement, ast.AnnAssign)
                        and isinstance(init_body_statement.target, ast.Attribute)
                        and isinstance(init_body_statement.target.value, ast.Name)
                        and init_body_statement.target.value.id == "self"
                    ):
                        slots.append(init_body_statement.target.attr)
                    if isinstance(init_body_statement, ast.Assign):
                        for target in init_body_statement.targets:
                            if (
                                isinstance(target, ast.Attribute)
                                and isinstance(target.value, ast.Name)
                                and target.value.id == "self"
                            ):
                                slots.append(target.attr)
        if slots_declaration:

            def patch_function(slots_declaration=slots_declaration, slots=slots):
                global source, source_as_lines
                source_as_lines[0 : slots_declaration.lineno]
                before = "\n".join(
                    source_as_lines[0 : slots_declaration.lineno - 1]
                    + [
                        source_as_lines[slots_declaration.lineno][
                            0 : slots_declaration.col_offset
                        ]
                    ]
                )
                t = ", ".join([f'"{slot}"' for slot in slots])
                new_slots_declaration_text = f"__slots__ = ({t})"
                after = "\n".join(
                    [
                        source_as_lines[slots_declaration.end_lineno][
                            slots_declaration.end_col_offset :
                        ]
                    ]
                    + source_as_lines[slots_declaration.end_lineno :]
                )
                source = f"{before}{new_slots_declaration_text}{after}"
                source_as_lines = source.split("\n")

            patch_functions.append(patch_function)
patch_functions.reverse()
for patch_function in patch_functions:
    patch_function()
print(source)
