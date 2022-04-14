from flask import Flask, render_template, request, redirect, abort
import os
import sys
import hashlib
import pickle
import asyncio

# Check for clang-format


def system_check_clang(clang: str = 'clang-format') -> int:
    # returns clang-format version and -1 if no clang-format
    cmd = f"{clang} --version > temp/log.txt"
    retcode = os.system(cmd)
    if retcode != 0:
        print(f"[WARN] : {clang} not found.")
        return -1
    clang_string = ""
    with open("temp/log.txt", "r") as f:
        clang_string = f.read()[:-1]
    print("[LOG] : Detected clang-format - ", clang_string)
    return int(clang_string.split(" ")[2].split(".")[0])


def install_pip_clang() -> bool:
    # installs clang-format 14 via pip (04.14.2022)
    print(f"[LOG] : Trying to install clang-format 14 via pip...")
    cmd = f"pip install clang-format"
    retcode = os.system(cmd)
    return retcode == 0


async def update_state(new_config: dict,  variables_pickle_file: str):
    with open(variables_pickle_file, "wb") as f:
        pickle.dump(new_config, f)


def load_state(variables_pickle_file: str) -> dict:
    try:
        with open(variables_pickle_file, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError as e:
        print("[WARN] : Config file not found, using default")
        default_config = {
            "button_pressed_times": 95,
        }
        update_state(default_config, variables_pickle_file)
        return default_config
    except Exception as e:
        print(
            "[ERR] : Something went exceptionally wrong with config file, exitting...: ", e)
        sys.exit(2)


STATE_PICKLE = "config.pickle"
state_dict = load_state(STATE_PICKLE)

CLANG_FORMAT_EXEC = "clang-format"
CLANG_FORCE_CHECK_14 = True
clang_version = system_check_clang(CLANG_FORMAT_EXEC)


def force_clang_updated(CLANG_FORMAT_EXEC: str):
    change = False
    if (clang_version < 14):
        print("[LOG] : Installing pip clang-format... (required version is 14+)")
        success = install_pip_clang()
        change = True
        if (success):
            print("[LOG] : pip clang-format installed successfully")
            CLANG_FORMAT_EXEC = 'clang-format'  # clang-format 14+
    if change and not system_check_clang(CLANG_FORMAT_EXEC):
        print("[ERR] : clang-format not found and/or automatic installation failed. Exitting... (use clang-format-14 for the best experience)")
        sys.exit(2)


if clang_version == -1 or CLANG_FORCE_CHECK_14:
    force_clang_updated(CLANG_FORMAT_EXEC)
loop = asyncio.get_event_loop()  # Kosteel

print(
    f"[LOG] : ANTIZHARKO has already been used {state_dict['button_pressed_times']} times")
app = Flask(__name__)


def formatted(code: str) -> str:
    buffer_name = hashlib.md5(code.encode()).hexdigest() + "_buffer"

    # Newline in the end of file check (unfortunately not found in clang-format 14)
    if code[-1] != '\n':
        code += '\n'

    with open(f"temp/{buffer_name}.cpp", "w") as f:
        f.write(code)

    cmd = f"{CLANG_FORMAT_EXEC} temp/{buffer_name}.cpp > temp/{buffer_name}_formatted.cpp"
    retcode = os.system(cmd)
    if retcode != 0:
        # Save error information
        cmd = f"mv temp/{buffer_name}.cpp temp/error.cpp"
        retcode = os.system(cmd)
        cmd = f"mv temp/{buffer_name}_formatted.cpp temp/error_formatted.cpp"
        retcode = os.system(cmd)
        return "ERROR"

    cmd = f"rm temp/{buffer_name}.cpp temp/{buffer_name}_formatted.cpp"
    formatted_code = ""
    with open(f"temp/{buffer_name}_formatted.cpp", "r") as f:
        formatted_code = f.read()
        retcode = os.system(cmd)
    return formatted_code


@ app.route("/", methods=["GET"])
def only_route():
    return render_template("index.html",
                           button_pressed_times=state_dict["button_pressed_times"],
                           jarkotik="static/jarkotik/jarkotik.jpg"), 200


@ app.route('/', methods=["POST"])
def button():
    # Limit POST to ~750kb (around 20k lines)
    cl = request.content_length
    if cl is not None and cl > 3 * 256 * 1024:
        abort(413)

    code = request.form.get('input_ta')
    if code == "":
        return redirect('/')
    # le Kosteel for saving state at all times
    state_dict["button_pressed_times"] += 1
    loop.run_until_complete(update_state(state_dict, STATE_PICKLE))
    return render_template("index.html",
                           formatted_code=formatted(code),
                           code=code,
                           button_pressed_times=state_dict["button_pressed_times"],
                           jarkotik="static/jarkotik/jarkotik_ears.gif"), 200
