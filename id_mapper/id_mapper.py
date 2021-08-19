from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import win32com.client
import time
from secrets import __LOGIN_URL__, __STUDENT_URL__, USRNAME, PSWRD
import argparse

__DELAY__ = 2  # don't reduce


def init_webdriver():
    # init webdriver and login
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(__LOGIN_URL__)
    driver.implicitly_wait(__DELAY__)  # seconds
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.Sendkeys(USRNAME)
    time.sleep(__DELAY__)  # seconds
    shell.Sendkeys(r"{TAB}")
    time.sleep(__DELAY__)  # seconds
    shell.Sendkeys(PSWRD)
    time.sleep(__DELAY__)  # seconds
    shell.Sendkeys(r"{ENTER}")
    time.sleep(__DELAY__)  # seconds
    return driver


def find_csu_id(driver, sg_id):
    driver.get(__STUDENT_URL__ + sg_id)
    csu_id_obj = driver.find_element_by_id(
        "ctl00_ctl00_MainContent_MainContent_PrimaryDetails_StudentExternalRepeater_ctl00_ExternalIDTextBox"
    )
    return csu_id_obj.get_property("value")


def main(args):
    # load students list
    try:
        df = pd.read_csv(args.i, dtype={"SG_ID": str})
    except:
        print(f"File {args.i} does not exist!")
        exit()

    driver = init_webdriver()

    csu_ids = []
    for _, row in df.iterrows():
        # current sg id
        sg_id = row.SG_ID

        # find csu id
        try:
            csu_id = find_csu_id(driver, sg_id)
        except:
            csu_id = "Could'd find ID"

        # store csu id
        csu_ids.append(csu_id)

    df["CSU_ID"] = csu_ids

    # finally save list
    if args.o:
        df.to_csv(args.o, index=False)
    else:
        df.to_csv("csu_" + args.i, index=False)

    # clean-up
    driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input csv file-name", type=str)
    parser.add_argument("-o", help="out csv file-name", type=str)
    args = parser.parse_args()
    main(args)
