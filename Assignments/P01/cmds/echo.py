"""
This file is about  echo command.
"""
import re


# ███████╗░█████╗░██╗░░██╗░█████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔════╝██╔══██╗██║░░██║██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# █████╗░░██║░░╚═╝███████║██║░░██║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██╔══╝░░██║░░██╗██╔══██║██║░░██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ███████╗╚█████╔╝██║░░██║╚█████╔╝  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚══════╝░╚════╝░╚═╝░░╚═╝░╚════╝░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def echo(**kwargs):
    """
        Used to print the value of the given argument to console
"""
    if "params" in kwargs:
            params = kwargs["params"] if kwargs.get("params") else []
    #print( "\r"+re.sub(r'[\'"]', '', " ".join(params))  )
    return re.sub(r'[\'"]', '', " ".join(params))         