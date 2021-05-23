from bs4 import BeautifulSoup
import requests
def get_coefs(userid):
    pass


def get_solve_time(studentname):
    pass


def get_stud_list(html):
    res=[]
    cur=""
    for i in html:
        if i==';':
            if cur:
                res.append(cur[1:])
                cur=""
            else:
                cur+=i
        else:
            if cur:
                cur+=i
    return res


def get_bet(inits, coef, cost, willsolve):
    pass
